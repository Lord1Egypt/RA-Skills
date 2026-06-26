---
name: oo-toggl
description: "Toggl Track (toggl.com). Use this skill for ANY Toggl Track request — reading, creating, updating, and deleting data. Whenever a task involves Toggl Track, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Toggl Track"
  author: "OOMOL"
  version: "1.0.1"
  services: ["toggl"]
  icon: "https://static.oomol.com/logo/third-party/Toggl.svg"
---

# Toggl Track

Operate **Toggl Track** through your OOMOL-connected account. This skill calls the `toggl` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Toggl Track. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "toggl" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "toggl" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_project` — Create a new Toggl Track project in a workspace. [write]
- `create_tag` — Create a new Toggl Track tag in a workspace. [write]
- `create_task` — Create a new Toggl Track task inside a project. [write]
- `create_time_entry` — Create a new Toggl Track time entry in a workspace. [write]
- `delete_project` — Delete a Toggl Track project by ID. [destructive]
- `delete_tag` — Delete a Toggl Track tag by ID. [destructive]
- `delete_task` — Delete a Toggl Track task by ID. [destructive]
- `delete_time_entry` — Delete a Toggl Track time entry by ID. [destructive]
- `get_current_time_entry` — Get the current running Toggl Track time entry, if one exists.
- `get_current_user` — Get the currently authenticated Toggl Track user.
- `get_project` — Get a single Toggl Track project by ID.
- `get_task` — Get a single Toggl Track task by ID.
- `get_time_entry` — Get a single Toggl Track time entry by ID.
- `get_workspace` — Get a single Toggl Track workspace by ID.
- `list_projects` — List Toggl Track projects in a workspace.
- `list_tags` — List Toggl Track tags in a workspace.
- `list_tasks` — List Toggl Track tasks for a project.
- `list_time_entries` — List Toggl Track time entries for the authenticated user.
- `list_workspaces` — List the Toggl Track workspaces available to the authenticated user.
- `stop_time_entry` — Stop a running Toggl Track time entry. [write]
- `update_project` — Update an existing Toggl Track project. [write]
- `update_tag` — Update an existing Toggl Track tag. [write]
- `update_task` — Update an existing Toggl Track task. [write]
- `update_time_entry` — Update an existing Toggl Track time entry. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Toggl Track state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Toggl Track is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=toggl
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Toggl Track homepage: https://toggl.com/track/
