---
name: omnisend-marketing
description: Manage contacts, campaigns, automations, and ecommerce marketing workflows in Omnisend. Use this skill when users want to create or update contacts, run email campaigns, manage automations, and review marketing performance data via the Omnisend API.
---

# Omnisend Marketing

![Omnisend Marketing](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/omnisend.svg)

Access Omnisend's marketing platform via the Omnisend API. Manage contacts, campaigns, automations, and ecommerce marketing workflows including email, SMS, and automation sequences.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=omnisend-marketing) for hosted connection flows and credentials so you do not need to configure Omnisend API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Omnisend |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Omnisend |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Omnisend API   │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Omnisend │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Omnisend │
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

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Omnisend again."

## Quick Start

```bash
# List contacts
clawlink_call_tool --tool "omnisend_list_contacts" --params '{"limit": 50}'

# Get campaign details
clawlink_call_tool --tool "omnisend_get_campaign" --params '{"campaign_id": "CAMPAIGN_ID"}'

# List automations
clawlink_call_tool --tool "omnisend_list_automations" --params '{"status": "active"}'
```

## Authentication

All Omnisend tool calls are authenticated automatically by ClawLink using the user's connected Omnisend account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Omnisend API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=omnisend and connect Omnisend.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `omnisend` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration omnisend
```

**Response:** Returns the live tool catalog for Omnisend.

### Reconnect

If Omnisend tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=omnisend
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration omnisend`

## Security& Permissions

- Access is scoped to contacts, campaigns, automations, and marketing data within the connected Omnisend account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete contact, cancel campaign) must be confirmed.
- Sending emails, SMS, or triggering automations are high-impact actions that require explicit user confirmation.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Omnisend is connected.
2. Call `clawlink_list_tools --integration omnisend` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `omnisend`.
5. If no Omnisend tools appear, direct the user to https://claw-link.dev/dashboard?add=omnisend.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List contacts → Read details → Show results       │
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

## Code Examples

### List contacts

```bash
clawlink_call_tool --tool "omnisend_list_contacts" \
  --params '{
    "limit": 100,
    "segment_id": "SEGMENT_ID"
  }'
```

### Create or update a contact

```bash
clawlink_call_tool --tool "omnisend_create_or_update_contact" \
  --params '{
    "email": "user@example.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "tags": ["customer", "premium"],
    "customProperties": {
      "plan": "enterprise"
    }
  }'
```

### Get campaign metrics

```bash
clawlink_call_tool --tool "omnisend_get_campaign_metrics" \
  --params '{
    "campaign_id": "CAMPAIGN_ID"
  }'
```

### Trigger an automation

```bash
clawlink_call_tool --tool "omnisend_trigger_automation" \
  --params '{
    "automation_id": "AUTOMATION_ID",
    "email": "user@example.com"
  }'
```

## Notes

- Omnisend API has rate limits. Use exponential backoff when encountering 429 errors.
- Contact email addresses must be valid format — invalid emails will be rejected.
- Campaign and automation IDs are strings — verify IDs before passing to write operations.
- Tags on contacts are strings — avoid duplicate tags to prevent redundant processing.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration omnisend`. |
| Missing connection | Omnisend is not connected. Direct the user to https://claw-link.dev/dashboard?add=omnisend. |
| `not_found` | Contact, campaign, or automation does not exist. Check the ID. |
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

1. Ensure the integration slug is exactly `omnisend`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Omnisend API Documentation](https://api-docs.omnisend.com/)
- [Omnisend Integrations](https://www.omnisend.com/integrations/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=omnisend-marketing
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Mailchimp Marketing](https://clawhub.ai/hith3sh/mailchimp-marketing) — For Mailchimp email marketing
- [Omnisend](https://clawhub.ai/hith3sh/omnisend-marketing) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=omnisend-marketing)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
