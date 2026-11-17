---
name: oo-komos
description: "Komos (komos.ai). Use this skill for ANY Komos request — reading, creating, updating, and deleting data. Whenever a task involves Komos, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Komos"
  author: "OOMOL"
  version: "1.0.1"
  services: ["komos"]
  icon: "https://static.oomol.com/logo/third-party/komos.svg"
---

# Komos

Operate **Komos** through your OOMOL-connected account. This skill calls the `komos` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Komos. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "komos" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "komos" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_task_run` — Request cancellation of a pending or running task run, with an optional audit reason. [destructive]
- `get_task` — Retrieve a saved task including its definition and execution plan summary.
- `get_task_run` — Retrieve the latest task run status and outputs, including terminal failures or cancellation.
- `get_task_run_logs` — Retrieve ordered execution log entries for a task run.
- `list_runs` — List runs across tasks with pagination, status and creation time filters. By default Komos returns runs from the last seven days.
- `list_task_runs` — Retrieve the 50 most recent runs for one saved task. This endpoint does not support pagination.
- `list_tasks` — List saved tasks with pagination, name search and preparation status filters.
- `queue_task_run` — Queue a saved task with optional input overrides and an idempotency key. Wait for get_task_run to obtain final outputs. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Komos state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Komos is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/komos
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Komos homepage: https://komos.ai/
- API documentation: https://docs.komos.ai/api-reference/introduction
