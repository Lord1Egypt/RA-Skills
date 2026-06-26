---
name: nba
description: Get today's NBA game schedule, live scores, final results, and current season standings. Use when the user asks about NBA games today, live NBA scores, game results, NBA standings, team records, or anything about the current NBA season. Triggers on phrases like "NBA schedule", "NBA scores today", "NBA standings", "what NBA games are on", "NBA results", "who won last night in NBA".
---

# NBA Skill

Fetches live NBA data via the NBA CDN API (scoreboard) and StatMuse HTML (standings).

## Data Sources

| Data | Source |
|------|--------|
| Today's games & live scores | `https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json` |
| Standings (East/West) | StatMuse HTML tables — `https://www.statmuse.com/nba/ask/nba-2025-26-eastern-conference-standings` |
| Full schedule | `https://www.nba.com/schedule` |

## Quick Usage

Run the script from the skill directory:

```bash

# Today's schedule + live scores
python scripts/nba_data.py scoreboard

# Current standings
python scripts/nba_data.py standings

# Both (default)
python scripts/nba_data.py all
```

On Linux/macOS:
```bash
python3 scripts/nba_data.py all
```

## Script: `scripts/nba_data.py`

- **`scoreboard`** — Fetches today's games from NBA CDN. Shows status (upcoming/live/final), scores, quarter/clock, and game leaders (pts/reb/ast).
- **`standings`** — Scrapes StatMuse for East + West conference tables: rank, team, W, L, pct, home record.
- **`all`** — Both commands combined.

No API key required. Pure stdlib (urllib, json, re).

## Workflow

1. Run `python scripts/nba_data.py all` (set `PYTHONIOENCODING=utf-8` on Windows first).
2. Run `python -c "from datetime import datetime; print(datetime.now().astimezone().tzinfo)` to get timezone.
3. Parse and present output to the user in clean readable format, change UTC time to local timezone.
4. For deeper stats (player stats, box scores, specific game details), direct user to:
   - `https://www.nba.com/game/<gameId>` for box scores
   - `https://www.statmuse.com/nba` for historical stats queries

## Notes

- The NBA CDN scoreboard updates every ~30 seconds during live games.
- Season year in StatMuse URLs (e.g. `2025-26`) may need updating at season start.
- StatMuse standings URL pattern: `https://www.statmuse.com/nba/ask/nba-YYYY-YY-[eastern|western]-conference-standings`
