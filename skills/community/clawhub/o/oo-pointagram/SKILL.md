---
name: oo-pointagram
description: "Pointagram (pointagram.com). Use this skill for ANY Pointagram request — reading, creating, updating, and deleting data. Whenever a task involves Pointagram, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pointagram"
  author: "OOMOL"
  version: "1.0.2"
  services: ["pointagram"]
  icon: "https://static.oomol.com/logo/third-party/pointagram.png"
---

# Pointagram

Operate **Pointagram** through your OOMOL-connected account. This skill calls the `pointagram` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pointagram. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pointagram" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pointagram" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_team_player` — Add a player to a Pointagram team using a player ID, email address or external ID. [write]
- `create_player` — Create a Pointagram player. Online players receive an invitation; an existing player produces a conflict. [write]
- `create_team` — Create a Pointagram team with an existing icon filename. [write]
- `delete_player` — Soft-delete a Pointagram player. Administrators cannot be removed. Complete anonymization requires the Pointagram UI; inspect the upstream status and message. [destructive]
- `get_player` — Get a Pointagram player by ID.
- `get_team` — Get a Pointagram team by ID.
- `list_players` — List or search Pointagram players. Continue with data.pagination.next_offset; offset is a player ID, not a row count.
- `list_team_players` — List the players belonging to a Pointagram team.
- `list_teams` — List Pointagram teams.
- `remove_team_player` — Remove a player from a Pointagram team's membership without deleting the player. [write]
- `update_player` — Update a Pointagram player using the provided fields. [write]
- `update_team` — Update a Pointagram team's name, icon and filter settings. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pointagram state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pointagram is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pointagram
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Pointagram homepage: https://www.pointagram.com/
- API documentation: https://www.pointagram.com/custom-api-2-0-gamification/
