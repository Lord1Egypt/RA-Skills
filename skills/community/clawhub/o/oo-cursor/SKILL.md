---
name: oo-cursor
description: "Cursor (cursor.com). Use this skill for ANY Cursor request — reading, creating, updating, and deleting data. Whenever a task involves Cursor, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cursor"
  author: "OOMOL"
  version: "1.0.6"
  services: ["cursor"]
  icon: "https://static.oomol.com/logo/third-party/cursor.svg"
---

# Cursor

Operate **Cursor** through your OOMOL-connected account. This skill calls the `cursor` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cursor. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cursor" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cursor" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_agent` — Archive a session while retaining readable history. Call unarchive_agent before sending another prompt. [destructive]
- `cancel_run` — Cancel an active run. To continue afterward, create a new run on the same session. [destructive]
- `create_agent` — Create a durable Cursor cloud session and enqueue its first run. Returns immediately; poll get_run for the result. MCP servers can give the session access to external tools. [write]
- `create_run` — Send a follow-up using the session's conversation and workspace. Wait for or cancel an active run before starting another. Unarchive archived sessions first. [write]
- `delete_agent` — Permanently delete a cloud session. This is irreversible; archive_agent provides reversible removal. [destructive]
- `get_agent` — Read a cloud session's configuration and latestRunId. Use get_run for execution status and results.
- `get_daily_usage_data` — Retrieve Cursor daily usage metrics for a team over a date range of up to 30 days.
- `get_run` — Read a run's progress, final assistant reply, and pushed branches. FINISHED, ERROR, CANCELLED, and EXPIRED are terminal statuses.
- `get_team_spend` — Retrieve Cursor team spending for the current billing cycle with optional search, sort, and pagination.
- `list_agents` — List cloud sessions, newest first. Use nextCursor to request another page.
- `list_audit_logs` — List Cursor team audit log events with optional time, event type, user, search, and page filters.
- `list_models` — List available cloud agent models and their supported parameters and variants.
- `list_runs` — List a cloud session's runs, newest first, with cursor pagination.
- `list_team_members` — List Cursor team members visible to the team API key.
- `unarchive_agent` — Restore an archived session so it can accept new runs. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cursor state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cursor is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/cursor
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cursor homepage: https://cursor.com
- API documentation: https://cursor.com/docs/api
