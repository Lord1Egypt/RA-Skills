---
name: google-drive-files
description: Google Drive API integration with managed OAuth. Search Drive files, manage permissions, organize folders, upload and download files, and handle sharing changes. Use this skill when users want to find, organize, share, or move files in Google Drive.
---

# Google Drive

![Google Drive](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-drive.svg)

Access Google Drive via the Google Drive API with managed OAuth authentication. Search files, manage permissions, organize folders, upload and download, and handle sharing changes.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-drive-files) for hosted connection flows and credentials so you do not need to configure Google Drive API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Drive |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Drive |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Drive   │
│   (User Chat)   │     │   (OAuth)    │     │   (Drive API)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Drive     │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Drive   │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Drive again."

## Quick Start

```bash
# Find a file by name
clawlink_call_tool --tool "googledrive_find_file" --params '{"query": "report.xlsx"}'

# Get file metadata
clawlink_call_tool --tool "googledrive_get_file_metadata" --params '{"file_id": "YOUR_FILE_ID"}'

# List permissions
clawlink_call_tool --tool "googledrive_list_permissions" --params '{"file_id": "YOUR_FILE_ID"}'
```

## Authentication

All Google Drive tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Drive API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-drive and connect Google Drive.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-drive` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-drive
```

**Response:** Returns the live tool catalog for Google Drive.

### Reconnect

If Google Drive tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-drive
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-drive`

## Security & Permissions

- Access is scoped to files and folders within the connected Google account (My Drive and shared drives).
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete, empty trash, delete permission) are marked as high-impact and must be confirmed.
- Permission changes may have a brief propagation delay before appearing in results.

## Tool Reference

### File & Folder Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_find_file` | Search files by name, MIME type, date, query string, and more | Read |
| `googledrive_find_folder` | Find a folder by name and optional parent folder | Read |
| `googledrive_list_children_v2` | List immediate children of a folder | Read |
| `googledrive_get_file_metadata` | Get file metadata (MIME type, parents, trashed status) | Read |
| `googledrive_list_shared_drives` | List all accessible shared drives | Read |
| `googledrive_get_drive` | Get a specific shared drive's metadata | Read |
| `googledrive_get_about` | Get user info, storage quota, and Drive capabilities | Read |

### File Creation & Upload

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_create_file` | Create an empty file or folder (content added separately) | Write |
| `googledrive_create_file_from_text` | Create a file from text content (up to 10MB) with optional format conversion | Write |
| `googledrive_create_folder` | Create a new folder (parent must already exist) | Write |
| `googledrive_upload_file` | Upload a binary file up to 5MB to a folder | Write |
| `googledrive_upload_from_url` | Fetch a file from a URL and upload to Drive server-side | Write |
| `googledrive_resumable_upload` | Start and complete a resumable upload session for large files | Write |
| `googledrive_upload_update_file` | Replace contents of an existing file | Write |
| `googledrive_edit_file` | Overwrite binary file content (not for Google Workspace files) | Write |

### Download & Export

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_download_file` | Download a file by ID, optionally export Google Workspace files | Read |
| `googledrive_download_file_operation` | Download via long-running operation (for Google Vids, large files) | Read |
| `googledrive_export_google_workspace_file` | Export a Google Doc/Sheet/Slide to a specified MIME type | Read |

### File Organization

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_move_file` | Move a file between folders (supply both add_parents and remove_parents) | Write |
| `googledrive_copy_file_advanced` | Copy a file with advanced options (labels, visibility, metadata) | Write |
| `googledrive_add_parent` | Add a parent folder to a file | Write |
| `googledrive_delete_parent` | Remove a file from a folder | Write |
| `googledrive_insert_child` | Add an existing file to a folder | Write |
| `googledrive_delete_child` | Remove a file from a specific folder | Write |
| `googledrive_create_shortcut_to_file` | Create a shortcut to an existing Drive item | Write |

### File Metadata & Properties

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_update_file_metadata_patch` | Update file metadata (name, description, labels) using PATCH | Write |
| `googledrive_update_file_put` | Update file metadata using PUT semantics (partial update) | Write |
| `googledrive_add_property` | Add or update a custom key-value property on a file | Write |
| `googledrive_patch_property` | Partially update a file property | Write |
| `googledrive_update_file_property` | Update an existing file property | Write |
| `googledrive_get_file_property` | Get a specific custom property from a file | Read |
| `googledrive_list_file_properties` | List all custom properties on a file | Read |
| `googledrive_delete_property` | Delete a property from a file | Write |
| `googledrive_modify_file_labels` | Add, update, or remove labels on a file | Write |
| `googledrive_list_file_labels` | List labels applied to a file | Read |

### Permissions & Sharing

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_create_permission` | Share a file or folder with users, groups, domains, or publicly | Write |
| `googledrive_update_permission` | Update an existing permission | Write |
| `googledrive_patch_permission` | Partially update a permission | Write |
| `googledrive_delete_permission` | Revoke access from a file (including link-sharing) | Write |
| `googledrive_list_permissions` | List all permissions on a file or shared drive | Read |
| `googledrive_get_permission` | Get a specific permission by ID | Read |
| `googledrive_get_permission_id_for_email` | Convert an email address to a permission ID | Read |
| `googledrive_list_access_proposals` | List pending access proposals on a file | Read |
| `googledrive_list_approvals` | List approval workflow approvals on a file | Read |

### Comments & Replies

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_create_comment` | Create a comment on a file | Write |
| `googledrive_list_comments` | List all comments on a file | Read |
| `googledrive_get_comment` | Get a specific comment by ID | Read |
| `googledrive_update_comment` | Update a comment's content | Write |
| `googledrive_delete_comment` | Permanently delete a comment thread and all replies | Write |
| `googledrive_create_reply` | Reply to an existing comment | Write |
| `googledrive_list_replies` | List replies to a comment | Read |
| `googledrive_get_reply` | Get a specific reply | Read |
| `googledrive_update_reply` | Update a reply | Write |
| `googledrive_delete_reply` | Delete a specific reply | Write |

