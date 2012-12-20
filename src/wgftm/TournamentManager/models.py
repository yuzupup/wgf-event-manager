from django.db import models

#
# Personel/attendee level models:
#

# Guest: a user who is not a player
class Guest(models.Model):
   name = models.CharField(max_length=60)

# Player: A player in the Event.
class Player(models.Model):
   name = models.CharField(max_length=60)                #
   email = models.EmailField()                           #
   phoneNumber = models.CharField(max_length=10)         # Optional field
   isUcsd = models.BooleanField()                        # Is the player a UCSD student?
   ucsdCollege = models.CharField(max_length=32)         # What UCSD college does the player belong to?              
   age = models.IntegerField()                           # To check for whether or not we need to distribute legal forms for prizes
   isBusy = models.BooleanField()                        # Is the player CURRENTLY busy - may be used for something
   tournamentsIn = models.ManyToManyField(Tournament)    # What tournaments is the player in?

# TL: The PRIMARY administrator/s of the tournament
class TournamentLeader(models.Model):
   name = models.CharField(max_length=255)
   
# TA: Someone who administrates a tournament, but does not make the primary
# decisions. A lackey.
class TournamentAssistant(models.Model):
   name = models.CharField(max_length=255)
   superior = models.ManyToManyField(TournamentLeader)   # Who is the TL for this person?
   
# Team: Can be a single player or a collection of players, but ONLY teams are part of Games. The participants
# in a game
class Team:
   numOfPlayers = models.IntegerField()                  # How many players are on this team?
   players = models.ManyToManyField(Player)              # What players are on the this team?
   captain = models.ForeignKey(Player)                   # Who is the team captain? 
   metadata = models.IntegerField()                      # Data for matchmaking - if a matchmaking algorithm is specified, use this to determine rankings
   
#   
# Event level models:
#

# Event: The highest level of the Tournament. 
class Event(models.Model):                               
   name = models.CharField(max_length=255)               # The name of the tournament.
   headcount = models.IntegerField()                     # How many people checked-in at this event?
   
# Tournament: a tournament for a single game.
class Tournament(models.Model):
   event = models.ForeignKey(Event)                      # What Event does this Tournament belong to?
   name = models.CharField(max_length=255)               # Tournament name
   date = models.TimeField()                             # Tournament date
   curNumTeams = models.IntegerField()                   # What is the current number of teams in this tournament?
   maxNumTeams = models.IntegerField()                   # The maximum number of teams in this tournament?
   tournamentLeaders = models.ManyToManyField(TournamentLeader)      # Who are the TLs?
   tournamentAssistants = models.ManyToManyField(TournamentAssitant) # Who are the TAs?
   prizes = models.CharField(max_length=500)             # Textfield for prizes
   bracket = models.CharField(max_length=1024)           # Bracket field - contains a string describing the current state/structure of the tournament
   
# Match: single Match for the tournament (one node of the tournament) - a Match can consist of many games
class Match(models.Model):
   tournament = models.ForeignKey(Tournament)            # What tournament does this match belong to?
   name = models.CharField(max_length=64)                # What is the name of this match 
   matchType = models.CharField(max_length=64)           # What kind of match is this? (i.e.: single elim, double elim, round robin, any other format)
   teams = models.ManyToManyField(Team)                  # What teams are participaiting?
   winnerParent = models.OneToOneField(Match)            # Where should the winners go?
   loserParent = models.OneToOneField(Match)             # Where should the losers go?
   winners = models.ManyToManyField(Team)                # Who are the winners?
   losers = models.ManyToManyField(Team)                 # Who are the losers?
   
#
# Games: a Match consists of any number of games
# CAN support round robin/pool play.
#   
class Game(models.Model):
   match = models.ForeignKey(Match)                      # The Match the Game is associated with
   teams = models.ManyToManyField(Team)                  # Who are the teams in this game (may be more than just 2)
   verified = models.BooleanField()                      # Has the game been verified?
   startTime = models.TimeField()                        # When should the game start?
   winners = models.ManyToManyField(Team)                # Who were the winners?
   losers = models.ManyToManyField(Team)                 # Who were the losers?