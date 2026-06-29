---
name: oo-n8n
description: "n8n (n8n.io). Use this skill for ANY n8n request — reading, creating, updating, and deleting data. Whenever a task involves n8n, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "n8n"
  author: "OOMOL"
  version: "1.0.0"
  services: ["n8n"]
  icon: "https://static.oomol.com/logo/third-party/n8n.svg"
---

# n8n

Operate **n8n** through your OOMOL-connected account. This skill calls the `n8n` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected n8n. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "n8n" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "n8n" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `activate_workflow` — Activate or publish an n8n workflow. [write]
- `archive_workflow` — Archive an n8n workflow. [write]
- `create_data_table` — Create an n8n data table with columns. [write]
- `create_data_table_column` — Add a column to an n8n data table. [write]
- `create_tag` — Create an n8n tag. [write]
- `create_variable` — Create an n8n variable for workflow runtime configuration. [write]
- `deactivate_workflow` — Deactivate an n8n workflow. [destructive]
- `delete_data_table` — Delete an n8n data table. [destructive]
- `delete_data_table_column` — Delete a column from an n8n data table. [destructive]
- `delete_tag` — Delete an n8n tag. [destructive]
- `delete_variable` — Delete an n8n variable. [destructive]
- `get_data_table` — Retrieve one n8n data table by ID.
- `get_execution` — Retrieve one n8n execution by ID.
- `get_execution_tags` — Get annotation tags attached to an n8n execution.
- `get_insights_summary` — Retrieve n8n insights summary metrics for a time range and project.
- `get_workflow` — Retrieve one n8n workflow by ID.
- `get_workflow_tags` — Get tags attached to an n8n workflow.
- `insert_data_table_rows` — Insert rows into an n8n data table. [write]
- `list_data_table_columns` — List columns in an n8n data table.
- `list_data_table_rows` — List rows in an n8n data table with filters, search, and sorting.
- `list_data_tables` — List n8n data tables with optional filters and cursor pagination.
- `list_executions` — List n8n executions with optional filters and cursor pagination.
- `list_tags` — List n8n tags with cursor pagination.
- `list_variables` — List n8n variables with optional filters and cursor pagination.
- `list_workflows` — List n8n workflows with optional filters and cursor pagination.
- `retry_execution` — Retry one n8n execution.
- `stop_execution` — Stop one running n8n execution. [write]
- `unarchive_workflow` — Unarchive an n8n workflow.
- `update_data_table` — Rename an n8n data table. [write]
- `update_data_table_column` — Rename or reorder an n8n data table column. [write]
- `update_data_table_rows` — Update rows in an n8n data table by filter. [write]
- `update_execution_tags` — Replace annotation tags attached to an n8n execution. [write]
- `update_tag` — Update an n8n tag. [write]
- `update_variable` — Update an n8n variable value. [write]
- `update_workflow_tags` — Replace tags attached to an n8n workflow. [write]
- `upsert_data_table_row` — Upsert one row in an n8n data table by filter. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change n8n state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — n8n is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=n8n
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- n8n homepage: https://n8n.io
