---
name: oo-outlook-calendar
description: "Outlook Calendar (microsoft.com). Use this skill for ANY Outlook Calendar request — reading, creating, updating, and deleting data. Whenever a task involves Outlook Calendar, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Outlook Calendar"
  author: "OOMOL"
  version: "1.0.2"
  services: ["outlook_calendar"]
  icon: "https://static.oomol.com/logo/third-party/outlook_calendar.svg"
---

# Outlook Calendar

Operate **Outlook Calendar** through your OOMOL-connected account. This skill calls the `outlook_calendar` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Outlook Calendar. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "outlook_calendar" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "outlook_calendar" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `accept_event` — Accept an event invitation for the connected account. [write]
- `cancel_event` — Cancel an organized event and notify its attendees. [destructive]
- `create_event` — Create an event in the default calendar or a selected calendar. [write]
- `decline_event` — Decline an event invitation for the connected account. [write]
- `delete_event` — Delete an Outlook event; deleting an organized meeting sends a cancellation to attendees. [destructive]
- `find_meeting_times` — Suggest meeting times that satisfy attendee, location, and time constraints.
- `get_calendar` — Get one Outlook calendar by ID.
- `get_current_user` — Get the profile for the connected Microsoft account.
- `get_event` — Get one Outlook event by ID.
- `get_schedule` — Get free and busy availability for users, rooms, or resources.
- `list_calendar_view` — List event occurrences and exceptions within a date-time range.
- `list_calendars` — List calendars belonging to the connected Microsoft account.
- `list_events` — List events from the default calendar or a selected calendar.
- `tentatively_accept_event` — Tentatively accept an event invitation for the connected account. [write]
- `update_event` — Update writable fields on an Outlook event. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Outlook Calendar state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Outlook Calendar is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/outlook_calendar
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Outlook Calendar homepage: https://www.microsoft.com/microsoft-365/outlook/outlook-calendar
- API documentation: https://learn.microsoft.com/en-us/graph/api/resources/calendar
