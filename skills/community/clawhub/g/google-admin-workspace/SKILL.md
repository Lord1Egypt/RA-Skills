---
name: google-admin-workspace
description: Manage Google Workspace users, groups, domains, devices, and admin directory data via the Google Admin SDK API. Use this skill when users want to list and inspect users, create or update user accounts, manage groups and memberships, review organization units and directory metadata, or manage devices and admin resources in Google Workspace.
---

# Google Admin

![Google Admin](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-admin.png)

Access Google Workspace Admin SDK via the Google Admin API with OAuth authentication. Manage users, groups, domains, devices, and directory data.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-admin-workspace) for hosted connection flows and credentials so you do not need to configure Google Admin API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Admin |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Admin |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Google Admin SDK │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Google Admin                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Google   │
   │  File    │           │ Auth     │           │ Workspace│
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Admin again."

## Quick Start

```bash
# List all users in the domain
clawlink_call_tool --tool "google_admin_list_all_users" --params '{}'

# Get a specific user
clawlink_call_tool --tool "google_admin_get_a_user" --params '{"user_key": "user@example.com"}'

# List groups
clawlink_call_tool --tool "google_admin_list_all_groups" --params '{}'
```

## Authentication

All Google Admin tool calls are authenticated automatically by ClawLink using the user's connected Google Workspace admin account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Admin API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-admin and connect Google Admin.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-admin` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-admin
```

**Response:** Returns the live tool catalog for Google Admin.

### Reconnect

If Google Admin tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-admin
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-admin`

## Security & Permissions

- Access is scoped to the Google Workspace domain and resources the connected admin account can manage.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting users, removing groups) are marked as high-impact and must be confirmed.
- This skill requires Google Workspace admin privileges. Personal Gmail accounts do not have access to the Admin SDK.

## Tool Reference

### Users

| Tool | Description | Mode |
|------|-------------|------|
| `google_admin_list_all_users` | List all users in the domain | Read |
| `google_admin_get_a_user` | Get user details by email or ID | Read |
| `google_admin_create_user` | Create a new user account | Write |
| `google_admin_update_user` | Update user fields (name, departments, etc.) | Write |
| `google_admin_delete_user` | Delete a user account | Write |
| `google_admin_add_user_alias` | Add an email alias to a user | Write |
| `google_admin_turn_off_2_step_verification` | Disable 2SV for a user (admin only) | Write |

### Groups

| Tool | Description | Mode |
|------|-------------|------|
| `google_admin_list_all_groups` | List all groups in the domain | Read |
| `google_admin_get_group` | Get group details | Read |
| `google_admin_create_group` | Create a new group | Write |
| `google_admin_delete_group` | Delete a group | Write |
| `google_admin_add_user_to_group` | Add a user to a group | Write |
| `google_admin_remove_user_from_group` | Remove a user from a group | Write |

### Organization Units

| Tool | Description | Mode |
|------|-------------|------|
| `google_admin_list_all_organization_units` | List all organization units | Read |
| `google_admin_get_organization_unit` | Get OU details | Read |
| `google_admin_move_users_and_printers_to_ou` | Move users or printers to an OU | Write |

### Devices

| Tool | Description | Mode |
|------|-------------|------|
| `google_admin_list_all_devices` | List all devices in the domain | Read |
| `google_admin_get_device` | Get device details | Read |
| `google_admin_update_device` | Update device status or attributes | Write |

### Domain Management

| Tool | Description | Mode |
|------|-------------|------|
| `google_admin_get_domain_info` | Get domain information | Read |
| `google_admin_list_domains` | List all domains in the account | Read |

## Code Examples

### List all users

```bash
clawlink_call_tool --tool "google_admin_list_all_users" \
  --params '{
    "customer": "my_customer",
    "max_results": 100
  }'
```

### Create a new user

```bash
clawlink_call_tool --tool "google_admin_create_user" \
  --params '{
    "primary_email": "newuser@example.com",
    "name": {
      "given_name": "New",
      "family_name": "User"
    },
    "password": "secure-password-here"
  }'
```

### Add user to group

```bash
clawlink_call_tool --tool "google_admin_add_user_to_group" \
  --params '{
    "group_email": "engineering@example.com",
    "user_email": "newuser@example.com",
    "role": "MEMBER"
  }'
```

### List groups

```bash
clawlink_call_tool --tool "google_admin_list_all_groups" \
  --params '{}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Admin is connected.
2. Call `clawlink_list_tools --integration google-admin` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-admin`.
5. If no Google Admin tools appear, direct the user to https://claw-link.dev/dashboard?add=google-admin.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List users → Get user → Show details              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview user creation             │
│           → User approves → Execute create                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- This skill requires Google Workspace admin privileges. Personal Gmail accounts do not have Admin SDK access.
- User and group email addresses must belong to the verified Google Workspace domain.
- Some admin operations (like deleting users or moving OUs) may be restricted by admin policies.
- The `customer` parameter for user queries can be `my_customer` or the specific customer ID.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-admin`. |
| Missing connection | Google Admin is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-admin. |
| `404 Not Found` | User, group, or resource does not exist in the domain. |
| `403 Forbidden` | The connected account is not a Workspace admin or lacks permission for this operation. |
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

1. Ensure the integration slug is exactly `google-admin`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Admin SDK Documentation](https://developers.google.com/admin-sdk)
- [Directory API Reference](https://developers.google.com/admin-sdk/directory/reference/rest)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-admin-workspace)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Google Calendar](https://clawhub.ai/hith3sh/google-calendar-scheduling) — For calendar management
- [Gmail](https://clawhub.ai/hith3sh/gmail-email) — For email management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-admin-workspace)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)