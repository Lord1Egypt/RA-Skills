---
name: oo-productive
description: "Productive (productive.io). Use this skill for ANY Productive request — reading, creating, updating, and deleting data. Whenever a task involves Productive, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Productive"
  author: "OOMOL"
  version: "1.0.1"
  services: ["productive"]
  icon: "https://static.oomol.com/logo/third-party/productive.svg"
---

# Productive

Operate **Productive** through your OOMOL-connected account. This skill calls the `productive` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Productive. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "productive" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "productive" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_task` — Create a Productive task using JSON:API attributes and relationships. [write]
- `create_time_entry` — Create a Productive time entry in minutes for a person and service. [write]
- `delete_time_entry` — Delete a Productive time entry by ID. [destructive]
- `get_task` — Retrieve one Productive task by ID.
- `list_tasks` — List Productive tasks with optional pagination, sorting, filters, and includes.
- `list_time_entries` — List Productive time entries with optional pagination, sorting, filters, and includes.
- `update_task` — Update a Productive task by ID. [write]
- `update_time_entry` — Update a Productive time entry by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Productive state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Productive is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=productive
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Productive homepage: https://productive.io
