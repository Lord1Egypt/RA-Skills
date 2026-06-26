---
name: mailerlite-email-marketing
description: Manage MailerLite email marketing campaigns, automations, subscribers, and e-commerce stores. Create campaigns, manage groups and segments, handle subscribers, and track e-commerce activity.
---

# MailerLite

![MailerLite](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/mailerlite.svg)

Manage MailerLite email marketing operations. Create campaigns and automations, manage subscribers and groups, handle e-commerce stores, and track performance with analytics.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=mailerlite-email-marketing) for hosted connection flows and credentials so you do not need to configure MailerLite API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect MailerLite |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ MailerLite API   │
│   (User Chat)   │     │   (OAuth)    │     │   (v2)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect MailerLite│                     │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │MailerLite│
   │  File    │      │ Auth     │           │ Marketing│
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for MailerLite again."

## Quick Start

```bash
# Get account info
clawlink_call_tool --tool "mailerlite_get_account_info" --params '{}'

# List subscribers
clawlink_call_tool --tool "mailerlite_get_subscribers" --params '{}'

# List campaigns
clawlink_call_tool --tool "mailerlite_get_campaigns" --params '{}'
```

## Authentication

All MailerLite tool calls are authenticated automatically by ClawLink using the user's connected MailerLite account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every MailerLite API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=mailerlite and connect MailerLite (requires an active MailerLite account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `mailerlite` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration mailerlite
```

**Response:** Returns the live tool catalog for MailerLite.

### Reconnect

If MailerLite tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=mailerlite
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration mailerlite`

## Security & Permissions

- Access is scoped to the connected MailerLite account only.
- **All write operations require explicit user confirmation.** Before executing any campaign, subscriber, or automation action, confirm the target resource and intended effect with the user.
- Destructive actions (delete automation, delete subscriber, delete shop) are marked as high-impact and must be confirmed.
- Subscriber deletion and GDPR "forget" operations are permanent — confirm before executing.

## Tool Reference

### Account

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_account_info` | Get basic MailerLite account details and metadata | Read |

### Subscribers

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_subscribers` | List subscribers with pagination | Read |
| `mailerlite_get_subscriber` | Get subscriber details by ID | Read |
| `mailerlite_create_subscriber` | Create or update (upsert) subscriber by email | Write |
| `mailerlite_update_subscriber` | Update existing subscriber details | Write |
| `mailerlite_delete_subscriber` | Permanently delete subscriber by ID | Write |
| `mailerlite_forget_subscriber` | GDPR-compliant deletion (erases all data within 30 days) | Write |

### Groups & Segments

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_groups` | List all subscriber groups | Read |
| `mailerlite_get_group` | Get group details by ID | Read |
| `mailerlite_create_group` | Create a new subscriber group | Write |
| `mailerlite_update_group` | Update group name or settings | Write |
| `mailerlite_delete_group` | Permanently delete a group and its associations | Write |
| `mailerlite_add_subscriber_to_group` | Add subscriber to a group | Write |
| `mailerlite_remove_subscriber_from_group` | Remove subscriber from a group | Write |
| `mailerlite_get_segments` | List all subscriber segments | Read |
| `mailerlite_get_segment` | Get segment details by ID | Read |
| `mailerlite_create_segment` | Create a new segment with criteria | Write |
| `mailerlite_update_segment` | Update segment configuration | Write |
| `mailerlite_delete_segment` | Permanently delete a segment | Write |

### Custom Fields

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_fields` | List all custom fields | Read |
| `mailerlite_get_field` | Get custom field details by ID | Read |
| `mailerlite_create_field` | Create a new custom field | Write |
| `mailerlite_update_field` | Update custom field properties | Write |
| `mailerlite_delete_field` | Permanently delete a custom field | Write |

### Campaigns

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_campaigns` | List all campaigns with pagination | Read |
| `mailerlite_get_campaign` | Get campaign details by ID | Read |
| `mailerlite_create_campaign` | Create a new email campaign draft | Write |
| `mailerlite_update_campaign` | Update campaign settings and content | Write |
| `mailerlite_delete_campaign` | Permanently delete a campaign | Write |
| `mailerlite_schedule_campaign` | Schedule campaign for future sending | Write |
| `mailerlite_unschedule_campaign` | Remove campaign from schedule | Write |
| `mailerlite_pause_campaign` | Pause a sending campaign | Write |
| `mailerlite_resume_campaign` | Resume a paused campaign | Write |
| `mailerlite_send_campaign` | Send campaign immediately | Write |
| `mailerlite_clone_campaign` | Clone an existing campaign | Write |

### Automations

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_automations` | List all automations | Read |
| `mailerlite_get_automation` | Get automation details by ID | Read |
| `mailerlite_create_automation` | Create a new automation workflow | Write |
| `mailerlite_update_automation` | Update automation settings | Write |
| `mailerlite_delete_automation` | Permanently delete an automation | Write |
| `mailerlite_start_automation` | Start an automation | Write |
| `mailerlite_stop_automation` | Stop a running automation | Write |

