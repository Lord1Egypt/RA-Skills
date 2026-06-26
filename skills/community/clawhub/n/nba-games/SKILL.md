---
name: nba_games
description: Gets upcoming and/or recent NBA game results for a specified team. Use this skill when asked about scheduled, upcoming, or past games for any NBA team.
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---
# NBA Games Skill

Fetch NBA schedule and results for a team using the python program nba-schedule.py.

## Install
Run once to install the script from github. Skip if script is already present.

```bash
SCRIPT_PATH="$HOME/.openclaw/skills/nba_games/nba-schedule.py"
if [ ! -f "$SCRIPT_PATH" ]; then
  mkdir -p "$(dirname "$SCRIPT_PATH")"
  curl -fsSL \
    https://raw.githubusercontent.com/highdeserthacker/nba-schedule/main/nba-schedule.py \
    -o "$SCRIPT_PATH"
fi
```

> Source: https://github.com/highdeserthacker/nba-schedule

## Script

```
$HOME/.openclaw/skills/nba_games/nba-schedule.py
```

## Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `--team-id <id>` | Yes | - | ESPN team ID |
| `--days-future <n>` | No | 3 | Upcoming days to include (0 = none) |
| `--days-past <n>` | No | 0 | Past days to include (0 = none) |

## Team ID Lookup

If the team ID is unknown, run:
```bash
python3 /home/node/python/nba-schedule/nba-schedule.py --list
```
This prints all 30 teams with their IDs.

## Usage Examples

```bash
# Next 3 upcoming Golden State Warriors games
python3 $HOME/.openclaw/skills/nba_games/nba-schedule.py --team-id 9

# Warriors games in the next 2 days only
python3 $HOME/.openclaw/skills/nba_games/nba-schedule.py --team-id 9 --days-future 2

# Warriors games in the next 2 days plus yesterday's result
python3 $HOME/.openclaw/skills/nba_games/nba-schedule.py --team-id 9 --days-future 2 --days-past 1

# Lakers: next 5 days
python3 $HOME/.openclaw/skills/nba_games/nba-schedule.py --team-id 13 --days-future 5
```

## Output Format

Returns a JSON array of game objects sorted by date ascending. Empty array `[]` means no games in the requested window.

```json
[
  {
    "team":     "Golden State Warriors",
    "opponent": "Los Angeles Lakers",
    "location": "home",
    "datetime": "Fri Mar 28, 7:30 PM PDT",
    "result":   ""
  }
]
```

| Field | Description |
|---|---|
| `team` | Full display name of the requested team |
| `opponent` | Full display name of the opposing team |
| `location` | `"home"` or `"away"` |
| `datetime` | Game time in the container's local timezone |
| `result` | Empty string for upcoming games; score string for completed games (e.g. `"Golden State Warriors (W) 112, Los Angeles Lakers 98"`) |

## Presentation Guidelines

- For **upcoming games**: state opponent, home/away, and tip-off date/time.
- For **completed games**: state opponent, final score, and win/loss.
- If the result array is empty, no games fall in the requested window - do not fabricate or guess.
- Present results conversationally unless the caller context requires structured output.

## Trigger Examples

- "When is the next Warriors game?"
- "Did the Bulls win last night?"
- "Show me the Lakers schedule for the next week."
- "What are the upcoming Celtics games?"
