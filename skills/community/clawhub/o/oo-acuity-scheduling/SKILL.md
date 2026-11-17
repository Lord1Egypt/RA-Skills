---
name: oo-acuity-scheduling
description: "Acuity Scheduling (acuityscheduling.com). Use this skill for ANY Acuity Scheduling request — reading, creating, updating, and deleting data. Whenever a task involves Acuity Scheduling, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Acuity Scheduling"
  author: "OOMOL"
  version: "1.0.5"
  services: ["acuity_scheduling"]
  icon: "https://static.oomol.com/logo/third-party/acuity_scheduling.png"
---

# Acuity Scheduling

Operate **Acuity Scheduling** through your OOMOL-connected account. This skill calls the `acuity_scheduling` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Acuity Scheduling. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "acuity_scheduling" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "acuity_scheduling" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_appointment` — Cancel an Acuity Scheduling appointment. [destructive]
- `create_appointment` — Create an appointment in Acuity Scheduling. [write]
- `get_account` — Retrieve the Acuity Scheduling account associated with the credential.
- `get_appointment` — Retrieve one Acuity Scheduling appointment by ID.
- `list_appointment_types` — List appointment types configured in Acuity Scheduling.
- `list_appointments` — List Acuity Scheduling appointments with optional client and date filters.
- `list_available_dates` — List available Acuity Scheduling dates for a month and appointment type.
- `list_available_times` — List available Acuity Scheduling times for a date and appointment type.
- `list_calendars` — List calendars configured in the Acuity Scheduling account.
- `list_intake_forms` — List intake forms configured in Acuity Scheduling.
- `reschedule_appointment` — Reschedule an Acuity appointment to a new date and time. [write]
- `update_appointment` — Update client details, forms, notes, or labels on an Acuity appointment. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Acuity Scheduling state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Acuity Scheduling is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/acuity_scheduling
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Acuity Scheduling homepage: https://acuityscheduling.com/
- API documentation: https://developers.acuityscheduling.com/
