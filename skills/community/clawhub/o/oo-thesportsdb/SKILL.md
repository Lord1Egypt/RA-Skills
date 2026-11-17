---
name: oo-thesportsdb
description: "TheSportsDB (thesportsdb.com). Use this skill for ANY TheSportsDB request — searching and reading data. Whenever a task involves TheSportsDB, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TheSportsDB"
  author: "OOMOL"
  version: "1.0.2"
  services: ["thesportsdb"]
  icon: "https://static.oomol.com/logo/third-party/thesportsdb.svg"
---

# TheSportsDB

Operate **TheSportsDB** through your OOMOL-connected account. This skill calls the `thesportsdb` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TheSportsDB. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "thesportsdb" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "thesportsdb" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_league_season_schedule` — Get a TheSportsDB league schedule for a specific season.
- `get_livescores` — Get current TheSportsDB live scores for all sports, one sport or a league ID.
- `get_schedule` — Get upcoming or previous events for a league, team or venue. TheSportsDB controls the result limit.
- `get_team_season_schedule` — Get the full current season schedule for a TheSportsDB team.
- `list_catalog` — List the countries, sports or leagues supported by TheSportsDB.
- `list_related` — List teams or seasons in a league, or players in a team, using TheSportsDB IDs.
- `lookup_entity` — Look up a TheSportsDB league, team, player, event or venue by ID.
- `search_entities` — Search TheSportsDB leagues, teams, players, events or venues by name. Requires a Premium API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TheSportsDB state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TheSportsDB is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/thesportsdb
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TheSportsDB homepage: https://www.thesportsdb.com/
- API documentation: https://www.thesportsdb.com/documentation
