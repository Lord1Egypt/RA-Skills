---
name: oo-sling
description: "Sling (getsling.com). Use this skill for ANY Sling request — searching and reading data. Whenever a task involves Sling, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sling"
  author: "OOMOL"
  version: "1.0.0"
  services: ["sling"]
  icon: "https://static.oomol.com/logo/third-party/sling.png"
---

# Sling

Operate **Sling** through your OOMOL-connected account. This skill calls the `sling` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sling. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sling" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sling" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_current_session` — Retrieve the current Sling API session, including user and organization details.
- `get_current_shift` — Retrieve the current shift for the connected Sling user.
- `get_detailed_shift` — Retrieve supplementary details for one Sling shift.
- `get_group` — Retrieve one Sling group by id.
- `get_next_shift` — Retrieve the next shift for the connected Sling user.
- `get_shift` — Retrieve one Sling shift by id.
- `get_task` — Retrieve one Sling task by id.
- `get_user` — Retrieve one Sling user by id.
- `list_calendar_events` — List Sling calendar events for one user and organization within an ISO interval.
- `list_groups` — List Sling groups in the current organization with optional filters.
- `list_shift_coworkers` — List coworkers for one Sling shift.
- `list_tasks` — List Sling tasks with optional type and cursor-like id filters.
- `list_users` — List Sling users in the current organization with optional filters.
- `list_working_users` — List Sling users working on a specific date.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sling state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sling is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=sling
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Sling homepage: https://getsling.com