### Shared Drives

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_create_drive` | Create a new shared drive | Write |
| `googledrive_update_drive` | Update shared drive metadata (name, theme, restrictions) | Write |
| `googledrive_delete_drive` | Permanently delete a shared drive | Write |
| `googledrive_hide_drive` | Hide a shared drive from the default view | Write |
| `googledrive_unhide_drive` | Restore a shared drive to the default view | Write |

### Revision Management

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_list_revisions` | List a file's revision metadata | Read |
| `googledrive_get_revision` | Get a specific revision's metadata | Read |
| `googledrive_update_file_revision_metadata` | Update revision metadata (keepForever, published) | Write |
| `googledrive_delete_revision` | Permanently delete a file revision | Write |

### Trash & Deletion

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_trash_file` | Move a file to trash (soft delete, recoverable) | Write |
| `googledrive_untrash_file` | Restore a file from trash | Write |
| `googledrive_google_drive_delete_folder_or_file_action` | Permanently delete a file or folder | Write |
| `googledrive_empty_trash` | Permanently delete ALL trashed files (irreversible) | Write |

### Change Tracking

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_get_changes_start_page_token` | Get the starting token for listing future changes | Read |
| `googledrive_list_changes` | List file changes since a page token | Read |
| `googledrive_watch_changes` | Subscribe to push notifications for Drive changes | Write |
| `googledrive_watch_file` | Subscribe to push notifications for a specific file | Write |
| `googledrive_stop_watch_channel` | Stop an active watch channel | Write |

### Utility

| Tool | Description | Mode |
|------|-------------|------|
| `googledrive_generate_ids` | Pre-allocate file IDs for new files or copies | Read |
| `googledrive_get_app` | Get information about a Drive app by ID | Read |
| `googledrive_get_child` | Verify a specific child exists in a folder | Read |
| `googledrive_get_parent` | Get a specific parent reference for a file | Read |

## Code Examples

### Search for files by name

```bash
clawlink_call_tool --tool "googledrive_find_file" \
  --params '{
    "query": "name contains '\''report'\''"
  }'
```

### Create a folder

```bash
clawlink_call_tool --tool "googledrive_create_folder" \
  --params '{
    "name": "Project Files",
    "parent_folder_id": "YOUR_FOLDER_ID"
  }'
```

### Share a file with someone

```bash
clawlink_call_tool --tool "googledrive_create_permission" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "type": "user",
    "email": "colleague@example.com",
    "role": "writer",
    "pending_owner": false
  }'
```

### Move a file to a folder

```bash
clawlink_call_tool --tool "googledrive_move_file" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "add_parents": ["DESTINATION_FOLDER_ID"],
    "remove_parents": ["SOURCE_FOLDER_ID"]
  }'
```

### Download and export a Google Sheet as CSV

```bash
clawlink_call_tool --tool "googledrive_download_file" \
  --params '{
    "file_id": "YOUR_SHEET_ID",
    "mime_type": "text/csv"
  }'
```

### Trash a file

```bash
clawlink_call_tool --tool "googledrive_trash_file" \
  --params '{
    "file_id": "YOUR_FILE_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Drive is connected.
2. Call `clawlink_list_tools --integration google-drive` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-drive`.
5. If no Google Drive tools appear, direct the user to https://claw-link.dev/dashboard?add=google-drive.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  find → list → get → describe → call                        │
│                                                             │
│  Example: Find file → Get metadata → Show results           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer search, list, and metadata reads before writes.
4. For uploads, sharing updates, folder changes, or other high-impact actions, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- File IDs are stable across moves — capture from list/search responses for subsequent operations.
- `storageQuota` in `get_about` reflects My Drive only, not shared drives.
- Concurrent permission operations on the same file are not supported — only the last update is applied.
- For Google Workspace native files (Docs, Sheets, Slides), use the dedicated API tools (googledocs_*, googlesheets_*) rather than GOOGLEDRIVE_EDIT_FILE.
- Empty trash is irreversible — always confirm with the user first.
- Newly created files are private by default — set sharing permissions afterward.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-drive`. |
| Missing connection | Google Drive is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-drive. |
| `RESOURCE_NOT_FOUND` | File or folder does not exist. Check the file_id or path. |
| `PERMISSION_DENIED` | No access to the file. Check sharing permissions. |
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

1. Ensure the integration slug is exactly `google-drive`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Drive API Overview](https://developers.google.com/drive/api/v3/about)
- [Files Resource](https://developers.google.com/drive/api/v3/reference/files)
- [Permissions Resource](https://developers.google.com/drive/api/v3/reference/permissions)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-drive-files
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Docs](https://clawhub.ai/hith3sh/google-docs-documents) — For document reading and editing
- [Google Sheets](https://clawhub.ai/hith3sh/google-sheets-spreadsheets) — For spreadsheet operations
- [Google Slides](https://clawhub.ai/hith3sh/google-slides-presentations) — For presentation operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-drive-files)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)