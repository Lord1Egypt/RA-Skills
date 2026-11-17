---
name: oo-qingflow
description: "Qingflow (qingflow.com). Use this skill for ANY Qingflow request — reading, creating, updating, and deleting data. Whenever a task involves Qingflow, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Qingflow"
  author: "OOMOL"
  version: "1.0.6"
  services: ["qingflow"]
  icon: "https://static.oomol.com/logo/third-party/qingflow.png"
---

# Qingflow

Operate **Qingflow** through your OOMOL-connected account. This skill calls the `qingflow` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Qingflow. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "qingflow" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "qingflow" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_record_comment` — Add a comment to one Qingflow business-data record. [write]
- `create_record` — Create one business-data record in a Qingflow application and return its asynchronous request ID. [write]
- `find_members` — Find Qingflow workspace member IDs by email address or mobile number.
- `get_department` — Get one Qingflow department by department ID.
- `get_form` — Get the current form fields, options, and field metadata for a Qingflow application.
- `get_member` — Get one Qingflow workspace member by external user ID.
- `get_operation_result` — Get Qingflow's processing result for a create, update, or other asynchronous request.
- `get_record` — Get one Qingflow business-data record and its current field answers.
- `list_apps` — List Qingflow applications visible to the workspace or one specified member.
- `list_departments` — List Qingflow departments, optionally rooted at one department.
- `list_members` — List members in the connected Qingflow workspace.
- `list_record_change_logs` — List data-change logs for one Qingflow record, optionally filtered by field.
- `list_record_comments` — List comments attached to one Qingflow business-data record.
- `list_records` — List and filter business-data records from one Qingflow application.
- `list_roles` — List roles in the connected Qingflow workspace.
- `list_workflow_logs` — List workflow-node processing logs for one Qingflow record.
- `process_record` — Submit, approve, reject, complete, or copy a Qingflow workflow node. [write]
- `reassign_record` — Reassign active approval or fill-in nodes on one Qingflow record. [write]
- `rollback_record` — Roll one Qingflow record back to an allowed earlier workflow node. [destructive]
- `update_record` — Update selected field answers on one Qingflow record and return its asynchronous request ID. [write]
- `urge_record` — Send a Qingflow reminder for one in-progress business-data record. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Qingflow state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Qingflow is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/qingflow
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Qingflow homepage: https://qingflow.com/
- API documentation: https://exiao.yuque.com/ixwxsb/bgzs0e
