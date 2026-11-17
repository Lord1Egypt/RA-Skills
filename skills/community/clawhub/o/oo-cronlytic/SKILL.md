---
name: oo-cronlytic
description: "Cronlytic (cronlytic.com). Use this skill for ANY Cronlytic request — reading, creating, updating, and deleting data. Whenever a task involves Cronlytic, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cronlytic"
  author: "OOMOL"
  version: "1.0.2"
  services: ["cronlytic"]
  icon: "https://static.oomol.com/logo/third-party/cronlytic.png"
---

# Cronlytic

Operate **Cronlytic** through your OOMOL-connected account. This skill calls the `cronlytic` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cronlytic. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cronlytic" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cronlytic" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_job` — Create a recurring HTTP job in Cronlytic. [write]
- `delete_job` — Permanently delete a Cronlytic job and all its execution logs. [destructive]
- `get_job` — Get a Cronlytic job and its current schedule.
- `get_job_logs` — Get the latest 50 execution logs for a Cronlytic job, newest first.
- `list_jobs` — List all Cronlytic jobs for the connected user.
- `pause_job` — Pause a Cronlytic job to stop scheduled executions while retaining its configuration. [destructive]
- `resume_job` — Resume a paused Cronlytic job according to its cron expression. [write]
- `update_job` — Update a Cronlytic job using its complete configuration; provide all six job fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cronlytic state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cronlytic is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/cronlytic
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cronlytic homepage: https://www.cronlytic.com
- API documentation: https://www.cronlytic.com/api-documentation
