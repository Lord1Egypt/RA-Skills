---
name: oo-api-sports
description: "API-SPORTS (api-sports.io). Use this skill for ANY API-SPORTS request — searching and reading data. Whenever a task involves API-SPORTS, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "API-SPORTS"
  author: "OOMOL"
  version: "1.0.1"
  services: ["api_sports"]
  icon: "https://static.oomol.com/logo/third-party/API-Sports.svg"
---

# API-SPORTS

Operate **API-SPORTS** through your OOMOL-connected account. This skill calls the `api_sports` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected API-SPORTS. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "api_sports" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "api_sports" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `football_get_fixture_events` — Query the event stream for a specified football match, such as goals, red and yellow cards, substitutions, and VAR.
- `football_get_fixture_lineups` — Query the lineup, formation, starting lineup, substitutes and coaching information for a specified football game.
- `football_get_fixture_statistics` — Query the technical statistics of the specified football match, optionally returning the statistics of the first and second halves.
- `football_get_predictions` — Check official predictions and recommendations for selected football matches.
- `football_get_standings` — Query the football standings for a specified season, and the results can be converged by league or team.
- `football_get_team_statistics` — Query the overall statistical performance of a specified team in a certain league season.
- `football_list_fixtures` — Check football schedules and scores by game, league, team, date, live status or time range.
- `football_list_injuries` — Check football injury information by game, league, team, player or date.
- `football_list_leagues` — Query football leagues by league, country, season or search keyword and return the current available data coverage capabilities.
- `football_list_players_profiles` — Search football player profiles by player ID, search keyword or pagination page number.
- `football_list_players_statistics` — Query player season statistics by player, team or league, support paging and search.
- `football_list_team_squad` — Query the current lineup of the specified team.
- `football_list_teams` — Search football teams by league, season, country, stadium or search keyword.
- `football_list_top_scorers` — Query the scorer list of the specified league season.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change API-SPORTS state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — API-SPORTS is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=api_sports
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- API-SPORTS homepage: https://api-sports.io
