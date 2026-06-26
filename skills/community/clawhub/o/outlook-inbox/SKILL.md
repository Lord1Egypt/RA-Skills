---
name: outlook-inbox
description: Search Outlook mail, read threads, manage drafts, send or reply to email, and manage calendar events via Microsoft Graph. Use this skill when users want to manage Outlook email, calendar events, contacts, and tasks via the Microsoft Graph Mail API.
---

# Outlook Inbox

![Outlook Inbox](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/outlook.svg)

Access Outlook mail, calendar, contacts, and tasks via Microsoft Graph API with managed OAuth authentication. Search mail, read threads, manage drafts, send or reply to email, and coordinate calendar events.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=outlook-inbox) for hosted connection flows and credentials so you do not need to configure Outlook API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Outlook |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Outlook |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Microsoft Graph │
│   (User Chat)   │     │   (OAuth)    │     │  (Mail API) │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Outlook  │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Outlook  │
    │  File    │           │ Auth     │           │ Mailbox  │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Outlook again."

## Quick Start

```bash
# List messages in inbox
clawlink_call_tool --tool "outlook_list_messages" --params '{"folder_id": "inbox", "top": 25}'

# Search messages
clawlink_call_tool --tool "outlook_search_messages" --params '{"query": "quarterly report"}'

# Get message details
clawlink_call_tool --tool "outlook_get_message" --params '{"message_id": "MESSAGE_ID"}'
```

## Authentication

All Outlook tool calls are authenticated automatically by ClawLink using the user's connected Microsoft account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Microsoft Graph request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=outlook and connect Outlook.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `outlook` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration outlook
```

**Response:** Returns the live tool catalog for Outlook.

### Reconnect

If Outlook tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=outlook
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration outlook`

## Security & Permissions

- Access is scoped to mail, calendar, contacts, and tasks within the connected Microsoft account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete message, cancel event) must be confirmed.
- Sending email, sending replies, or deleting calendar events are high-impact actions that require explicit user confirmation.

## Tool Reference

### Mail Operations

| Tool | Description | Mode |
|------|-------------|------|
| `outlook_list_messages` | List messages in a folder | Read |
| `outlook_get_message` | Get a message by ID | Read |
| `outlook_search_messages` | Search messages by query | Read |
| `outlook_create_draft` | Create a new email draft | Write |
| `outlook_create_draft_reply` | Create a draft reply to a message | Write |
| `outlook_create_forward_draft` | Create a draft forward | Write |
| `outlook_send_message` | Send a message | Write |
| `outlook_send_reply` | Send a reply to a message | Write |
| `outlook_move_message` | Move a message to a folder | Write |
| `outlook_batch_move_messages` | Move up to 20 messages at once | Write |
| `outlook_copy_message` | Copy a message to another folder | Write |
| `outlook_delete_message` | Delete a message | Write |
| `outlook_batch_update_messages` | Batch update up to 20 messages | Write |

### Mail Folder Operations

| Tool | Description | Mode |
|------|-------------|------|
| `outlook_list_mail_folders` | List all mail folders | Read |
| `outlook_create_mail_folder` | Create a new mail folder | Write |
| `outlook_copy_mail_folder` | Copy a mail folder | Write |
| `outlook_delete_mail_folder` | Delete a mail folder | Write |

### Calendar Events

| Tool | Description | Mode |
|------|-------------|------|
| `outlook_list_events` | List calendar events | Read |
| `outlook_get_event` | Get an event by ID | Read |
| `outlook_calendar_create_event` | Create a new calendar event | Write |
| `outlook_create_me_event` | Create an event in the user's calendar | Write |
| `outlook_update_event` | Update an existing event | Write |
| `outlook_delete_calendar_event` | Delete a calendar event | Write |
| `outlook_accept_event` | Accept a meeting invitation | Write |
| `outlook_decline_event` | Decline a meeting invitation | Write |
| `outlook_cancel_event` | Cancel a meeting and notify attendees | Write |

### Contacts

