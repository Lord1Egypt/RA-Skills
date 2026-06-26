# NBA Tracker

**NBA Game Viewing Assistant**

Wrapper for `nba_api` to support game viewing scenarios:
- Track favorite players/teams
- View schedules and add to calendar
- Real-time scores
- Crunch time alerts (last 5 minutes + score difference < 5)

⚠️ **Note**: This tool is designed for **viewing** purposes. For **prediction markets/betting** use cases, consider more real-time professional data sources (e.g., Sportradar, Genius Sports) with lower latency and higher reliability requirements.

---

## Installation

```bash
pip install nba_api pandas
```

---

## Quick Start

### Check Team Standings

```python
from nba_api.stats.endpoints import leaguestandings

standings = leaguestandings.LeagueStandings()
df = standings.get_data_frames()[0]

# Check Hornets record
hornets = df[df['TeamName'] == 'Hornets']
print(hornets[['TeamName', 'WINS', 'LOSSES', 'WinPCT']])
```

### View Today's Schedule

```python
from nba_api.stats.endpoints import scoreboardv3
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
board = scoreboardv3.ScoreboardV3(game_date=today, league_id='00')
data = board.get_dict()

for game in data['scoreboard']['games']:
    home = game['homeTeam']
    away = game['awayTeam']
    print(f"{away['teamName']} @ {home['teamName']}")
```

### Get Player Stats

```python
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

# Find player ID
ball_info = players.find_players_by_full_name("LaMelo Ball")
player_id = ball_info[0]['id']

# Get career stats
career = playercareerstats.PlayerCareerStats(player_id=player_id)
df = career.season_totals_regular_season.get_data_frame()
print(df.tail())
```

### Real-time Scores

```python
from nba_api.live.nba.endpoints import scoreboard

games = scoreboard.ScoreBoard()
data = games.get_dict()

for game in data['scoreboard']['games']:
    home = game['homeTeam']['teamName']
    away = game['awayTeam']['teamName']
    home_score = game['homeTeam']['score']
    away_score = game['awayTeam']['score']
    status = game['gameStatusText']
    print(f"{away} @ {home}: {away_score}-{home_score} ({status})")
```

---

## Example Use Cases

### Example 1: Track a Specific Player

**Scenario**: Track LaMelo Ball's games and add to calendar

```python
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerinjuries, teamgamelog
from datetime import datetime, timedelta

# 1. Find player
ball = players.find_players_by_full_name("LaMelo Ball")[0]
print(f"Player: {ball['full_name']}")

# 2. Check injury status
try:
    injuries = playerinjuries.PlayerInjuries(player_id=ball['id'])
    injury_df = injuries.get_data_frames()[0]
    if not injury_df.empty:
        print(f"⚠️ Injury: {injury_df.iloc[0]['INJURY']}")
    else:
        print("✅ No injuries")
except:
    print("⚠️ Injury info not available")

# 3. Get upcoming games
gamelog = teamgamelog.TeamGameLog(
    team_id=ball['team_id'], 
    season='2025-26'
)
df = gamelog.get_data_frames()[0]

# Filter future games
today = datetime.now()
upcoming = []
for idx, row in df.iterrows():
    try:
        game_date = datetime.strptime(row['GAME_DATE'], '%Y-%m-%d')
        if game_date > today:
            upcoming.append({
                'date': row['GAME_DATE'],
                'matchup': row['MATCHUP']
            })
    except:
        continue

print(f"\nUpcoming games:")
for game in upcoming[:5]:
    print(f"  {game['date']}: {game['matchup']}")
```

### Example 2: Crunch Time Alerts

**Scenario**: Get notified when game is in crunch time (last 5 min + close score)

