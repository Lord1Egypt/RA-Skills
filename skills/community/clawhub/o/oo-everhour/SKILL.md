---
name: oo-everhour
description: "Everhour (everhour.com). Use this skill for ANY Everhour request — reading, creating, and updating data. Whenever a task involves Everhour, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Everhour"
  author: "OOMOL"
  version: "1.0.1"
  services: ["everhour"]
  icon: "https://static.oomol.com/logo/third-party/everhour.png"
---

# Everhour

Operate **Everhour** through your OOMOL-connected account. This skill calls the `everhour` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Everhour. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "everhour" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "everhour" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_time_record` — Create one Everhour time record with a duration, date, and optional task or user assignment. [write]
- `get_current_timer` — Get the current running Everhour timer.
- `get_current_user` — Get the current Everhour user profile associated with the API key.
- `get_project` — Get one Everhour project by its project ID.
- `get_task` — Get one Everhour task by its task ID.
- `list_project_tasks` — List the tasks in one Everhour project with optional paging and search filters.
- `list_projects` — List Everhour projects with optional text, platform, and limit filters.
- `list_time_records` — List Everhour team time records with optional date range and paging filters.
- `list_users` — List the users in the Everhour team that the API key can access.
- `search_tasks` — Search Everhour tasks across accessible projects.
- `start_timer` — Start an Everhour timer for a task with an optional user date and comment. [write]
- `stop_timer` — Stop the current Everhour timer and return the final timer snapshot. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Everhour state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Everhour is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=everhour
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Everhour homepage: https://everhour.com
