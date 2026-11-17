---
name: oo-bazhuayu
description: "Bazhuayu (bazhuayu.com). Use this skill for ANY Bazhuayu request — reading, creating, updating, and deleting data. Whenever a task involves Bazhuayu, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bazhuayu"
  author: "OOMOL"
  version: "1.0.5"
  services: ["bazhuayu"]
  icon: "https://static.oomol.com/logo/third-party/bazhuayu.png"
---

# Bazhuayu

Operate **Bazhuayu** through your OOMOL-connected account. This skill calls the `bazhuayu` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bazhuayu. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bazhuayu" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bazhuayu" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `copy_task` — Copy a Bazhuayu task into a task group and return the new task ID. Requires a Flagship+, Enterprise, or Team plan. [write]
- `get_task_actions` — Get API-addressable steps from Bazhuayu tasks so their action IDs can be used in parameter updates. Requires a Flagship+, Enterprise, or Team plan.
- `get_task_batch_data` — Get a page of collected data from one Bazhuayu task execution batch. Requires a Flagship, Flagship+, Enterprise, or Team plan.
- `get_task_data` — Get a page of collected data from a Bazhuayu task using the offset returned by the previous page. Requires a Flagship, Flagship+, Enterprise, or Team plan.
- `get_task_stats` — Get account-wide counts for waiting, extracting, and finished Bazhuayu cloud tasks and subtasks. Requires an Enterprise plan.
- `get_task_statuses` — Get the latest execution status for Bazhuayu tasks. Requires a Flagship+, Enterprise, or Team plan.
- `get_unexported_data` — Get the next unexported records from a Bazhuayu task. Use this with mark_data_exported through only one sequential consumer per task because Bazhuayu acknowledgements are task-scoped. Requires a Flagship, Flagship+, Enterprise, or Team plan.
- `list_subtask_statuses` — List the latest batch's Bazhuayu subtask statuses. Requires a Flagship+, Enterprise, or Team plan.
- `list_task_groups` — List the task groups available to the connected Bazhuayu account. Requires a Flagship, Flagship+, Enterprise, or Team plan.
- `list_tasks` — List the Bazhuayu tasks in one task group. Requires a Flagship, Flagship+, Enterprise, or Team plan.
- `mark_data_exported` — Mark the current unexported data for a Bazhuayu task as exported. Call this only after a single sequential consumer has persisted the preceding get_unexported_data result. Requires a Flagship, Flagship+, Enterprise, or Team plan. [write]
- `query_task_analytics` — Query Bazhuayu collection volume, execution, success-rate, and resource-usage metrics for the last three months. Requires a Flagship, Flagship+, Enterprise, or Team plan.
- `start_subtasks` — Start selected cloud subtasks for a Bazhuayu task. Requires a Flagship+, Enterprise, or Team plan. [write]
- `start_task` — Start a Bazhuayu task on cloud workers and return its batch number. Requires a Flagship+, Enterprise, or Team plan. [write]
- `stop_subtasks` — Stop selected cloud subtasks for a Bazhuayu task. Requires a Flagship+, Enterprise, or Team plan. [destructive]
- `stop_task` — Stop a running Bazhuayu cloud task. Requires a Flagship+, Enterprise, or Team plan. [destructive]
- `update_loop_items` — Replace or append the text or URL items used by one Bazhuayu loop step. Requires a Flagship+, Enterprise, or Team plan. [destructive]
- `update_task_parameters` — Update supported properties and loop items in a Bazhuayu task. Requires a Flagship+, Enterprise, or Team plan. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bazhuayu state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bazhuayu is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/bazhuayu
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Bazhuayu homepage: https://www.bazhuayu.com/
- API documentation: https://openapi.bazhuayu.com/zh-CN/
