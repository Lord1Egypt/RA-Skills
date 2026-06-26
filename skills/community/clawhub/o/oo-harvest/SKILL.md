---
name: oo-harvest
description: "Harvest (getharvest.com). Use this skill for ANY Harvest request — reading, creating, updating, and deleting data. Whenever a task involves Harvest, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Harvest"
  author: "OOMOL"
  version: "1.0.1"
  services: ["harvest"]
  icon: "https://static.oomol.com/logo/third-party/Harvest.svg"
---

# Harvest

Operate **Harvest** through your OOMOL-connected account. This skill calls the `harvest` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Harvest. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "harvest" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "harvest" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_time_entry` — Create a new Harvest time entry. [write]
- `delete_time_entry` — Delete a Harvest time entry by ID. [destructive]
- `get_client` — Get a single Harvest client by ID.
- `get_current_user` — Get the current authenticated Harvest user.
- `get_project` — Get a single Harvest project by ID.
- `get_task` — Get a single Harvest task by ID.
- `get_time_entry` — Get a single Harvest time entry by ID.
- `list_clients` — List clients available in the connected Harvest account.
- `list_project_task_assignments` — List task assignments for a specific Harvest project.
- `list_projects` — List projects available in the connected Harvest account.
- `list_tasks` — List tasks available in the connected Harvest account.
- `list_time_entries` — List Harvest time entries with optional resource and date filters.
- `restart_time_entry` — Restart a stopped Harvest time entry. [write]
- `stop_time_entry` — Stop a running Harvest time entry. [write]
- `update_time_entry` — Update an existing Harvest time entry. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Harvest state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Harvest is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=harvest
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Harvest homepage: https://www.getharvest.com
