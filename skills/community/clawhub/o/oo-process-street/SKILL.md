---
name: oo-process-street
description: "Process Street (process.st). Use this skill for ANY Process Street request — reading, creating, and updating data. Whenever a task involves Process Street, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Process Street"
  author: "OOMOL"
  version: "1.0.1"
  services: ["process_street"]
  icon: "https://static.oomol.com/logo/third-party/process_street.png"
---

# Process Street

Operate **Process Street** through your OOMOL-connected account. This skill calls the `process_street` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Process Street. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "process_street" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "process_street" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_workflow_run` — Create one Process Street workflow run from an existing workflow. [write]
- `get_workflow` — Get one Process Street workflow by workflow ID.
- `get_workflow_run` — Get one Process Street workflow run by workflow run ID.
- `list_workflow_form_fields` — List Process Street workflow form field definitions for one workflow.
- `list_workflow_run_form_fields` — List Process Street workflow run form field values for one workflow run.
- `list_workflow_runs` — List Process Street workflow runs with optional workflow, status, and cursor filters.
- `list_workflow_tasks` — List Process Street tasks for one workflow run.
- `list_workflows` — List Process Street workflows with optional name filtering and cursor pagination.
- `update_workflow_run_form_fields` — Batch update Process Street workflow run form field values for one workflow run. [write]
- `update_workflow_task` — Update one Process Street workflow task status and optional due date by workflow run ID and task ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Process Street state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Process Street is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=process_street
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Process Street homepage: https://www.process.st/
