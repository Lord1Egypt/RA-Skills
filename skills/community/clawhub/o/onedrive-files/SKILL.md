---
name: onedrive-files
description: Browse, search, download, and share OneDrive files, create folders, upload files, and manage file actions via Microsoft Graph. Use this skill when users want to manage OneDrive files, SharePoint documents, sharing links, and drive metadata using the Microsoft Graph API.
---

# OneDrive Files

![OneDrive Files](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/onedrive.svg)

Access OneDrive and SharePoint via Microsoft Graph API with managed OAuth authentication. Browse files, search folders, inspect details, create folders, share links, upload files, and manage drive metadata.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onedrive-files) for hosted connection flows and credentials so you do not need to configure Microsoft Graph access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect OneDrive |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect OneDrive |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Microsoft Graph  │
│   (User Chat)   │     │   (OAuth)    │     │   (OneDrive API) │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect OneDrive  │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ OneDrive│
    │  File    │           │ Auth     │           │ /SharePt│
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for OneDrive again."

## Quick Start

```bash
# List items in OneDrive root
clawlink_call_tool --tool "one_drive_onedrive_list_items" --params '{}'

# Search for files
clawlink_call_tool --tool "one_drive_search_items" --params '{"query": "report.xlsx"}'

# Get file metadata
clawlink_call_tool --tool "one_drive_get_item" --params '{"item_id": "FILE_ID"}'
```

## Authentication

All OneDrive tool calls are authenticated automatically by ClawLink using the user's connected Microsoft account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Microsoft Graph request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=onedrive and connect OneDrive.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `onedrive` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration onedrive
```

**Response:** Returns the live tool catalog for OneDrive.

### Reconnect

If OneDrive tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=onedrive
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration onedrive`

## Security& Permissions

- Access is scoped to files, folders, and drive data within the connected Microsoft account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete file, remove sharing permission) must be confirmed.
- Sharing link creation grants external access — confirm the recipient and permission level.

## Tool Reference

### Drive & Item Operations

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_list_drives` | List all drives accessible to the authenticated user | Read |
| `one_drive_get_drive` | Get drive properties by ID | Read |
| `one_drive_get_root` | Get the root folder of the user's OneDrive | Read |
| `one_drive_get_item` | Get file or folder metadata by ID | Read |
| `one_drive_get_item_permissions` | List permissions on a file or folder | Read |
| `one_drive_get_item_thumbnails` | Get thumbnail URLs for a file | Read |
| `one_drive_get_item_versions` | Get version history of a file | Read |
| `one_drive_list_folder_children` | List contents of a folder by ID or path | Read |
| `one_drive_list_root_drive_changes` | Track changes in the drive root via delta token | Read |
| `one_drive_search_items` | Search files and folders by keyword | Read |
| `one_drive_get_recent_items` | Get recently accessed files | Read |
| `one_drive_get_shared_items` | Get items shared with the user | Read |
| `one_drive_preview_drive_item` | Generate a short-lived preview URL for a file | Read |

### File & Folder Management

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_onedrive_list_items` | List files and folders in OneDrive root | Read |
| `one_drive_onedrive_find_file` | Find a file in a specific folder | Read |
| `one_drive_onedrive_find_folder` | Find folders by name | Read |
| `one_drive_onedrive_create_folder` | Create a new folder in OneDrive | Write |
| `one_drive_onedrive_create_text_file` | Create a text file in OneDrive | Write |
| `one_drive_onedrive_upload_file` | Upload a file to OneDrive | Write |
| `one_drive_move_item` | Move a file or folder to a new location | Write |
| `one_drive_copy_item` | Copy a file or folder to a new location | Write |
| `one_drive_update_drive_item_metadata` | Update file/folder metadata (rename, move) | Write |
| `one_drive_update_file_content` | Update file content via upload session | Write |
| `one_drive_delete_item` | Delete a file or folder (moves to recycle bin) | Write |
| `one_drive_delete_item_permanently` | Permanently delete a file or folder | Write |

### Sharing & Permissions

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_create_link` | Create a sharing link for a file or folder | Write |
| `one_drive_invite_user_to_item` | Invite a user to access a file or folder | Write |
| `one_drive_grant_share_permission` | Grant access via a sharing URL | Write |
| `one_drive_create_item_permission` | Create a permission on an item | Write |
| `one_drive_delete_item_permission` | Remove a permission from an item | Write |
| `one_drive_update_drive_items_permissions` | Update permission roles | Write |
| `one_drive_list_share_permissions` | List permissions from a sharing URL | Read |

### Check In / Check Out

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_checkout_item` | Check out a file to prevent others from editing | Write |
| `one_drive_checkin_item` | Check in a previously checked-out file | Write |
| `one_drive_discard_checkout` | Discard checkout and discard changes | Write |