| Tool | Description | Mode |
|------|-------------|------|
| `outlook_list_contacts` | List contacts | Read |
| `outlook_get_contact` | Get a contact by ID | Read |
| `outlook_create_contact` | Create a new contact | Write |
| `outlook_update_contact` | Update an existing contact | Write |
| `outlook_delete_contact` | Delete a contact | Write |
| `outlook_list_contact_folders` | List contact folders | Read |

### Attachments

| Tool | Description | Mode |
|------|-------------|------|
| `outlook_add_mail_attachment` | Add an attachment to a message | Write |
| `outlook_create_attachment_upload_session` | Create an upload session for large attachments (>3 MB) | Write |
| `outlook_list_attachments` | List attachments on a message | Read |

### Rules & Categories

| Tool | Description | Mode |
|------|-------------|------|
| `outlook_create_email_rule` | Create an email rule | Write |
| `outlook_list_email_rules` | List email rules | Read |
| `outlook_create_master_category` | Create a category | Write |
| `outlook_list_master_categories` | List categories | Read |

## Code Examples

### List messages in inbox

```bash
clawlink_call_tool --tool "outlook_list_messages" \
  --params '{
    "folder_id": "inbox",
    "top": 25,
    "filter": "isRead eq false",
    "orderby": "sentDateTime desc"
  }'
```

### Send a message

```bash
clawlink_call_tool --tool "outlook_send_message" \
  --params '{
    "subject": "Quarterly Report",
    "body": {
      "contentType": "text",
      "content": "Please find the quarterly report attached."
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "colleague@example.com"
        }
      }
    ]
  }'
```

### Create a calendar event

```bash
clawlink_call_tool --tool "outlook_create_me_event" \
  --params '{
    "subject": "Team Meeting",
    "start_datetime": "2024-07-15T10:00:00Z",
    "end_datetime": "2024-07-15T11:00:00Z",
    "body": {
      "contentType": "text",
      "content": "Weekly sync with the team."
    },
    "location": {
      "displayName": "Conference Room A"
    },
    "attendees": [
      {
        "emailAddress": {
          "address": "teammate@example.com"
        },
        "type": "required"
      }
    ]
  }'
```

### Search messages

```bash
clawlink_call_tool --tool "outlook_search_messages" \
  --params '{
    "query": "from:manager@example.com subject:review",
    "folder_id": "inbox"
  }'
```

### Create a draft reply

```bash
clawlink_call_tool --tool "outlook_create_draft_reply" \
  --params '{
    "message_id": "MESSAGE_ID",
    "comment": "Thanks for the update! I will review and get back to you shortly."
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Outlook is connected.
2. Call `clawlink_list_tools --integration outlook` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `outlook`.
5. If no Outlook tools appear, direct the user to https://claw-link.dev/dashboard?add=outlook.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Search messages → Read thread → Show results     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Message IDs are immutable identifiers — use them directly from list or search results.
- Large attachments (>3 MB) require an upload session — use `create_attachment_upload_session` first.
- Batch operations are limited to 20 items per call.
- `start_datetime` must chronologically precede `end_datetime` on calendar events.
- Sending a message moves it from Drafts — no separate send action needed for drafts.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration outlook`. |
| Missing connection | Outlook is not connected. Direct the user to https://claw-link.dev/dashboard?add=outlook. |
| `ItemNotFound` | Message or folder does not exist. Check the ID. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `SendAsDenied` | The authenticated user does not have permission to send as the specified account. |
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

1. Ensure the integration slug is exactly `outlook`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Microsoft Graph Mail API Overview](https://learn.microsoft.com/graph/api/resources/mail-api-overview)
- [Microsoft Graph Calendar API](https://learn.microsoft.com/graph/api/resources/calendar)
- [Message Resource](https://learn.microsoft.com/graph/api/resources/message)
- [Event Resource](https://learn.microsoft.com/graph/api/resources/event)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=outlook-inbox
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [OneDrive Files](https://clawhub.ai/hith3sh/onedrive-files) — For OneDrive file management
- [Microsoft Excel](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) — For Excel workbook operations
- [OneNote Notes](https://clawhub.ai/hith3sh/onenote-notes) — For OneNote notebook operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=outlook-inbox)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
