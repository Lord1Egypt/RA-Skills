---
name: jotform-forms
description: Manage Jotform forms, submissions, labels, and user accounts. Create and clone forms, retrieve submissions and reports, manage form labels, and monitor account usage and settings.
---

# Jotform

![Jotform](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/jotform.png)

Manage Jotform forms, submissions, labels, and account settings. Create and clone forms, retrieve submission data, organize forms with labels, generate reports, and monitor account usage.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=jotform-forms) for hosted connection flows and credentials so you do not need to configure Jotform API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Jotform |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Jotform API    │
│   (User Chat)   │     │   (OAuth)    │     │   (v2)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect Jotform│                      │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │  Jotform │
   │  File    │      │ Auth     │           │  Forms   │
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Jotform again."

## Quick Start

```bash
# List all forms
clawlink_call_tool --tool "jotform_get_user_forms" --params '{}'

# Get form submissions
clawlink_call_tool --tool "jotform_get_user_submissions" --params '{}'

# Get user account details
clawlink_call_tool --tool "jotform_get_user_details" --params '{}'
```

## Authentication

All Jotform tool calls are authenticated automatically by ClawLink using the user's connected Jotform account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Jotform API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=jotform and connect Jotform (requires an active Jotform account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `jotform` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration jotform
```

**Response:** Returns the live tool catalog for Jotform.

### Reconnect

If Jotform tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=jotform
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration jotform`

## Security & Permissions

- Access is scoped to the connected Jotform account only.
- **All write operations require explicit user confirmation.** Before executing any form or label action, confirm the target resource and intended effect with the user.
- Destructive actions (delete label) are marked as high-impact and must be confirmed.
- Form cloning copies all questions and settings — confirm before executing.
- Submission data contains personal information — handle according to your data policies.

## Tool Reference

### Forms & Submissions

| Tool | Description | Mode |
|------|-------------|------|
| `jotform_get_user_forms` | List all forms created by the authenticated user | Read |
| `jotform_get_user_submissions` | Get all submissions across all forms in the account | Read |
| `jotform_get_user_reports` | List report URLs for all forms (Excel, CSV, charts, embeddable) | Read |

### Labels

| Tool | Description | Mode |
|------|-------------|------|
| `jotform_get_user_folders` | List labels (folders replacement) for the authenticated user | Read |
| `jotform_get_label` | Get details of a specific label by ID (name and color) | Read |
| `jotform_get_label_resources` | Get forms assigned to a specific label | Read |
| `jotform_create_label` | Create a new label for organizing forms | Write |
| `jotform_update_label` | Update a label's name or color | Write |
| `jotform_delete_label` | Delete a label and all its sublabels | Write |
| `jotform_remove_label_resources` | Remove specific forms from a label | Write |

### User Account

| Tool | Description | Mode |
|------|-------------|------|
| `jotform_get_user_details` | Get account details and usage info | Read |
| `jotform_get_user_settings` | Get user settings including timezone, language, email | Read |
| `jotform_get_user_settings_by_key` | Get a specific user setting by key | Read |
| `jotform_update_user_settings` | Update user settings like timezone, language, email | Write |
| `jotform_get_user_history` | Get user activity history records | Read |
| `jotform_get_user_usage` | Get monthly usage statistics (submissions, SSL, storage) | Read |
| `jotform_get_system_plan` | Get plan limits and pricing details | Read |

### Form Operations

| Tool | Description | Mode |
|------|-------------|------|
| `jotform_clone_form` | Clone a complete form with all questions and settings | Write |

## Code Examples

### List all forms

```bash
clawlink_call_tool --tool "jotform_get_user_forms" \
  --params '{}'
```

### Get all submissions

```bash
clawlink_call_tool --tool "jotform_get_user_submissions" \
  --params '{}'
```

### Clone a form

```bash
clawlink_call_tool --tool "jotform_clone_form" \
  --params '{"form_id": "FORM_ID"}'
```

### Get user account details

```bash
clawlink_call_tool --tool "jotform_get_user_details" \
  --params '{}'
```

### Get monthly usage

```bash
clawlink_call_tool --tool "jotform_get_user_usage" \
  --params '{}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Jotform is connected.
2. Call `clawlink_list_tools --integration jotform` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `jotform`.
5. If no Jotform tools appear, direct the user to https://claw-link.dev/dashboard?add=jotform.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List forms → Get submissions → Show results      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview form clone → User approves → Execute      │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Jotform migrated from folders to labels — use label tools instead of folder tools.
- Submission answers are keyed by question IDs, not question text.
- Form reports include Excel, CSV, printable charts, and embeddable HTML tables.
- User history supports filtering by type and date range.
- Usage statistics are monthly and include form submissions, payment forms, SSL submissions, and storage.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration jotform`. |
| Missing connection | Jotform is not connected. Direct the user to https://claw-link.dev/dashboard?add=jotform. |
| Permission error | The connected account lacks permission for this operation. |
| Form not found | The form ID does not exist. Verify with `jotform_get_user_forms`. |
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

- [Jotform API Documentation](https://api.jotform.com/docs/)
- [Jotform Form Management](https://www.jotform.com/form-management/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=jotform-forms
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Intercom Support](https://clawhub.ai/hith3sh/intercom-support) — For customer support and contact management
- [Mailchimp Marketing](https://clawhub.ai/hith3sh/mailchimp-marketing) — For email marketing and audience management
- [Instantly Campaigns](https://clawhub.ai/hith3sh/instantly-campaigns) — For cold email outreach campaigns

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=jotform-forms)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)