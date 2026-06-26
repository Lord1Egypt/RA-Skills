# NBA API Reference

Complete reference for `nba_api` library (direct access to NBA.com official API).

---

## Table of Contents

1. [Static Data (No Requests)](#static-data)
2. [Player Endpoints](#player-endpoints)
3. [Team Endpoints](#team-endpoints)
4. [Game Endpoints](#game-endpoints)
5. [Standings & Stats](#standings--stats)
6. [Live Data](#live-data)
7. [Advanced Features](#advanced-features)

---

## Static Data

Built-in data, no network requests needed.

### teams.get_teams()

Get all teams

```python
from nba_api.stats.static import teams

all_teams = teams.get_teams()

# Find specific team
hawks = [t for t in all_teams if t['abbreviation'] == 'ATL'][0]
print(hawks['full_name'])  # Atlanta Hawks
```

**Fields:**
- `id`: Team ID
- `full_name`: Full name
- `abbreviation`: Abbreviation
- `nickname`: Nickname
- `city`: City
- `state`: State/Province
- `year_founded`: Founding year

---

### players.get_players()

Get all players

```python
from nba_api.stats.static import players

all_players = players.get_players()

# Search by name
lebron = players.find_players_by_full_name("LeBron James")
print(lebron[0]['id'])  # 2544

# Get active players
active = players.get_active_players()

# Get inactive players
inactive = players.get_inactive_players()
```

**Fields:**
- `id`: Player ID
- `full_name`: Full name
- `first_name`: First name
- `last_name`: Last name
- `is_active`: Active status

---

## Player Endpoints

### PlayerCareerStats

Player career statistics

```python
from nba_api.stats.endpoints import playercareerstats

career = playercareerstats.PlayerCareerStats(player_id='2544')

# Season totals
df_season = career.season_totals_regular_season.get_data_frame()

# Career totals
df_career = career.career_totals_regular_season.get_data_frame()

# Playoff data
df_playoffs = career.season_totals_post_season.get_data_frame()
```

**Available datasets:**
- `season_totals_regular_season`: Regular season totals
- `career_totals_regular_season`: Career totals
- `season_totals_post_season`: Playoff totals
- `all_star_season_totals`: All-Star data

---

### PlayerGameLog

Player game-by-game log

```python
from nba_api.stats.endpoints import playergamelog

log = playergamelog.PlayerGameLog(
    player_id='2544',
    season='2025-26',
    season_type_all_star='Regular Season'
)

df = log.get_data_frames()[0]
print(df[['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST', 'WL']].head(10))
```

**Fields:**
- `GAME_DATE`: Game date
- `MATCHUP`: Opponent (@ = away)
- `WL`: Win/Loss
- `MIN`: Minutes
- `PTS`: Points
- `REB`: Rebounds
- `AST`: Assists
- `STL`: Steals
- `BLK`: Blocks
- `TOV`: Turnovers
- `PLUS_MINUS`: Plus/minus

---

### PlayerInfo

Basic player information

```python
from nba_api.stats.endpoints import playerinfobase

info = playerinfobase.PlayerInfoBase(player_id='2544')
df = info.get_data_frames()[0]

print(df['DISPLAY_FIRST_LAST'].values[0])  # LeBron James
print(df['HEIGHT'].values[0])              # 6-9
print(df['WEIGHT'].values[0])              # 250
print(df['SCHOOL'].values[0])              # St. Vincent-St. Mary HS
```

---

### PlayerInjuries

Injury information

```python
from nba_api.stats.endpoints import playerinjuries

injuries = playerinjuries.PlayerInjuries(player_id='1630163')
df = injuries.get_data_frames()[0]

print(df[['PLAYER', 'TEAM', 'INJURY', 'STATUS', 'DATE']])
```

**Status values:**
- `Out`: Not playing
- `Day-To-Day`: Daily evaluation
- `Probable`: Likely to play
- `Questionable`: Uncertain

---

## Team Endpoints

### TeamGameLog

Team game records

```python
from nba_api.stats.endpoints import teamgamelog

log = teamgamelog.TeamGameLog(
    team_id='1610612766',  # Hornets
    season='2025-26'
)

df = log.get_data_frames()[0]
print(df[['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST', 'WL']].head(10))
```

---

### LeagueStandings

League standings

```python
from nba_api.stats.endpoints import leaguestandings

standings = leaguestandings.LeagueStandings()
df = standings.get_data_frames()[0]

# Filter Hornets
hornets = df[df['TeamName'] == 'Hornets']
print(hornets[['TeamName', 'WINS', 'LOSSES', 'WinPCT', 'Conference']])

# Top 8 East
east = df[df['Conference'] == 'East'].sort_values('WinPCT', ascending=False).head(8)
print(east[['TeamName', 'WINS', 'LOSSES', 'WinPCT']])
```

---

## Game Endpoints

### ScoreboardV3

Daily schedule

```python
from nba_api.stats.endpoints import scoreboardv3
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
board = scoreboardv3.ScoreboardV3(game_date=today, league_id='00')
data = board.get_dict()

for game in data['scoreboard']['games']:
    home = game['homeTeam']
    away = game['awayTeam']
    game_time = game['gameTimeUTC']
    print(f"{away['teamName']} @ {home['teamName']}")
    print(f"  Time: {game_time}")
```

---

### BoxScoreTraditional

Traditional box score

```python
from nba_api.stats.endpoints import boxscoretraditionalv2

box = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id='0022500123')

# Player stats
player_stats = box.player_stats.get_data_frame()
print(player_stats[['PLAYER_NAME', 'PTS', 'REB', 'AST', 'MIN']])

# Team stats
team_stats = box.team_stats.get_data_frame()
print(team_stats[['TEAM_NAME', 'PTS', 'FG_PCT', 'FG3_PCT']])
```

---

### PlayByPlay

Play-by-play data

```python
from nba_api.stats.endpoints import playbyplayv2

pbp = playbyplayv2.PlayByPlayV2(game_id='0022500123')
df = pbp.get_data_frames()[0]

# Filter crunch time (4th quarter, last 5 minutes)
crunch = df[
    (df['PERIOD'] >= 4) & 
    (df['PCTIMESTRING'] < '5:00')
]

print(crunch[['PERIOD', 'PCTIMESTRING', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION', 'SCORE']])
```

**Fields:**
- `GAME_ID`: Game ID
- `EVENTNUM`: Event number
- `EVENTMSGTYPE`: Event type (1=score, 2=turnover, 3=rebound, ...)
- `PERIOD`: Quarter
- `PCTIMESTRING`: Game clock
- `HOMEDESCRIPTION`: Home team description
- `VISITORDESCRIPTION`: Away team description
- `SCORE`: Current score
- `SCOREMARGIN`: Score difference

---

## Standings & Stats

### LeagueLeaders

League leaders

```python
from nba_api.stats.endpoints import leagueleaders

# Scoring leaders
scoring = leagueleaders.LeagueLeaders(
    stat_type_abbreviation='PTS',
    per_mode48='PerGame',
    season='2025-26'
)

df = scoring.get_data_frames()[0]
print(df[['RANK', 'PLAYER', 'TEAM', 'PTS']].head(10))

# Other stats: 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT'
```

---

## Live Data

### scoreboard.ScoreBoard()

Real-time scores

```python
from nba_api.live.nba.endpoints import scoreboard

games = scoreboard.ScoreBoard()
data = games.get_dict()

for game in data['scoreboard']['games']:
    home = game['homeTeam']
    away = game['awayTeam']
    
    print(f"{away['teamName']} @ {home['teamName']}")
    print(f"  Score: {away['score']} - {home['score']}")
    print(f"  Status: {game['gameStatusText']}")
    print(f"  Period: {game.get('period', 'N/A')}")
```

**gameStatus values:**
- 1: Not started
- 2: In progress
- 3: Final

---

### playbyplay.PlayByPlay()

Real-time play-by-play

```python
from nba_api.live.nba.endpoints import playbyplay

pbp = playbyplay.PlayByPlay(game_id='0022500123')
data = pbp.get_dict()

# Latest events
actions = data['game']['actions']
for action in actions[-10:]:
    print(f"{action['clock']} - {action.get('description', 'N/A')}")
```

---

## Advanced Features

### Proxy & Custom Headers

```python
from nba_api.stats.endpoints import playercareerstats

career = playercareerstats.PlayerCareerStats(
    player_id='2544',
    proxy='http://127.0.0.1:8080',
    timeout=30,
    headers={'User-Agent': 'Custom User Agent'}
)
```

---

### Error Handling

```python
from nba_api.stats.library.http import NBAHTTPError
import time

def safe_api_call(func, max_retries=3, delay=1):
    """Safe API call wrapper"""
    
    for attempt in range(max_retries):
        try:
            return func()
        except NBAHTTPError as e:
            if '404' in str(e):
                print(f"Not found: {e}")
                return None
            elif '429' in str(e):
                wait = delay * (2 ** attempt)
                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"API error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise
        except Exception as e:
            print(f"Unknown error: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise
    
    return None

# Usage
result = safe_api_call(
    lambda: playercareerstats.PlayerCareerStats(player_id='2544')
)
```

---

## Team ID Reference

| Team | ID |
|------|-----|
| Atlanta Hawks | 1610612737 |
| Boston Celtics | 1610612738 |
| Brooklyn Nets | 1610612751 |
| Charlotte Hornets | 1610612766 |
| Chicago Bulls | 1610612741 |
| Cleveland Cavaliers | 1610612739 |
| Dallas Mavericks | 1610612742 |
| Denver Nuggets | 1610612743 |
| Detroit Pistons | 1610612765 |
| Golden State Warriors | 1610612744 |
| Houston Rockets | 1610612745 |
| Indiana Pacers | 1610612754 |
| LA Clippers | 1610612746 |
| Los Angeles Lakers | 1610612747 |
| Memphis Grizzlies | 1610612763 |
| Miami Heat | 1610612748 |
| Milwaukee Bucks | 1610612749 |
| Minnesota Timberwolves | 1610612750 |
| New Orleans Pelicans | 1610612740 |
| New York Knicks | 1610612752 |
| Oklahoma City Thunder | 1610612760 |
| Orlando Magic | 1610612753 |
| Philadelphia 76ers | 1610612755 |
| Phoenix Suns | 1610612756 |
| Portland Trail Blazers | 1610612757 |
| Sacramento Kings | 1610612758 |
| San Antonio Spurs | 1610612759 |
| Toronto Raptors | 1610612761 |
| Utah Jazz | 1610612762 |
| Washington Wizards | 1610612764 |

---

## Best Practices

1. **Cache Data**: Cache frequently accessed data (e.g., team info)
2. **Rate Limiting**: Add `time.sleep(0.5)` between requests
3. **Error Retry**: Auto-retry 2-3 times on network errors
4. **Data Cleaning**: Use pandas to handle missing values and type conversions
5. **Timezone**: NBA times are ET, convert to local timezone

---

## Official Documentation

- GitHub: https://github.com/swar/nba_api
- Docs: https://github.com/swar/nba_api/tree/master/docs
- Examples: https://github.com/swar/nba_api/tree/master/docs/examples
