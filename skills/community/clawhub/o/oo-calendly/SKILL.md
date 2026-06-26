---
name: oo-calendly
description: "Calendly (calendly.com). Use this skill for ANY Calendly request — reading, creating, updating, and deleting data. Whenever a task involves Calendly, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Calendly"
  author: "OOMOL"
  version: "1.0.1"
  services: ["calendly"]
  icon: "https://static.oomol.com/logo/third-party/Calendly.svg"
---

# Calendly

Operate **Calendly** through your OOMOL-connected account. This skill calls the `calendly` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Calendly. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "calendly" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "calendly" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_scheduled_event` — Cancel one Calendly scheduled event by scheduled-event URI. [write]
- `create_event_invitee` — Create one Calendly invitee booking for a confirmed available start time. [write]
- `create_invitee_no_show` — Mark one Calendly invitee as a no-show by invitee URI. [write]
- `create_organization_invitation` — Create one organization invitation for a Calendly organization. [write]
- `create_share` — Create one customized single-use share from an existing Calendly event type. [write]
- `create_single_use_scheduling_link` — Create one single-use scheduling link from an existing Calendly event type without customization. [write]
- `create_webhook_subscription` — Create one Calendly webhook subscription for an organization or one user. [write]
- `delete_invitee_no_show` — Delete one Calendly invitee no-show by no-show URI. [destructive]
- `delete_organization_membership` — Delete one Calendly organization membership by membership URI. [destructive]
- `delete_webhook_subscription` — Delete one Calendly webhook subscription by URI. [destructive]
- `get_current_user` — Retrieve the authenticated Calendly user for the connected personal access token.
- `get_event_invitee` — Retrieve one Calendly invitee by invitee URI.
- `get_event_type` — Retrieve one Calendly event type by event type URI.
- `get_invitee_no_show` — Retrieve one Calendly invitee no-show by no-show URI.
- `get_organization` — Retrieve one Calendly organization by organization URI.
- `get_organization_membership` — Retrieve one Calendly organization membership by membership URI.
- `get_routing_form` — Retrieve one Calendly routing form by routing-form URI.
- `get_routing_form_submission` — Retrieve one Calendly routing form submission by submission URI.
- `get_scheduled_event` — Retrieve one Calendly scheduled event by scheduled-event URI.
- `get_user` — Retrieve one Calendly user by user URI.
- `get_user_availability_schedule` — Retrieve one Calendly user availability schedule by schedule URI. [write]
- `get_webhook_subscription` — Retrieve one Calendly webhook subscription by URI.
- `list_event_invitees` — List invitees for one Calendly scheduled event.
- `list_event_type_availability_schedules` — List the official Calendly availability schedules attached to one event type.
- `list_event_type_available_times` — List available time slots for one Calendly event type within a 7-day window.
- `list_event_types` — List Calendly event types for exactly one user or one organization, including scheduling URLs.
- `list_organization_invitations` — List organization invitations for one Calendly organization.
- `list_organization_memberships` — List Calendly organization memberships for one organization or one user.
- `list_routing_form_submissions` — List Calendly routing form submissions for one routing form.
- `list_routing_forms` — List Calendly routing forms for one organization.
- `list_scheduled_events` — List Calendly scheduled events for exactly one user or one organization.
- `list_user_availability_schedules` — List user availability schedules for one Calendly user.
- `list_user_busy_times` — List busy time slots for one Calendly user within a 7-day window.
- `list_user_meeting_locations` — List the configured meeting locations for one Calendly user.
- `list_webhook_subscriptions` — List Calendly webhook subscriptions for an organization or one user.
- `revoke_organization_invitation` — Revoke one organization invitation from a Calendly organization. [destructive]
- `update_event_type_availability_schedule` — Update the official Calendly availability schedule for one event type. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Calendly state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Calendly is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=calendly
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Calendly homepage: https://calendly.com
