---
name: gogcli-mcp-drive
description: Use when the user asks to browse, upload, download, share, or manage Google Drive files and folders. Triggers for requests involving Drive uploads/downloads, file permissions, shared drives (Team Drives), comments on files, copying or moving files, or any Drive operation. Includes auth and Drive tools only.
---

# gogcli-mcp-drive

Extended Google Drive MCP server via [gogcli](https://github.com/openclaw/gogcli) — 27 tools: auth + 9 base Drive + 13 extra dedicated Drive tools.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-drive": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-drive"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra Drive Tools

| Tool | What it does |
|------|-------------|
| `gog_drive_download` | Download a file (Google Docs → pdf/docx/xlsx/etc.) |
| `gog_drive_upload` | Upload a local file, replace existing, or convert to Google format |
| `gog_drive_copy` | Copy a file to a new file |
| `gog_drive_url` | Print shareable URLs for one or more files |
| `gog_drive_permissions` | List permissions on a file |
| `gog_drive_unshare` | Remove a permission |
| `gog_drive_drives_list` | List shared drives (Team Drives) |
| `gog_drive_comments_list` | List comments on a file |
| `gog_drive_comments_get` | Get a comment by ID |
| `gog_drive_comments_add` | Add a new comment |
| `gog_drive_comments_update` | Edit a comment |
| `gog_drive_comments_delete` | Delete a comment |
| `gog_drive_comments_reply` | Reply to a comment |

Plus 5 auth tools and 9 base Drive tools (ls, search, get, mkdir, rename, move, delete, share, run).
