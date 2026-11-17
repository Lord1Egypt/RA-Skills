---
name: oo-webex
description: "Webex (webex.com). Use this skill for ANY Webex request — reading, creating, updating, and deleting data. Whenever a task involves Webex, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Webex"
  author: "OOMOL"
  version: "1.0.4"
  services: ["webex"]
  icon: "https://static.oomol.com/logo/third-party/webex.svg"
---

# Webex

Operate **Webex** through your OOMOL-connected account. This skill calls the `webex` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Webex. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "webex" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "webex" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_meeting` — Schedule a Webex meeting. [write]
- `create_membership` — Create a Webex membership. [write]
- `create_message` — Send a message to a Webex room or person. [write]
- `create_room` — Create a Webex room. [write]
- `create_team` — Create a Webex team. [write]
- `create_team_membership` — Create a Webex team membership. [write]
- `delete_meeting` — Delete a scheduled Webex meeting. [destructive]
- `delete_membership` — Delete a Webex membership. [destructive]
- `delete_message` — Delete a Webex message. [destructive]
- `delete_room` — Delete a Webex room. [destructive]
- `delete_team` — Delete a Webex team. [destructive]
- `delete_team_membership` — Delete a Webex team membership. [destructive]
- `download_meeting_transcript` — Download a Webex meeting transcript as VTT or plain text.
- `get_meeting` — Get a scheduled or historical Webex meeting by ID.
- `get_meeting_participant` — Get a Webex meeting participant by ID.
- `get_meeting_summary` — Get the AI-generated summary for a Webex meeting.
- `get_membership` — Get a Webex membership by ID.
- `get_message` — Get a Webex message by ID.
- `get_person` — Get a Webex person by ID.
- `get_recording` — Get Webex meeting recording details.
- `get_room` — Get a Webex room by ID.
- `get_team` — Get a Webex team by ID.
- `get_team_membership` — Get a Webex team membership by ID.
- `list_direct_messages` — List direct messages involving the authenticated Webex user.
- `list_meeting_participants` — List participants for a Webex meeting.
- `list_meeting_transcripts` — List transcripts generated for Webex meetings.
- `list_meetings` — List meetings visible to the authenticated Webex user.
- `list_memberships` — List Webex memberships.
- `list_messages` — List messages in a Webex room.
- `list_people` — List people visible to the authenticated Webex user.
- `list_recordings` — List Webex meeting recordings.
- `list_rooms` — List rooms visible to the authenticated Webex user.
- `list_team_memberships` — List Webex team memberships.
- `list_teams` — List Webex teams.
- `update_meeting` — Update a scheduled Webex meeting. [write]
- `update_membership` — Update a Webex membership. [write]
- `update_message` — Update a Webex message. [write]
- `update_room` — Update a Webex room. [write]
- `update_team` — Update a Webex team. [write]
- `update_team_membership` — Update a Webex team membership. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Webex state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Webex is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/webex
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Webex homepage: https://www.webex.com
- API documentation: https://developer.webex.com/docs/getting-started