### Site & SharePoint Operations

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_get_site` | Get SharePoint site metadata | Read |
| `one_drive_get_site_page_content` | Get SharePoint site page content | Read |
| `one_drive_list_site_lists` | List SharePoint lists in a site | Read |
| `one_drive_list_site_subsites` | List subsites of a SharePoint site | Read |
| `one_drive_list_site_columns` | List column definitions for a SharePoint site | Read |
| `one_drive_get_sharepoint_list_items` | Get items from a SharePoint list | Read |
| `one_drive_get_group_drive` | Get the document library for a Microsoft 365 group | Read |

### Download & Conversion

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_download_file` | Download a file by ID (returns S3 URL) | Read |
| `one_drive_download_file_by_path` | Download a file by path | Read |
| `one_drive_download_item_as_format` | Download a file converted to PDF or HTML | Read |
| `one_drive_download_item_version` | Download a specific previous version of a file | Read |

### Following & Activity

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_follow_item` | Follow a file or folder | Write |
| `one_drive_unfollow_item` | Stop following a file or folder | Write |
| `one_drive_get_followed_item` | Get a followed item | Read |
| `one_drive_list_activities` | Get recent activity on the drive | Read |
| `one_drive_list_item_activities` | Get activities for a specific item | Read |

### Sharing URL Resolution

| Tool | Description | Mode |
|------|-------------|------|
| `one_drive_get_drive_item_by_sharing_url` | Resolve a sharing URL to item metadata | Read |
| `one_drive_get_share` | Get a shared item by share ID | Read |

## Code Examples

### List files in a folder

```bash
clawlink_call_tool --tool "one_drive_list_folder_children" \
  --params '{
    "item_id": "FOLDER_ID"
  }'
```

### Search for files

```bash
clawlink_call_tool --tool "one_drive_search_items" \
  --params '{
    "query": "quarterly report",
    "filter": "file neq null"
  }'
```

### Create a sharing link

```bash
clawlink_call_tool --tool "one_drive_create_link" \
  --params '{
    "item_id": "FILE_ID",
    "type": "view",
    "scope": "organization"
  }'
```

### Upload a file

```bash
clawlink_call_tool --tool "one_drive_onedrive_upload_file" \
  --params '{
    "parent_folder_id": "FOLDER_ID",
    "file_name": "document.pdf",
    "file_content": "BASE64_ENCODED_CONTENT"
  }'
```

### Move a file

```bash
clawlink_call_tool --tool "one_drive_move_item" \
  --params '{
    "item_id": "FILE_ID",
    "parent_folder_id": "NEW_FOLDER_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm OneDrive is connected.
2. Call `clawlink_list_tools --integration onedrive` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `onedrive`.
5. If no OneDrive tools appear, direct the user to https://claw-link.dev/dashboard?add=onedrive.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List folder → Get file → Show metadata           │
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

- Item IDs containing `{` and `}` must be URL-encoded (`%7B` and `%7D`) in raw Graph URLs. ClawLink handles this automatically.
- Large file uploads (>4 MB) use chunked upload sessions — do not assume the upload is complete immediately.
- Deleted items are moved to the recycle bin, not permanently deleted, unless using `delete_item_permanently`.
- Sharing links have independent availability — thumbnail URLs are external HTTP endpoints.
- Rate limit errors (HTTP 429) include a `Retry-After` header — use exponential backoff.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration onedrive`. |
| Missing connection | OneDrive is not connected. Direct the user to https://claw-link.dev/dashboard?add=onedrive. |
| `ItemNotFound` | File or folder does not exist. Check the `item_id` or path. |
| `nameAlreadyExists` | A file or folder with that name already exists at the destination. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
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

1. Ensure the integration slug is exactly `onedrive`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Microsoft Graph OneDrive API Overview](https://learn.microsoft.com/en-us/graph/api/resources/onedrive)
- [DriveItem Resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onedrive-files
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Microsoft Excel](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) — For Excel workbook operations
- [Outlook Inbox](https://clawhub.ai/hith3sh/outlook-inbox) — For Outlook email and calendar
- [OneNote Notes](https://clawhub.ai/hith3sh/onenote-notes) — For OneNote notebook operations
- [SharePoint Sites](https://clawhub.ai/hith3sh/sharepoint-sites) — For SharePoint site operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onedrive-files)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
