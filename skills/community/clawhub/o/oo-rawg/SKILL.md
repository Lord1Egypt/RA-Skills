---
name: oo-rawg
description: "RAWG (rawg.io). Use this skill for ANY RAWG request — searching and reading data. Whenever a task involves RAWG, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "RAWG"
  author: "OOMOL"
  version: "1.0.1"
  services: ["rawg"]
  icon: "https://static.oomol.com/logo/third-party/RAWG%20Video%20Games%20Database.svg"
---

# RAWG

Operate **RAWG** through your OOMOL-connected account. This skill calls the `rawg` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected RAWG. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "rawg" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "rawg" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_developer` — Get detailed information for one developer from RAWG.
- `get_game` — Get detailed information for one game from RAWG.
- `get_genre` — Get detailed information for one genre from RAWG.
- `get_platform` — Get detailed information for one platform from RAWG.
- `get_publisher` — Get detailed information for one publisher from RAWG.
- `get_store` — Get detailed information for one store from RAWG.
- `get_tag` — Get detailed information for one tag from RAWG.
- `list_developers` — List game developers from RAWG.
- `list_game_additions` — List additions for one RAWG game.
- `list_game_movies` — Get the RAWG movie payload for one game.
- `list_game_reddit_posts` — Get the RAWG Reddit post payload for one game.
- `list_game_screenshots` — List screenshots for one RAWG game.
- `list_game_series` — List series games related to one RAWG game.
- `list_game_stores` — List stores for one RAWG game.
- `list_games` — List games from RAWG with optional search, filtering, sorting, and pagination.
- `list_genres` — List game genres from RAWG.
- `list_parent_platforms` — List parent platforms from RAWG.
- `list_platforms` — List gaming platforms from RAWG.
- `list_publishers` — List game publishers from RAWG.
- `list_stores` — List video game stores from RAWG.
- `list_tags` — List game tags from RAWG.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change RAWG state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — RAWG is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=rawg
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- RAWG homepage: https://rawg.io
