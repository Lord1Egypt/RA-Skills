---
name: oo-qiuxiaoce
description: "QiuXiaoCe (qiuxiaoce.com). Use this skill for ANY QiuXiaoCe request — searching and reading data. Whenever a task involves QiuXiaoCe, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "QiuXiaoCe"
  author: "OOMOL"
  version: "1.0.2"
  services: ["qiuxiaoce"]
  icon: "https://static.oomol.com/logo/third-party/qiuxiaoce.png"
---

# QiuXiaoCe

Operate **QiuXiaoCe** through your OOMOL-connected account. This skill calls the `qiuxiaoce` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected QiuXiaoCe. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "qiuxiaoce" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "qiuxiaoce" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_daily_digest` — List matches for a sales date, including fixture IDs and report availability. Omit date for the current sales day.
- `get_fixture` — Read a fixture's kickoff, score, status and teams.
- `get_fixture_events` — Read goals, cards and substitutions for a fixture.
- `get_fixture_lineups` — Read announced starting lineups and substitutes for a fixture.
- `get_fixture_players` — Read player-by-player post-match statistics for a fixture.
- `get_fixture_stats` — Read post-match technical statistics for a fixture.
- `get_league` — Read league details and current standings.
- `get_quota` — Read remaining credits, expiration and today's usage without consuming credits.
- `get_standings` — Read league standings for a season, defaulting to the latest available season.
- `get_team` — Read a team's names, country, venue and founding information.
- `list_fixtures` — Find fixtures by date, date range, league, team, round, status or fixture ID. Use either date or from/to.
- `list_league_fixtures` — List all league fixtures and scores for a season.
- `list_league_seasons` — List available season years before querying historical league data.
- `list_league_teams` — List participating teams for a league season.
- `list_league_top_assists` — Read a league season's assist leaders.
- `list_league_top_scorers` — Read a league season's top scorers.
- `list_leagues` — List supported leagues, optionally searching by name or Chinese alias.
- `search_teams` — Search teams by name, including Chinese aliases. Verify the returned identity before selecting an ID.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change QiuXiaoCe state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — QiuXiaoCe is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/qiuxiaoce
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- QiuXiaoCe homepage: https://www.qiuxiaoce.com/
- API documentation: https://www.qiuxiaoce.com/data-docs/
