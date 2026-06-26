---
name: oo-googlecalendar
description: "Google Calendar (workspace.google.com). Use this skill for ANY Google Calendar request — reading, creating, updating, and deleting data. Whenever a task involves Google Calendar, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Calendar"
  author: "OOMOL"
  version: "1.0.1"
  services: ["googlecalendar"]
  icon: "https://static.oomol.com/logo/third-party/Google%20Calendar.svg"
---

# Google Calendar

Operate **Google Calendar** through your OOMOL-connected account. This skill calls the `googlecalendar` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Calendar. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googlecalendar" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googlecalendar" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_calendar_to_list` — Add a calendar to the current user's Google Calendar list. [write]
- `clear_calendar` — Clear all events from a Google Calendar. [destructive]
- `create_acl_rule` — Create an ACL rule on a Google Calendar. [write]
- `create_calendar` — Create a Google Calendar. [write]
- `create_event` — Create a Google Calendar event. [write]
- `delete_acl_rule` — Delete an ACL rule from a Google Calendar. [destructive]
- `delete_calendar` — Delete a Google Calendar. [destructive]
- `delete_event` — Delete a Google Calendar event. [destructive]
- `find_event` — Search events in a Google Calendar using a query string.
- `find_free_slots` — Derive free slots from Google Calendar freeBusy data.
- `free_busy_query` — Query busy intervals for calendars and groups.
- `get_acl_rule` — Fetch one ACL rule from a Google Calendar.
- `get_calendar` — Fetch one Google Calendar resource by ID.
- `get_calendar_list_entry` — Fetch one Google Calendar list entry by calendar ID.
- `get_colors` — Fetch the Google Calendar colors resource.
- `get_event` — Fetch one Google Calendar event.
- `get_setting` — Fetch one Google Calendar setting.
- `import_event` — Import an event into Google Calendar without conferenceData or attachments. [write]
- `list_acl` — List ACL rules for a Google Calendar.
- `list_calendars` — List the current user's Google Calendar list entries.
- `list_event_instances` — List instances of a recurring Google Calendar event.
- `list_events` — List events from a Google Calendar.
- `list_events_all_calendars` — List events across multiple Google Calendars and aggregate the result.
- `list_settings` — List Google Calendar settings.
- `move_event` — Move a Google Calendar event to another calendar. [write]
- `patch_acl_rule` — Patch writable fields on a Google Calendar ACL rule. [write]
- `patch_calendar` — Patch writable fields on a Google Calendar resource. [write]
- `patch_calendar_list_entry` — Patch writable fields on a Google Calendar list entry. [write]
- `patch_event` — Patch writable fields on a Google Calendar event. [write]
- `quick_add_event` — Create a Google Calendar event with natural language text. [write]
- `remove_attendee` — Remove one attendee email from a Google Calendar event. [destructive]
- `remove_calendar_from_list` — Remove a calendar from the current user's Calendar list. [destructive]
- `sync_events` — Incrementally sync events from a Google Calendar. [write]
- `update_acl_rule` — Replace writable fields on a Google Calendar ACL rule. [write]
- `update_calendar` — Replace writable fields on a Google Calendar resource. [write]
- `update_calendar_list_entry` — Replace writable fields on a Google Calendar list entry. [write]
- `update_event` — Replace writable fields on a Google Calendar event. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Calendar state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Calendar is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=googlecalendar
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Calendar homepage: https://workspace.google.com/products/calendar/
