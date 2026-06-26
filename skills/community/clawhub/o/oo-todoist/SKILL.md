---
name: oo-todoist
description: "Todoist (todoist.com). Use this skill for ANY Todoist request — reading, creating, and updating data. Whenever a task involves Todoist, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Todoist"
  author: "OOMOL"
  version: "1.0.1"
  services: ["todoist"]
  icon: "https://static.oomol.com/logo/third-party/Todoist.svg"
---

# Todoist

Operate **Todoist** through your OOMOL-connected account. This skill calls the `todoist` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Todoist. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "todoist" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "todoist" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `close_task` — Mark a Todoist task complete. Recurring tasks advance to their next occurrence. [write]
- `create_comment` — Create a Todoist comment on exactly one task or project. [write]
- `create_project` — Create a Todoist project with optional description, color, parent, view style, and workspace placement. [write]
- `create_section` — Create a Todoist section inside a project. [write]
- `create_task` — Create a Todoist task with optional project, section, parent, labels, assignment, due date, deadline, and duration fields. [write]
- `get_comment` — Get a Todoist comment by comment ID. [write]
- `get_current_user` — Retrieve the current Todoist user profile and plan metadata.
- `get_project` — Get a Todoist project by project ID.
- `get_section` — Get a Todoist section by section ID.
- `get_task` — Get a Todoist task by task ID.
- `list_comments` — List Todoist comments for exactly one task or project.
- `list_labels` — List Todoist labels with cursor pagination.
- `list_projects` — List active Todoist projects with optional folder, workspace, and cursor filters.
- `list_sections` — List active Todoist sections with optional project and cursor filters.
- `list_tasks` — List active Todoist tasks with optional project, section, parent, label, goal, ID, and cursor filters.
- `update_comment` — Update a Todoist comment by comment ID. [write]
- `update_project` — Update a Todoist project by project ID. [write]
- `update_section` — Update a Todoist section by section ID. [write]
- `update_task` — Update a Todoist task by task ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Todoist state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Todoist is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=todoist
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Todoist homepage: https://www.todoist.com
