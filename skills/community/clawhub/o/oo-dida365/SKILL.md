---
name: oo-dida365
description: "Dida365 (dida365.com). Use this skill for ANY Dida365 request — reading, creating, updating, and deleting data. Whenever a task involves Dida365, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Dida365"
  author: "OOMOL"
  version: "1.0.2"
  services: ["dida365"]
  icon: "https://static.oomol.com/logo/third-party/ticktick.svg"
---

# Dida365

Operate **Dida365** through your OOMOL-connected account. This skill calls the `dida365` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Dida365. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "dida365" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "dida365" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `complete_task` — Mark a Dida365 (滴答清单) task as completed by project ID and task ID. [write]
- `create_or_update_habit_checkin` — Create or update a Dida365 (滴答清单) habit check-in for a date stamp. [write]
- `create_project` — Create a Dida365 (滴答清单) project with optional color, sort order, view mode, and kind. [write]
- `create_task` — Create a Dida365 (滴答清单) task under a project with optional schedule, reminders, recurrence, and checklist items. [write]
- `delete_project` — Delete a Dida365 (滴答清单) project by project ID. The connector treats a missing project as already deleted. [destructive]
- `delete_task` — Delete a Dida365 (滴答清单) task by project ID and task ID. The connector treats a missing task as already deleted. [destructive]
- `filter_tasks` — Filter Dida365 (滴答清单) tasks by project, date range, priority, tags, and status by using the official filter endpoint.
- `get_habit` — Get a Dida365 (滴答清单) habit by its habit ID.
- `get_project_by_id` — Get a Dida365 (滴答清单) project by its project ID.
- `get_project_with_data` — Get a Dida365 (滴答清单) project together with its undone tasks and columns by project ID.
- `get_task_by_project_and_id` — Get a Dida365 (滴答清单) task by project ID and task ID.
- `get_user_project` — List the projects available to the connected Dida365 (滴答清单) account.
- `list_all_tasks` — List undone Dida365 (滴答清单) tasks across projects. This is a connector-level aggregate helper over list-projects plus project-data fetches.
- `list_completed_tasks` — List completed Dida365 (滴答清单) tasks within optional project and date filters by using the official completed-tasks endpoint.
- `list_habit_checkins` — List Dida365 (滴答清单) habit check-ins for one or more habits over a date stamp range.
- `list_habits` — List habits available to the connected Dida365 (滴答清单) account.
- `move_tasks` — Move one or more Dida365 (滴答清单) tasks between projects by using the official move endpoint. [write]
- `update_project` — Update a Dida365 (滴答清单) project by project ID. [write]
- `update_task` — Update a Dida365 (滴答清单) task by task ID and project ID, including checklist items and recurrence fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Dida365 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Dida365 is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=dida365
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Dida365 homepage: https://dida365.com
