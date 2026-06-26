---
name: oo-manus
description: "Manus (manus.im). Use this skill for ANY Manus request — reading, creating, updating, and deleting data. Whenever a task involves Manus, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Manus"
  author: "OOMOL"
  version: "1.0.1"
  services: ["manus"]
  icon: "https://static.oomol.com/logo/third-party/manus.svg"
---

# Manus

Operate **Manus** through your OOMOL-connected account. This skill calls the `manus` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Manus. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "manus" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "manus" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `confirm_task_action` — Confirm a pending Manus task action from a waiting status event. Use send_message instead for messageAskUser events. [write]
- `create_project` — Create a Manus project for grouping tasks under shared instructions. [write]
- `create_task` — Create a new asynchronous Manus task from a message and optional project, connector, skill, sharing, or structured-output settings. [write]
- `delete_task` — Permanently delete a stopped Manus task. Stop a running task before deleting it. [destructive]
- `get_agent` — Retrieve a Manus custom agent by ID.
- `get_task` — Retrieve a Manus task's current status and metadata.
- `list_agents` — List Manus custom agents in the current account.
- `list_connectors` — List Manus connectors installed in the current account.
- `list_online_browser_clients` — List online Manus browser clients that can be selected when confirming needConnectMyBrowser waiting events.
- `list_projects` — List Manus projects available to the current account.
- `list_skills` — List Manus skills available to the current account or project.
- `list_task_messages` — List Manus task event messages with cursor pagination.
- `list_tasks` — List Manus tasks with optional scope filters and cursor pagination.
- `send_message` — Send a follow-up message to an existing Manus task. [write]
- `stop_task` — Stop a running Manus task. [write]
- `update_agent` — Update a Manus custom agent's display name or description. [write]
- `update_task` — Update a Manus task title, sharing visibility, or task-list visibility. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Manus state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Manus is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=manus
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Manus homepage: https://manus.im
