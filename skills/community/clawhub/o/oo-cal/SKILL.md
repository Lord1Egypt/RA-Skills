---
name: oo-cal
description: "Cal.com (cal.com). Use this skill for ANY Cal.com request — reading, creating, updating, and deleting data. Whenever a task involves Cal.com, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cal.com"
  author: "OOMOL"
  version: "1.0.1"
  services: ["cal"]
  icon: "https://static.oomol.com/logo/third-party/Cal.svg"
---

# Cal.com

Operate **Cal.com** through your OOMOL-connected account. This skill calls the `cal` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cal.com. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cal" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cal" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_attendee` — Add an attendee to a Cal.com booking. [write]
- `cancel_booking` — Cancel a Cal.com booking by UID, optionally providing a cancellation reason. [write]
- `cancel_booking_via_uid` — Compatibility alias for Composio's cancel-booking-via-uid action. Cancels a booking by UID. [write]
- `confirm_booking_by_uid` — Confirm a Cal.com booking by UID. [write]
- `create_booking` — Create a Cal.com booking. [write]
- `create_event_type` — Create a Cal.com event type for the authenticated user. [write]
- `create_schedule` — Create a schedule for the authenticated Cal.com user. [write]
- `create_user_availability_schedule` — Compatibility alias for Composio's create-user-availability-schedule action. Creates a schedule. [write]
- `decline_booking_with_reason` — Decline a Cal.com booking by UID with an optional reason. [write]
- `delete_event_type` — Delete a Cal.com event type by numeric ID. [destructive]
- `delete_event_type_by_id` — Compatibility alias for Composio's delete-event-type-by-id action. Deletes a Cal.com event type by ID. [destructive]
- `delete_schedule` — Delete a schedule for the authenticated Cal.com user. [destructive]
- `delete_schedule_by_id` — Compatibility alias for Composio's delete-schedule-by-id action. Deletes a schedule. [destructive]
- `fetch_all_bookings` — Compatibility alias for Composio's fetch-all-bookings action. Lists bookings with optional filters and pagination.
- `fetch_event_type_details` — Compatibility alias for Composio's fetch-event-type-details action. Gets a single Cal.com event type by ID.
- `fetch_schedule_by_id` — Compatibility alias for Composio's fetch-schedule-by-id action. Gets a schedule by numeric ID. [write]
- `get_available_slots_info` — Compatibility action for Composio's get-available-slots-info. Returns available slots for a user, team, or event type.
- `get_booking` — Get a Cal.com booking by booking UID.
- `get_booking_references` — Compatibility alias for Composio's get-booking-references action. Lists booking references.
- `get_default_schedule` — Get the default schedule for the authenticated Cal.com user. [write]
- `get_default_schedule_details` — Compatibility alias for Composio's get-default-schedule-details action. Returns the default schedule for the authenticated user. [write]
- `get_event_type` — Get a single Cal.com event type by its numeric ID.
- `get_event_type_private_links` — List private links configured for a Cal.com event type.
- `get_my_profile` — Get the current Cal.com user profile from the authenticated OAuth account.
- `get_schedule` — Get a Cal.com schedule by numeric schedule ID. [write]
- `list_attendees` — List attendees for a Cal.com booking by booking UID.
- `list_booking_references` — List booking references for a Cal.com booking.
- `list_bookings` — List bookings for the authenticated Cal.com user with optional date, attendee, and event-type filters.
- `list_event_types` — List Cal.com event types for the authenticated user with optional pagination and status filters.
- `list_schedules` — List schedules available to the authenticated Cal.com user.
- `mark_booking_absent_for_uid` — Mark a Cal.com booking host or attendees absent. [write]
- `post_new_booking_request` — Compatibility alias for Composio's post-new-booking-request action. Creates a booking. [write]
- `reassign_booking_with_uid` — Reassign a round-robin booking to a specific host user ID. [write]
- `reschedule_booking` — Reschedule a Cal.com booking by UID to a new start time. [write]
- `reschedule_booking_by_uid` — Compatibility alias for Composio's reschedule-booking-by-uid action. Reschedules a booking by UID. [write]
- `retrieve_booking_details_by_uid` — Compatibility alias for Composio's retrieve-booking-details-by-uid action. Gets a booking by UID.
- `retrieve_calendar_busy_times` — Compatibility alias for Composio's retrieve-calendar-busy-times action. Returns busy ranges for specific calendars.
- `retrieve_calendar_list` — Compatibility alias for Composio's retrieve-calendar-list action. Lists connected calendars and the selected destination calendar.
- `retrieve_event_type_by_id` — Compatibility alias for Composio's retrieve-event-type-by-id action. Gets a single Cal.com event type by ID.
- `retrieve_my_information` — Compatibility alias for Composio's retrieve-my-information action. Returns the authenticated Cal.com user's profile.
- `retrieve_schedules_list` — Compatibility alias for Composio's retrieve-schedules-list action. Lists schedules for the authenticated user.
- `update_destination_calendar_integration` — Compatibility alias for Composio's update-destination-calendar-integration action. Updates the destination calendar used for created events. [write]
- `update_event_type` — Update a Cal.com event type by numeric ID. [write]
- `update_my_profile` — Update the current Cal.com user's profile fields such as name, bio, timezone, and branding. [write]
- `update_schedule` — Update a schedule for the authenticated Cal.com user. [write]
- `update_schedule_by_id` — Compatibility alias for Composio's update-schedule-by-id action. Updates a schedule. [write]
- `update_user_profile_details` — Compatibility alias for Composio's update-user-profile-details action. Updates the authenticated Cal.com user's profile. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cal.com state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cal.com is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=cal
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Cal.com homepage: https://cal.com
