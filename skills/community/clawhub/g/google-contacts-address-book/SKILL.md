---
name: google-contacts-address-book
description: Google Contacts API integration with managed OAuth. Search, inspect, create, and update contacts and contact groups stored in Google People. Use this skill when users want to read or modify Google Contacts, manage groups, or look up people data.
---

# Google Contacts

![Google Contacts](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-contacts.svg)

Access Google Contacts via the Google People API with managed OAuth authentication. Search, inspect, create, and update contacts and contact groups stored in Google Contacts.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-contacts-address-book) for hosted connection flows and credentials so you do not need to configure Google Contacts API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Contacts |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Contacts |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google People  │
│   (User Chat)   │     │   (OAuth)    │     │   (Contacts API) │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Contacts   │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  People  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Contacts again."

## Quick Start

```bash
# List contacts
clawlink_call_tool --tool "googlecontacts_list_contacts" --params '{}'

# Search contacts by name
clawlink_call_tool --tool "googlecontacts_search_contacts" --params '{"query": "John Smith"}'

# Get a contact by ID
clawlink_call_tool --tool "googlecontacts_get_contact" --params '{"resource_name": "people/123456789"}'
```

## Authentication

All Google Contacts tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google People API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-contacts and connect Google Contacts.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-contacts` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-contacts
```

**Response:** Returns the live tool catalog for Google Contacts.

### Reconnect

If Google Contacts tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-contacts
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-contacts`

## Security & Permissions

- Access is scoped to contacts and contact groups within the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete contact, delete group) are marked as high-impact and must be confirmed.
- Contact permissions can be inspected to understand sharing state before making changes.

## Tool Reference

### Contact Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlecontacts_list_contacts` | List all contacts in the user's Google Contacts | Read |
| `googlecontacts_search_contacts` | Search contacts by name, email, or other fields | Read |
| `googlecontacts_get_contact` | Retrieve a specific contact by resource name | Read |
| `googlecontacts_create_contact` | Create a new contact in Google Contacts | Write |
| `googlecontacts_update_contact` | Update an existing contact's information | Write |
| `googlecontacts_delete_contact` | Delete a contact from Google Contacts | Write |

### Contact Group Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlecontacts_list_contact_groups` | List all contact groups | Read |
| `googlecontacts_get_contact_group` | Retrieve a specific contact group | Read |
| `googlecontacts_create_contact_group` | Create a new contact group | Write |
| `googlecontacts_update_contact_group` | Update a contact group's name | Write |
| `googlecontacts_delete_contact_group` | Delete a contact group | Write |

### Batch Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlecontacts_batch_create_contacts` | Create multiple contacts in a single request | Write |
| `googlecontacts_batch_update_contacts` | Update multiple contacts in a single request | Write |
| `googlecontacts_batch_delete_contacts` | Delete multiple contacts in a single request | Write |

### Directory & Profile

| Tool | Description | Mode |
|------|-------------|------|
| `googlecontacts_get_profile` | Get the user's Google profile information | Read |
| `googlecontacts_list_people` | Search the directory for people | Read |

### Photo Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlecontacts_get_contact_photo` | Get a contact's profile photo | Read |
| `googlecontacts_update_contact_photo` | Update a contact's profile photo | Write |

## Code Examples

### List all contacts

```bash
clawlink_call_tool --tool "googlecontacts_list_contacts" \
  --params '{
    "page_size": 100
  }'
```

### Search contacts by name

```bash
clawlink_call_tool --tool "googlecontacts_search_contacts" \
  --params '{
    "query": "John Smith"
  }'
```

### Create a new contact

```bash
clawlink_call_tool --tool "googlecontacts_create_contact" \
  --params '{
    "names": [{"givenName": "Jane", "familyName": "Doe"}],
    "emailAddresses": [{"value": "jane.doe@example.com", "type": "home"}],
    "phoneNumbers": [{"value": "+1-555-0100", "type": "mobile"}]
  }'
```

### Create a contact group

```bash
clawlink_call_tool --tool "googlecontacts_create_contact_group" \
  --params '{
    "name": "Work Colleagues"
  }'
```

### Update a contact

```bash
clawlink_call_tool --tool "googlecontacts_update_contact" \
  --params '{
    "resource_name": "people/123456789",
    "names": [{"givenName": "Jane", "familyName": "Smith"}],
    "emailAddresses": [{"value": "jane.smith@example.com", "type": "work"}]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Contacts is connected.
2. Call `clawlink_list_tools --integration google-contacts` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-contacts`.
5. If no Google Contacts tools appear, direct the user to https://claw-link.dev/dashboard?add=google-contacts.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → search → get → call                                  │
│                                                             │
│  Example: Search contacts → Get details → Show results      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Google Contacts uses the Google People API under the hood.
- Contact IDs (resource names) are stable but not human-readable — always capture them from list/search responses for subsequent operations.
- Contact groups let you organize contacts and can be used for batch operations.
- Due to Google API scope restrictions, some directory and profile features may require additional OAuth scopes.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-contacts`. |
| Missing connection | Google Contacts is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-contacts. |
| `RESOURCE_NOT_FOUND` | Contact or contact group does not exist. Check the resource name. |
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

1. Ensure the integration slug is exactly `google-contacts`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google People API Overview](https://developers.google.com/people/api/rest)
- [Google Contacts API](https://developers.google.com/contacts/v3)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-contacts-address-book
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Drive](https://clawhub.ai/hith3sh/google-drive-files) — For general Google Drive file management
- [Gmail](https://clawhub.ai/hith3sh/gmail) — For email operations in Google Workspace

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-contacts-address-book)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)