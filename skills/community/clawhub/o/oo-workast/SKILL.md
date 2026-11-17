---
name: oo-workast
description: "Workast (workast.com). Use this skill for ANY Workast request — reading, creating, and updating data. Whenever a task involves Workast, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Workast"
  author: "OOMOL"
  version: "1.0.4"
  services: ["workast"]
  icon: "https://static.oomol.com/logo/third-party/workast.svg"
---

# Workast

Operate **Workast** through your OOMOL-connected account. This skill calls the `workast` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Workast. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "workast" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "workast" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `complete_task` — Mark an existing Workast task as completed. [write]
- `create_task` — Create a task in a Workast space with common assignment and scheduling fields. [write]
- `get_my_details` — Get the Workast user represented by the connected API token.
- `get_space_details` — Get the details of one Workast space by ID.
- `get_space_tasks` — List tasks in a Workast space with status, pagination, and ordering controls.
- `get_task_details` — Get the details of one Workast task by ID.
- `search_spaces` — Search Workast spaces available to the connected user with filters and pagination.
- `update_task` — Update one or more common fields on an existing Workast task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Workast state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Workast is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/workast
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Workast homepage: https://www.workast.com/
- API documentation: https://developers.workast.com/
