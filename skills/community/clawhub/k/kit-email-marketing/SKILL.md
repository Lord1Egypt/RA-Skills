---
name: kit-email-marketing
description: Run email marketing campaigns via Kit (formerly ConvertKit). Manage subscribers, create broadcasts and sequences, handle tags and segments, track email stats, and automate workflows with webhooks.
---

# Kit

![Kit](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/kit.svg)

Run email marketing campaigns via Kit. Manage subscribers and tags, create broadcasts and email sequences, track email performance stats, and automate workflows with webhooks.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=kit-email-marketing) for hosted connection flows and credentials so you do not need to configure Kit API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Kit |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    Kit API        │
│   (User Chat)   │     │   (OAuth)    │     │   (v2)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect Kit  │                       │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │   Kit   │
   │  File    │      │ Auth     │           │Emails   │
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Kit again."

## Quick Start

```bash
# List all subscribers
clawlink_call_tool --tool "kit_list_subscribers" --params '{}'

# List all broadcasts
clawlink_call_tool --tool "kit_list_broadcasts" --params '{}'

# Get account info
clawlink_call_tool --tool "kit_get_account" --params '{}'
```

## Authentication

All Kit tool calls are authenticated automatically by ClawLink using the user's connected Kit account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Kit API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=kit and connect Kit (requires an active Kit account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `kit` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration kit
```

**Response:** Returns the live tool catalog for Kit.

### Reconnect

If Kit tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=kit
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration kit`

## Security & Permissions

- Access is scoped to the connected Kit account only.
- **All write operations require explicit user confirmation.** Before executing any subscriber, broadcast, or tag action, confirm the target resource and intended effect with the user.
- Destructive actions (delete subscriber, delete tag, delete broadcast) are marked as high-impact and must be confirmed.
- Subscriber deletion unsubscribes from all email communications — this cannot be undone.
- Broadcast creation can immediately send or schedule emails — confirm before executing.

## Tool Reference

### Account & Profile

| Tool | Description | Mode |
|------|-------------|------|
| `kit_get_account` | Get current account info including ID, plan, email, timezone | Read |
| `kit_get_creator_profile` | Get creator profile metadata (name, bio, avatar, profile URL) | Read |
| `kit_get_account_colors` | Get colors associated with the account | Read |
| `kit_update_account_colors` | Update account color palette (max 5 hex colors) | Write |

### Subscribers

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_subscribers` | List subscribers with optional filtering, sorting, and pagination | Read |
| `kit_get_subscriber` | Get subscriber details by ID | Read |
| `kit_filter_subscribers` | Filter subscribers by engagement (email opens, clicks, delivery) | Read |
| `kit_create_subscriber` | Create new subscriber or update existing (upsert by email) | Write |
| `kit_update_subscriber` | Update subscriber info (first name, email, custom fields) | Write |
| `kit_delete_subscriber` | Unsubscribe a subscriber from all communications | Write |
| `kit_tag_subscriber` | Add a tag to a subscriber by ID | Write |
| `kit_tag_subscriber_by_email` | Add a tag to a subscriber using their email address | Write |
| `kit_remove_tag_from_subscriber` | Remove a tag from a subscriber by ID | Write |
| `kit_untag_subscriber_by_email` | Remove a tag from a subscriber using their email | Write |
| `kit_get_subscriber_stats` | Get subscriber email stats (opens, clicks, bounces) | Read |
| `kit_list_subscribers_for_form` | Get subscribers for a specific form with filtering | Read |

### Tags

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_tags` | List all tags with pagination | Read |
| `kit_list_tag_subscribers` | Get subscribers for a specific tag | Read |
| `kit_create_tag` | Create a new tag for segmenting subscribers | Write |
| `kit_update_tag` | Update a tag's name by ID | Write |
| `kit_delete_tag` | Permanently delete a tag by ID | Write |

### Broadcasts

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_broadcasts` | List all broadcasts with cursor-based pagination | Read |
| `kit_get_broadcast` | Get broadcast details by ID | Read |
| `kit_get_broadcast_stats` | Get statistics for a specific broadcast | Read |
| `kit_get_broadcast_clicks` | Get link click data for a specific broadcast | Read |
| `kit_create_broadcast` | Create a new email broadcast (draft, scheduled, or immediate) | Write |
| `kit_delete_broadcast` | Permanently delete a broadcast by ID | Write |

### Sequences

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_sequences` | List all sequences with pagination | Read |