```python
from nba_api.live.nba.endpoints import scoreboard, playbyplay
import time
from datetime import datetime

def check_crunch_time():
    """Check for crunch time games (period >= 4, clock < 5:00, score diff <= 5)"""
    
    games = scoreboard.ScoreBoard()
    data = games.get_dict()
    
    crunch_games = []
    
    for game in data['scoreboard']['games']:
        if game['gameStatus'] != 2:  # Only live games
            continue
        
        home_score = game['homeTeam']['score']
        away_score = game['awayTeam']['score']
        score_diff = abs(home_score - away_score)
        
        if score_diff > 5:
            continue
        
        # Get detailed time from play-by-play
        try:
            pbp = playbyplay.PlayByPlay(game_id=game['gameId'])
            pbp_data = pbp.get_dict()
            
            if pbp_data['game']['actions']:
                last_action = pbp_data['game']['actions'][-1]
                period = last_action.get('period', 0)
                clock = last_action.get('clock', '12:00')
                
                # Only 4th quarter or OT
                if period >= 4:
                    mins, secs = clock.split(':')
                    remaining = int(mins) + int(secs) / 60
                    
                    if remaining < 5:
                        crunch_games.append({
                            'game': f"{game['awayTeam']['teamName']} @ {game['homeTeam']['teamName']}",
                            'score': f"{away_score} - {home_score}",
                            'clock': clock,
                            'period': period
                        })
        except:
            continue
    
    return crunch_games

# Monitor loop
print("🏀 Monitoring for crunch time games...")
notified = set()

while True:
    games = check_crunch_time()
    
    for game in games:
        key = f"{game['game']}_{game['clock']}"
        if key not in notified:
            print(f"\n🔥 CRUNCH TIME!")
            print(f"   {game['game']}")
            print(f"   Score: {game['score']}")
            print(f"   Time: {game['clock']} (Q{game['period']})")
            notified.add(key)
    
    time.sleep(30)  # Check every 30 seconds
```

### Example 3: Add Games to Calendar

**Scenario**: Automatically add player's games to Apple Calendar

```python
import subprocess
from datetime import datetime, timedelta

def add_game_to_calendar(player_name, game_date, matchup, calendar="NBA"):
    """Add game to Apple Calendar"""
    
    # Parse game time (assumes 7:00 PM local)
    game_time = datetime.strptime(game_date, '%Y-%m-%d')
    game_time = game_time.replace(hour=19, minute=0)
    
    title = f"🏀 {player_name}: {matchup}"
    end_time = game_time + timedelta(hours=2, minutes=30)
    
    script = f'''
    tell application "Calendar"
        tell calendar "{calendar}"
            make new event at end with properties {{summary:"{title}", start date:date "{game_time.strftime('%Y-%m-%d %H:%M:%S')}", end date:date "{end_time.strftime('%Y-%m-%d %H:%M:%S')}"}}
        end tell
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        print(f"✅ Added: {title} on {game_date}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

# Usage
add_game_to_calendar("LaMelo Ball", "2026-03-18", "Heat @ Hornets")
```

---

## Common Commands

```bash
# Hornets standings
python -c "from nba_api.stats.endpoints import leaguestandings; df = leaguestandings.LeagueStandings().get_data_frames()[0]; print(df[df['TeamName'] == 'Hornets'][['TeamName', 'WINS', 'LOSSES', 'WinPCT']])"

# Today's games
python -c "from nba_api.stats.endpoints import scoreboardv3; from datetime import datetime; board = scoreboardv3.ScoreboardV3(game_date=datetime.now().strftime('%Y-%m-%d'), league_id='00'); [print(f\"{g['awayTeam']['teamName']} @ {g['homeTeam']['teamName']}\") for g in board.get_dict()['scoreboard']['games']]"

# Player career stats
python -c "from nba_api.stats.static import players; from nba_api.stats.endpoints import playercareerstats; p = players.find_players_by_full_name('LaMelo Ball')[0]; df = playercareerstats.PlayerCareerStats(player_id=p['id']).season_totals_regular_season.get_data_frame(); print(df.tail())"
```

---

## Error Handling

```python
from nba_api.stats.library.http import NBAHTTPError

try:
    # API call
    pass
except NBAHTTPError as e:
    print(f"NBA API Error: {e}")
except Exception as e:
    print(f"Unknown error: {e}")
```

---

## Important Notes

1. **Rate Limiting**: Free but may be throttled if too frequent. Cache data when possible.
2. **Timezone Conversion**: NBA times are US Eastern Time. Convert to local timezone (+12/13 hours for Beijing).
3. **Live Data Delay**: Live API has 1-3 second delay.
4. **Update Frequency**: Stats API updates slowly. Check once per minute max.

---

## More Information

See [API_REFERENCE.md](./API_REFERENCE.md) for complete endpoint documentation.
