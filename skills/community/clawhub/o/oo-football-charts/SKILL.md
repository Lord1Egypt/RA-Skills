---
name: oo-football-charts
description: "Football Charts (football-charts.com). Use this skill for ANY Football Charts request — searching and reading data. Whenever a task involves Football Charts, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Football Charts"
  author: "OOMOL"
  version: "1.0.0"
  services: ["football_charts"]
  icon: "https://static.oomol.com/logo/third-party/football_charts.png"
---

# Football Charts

Operate **Football Charts** through your OOMOL-connected account. This skill calls the `football_charts` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Football Charts. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "football_charts" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "football_charts" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_fixtures` — Get upcoming fixtures for a league with kickoff times, match slugs, and calibrated Dixon-Coles model probabilities across match result, over/under goal lines, and both-teams-to-score markets.
- `get_goal_timing` — Get goals scored across 15-minute match intervals (0-15 through 90+) for every team in a league season, including peak scoring periods, late-goal share, and first-half share. Optionally filter by team name substring.
- `get_league_table` — Get the standings table for a league season, including form, expected points, luck category, and goal averages. Supports ordering by points (classic), over/under-performance (luck), or goals scored (goals).
- `get_match` — Get full details and calibrated Dixon-Coles probabilities for one match identified by its slug (country/league-slug/YYYY-MM-DD-home-vs-away).
- `get_results` — Get finished matches for a league season in chronological order with full-time and half-time scores, first-goal minute, and kickoff timestamps. Optionally filter by team name substring.
- `get_season_projection` — Get the daily 10,000-run Monte Carlo season projection for a league, returning each team's title, top-four, and relegation (bottom-three) probabilities, mean projected points, 10th-to-90th percentile points range, and finishing-position matrix.
- `get_team` — Get a single team's season profile in a league, including its standings row, full match log, 15-minute goal-timing breakdown, first-goal distribution, and per-match statistical averages where covered.
- `get_track_record` — Get the public calibration track record of the Football Charts probability model over settled matches, including overall hit rate, Brier score, reliability buckets, and recent scored predictions.
- `list_leagues` — List all 98 football leagues covered across 44 countries with their competition key, display name, country, and available season strings.
- `list_teams` — List all teams competing in a league season in standings order with their slugs and summary records.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Football Charts state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Football Charts is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/football_charts
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Football Charts homepage: https://www.football-charts.com
- API documentation: https://www.football-charts.com/developers
