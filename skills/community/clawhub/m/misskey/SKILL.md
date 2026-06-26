---
name: misskey
description: |
  Misskey API integration for posting notes and uploading media to Misskey/Fediverse instances.
  Use when users want to post to Misskey, upload images, or interact with Fediverse.
  Triggers: "post to misskey", "misskey upload", "fediverse post", "misskey note".
metadata:
  version: "1.0.1"
---

# Misskey API

Post notes and upload images to Misskey/Fediverse instances.

## Configuration

Set environment variables or create a config file:

```bash
# Misskey instance URL
export MISSKEY_HOST="https://your-instance.misskey.io"
# API Token (get from Settings > API)
export MISSKEY_TOKEN="your-token-here"
```

**Getting a Token:**
1. Login to your Misskey instance
2. Go to Settings > API > Access Tokens
3. Create a new token with required permissions

## Popular Misskey Instances

| Instance | URL | Description |
|----------|-----|-------------|
| maid.lat | https://maid.lat | メイド情報局 - A Misskey instance for maid lovers |
| misskey.io | https://misskey.io | Official Misskey instance |
| misskey.design | https://misskey.design | For designers |

## Posting

### Send Text

```bash
MISSKEY_HOST="https://maid.lat" MISSKEY_TOKEN="xxx" \
  bash ~/.openclaw/workspace/skills/misskey/scripts/post.sh "Hello, Fediverse!"
```

### Send with Image

```bash
MISSKEY_HOST="https://maid.lat" MISSKEY_TOKEN="xxx" \
  bash ~/.openclaw/workspace/skills/misskey/scripts/post.sh "Image caption" "/path/to/image.png"
```

### Send Multiple Images

```bash
MISSKEY_HOST="https://maid.lat" MISSKEY_TOKEN="xxx" \
  bash ~/.openclaw/workspace/skills/misskey/scripts/post.sh "Multiple images" "/path/to/img1.png" "/path/to/img2.png"
```

## Upload Image

Upload image to drive separately:

```bash
MISSKEY_HOST="https://maid.lat" MISSKEY_TOKEN="xxx" \
  bash ~/.openclaw/workspace/skills/misskey/scripts/upload.sh "/path/to/image.png"
```

## Visibility Options

Add visibility parameter after text:

```bash
# Public (default)
bash post.sh "Content" --visibility public

# Home timeline only
bash post.sh "Content" --visibility home

# Followers only
bash post.sh "Content" --visibility followers

# Specified users
bash post.sh "Content" --visibility specified --visible-user-ids "user-id"
```

## Content Warning (CW)

```bash
bash post.sh "Hidden content" --cw "Content warning title"
```

## Delete Note

```bash
MISSKEY_HOST="https://maid.lat" MISSKEY_TOKEN="xxx" \
  bash ~/.openclaw/workspace/skills/misskey/scripts/delete.sh "note-id"
```

Get note ID from URL: `https://maid.lat/notes/ak4lrcfalen102bc` → ID is `ak4lrcfalen102bc`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/notes/create | POST | Create note |
| /api/notes/delete | POST | Delete note |
| /api/drive/files/create | POST | Upload file |
| /api/i | POST | Get current user info |

## Error Handling

| Status | Meaning |
|--------|---------|
| 401 | Invalid or expired token |
| 400 | Invalid parameters |
| 429 | Rate limited |

## Scripts

| Script | Description |
|--------|-------------|
| post.sh | Create notes with optional images |
| delete.sh | Delete notes by ID |
| upload.sh | Upload files to drive |
| whoami.sh | Display current user info |