### Segments

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_segments` | List all segments with pagination | Read |

### Forms

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_forms` | List all forms (landing pages and embedded) with filtering | Read |
| `kit_add_subscriber_to_form` | Add an existing subscriber to a form by IDs | Write |
| `kit_add_subscriber_to_form_by_email` | Add a subscriber to a form using their email | Write |
| `kit_list_subscribers_for_form` | Get subscribers who joined a specific form | Read |

### Custom Fields

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_custom_fields` | List all custom fields with pagination | Read |
| `kit_create_custom_field` | Create a new custom field for subscriber data | Write |
| `kit_update_custom_field` | Update a custom field's label by ID | Write |
| `kit_delete_custom_field` | Permanently delete a custom field by ID | Write |

### Email Templates

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_email_templates` | List all email templates with pagination | Read |

### Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `kit_get_email_stats` | Get account email stats (sent, opened, clicked) for last 90 days | Read |
| `kit_get_growth_stats` | Get growth statistics over a date range | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `kit_list_webhooks` | List all configured webhooks with pagination | Read |
| `kit_create_webhook` | Create a webhook subscription for event notifications | Write |
| `kit_delete_webhook` | Permanently delete a webhook by ID | Write |

## Code Examples

### List subscribers

```bash
clawlink_call_tool --tool "kit_list_subscribers" \
  --params '{}'
```

### Create a subscriber

```bash
clawlink_call_tool --tool "kit_create_subscriber" \
  --params '{"email": "newsubscriber@example.com", "first_name": "John"}'
```

### Create a broadcast

```bash
clawlink_call_tool --tool "kit_create_broadcast" \
  --params '{"content": "<p>Hello! This is our newsletter.</p>", "public": true}'
```

### Tag a subscriber

```bash
clawlink_call_tool --tool "kit_tag_subscriber" \
  --params '{"subscriber_id": "SUBSCRIBER_ID", "tag_id": "TAG_ID"}'
```

### Get broadcast stats

```bash
clawlink_call_tool --tool "kit_get_broadcast_stats" \
  --params '{"broadcast_id": "BROADCAST_ID"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Kit is connected.
2. Call `clawlink_list_tools --integration kit` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `kit`.
5. If no Kit tools appear, direct the user to https://claw-link.dev/dashboard?add=kit.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List subscribers → Get stats → Show results       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview broadcast create → User approves → Send   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Kit uses cursor-based pagination for all list endpoints.
- Broadcast `send_at` parameter: set to null for draft, future timestamp for scheduled, omit for immediate publish.
- Setting `public` to true publishes the broadcast to the web.
- Subscriber upsert: if email exists, updates first name only; all other fields preserved.
- Subscriber stats data is only available for events from June 2025 onwards.
- Email stats cover the last 90 days in the account's sending timezone (not UTC).
- Account colors maximum is 5 hex color codes.
- Deleting a subscriber unsubscribes them from all sequences and forms; historical data is retained.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration kit`. |
| Missing connection | Kit is not connected. Direct the user to https://claw-link.dev/dashboard?add=kit. |
| Permission error | The connected account lacks permission for this operation. |
| Subscriber not found | The subscriber ID or email does not exist. Verify with `kit_list_subscribers`. |
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

## Resources

- [Kit API Documentation](https://api.kit.com/)
- [Kit Broadcasts Guide](https://kit.com/creators/broadcasts)
- [Kit Sequences Guide](https://kit.com/creators/sequences)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=kit-email-marketing
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Mailchimp Marketing](https://clawhub.ai/hith3sh/mailchimp-marketing) — For Mailchimp email campaigns
- [MailerLite Email Marketing](https://clawhub.ai/hith3sh/mailerlite-email-marketing) — For MailerLite campaigns and automation
- [Instantly Campaigns](https://clawhub.ai/hith3sh/instantly-campaigns) — For cold email outreach with Instantly

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=kit-email-marketing)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)