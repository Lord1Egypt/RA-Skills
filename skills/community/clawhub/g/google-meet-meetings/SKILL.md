---
name: google-meet-meetings
description: Google Meet API integration with managed OAuth. Create meeting spaces, inspect conference records, retrieve recordings and transcripts, and manage meeting participants. Use this skill when users want to manage Google Meet conferences or extract meeting artifacts.
---

# Google Meet

![Google Meet](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-meet.svg?v=2)

Access Google Meet via the Google Meet REST API with managed OAuth authentication. Create meeting spaces, inspect conference records, retrieve recordings and transcripts, and manage participants.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-meet-meetings) for hosted connection flows and credentials so you do not need to configure Google Meet API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Meet |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Meet |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Meet    │
│   (User Chat)   │     │   (OAuth)    │     │   (Meet API)     │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Meet      │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Meet    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Meet again."

## Quick Start

```bash
# Create a new meeting space
clawlink_call_tool --tool "googlemeet_create_meet" --params '{}'

# List conference records
clawlink_call_tool --tool "googlemeet_list_conference_records" --params '{}'

# Get a meeting space details
clawlink_call_tool --tool "googlemeet_get_meet" --params '{"name": "spaces/YOUR_SPACE_ID"}'
```

## Authentication

All Google Meet tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Meet API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-meet and connect Google Meet.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-meet` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-meet
```

**Response:** Returns the live tool catalog for Google Meet.

### Reconnect

If Google Meet tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-meet
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-meet`

## Security & Permissions

- Access is scoped to meeting spaces and conference records the authenticated user has access to.
- **Write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Ending an active conference is a high-impact action and must always be confirmed.
- Recordings and transcripts are subject to the organizer's domain policies — they may not be available for all meetings.

## Tool Reference

### Meeting Space Management

| Tool | Description | Mode |
|------|-------------|------|
| `googlemeet_create_meet` | Create a new Meet space with optional configuration | Write |
| `googlemeet_get_meet` | Retrieve details of a Meet space by its identifier | Read |
| `googlemeet_update_space` | Update an existing Meet space's settings | Write |
| `googlemeet_end_active_conference` | End an ongoing conference in a specified space | Write |

### Conference Records

| Tool | Description | Mode |
|------|-------------|------|
| `googlemeet_list_conference_records` | List past conference records, optionally filtered | Read |
| `googlemeet_get_conference_record_by_name` | Get details for a specific conference record | Read |

### Participants

| Tool | Description | Mode |
|------|-------------|------|
| `googlemeet_list_participants` | List all participants in a conference record | Read |
| `googlemeet_list_participant_sessions` | List all join/leave sessions for a participant | Read |
| `googlemeet_get_participant_session` | Get details of a specific participant session | Read |

### Recordings

| Tool | Description | Mode |
|------|-------------|------|
| `googlemeet_list_recordings` | List recording resources for a conference record | Read |
| `googlemeet_get_recordings_by_conference_record_id` | Get all recordings for a specific conference | Read |

### Transcripts

| Tool | Description | Mode |
|------|-------------|------|
| `googlemeet_get_transcripts_by_conference_record_id` | List all transcripts for a conference | Read |
| `googlemeet_get_transcript` | Get a specific transcript by resource name | Read |
| `googlemeet_list_transcript_entries` | List structured transcript entries (speaker, time, text) | Read |
| `googlemeet_get_transcript_entry` | Get a specific transcript entry by resource name | Read |

## Code Examples

### Create a new meeting space

```bash
clawlink_call_tool --tool "googlemeet_create_meet" \
  --params '{
    "config": {
      "accessType": "OPEN",
      "entryPointAccess": "anyone"
    }
  }'
```

### List conference records

```bash
clawlink_call_tool --tool "googlemeet_list_conference_records" \
  --params '{
    "page_size": 20
  }'
```

### Get meeting space details

```bash
clawlink_call_tool --tool "googlemeet_get_meet" \
  --params '{
    "name": "spaces/YOUR_SPACE_ID"
  }'
```

### List participants in a conference

```bash
clawlink_call_tool --tool "googlemeet_list_participants" \
  --params '{
    "parent": "conferenceRecords/YOUR_CONFERENCE_RECORD_ID"
  }'
```

### Get recordings for a conference

```bash
clawlink_call_tool --tool "googlemeet_get_recordings_by_conference_record_id" \
  --params '{
    "conference_record_id": "YOUR_CONFERENCE_RECORD_ID"
  }'
```

### End an active conference

```bash
clawlink_call_tool --tool "googlemeet_end_active_conference" \
  --params '{
    "space_name": "spaces/YOUR_SPACE_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Meet is connected.
2. Call `clawlink_list_tools --integration google-meet` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-meet`.
5. If no Google Meet tools appear, direct the user to https://claw-link.dev/dashboard?add=google-meet.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → call                                          │
│                                                             │
│  Example: List conferences → Get details → Show results      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- `create_meet` does not attach to any calendar event — calendar linking requires a separate Calendar tool call.
- Capture `meetingUri`, `meetingCode`, and `space.name` from the create response immediately for downstream lookups.
- Newly created spaces may return incomplete data — retry after 1–3 seconds if needed.
- Recordings and transcripts require that recording/transcription was enabled and permitted by the organizer's domain policies.
- After a meeting ends, recordings and transcripts may take several minutes to process — an empty result may be temporary.
- `end_active_conference` requires the `space_name` parameter and immediately drops all participants.
- HTTP 429 may occur under rapid calls — apply exponential backoff.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-meet`. |
| Missing connection | Google Meet is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-meet. |
| `NOT_FOUND` | Meeting space or conference record does not exist. Check the name/ID. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-meet`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Meet API Overview](https://developers.google.com/meet/rest/reference)
- [Conference Records](https://developers.google.com/meet/rest/reference/v1/conferenceRecords)
- [Spaces](https://developers.google.com/meet/rest/reference/v1/spaces)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-meet-meetings
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Calendar](https://clawhub.ai/hith3sh/google-calendar-scheduling) — For calendar scheduling and event management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-meet-meetings)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)