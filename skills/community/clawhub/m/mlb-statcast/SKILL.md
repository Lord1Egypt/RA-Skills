---
name: mlb-statcast
version: 1.0.0
description: Query MLB Statcast data via the statcast MCP server — player lookups, expected stats, pitch arsenals, exit velocity, barrel rate, percentile ranks, standings, and more. Use when asked about any MLB player, team, or pitching/hitting metric beyond traditional box score numbers.
---

# MLB Statcast

Get pitch-by-pitch Statcast data, expected stats, pitch arsenals, and advanced metrics for any MLB player, team, or season. Wraps the `statcast` MCP server (installed via `pip install statcast-mcp`).

## When to use

Use this skill whenever the user asks about:
- An MLB player’s Statcast metrics (exit velocity, barrel rate, launch angle, sprint speed, etc.)
- Expected stats (xBA, xSLG, xwOBA) vs actual performance
- A pitcher’s arsenal (fastball, slider, changeup, etc.) and performance by pitch type
- Matchup analysis (batter vs a specific pitch type)
- League leaderboards (EV, barrel%, sprint speed, OAA)
- MLB standings or team-level season stats
- Defensive metrics (Outs Above Average)

If the question can be answered with traditional box-score stats only, prefer `wikipedia` or a web search. This skill is for **advanced, Statcast-derived** numbers.

## Quick Usage

```bash
# Player ID lookup (always do this first for new players)
mcporter call statcast.player_lookup "player_name=Shohei Ohtani"

# Batter percentile ranks (note: param is `year`, not `season`)
mcporter call statcast.batter_percentile_ranks "player_name=Aaron Judge" "year=2025"

# Pitcher arsenal stats (param is `year`)
mcporter call statcast.statcast_pitcher_arsenal_stats "player_name=Paul Skenes" "year=2025"

# Expected stats for a custom group (param is `year`)
mcporter call statcast.expected_stats_batch "player_names=[\"Judge\",\"Ohtani\",\"Soto\"]" "year=2025"

# Standings (param is `year`)
mcporter call statcast.team_standings "year=2025"

# Pitch-level data for a single game
mcporter call statcast.statcast_search "start_date=2025-06-15" "end_date=2025-06-15" "team=NYY"
```

## Tools (24 total)

### Identity
- `player_lookup` — Look up MLBAM ID + alternate IDs (FanGraphs, Baseball-Reference, Retro) for a player
- `team_standings` — Current/season MLB division standings

### Pitch-level data (date-range)
- `statcast_search` — All pitches in a date range (optionally filtered by team)
- `statcast_batter` — All pitches seen by a specific batter
- `statcast_pitcher` — All pitches thrown by a specific pitcher

### Season-level actual stats (FanGraphs)
- `season_batting_stats` / `season_pitching_stats` — full-season traditional stats
- `batting_stats_date_range` / `pitching_stats_date_range` — same metrics over a custom window
- `team_season_batting_stats` / `team_season_pitching_stats` — full-roster team totals

### Expected stats (Statcast)
- `statcast_batter_expected_stats` / `statcast_pitcher_expected_stats` — xBA, xSLG, xwOBA for a player
- `expected_stats_batch` — same, but for many players in one call (cheaper)

### Pitch arsenals
- `statcast_batter_pitch_arsenal` — hitter’s outcomes split by incoming pitch type
- `statcast_pitcher_pitch_arsenal` — all pitchers’ pitch mix + outcomes
- `statcast_pitcher_arsenal_stats` — performance (BA/SLG/wOBA/Whiff%/K%/Hard-Hit%) by pitch type for one pitcher

### Batted-ball quality
- `statcast_batter_exitvelo_barrels` — hitter EV + barrel% leaderboard
- `statcast_pitcher_exitvelo_barrels` — pitcher EV-allowed + barrel%-allowed

### League leaderboards & percentiles
- `batter_percentile_ranks` — hitter percentile vs the league (EV, barrel%, xwOBA, sprint speed, etc.) — param: `year`
- `pitcher_percentile_ranks` — pitcher percentile vs the league (spin, whiff%, xERA, K%, etc.) — param: `year`
- `sprint_speed_leaderboard` — top sprinters (param: `year`)
- `outs_above_average` — OAA leaderboard by position (param: `year`, `position`)
- `outfield_directional_oaa` — outfield OAA split by direction

## Workflow: how agents should use this

1. **Resolve IDs first.** For any new player, call `player_lookup` to get the MLBAM ID. Some downstream tools are stricter about exact names; a `player_lookup` confirms spelling and years active.
2. **Prefer batch tools.** `expected_stats_batch` over multiple `statcast_batter_expected_stats` calls.
3. **Keep date ranges short for `statcast_search` / `statcast_batter` / `statcast_pitcher`.** The upstream API is slow on long windows. 1–5 days is ideal; a full month can take 30+ seconds.
4. **Use last names with care.** Substring matching is loose — `player_lookup("Trout")` works, but uncommon names may return multiple candidates. Always check the response.
5. **Cross-check with Wikipedia** for biographical context (career milestones, awards, draft info). The `wikipedia` MCP is the right companion tool.

## Naming & spelling gotchas

- For `player_lookup` use `player_name="Ohtani"` (last name only). The matcher is substring + last-name, and full first+last can over-match.
- For downstream tools like `batter_percentile_ranks` / `pitcher_percentile_ranks` / `statcast_pitcher_arsenal_stats`, use the **full name** (`"Aaron Judge"`, not `"Judge"`) — those tools reject single-name lookups.
- For “Joe Green”-style common names, `player_lookup` may return multiple candidates — read the response and disambiguate by `mlb_played_first` / `mlb_played_last` years.
- Pitcher/hitter ambiguity: if `player_lookup` returns a pitcher when you wanted a hitter (or vice versa), pass the full name in `Last, First` form to disambiguate.

## Installation (Universal)

### 1. Install the MCP server

```bash
pip install statcast-mcp
```

This gives you the `statcast-mcp` command. The server uses `pybaseball` under the hood (no API key needed — it pulls from public Baseball Savant / FanGraphs endpoints).

### 2. Register the server with mcporter

Add to your `mcporter.json`:

```json
{
  "mcpServers": {
    "statcast": {
      "command": "statcast-mcp"
    }
  }
}
```

### 3. Verify

```bash
mcporter call statcast.player_lookup "player_name=Aaron Judge"
```

You should see Judge’s MLBAM ID (592450) and active years.

## Requirements

- Python 3.10+
- `pip install statcast-mcp` (pulls in `lxml`, `mcp`, `pandas`, `pybaseball`, `tabulate`)

## Data sources

All data comes from public Baseball Savant (Statcast) and FanGraphs endpoints via `pybaseball`. No API keys, no rate-limit auth — but please be polite with call volume.

## What this skill does NOT do

- Live game scores / play-by-play (use `mlb-daily-scores` ClawHub skill or a sports-odds MCP)
- Odds, props, betting lines (use a sportsbook or odds API)
- Minor league or college baseball (Statcast coverage is MLB-only)
- Historical seasons before 2008 (Statcast launched in 2008)

## Example questions this answers

- “What was Aaron Judge’s 95th-percentile exit velocity in 2025?”
- “Show me Paul Skenes’ whiff% by pitch type.”
- “Which pitchers had the lowest barrel% allowed last season?”
- “Is Shohei Ohtani outperforming his expected stats?”
- “Who are the top 10 sprinters in baseball right now?”
- “Where did the Yankees rank in barrel% last year?”
