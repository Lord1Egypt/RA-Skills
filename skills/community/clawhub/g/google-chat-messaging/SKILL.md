---
name: google-chat-messaging
description: Work with Google Chat spaces, members, messages, attachments, and threaded conversations via the Google Chat API. Use this skill when users want to list spaces and members, read or inspect messages, send messages after confirmation, create or manage spaces, or work with threads and attachments in Google Chat.
---

# Google Chat

![Google Chat](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-chat.svg?v=2)

Access Google Chat via the Google Chat API with OAuth authentication. Manage spaces, members, messages, attachments, and threaded conversations.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-chat-messaging) for hosted connection flows and credentials so you do not need to configure Google Chat API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Chat |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Chat |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Google Chat API │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Google Chat                        │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Google   │
   │  File    │           │ Auth     │           │ Chat     │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Chat again."

## Quick Start

```bash
# List spaces the user is member of
clawlink_call_tool --tool "google_chat_list_spaces" --params '{}'

# List members in a space
clawlink_call_tool --tool "google_chat_list_members" --params '{"parent": "spaces/space-id"}'

# Send a message to a space
clawlink_call_tool --tool "google_chat_create_message" --params '{"parent": "spaces/space-id", "text": "Hello from OpenClaw!"}'
```

## Authentication

All Google Chat tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Chat API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-chat and connect Google Chat.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-chat` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-chat
```

**Response:** Returns the live tool catalog for Google Chat.

### Reconnect

If Google Chat tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-chat
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-chat`

## Security & Permissions

- Access is scoped to Google Chat spaces and messages accessible to the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any message send, space create, or member change, confirm the intended effect with the user.
- Destructive actions (deleting spaces, removing members) are marked as high-impact and must be confirmed.
- Message size is limited to 32,000 bytes. Card-based messages require bot authentication.

## Tool Reference

### Spaces

| Tool | Description | Mode |
|------|-------------|------|
| `google_chat_list_spaces` | List spaces the authenticated user is a member of | Read |
| `google_chat_get_space` | Get details for a specific space | Read |
| `google_chat_create_space` | Create a new space | Write |
| `google_chat_update_space` | Update space name, description, or settings | Write |
| `google_chat_delete_space` | Delete a space | Write |

### Members

| Tool | Description | Mode |
|------|-------------|------|
| `google_chat_list_members` | List all members in a space | Read |
| `google_chat_get_member` | Get details for a specific member | Read |
| `google_chat_create_membership` | Add a user or group to a space | Write |
| `google_chat_delete_membership` | Remove a member from a space | Write |

### Messages

| Tool | Description | Mode |
|------|-------------|------|
| `google_chat_list_messages` | List messages in a space | Read |
| `google_chat_get_message` | Get a specific message | Read |
| `google_chat_create_message` | Send a message to a space (supports threading) | Write |
| `google_chat_update_message` | Update a message's text or content | Write |
| `google_chat_delete_message` | Delete a message | Write |

### Reactions

| Tool | Description | Mode |
|------|-------------|------|
| `google_chat_list_reactions` | List reactions to a message | Read |
| `google_chat_create_reaction` | Add an emoji reaction to a message | Write |
| `google_chat_delete_reaction` | Remove an emoji reaction | Write |

### Attachments & Custom Emoji

| Tool | Description | Mode |
|------|-------------|------|
| `google_chat_list_attachments` | List attachments in a space | Read |
| `google_chat_create_custom_emoji` | Create a custom emoji for the organization | Write |

### Sections

| Tool | Description | Mode |
|------|-------------|------|
| `google_chat_create_section` | Create a custom section in a space | Write |

## Code Examples

### List spaces

```bash
clawlink_call_tool --tool "google_chat_list_spaces" \
  --params '{}'
```

### Send a message to a space

```bash
clawlink_call_tool --tool "google_chat_create_message" \
  --params '{
    "parent": "spaces/space-id",
    "text": "Hello team! Just wanted to share an update on the project status."
  }'
```

### Reply in a thread

```bash
clawlink_call_tool --tool "google_chat_create_message" \
  --params '{
    "parent": "spaces/space-id",
    "text": "Thanks for the update!",
    "thread": {
      "thread_key": "original-message-id"
    }
  }'
```

### Add a reaction to a message

```bash
clawlink_call_tool --tool "google_chat_create_reaction" \
  --params '{
    "parent": "spaces/space-id/messages/message-id",
    "emoji_unicode": "👍"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Chat is connected.
2. Call `clawlink_list_tools --integration google-chat` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-chat`.
5. If no Google Chat tools appear, direct the user to https://claw-link.dev/dashboard?add=google-chat.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List spaces → Get space → Show members            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Preview message → User confirms → Execute send    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Space names use format `spaces/space-id` in API calls.
- Message threading uses `thread_key` to reply to existing threads.
- Custom emojis are only available for Google Workspace accounts and require admin enablement.
- With user authentication, only plain text messages are supported. Card-based messages require bot authentication.
- Message size limit is 32,000 bytes.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-chat`. |
| Missing connection | Google Chat is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-chat. |
| `404 Not Found` | Space, message, or member does not exist. Verify the IDs. |
| `403 Forbidden` | Insufficient permissions or the space requires bot authentication. |
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

1. Ensure the integration slug is exactly `google-chat`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Chat API Reference](https://developers.google.com/workspace/chat/api/reference/rest)
- [Google Chat API Overview](https://developers.google.com/workspace/chat/api/guides/overview)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-chat-messaging)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Slack](https://clawhub.ai/hith3sh/slack) — For alternative team messaging
- [Gmail](https://clawhub.ai/hith3sh/gmail-email) — For email alongside chat

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-chat-messaging)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)