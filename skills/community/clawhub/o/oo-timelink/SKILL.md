---
name: oo-timelink
description: "timelink (timelink.io). Use this skill for ANY timelink request — searching and reading data. Whenever a task involves timelink, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "timelink"
  author: "OOMOL"
  version: "1.0.1"
  services: ["timelink"]
  icon: "https://static.oomol.com/logo/third-party/timelink.svg"
---

# timelink

Operate **timelink** through your OOMOL-connected account. This skill calls the `timelink` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected timelink. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "timelink" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "timelink" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_client` — Fetch one Timelink client by its identifier.
- `get_company` — Fetch the current Timelink company details for the authenticated token.
- `get_current_token` — Inspect the current Timelink API token metadata.
- `get_project` — Fetch one Timelink project by its identifier.
- `get_service` — Fetch one Timelink service by its identifier.
- `get_time_entry` — Fetch one Timelink time entry by its identifier.
- `get_user` — Fetch one Timelink user by its identifier.
- `list_active_time_entries` — List currently active Timelink time entries.
- `list_clients` — List Timelink clients with optional filtering and pagination parameters.
- `list_projects` — List Timelink projects with optional filtering and pagination parameters.
- `list_services` — List Timelink services with optional filtering and pagination parameters.
- `list_time_entries` — List Timelink time entries with optional filtering and pagination parameters.
- `list_time_entry_required_fields` — List the Timelink field names that are required for time entries.
- `list_users` — List Timelink users with optional filtering and pagination parameters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change timelink state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — timelink is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=timelink
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- timelink homepage: https://timelink.io
