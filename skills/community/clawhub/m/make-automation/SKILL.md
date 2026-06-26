---
name: make-automation
description: Manage Make.com organizations, users, teams, scenarios, and billing. Configure organization settings, manage team members, retrieve usage analytics, and access pricing information.
---

# Make

![Make](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/make.svg)

Manage Make.com organization administration, users, teams, and billing. Configure organizations, manage team members, retrieve usage analytics, and access pricing and feature information.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=make-automation) for hosted connection flows and credentials so you do not need to configure Make API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Make |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Make API        │
│   (User Chat)   │     │   (OAuth)    │     │   (v2)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect Make  │                       │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │   Make   │
   │  File    │      │ Auth     │           │Platform  │
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Make again."

## Quick Start

```bash
# Get current user info
clawlink_call_tool --tool "make_get_users_me" --params '{}'

# List organizations
clawlink_call_tool --tool "make_list_organizations" --params '{}'

# Get operations usage
clawlink_call_tool --tool "make_get_operations" --params '{}'
```

## Authentication

All Make tool calls are authenticated automatically by ClawLink using the user's connected Make account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Make API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=make and connect Make (requires an active Make account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `make` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration make
```

**Response:** Returns the live tool catalog for Make.

### Reconnect

If Make tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=make
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration make`

## Security & Permissions

- Access is scoped to the connected Make account and its organizations.
- **All write operations require explicit user confirmation.** Before executing any organization or user action, confirm the target resource and intended effect with the user.
- Destructive actions (delete resources) are marked as high-impact and must be confirmed.
- Password reset demands trigger emails to users — confirm before executing.

## Tool Reference

### Users & Authorization

| Tool | Description | Mode |
|------|-------------|------|
| `make_get_users_me` | Get current authenticated user details (ID, name, email, timezone) | Read |
| `make_get_current_authorization` | Get authorization details and permission scopes | Read |
| `make_create_users_password_reset_demand` | Create password reset demand for user by email | Write |

### Organizations

| Tool | Description | Mode |
|------|-------------|------|
| `make_list_organizations` | List organizations the user belongs to | Read |
| `make_create_organizations` | Create a new organization with region, timezone, country | Write |

### Teams

| Tool | Description | Mode |
|------|-------------|------|
| `make_list_teams` | List all teams within an organization | Read |

### Billing & Usage

| Tool | Description | Mode |
|------|-------------|------|
| `make_get_operations` | Get daily operations usage over past 30 days | Read |
| `make_get_cashier_products` | Get available subscription plans and add-ons | Read |
| `make_get_cashier_prices` | Get specific cashier price details | Read |

### Enums

| Tool | Description | Mode |
|------|-------------|------|
| `make_list_enums_countries` | Get all supported countries (ID, name, ISO codes) | Read |
| `make_list_enums_languages` | Get language codes and names | Read |
| `make_list_enums_llm_builtin_tiers` | Get LLM tiers (small, medium, large) with models and pricing | Read |
| `make_list_enums_locales` | Get supported locales with display names and codes | Read |
| `make_list_enums_timezones` | Get all supported timezones with GMT offsets | Read |
| `make_get_enums_apps_review_statuses` | Get app review statuses | Read |
| `make_get_enums_imt_regions` | Get Make regions and regionId values | Read |
| `make_get_enums_imt_zones` | Get available IMT zones for organization creation | Read |
| `make_get_enums_llm_models` | Get available Large Language Models for AI mapping | Read |
| `make_get_enums_module_types` | Get available module types for scenarios | Read |
| `make_get_enums_organization_features` | Get organization feature values | Read |
| `make_get_enums_user_api_token_scopes` | Get available API token scopes | Read |
| `make_get_enums_user_email_notifications` | Get email notification types | Read |
| `make_get_enums_user_features` | Get user features with titles and identifiers | Read |
| `make_get_enums_variable_types` | Get variable types for data stores | Read |

### API

| Tool | Description | Mode |
|------|-------------|------|
| `make_ping_api` | Verify Make API connectivity and availability | Read |

## Code Examples

### Get current user

```bash
clawlink_call_tool --tool "make_get_users_me" \
  --params '{}'
```

### List organizations

```bash
clawlink_call_tool --tool "make_list_organizations" \
  --params '{}'
```

### Get operations usage

```bash
clawlink_call_tool --tool "make_get_operations" \
  --params '{"organization_id": "ORG_ID"}'
```

### Get countries

```bash
clawlink_call_tool --tool "make_list_enums_countries" \
  --params '{}'
```

### Get LLM models

```bash
clawlink_call_tool --tool "make_get_enums_llm_models" \
  --params '{}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Make is connected.
2. Call `clawlink_list_tools --integration make` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `make`.
5. If no Make tools appear, direct the user to https://claw-link.dev/dashboard?add=make.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List organizations → Get teams → Show results     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview org create → User approves → Execute      │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Operations usage returns data for the past 30 days including operations count, data transfer, and centicredits consumption per day.
- List Organizations first to get `organization_id` before calling operations or teams endpoints.
- Countries, languages, locales, and timezones are needed for organization creation.
- LLM models are used for AI mapping and AI toolkit configurations.
- Variable types are used for creating data stores and variables.
- API token scopes are used for creating and managing API tokens.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration make`. |
| Missing connection | Make is not connected. Direct the user to https://claw-link.dev/dashboard?add=make. |
| Permission error | The authenticated user lacks permission for this operation. |
| Organization not found | The organization ID does not exist. Verify with `make_list_organizations`. |
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

- [Make API Documentation](https://www.make.com/en/api-docs)
- [Make Help Center](https://www.make.com/en/help)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=make-automation
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Monday Workflows](https://clawhub.ai/hith3sh/monday-workflows) — For Monday.com project management
- [Motion Planning](https://clawhub.ai/hith3sh/motion-planning) — For Motion task and project planning

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=make-automation)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)