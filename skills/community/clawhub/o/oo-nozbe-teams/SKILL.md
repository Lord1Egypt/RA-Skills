---
name: oo-nozbe-teams
description: "Nozbe (nozbe.com). Use this skill for ANY Nozbe request — reading, creating, updating, and deleting data. Whenever a task involves Nozbe, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Nozbe"
  author: "OOMOL"
  version: "1.0.5"
  services: ["nozbe_teams"]
  icon: "https://static.oomol.com/logo/third-party/nozbe_teams.svg"
---

# Nozbe

Operate **Nozbe** through your OOMOL-connected account. This skill calls the `nozbe_teams` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Nozbe. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nozbe_teams" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nozbe_teams" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_comment` — Add a comment to a Nozbe task. [write]
- `create_project` — Create a Nozbe project in a team. [write]
- `create_task` — Create a task in Nozbe. [write]
- `delete_comment` — Delete a Nozbe task comment and return the updated comment resource. [destructive]
- `delete_project` — Delete a Nozbe project by ID. [destructive]
- `delete_task` — Delete a Nozbe task by ID. [destructive]
- `get_comment` — Get a Nozbe task comment by ID.
- `get_project` — Get a Nozbe project by ID.
- `get_task` — Get a Nozbe task by ID.
- `list_comments` — List Nozbe task comments with pagination, sorting, and task filtering.
- `list_projects` — List Nozbe projects with pagination, sorting, and team filters.
- `list_tasks` — List Nozbe tasks with pagination, sorting, and project filtering.
- `list_teams` — List teams accessible with the connected Nozbe API token.
- `update_comment` — Update writable fields on a Nozbe task comment. [write]
- `update_project` — Update writable fields on a Nozbe project. [write]
- `update_task` — Update writable fields on a Nozbe task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Nozbe state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Nozbe is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/nozbe_teams
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Nozbe homepage: https://nozbe.com
- API documentation: https://nozbe.help/advancedfeatures/api/