### E-Commerce

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_ecommerce_shops` | List all connected e-commerce shops | Read |
| `mailerlite_get_ecommerce_shop` | Get shop details by ID | Read |
| `mailerlite_create_ecommerce_shop` | Connect a new e-commerce shop | Write |
| `mailerlite_delete_ecommerce_shop` | Disconnect an e-commerce shop | Write |
| `mailerlite_get_ecommerce_customers` | List customers in a shop | Read |
| `mailerlite_create_ecommerce_customer` | Create or update customer | Write |
| `mailerlite_delete_ecommerce_customer` | Delete customer from shop | Write |
| `mailerlite_get_ecommerce_products` | List products in a shop | Read |
| `mailerlite_create_ecommerce_product` | Add a new product | Write |
| `mailerlite_update_ecommerce_product` | Update product details | Write |
| `mailerlite_delete_ecommerce_product` | Delete product from shop | Write |
| `mailerlite_get_ecommerce_categories` | List product categories | Read |
| `mailerlite_create_ecommerce_category` | Create a product category | Write |
| `mailerlite_delete_ecommerce_category` | Delete category from shop | Write |
| `mailerlite_add_product_to_category` | Assign product to a category | Write |
| `mailerlite_get_ecommerce_orders` | List orders in a shop | Read |
| `mailerlite_create_ecommerce_order` | Create a new order | Write |
| `mailerlite_update_ecommerce_order` | Update order status | Write |
| `mailerlite_delete_ecommerce_order` | Delete order from shop | Write |
| `mailerlite_get_ecommerce_carts` | List active carts | Read |
| `mailerlite_create_ecommerce_cart_item` | Add item to cart (creates cart if needed) | Write |
| `mailerlite_delete_ecommerce_cart_item` | Remove item from cart | Write |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_get_webhooks` | List all webhooks | Read |
| `mailerlite_get_webhook` | Get webhook details by ID | Read |
| `mailerlite_create_webhook` | Register a new webhook URL | Write |
| `mailerlite_update_webhook` | Update webhook settings | Write |
| `mailerlite_delete_webhook` | Permanently delete a webhook | Write |

### Batch Operations

| Tool | Description | Mode |
|------|-------------|------|
| `mailerlite_execute_batch_request` | Execute multiple API requests in one call (max 50) | Write |

## Code Examples

### Get account info

```bash
clawlink_call_tool --tool "mailerlite_get_account_info" \
  --params '{}'
```

### List subscribers

```bash
clawlink_call_tool --tool "mailerlite_get_subscribers" \
  --params '{"limit": 25}'
```

### Create a subscriber

```bash
clawlink_call_tool --tool "mailerlite_create_subscriber" \
  --params '{"email": "newsubscriber@example.com", "name": "John Doe"}'
```

### Create a campaign

```bash
clawlink_call_tool --tool "mailerlite_create_campaign" \
  --params '{"subject": "Our Newsletter", "from_name": "My Company", "reply_to": "noreply@example.com"}'
```

### Schedule a campaign

```bash
clawlink_call_tool --tool "mailerlite_schedule_campaign" \
  --params '{"campaign_id": "CAMPAIGN_ID", "schedule_time": "2024-12-15T10:00:00+00:00"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm MailerLite is connected.
2. Call `clawlink_list_tools --integration mailerlite` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `mailerlite`.
5. If no MailerLite tools appear, direct the user to https://claw-link.dev/dashboard?add=mailerlite.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List subscribers → Get details → Show results     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview campaign send → User approves → Send     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Campaign creation sets `can_be_scheduled` based on plan capabilities.
- HTML content support is plan-dependent — insufficient plan sets `can_be_scheduled=false` on draft.
- Subscriber upsert updates non-destructively — omitted fields and groups are preserved.
- GDPR `forget_subscriber` permanently deletes all data within 30 days.
- Batch requests maximum 50 requests per call; individual failures don't stop processing.
- Webhooks are not supported in batch requests.
- Cart creation for abandoned cart automations creates cart if it does not exist.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration mailerlite`. |
| Missing connection | MailerLite is not connected. Direct the user to https://claw-link.dev/dashboard?add=mailerlite. |
| Permission error | The account lacks permission for this operation. |
| Subscriber not found | The subscriber ID or email does not exist. |
| Campaign not found | The campaign ID does not exist. Verify with `mailerlite_get_campaigns`. |
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

- [MailerLite API Documentation](https://developers.mailerlite.com/)
- [MailerLite Integrations](https://www.mailerlite.com/integrations)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=mailerlite-email-marketing
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Mailchimp Marketing](https://clawhub.ai/hith3sh/mailchimp-marketing) — For Mailchimp campaigns and automations
- [Kit Email Marketing](https://clawhub.ai/hith3sh/kit-email-marketing) — For Kit email broadcasts
- [Instantly Campaigns](https://clawhub.ai/hith3sh/instantly-campaigns) — For Instantly cold email outreach

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=mailerlite-email-marketing)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)