---
name: postmark-email
description: Inspect transactional email activity, manage templates, review message delivery events, and configure webhooks in Postmark via the Postmark API. Use this skill when users want to monitor email delivery, manage templates, check bounce and spam reports, and configure transactional email workflows via Postmark.
---

# Postmark Email

![Postmark Email](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/postmark.svg)

Access Postmark's transactional email platform via the Postmark API. Inspect outbound messages, templates, and delivery events. Review bounce, spam, and engagement statistics. Manage webhooks and message streams.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postmark-email) for hosted connection flows and credentials so you do not need to configure Postmark API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Postmark |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Postmark |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Postmark API   │
│   (User Chat)   │     │   (API Key)  │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │2. Pair Device      │                       │
          │3. Connect Postmark  │                       │
          │                      │  4. Secure Proxy      │
          │                      │  5. API Requests      │
          │                      │                       │
          ▼ ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Postmark │
    │  File    │           │ Auth     │           │ Platform │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Postmark again."

## Quick Start

```bash
# Get outbound overview
clawlink_call_tool --tool "postmark_get_outbound_overview" --params '{}'

# Search outbound messages
clawlink_call_tool --tool "postmark_search_outbound_messages" --params '{"status": "sent"}'

# List templates
clawlink_call_tool --tool "postmark_list_templates" --params '{}'
```

## Authentication

All Postmark tool calls are authenticated automatically by ClawLink using the user's Postmark account.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every Postmark API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=postmark and connect Postmark.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `postmark` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration postmark
```

**Response:** Returns the live tool catalog for Postmark.

### Reconnect

If Postmark tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=postmark
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration postmark`

## Security& Permissions

- Access is scoped to messages, templates, streams, and webhooks within the connected Postmark server.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete template, delete webhook, archive stream) must be confirmed.
- Server configuration changes affect all email sending on that server.

## Tool Reference

### Message Streams

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_list_message_streams` | List all message streams for a server | Read |
| `postmark_get_message_stream` | Get details of a specific stream | Read |
| `postmark_create_message_stream` | Create a new message stream | Write |
| `postmark_update_message_stream` | Update a stream's name or description | Write |
| `postmark_archive_message_stream` | Archive a message stream (soft delete) | Write |
| `postmark_unarchive_message_stream` | Restore an archived stream | Write |

### Outbound Messages

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_search_outbound_messages` | Search sent messages with filters | Read |
| `postmark_get_sent_counts` | Get sent message counts by date range | Read |
| `postmark_get_delivery_stats` | Get delivery statistics | Read |
| `postmark_list_outbound_message_opens` | List open events for outbound messages | Read |
| `postmark_list_outbound_message_clicks` | List click events for outbound messages | Read |

### Inbound Messages

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_search_inbound_messages` | Search inbound messages | Read |

### Templates

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_list_templates` | List all templates | Read |
| `postmark_get_template` | Get template details by ID | Read |
| `postmark_create_template` | Create a new template | Write |
| `postmark_edit_template` | Update an existing template | Write |
| `postmark_delete_template` | Delete a template permanently | Write |
| `postmark_validate_template` | Validate a template against sample data | Read |

### Bounces & Spam

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_get_bounce_counts` | Get aggregate bounce counts | Read |
| `postmark_get_bounces` | List bounces with filters | Read |
| `postmark_get_spam_complaints` | Get spam complaint counts | Read |
| `postmark_check_spam_score` | Check spam score of raw email | Read |

### Statistics & Engagement

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_get_outbound_overview` | Get outbound statistics overview | Read |
| `postmark_get_email_open_counts` | Get email open counts | Read |
| `postmark_get_click_counts` | Get link click counts | Read |
| `postmark_get_email_client_usage` | Get email client usage statistics | Read |
| `postmark_get_browser_usage` | Get browser usage for clicks | Read |
| `postmark_get_browser_platform_usage` | Get browser platform usage | Read |
| `postmark_get_clicks_by_browser_family` | Get clicks grouped by browser | Read |
| `postmark_get_clicks_by_location` | Get clicks by content type (HTML/Text) | Read |
| `postmark_get_opens_by_platform` | Get opens by platform | Read |
| `postmark_get_tracked_email_counts` | Get counts of tracked emails | Read |

### Suppressions

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_list_suppressions` | List suppressed email addresses | Read |
| `postmark_create_suppressions` | Add addresses to suppression list | Write |
| `postmark_delete_suppressions` | Remove addresses from suppression list | Write |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_list_webhooks` | List all webhooks | Read |
| `postmark_get_webhook` | Get webhook details | Read |
| `postmark_create_webhook` | Create a new webhook | Write |
| `postmark_edit_webhook` | Update a webhook's URL or triggers | Write |
| `postmark_delete_webhook` | Delete a webhook permanently | Write |

### Inbound Rules

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_list_inbound_rules` | List inbound rule triggers | Read |
| `postmark_create_inbound_rule` | Create an inbound rule | Write |
| `postmark_delete_inbound_rule` | Delete an inbound rule | Write |

### Server Configuration

| Tool | Description | Mode |
|------|-------------|------|
| `postmark_get_server` | Get server configuration details | Read |
| `postmark_edit_server` | Update server settings | Write |

## Code Examples

### Get outbound overview

```bash
clawlink_call_tool --tool "postmark_get_outbound_overview" \
  --params '{
    "from": "2024-01-01",
    "to": "2024-01-31"
  }'
```

### Search outbound messages

```bash
clawlink_call_tool --tool "postmark_search_outbound_messages" \
  --params '{
    "recipient": "customer@example.com",
    "status": "sent",
    "tag": "welcome"
  }'
```

### Get template details

```bash
clawlink_call_tool --tool "postmark_get_template" \
  --params '{
    "template_id": "TEMPLATE_ID"
  }'
```

### Create a webhook

```bash
clawlink_call_tool --tool "postmark_create_webhook" \
  --params '{
    "url": "https://example.com/webhook/postmark",
    "triggers": {
      "open": true,
      "click": true,
      "bounce": true,
      "spam_complaint": true
    },
    "http_headers": {
      "Authorization": "Bearer secret_token"
    }
  }'
```

### List suppressions

```bash
clawlink_call_tool --tool "postmark_list_suppressions" \
  --params '{
    "message_stream": "outbound"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Postmark is connected.
2. Call `clawlink_list_tools --integration postmark` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `postmark`.
5. If no Postmark tools appear, direct the user to https://claw-link.dev/dashboard?add=postmark.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Get outbound overview → List templates → Report  │
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

- Postmark API has rate limits. Use exponential backoff when encountering 429 errors.
- SpamComplaint suppressions cannot be removed from the suppression list — only HardBounce and ManualSuppression can be deleted.
- Archived message streams are permanently deleted after 45 days.
- Webhook triggers require link tracking to be enabled for click and open events.
- Date range filters use ISO 8601 format (YYYY-MM-DD).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration postmark`. |
| Missing connection | Postmark is not connected. Direct the user to https://claw-link.dev/dashboard?add=postmark. |
| `not_found` | Template, webhook, or stream does not exist. Check the ID. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Rate limited | Too many requests. Wait and retry with exponential backoff. |
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

1. Ensure the integration slug is exactly `postmark`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Postmark API Documentation](https://postmarkapp.com/developer/api/overview)
- [Message Streams API](https://postmarkapp.com/developer/api/message-streams)
- [Templates API](https://postmarkapp.com/developer/api/templates)
- [Webhooks API](https://postmarkapp.com/developer/api/webhooks)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postmark-email
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Postmark](https://clawhub.ai/hith3sh/postmark-email) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postmark-email)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
