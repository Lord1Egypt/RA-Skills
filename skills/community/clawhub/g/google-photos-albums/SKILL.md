---
name: google-photos-albums
description: Google Photos Library API integration with managed OAuth. Upload media, search photos, create and manage albums, and update media items. Use this skill when users want to manage their Google Photos library, create albums, or upload media.
---

# Google Photos

![Google Photos](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/googlephotos.svg?v=2)

Access Google Photos via the Google Photos Library API with managed OAuth authentication. Upload media, search photos, create and manage albums, and update media items.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-photos-albums) for hosted connection flows and credentials so you do not need to configure Google Photos API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Photos |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Photos |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Photos  │
│   (User Chat)   │     │   (OAuth)    │     │   (Photos API)   │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Photos    │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Photos  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Photos again."

## Quick Start

```bash
# List albums
clawlink_call_tool --tool "googlephotos_list_albums" --params '{}'

# List media items
clawlink_call_tool --tool "googlephotos_list_media_items" --params '{"page_size": 50}'

# Create an album
clawlink_call_tool --tool "googlephotos_create_album" --params '{"album_title": "Vacation Photos"}'
```

## Authentication

All Google Photos tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Photos API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=googlephotos and connect Google Photos.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `googlephotos` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration googlephotos
```

**Response:** Returns the live tool catalog for Google Photos.

### Reconnect

If Google Photos tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=googlephotos
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration googlephotos`

## Security & Permissions

- Access is scoped to media items and albums within the connected Google Photos account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Uploads and album changes must always be confirmed by the user.

## Important API Limitation

**As of March 31, 2025**, the Google Photos Library API only returns media items that were **uploaded or created by this application**. It cannot access photos taken by the user's camera or uploaded from other apps. For accessing the user's full photo library, use the [Google Photos Picker API](https://developers.google.com/photos/picker) instead.

## Tool Reference

### Album Management

| Tool | Description | Mode |
|------|-------------|------|
| `googlephotos_list_albums` | List all albums shown in the user's Albums tab | Read |
| `googlephotos_get_album` | Get a specific album by its ID | Read |
| `googlephotos_create_album` | Create a new album with a title | Write |
| `googlephotos_update_album` | Update an album's title or cover photo | Write |

### Media Item Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlephotos_list_media_items` | List media items created by this application | Read |
| `googlephotos_search_media_items` | Search media items in the user's library | Read |
| `googlephotos_batch_get_media_items` | Get specific media items by their IDs | Read |
| `googlephotos_get_media_item_download` | Download a media item as a file | Read |
| `googlephotos_update_media_item` | Update a media item's description | Write |

### Upload Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlephotos_upload_media` | Upload an image (up to 200MB) or video (up to 20GB) | Write |
| `googlephotos_batch_create_media_items` | Batch upload and create media items (up to 50 per request) | Write |

### Album Content Management

| Tool | Description | Mode |
|------|-------------|------|
| `googlephotos_batch_add_media_items` | Add existing media items to an album | Write |
| `googlephotos_add_enrichment` | Add an enrichment (text, location, etc.) at a position in an album | Write |

## Code Examples

### List all albums

```bash
clawlink_call_tool --tool "googlephotos_list_albums" \
  --params '{
    "page_size": 50
  }'
```

### List media items

```bash
clawlink_call_tool --tool "googlephotos_list_media_items" \
  --params '{
    "page_size": 100
  }'
```

### Create an album

```bash
clawlink_call_tool --tool "googlephotos_create_album" \
  --params '{
    "album_title": "Summer Vacation 2024"
  }'
```

### Batch upload media items from URLs

```bash
clawlink_call_tool --tool "googlephotos_batch_create_media_items" \
  --params '{
    "album_id": "YOUR_ALBUM_ID",
    "media_files": [
      {"url": "https://example.com/photo1.jpg", "file_name": "beach_sunset.jpg", "description": "Beautiful sunset at the beach"},
      {"url": "https://example.com/photo2.jpg", "file_name": "mountain_view.jpg", "description": "View from the mountain top"}
    ]
  }'
```

### Add media items to an album

```bash
clawlink_call_tool --tool "googlephotos_batch_add_media_items" \
  --params '{
    "album_id": "YOUR_ALBUM_ID",
    "media_item_ids": ["MEDIA_ITEM_ID_1", "MEDIA_ITEM_ID_2"]
  }'
```

### Update a media item description

```bash
clawlink_call_tool --tool "googlephotos_update_media_item" \
  --params '{
    "media_item_id": "YOUR_MEDIA_ITEM_ID",
    "description": "Updated description for this photo"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Photos is connected.
2. Call `clawlink_list_tools --integration googlephotos` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `googlephotos`.
5. If no Google Photos tools appear, direct the user to https://claw-link.dev/dashboard?add=googlephotos.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → call                                 │
│                                                             │
│  Example: List albums → Get album → Show results            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview → User approves            │
│           → Execute upload or update                         │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer list, search, and read operations before writes.
4. For uploads, album changes, or media item updates, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Media items created via the API are only visible to the app that created them, not in the user's main Google Photos UI.
- To display photos in the user's main Photos UI, the user must upload them through the Google Photos app directly.
- Batch upload supports up to 50 items per request via URLs or pre-uploaded files.
- Videos up to 20GB are supported for upload.
- Album enrichment adds contextual content (text, location pins) to albums.
- Media item IDs should be captured from creation or list responses for subsequent operations.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration googlephotos`. |
| Missing connection | Google Photos is not connected. Direct the user to https://claw-link.dev/dashboard?add=googlephotos. |
| `NOT_FOUND` | Album or media item does not exist. Check the ID. |
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

1. Ensure the integration slug is exactly `googlephotos`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Photos Library API Overview](https://developers.google.com/photos/library/guides/overview)
- [Media Items Reference](https://developers.google.com/photos/library/reference/rest/v1/mediaItems)
- [Albums Reference](https://developers.google.com/photos/library/reference/rest/v1/albums)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-photos-albums
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-photos-albums)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)