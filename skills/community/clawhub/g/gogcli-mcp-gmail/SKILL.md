---
name: gogcli-mcp-gmail
description: Use when the user asks to read, organize, draft, forward, autoreply, or otherwise work with Gmail in depth. Triggers for requests involving threads, labels, drafts, attachments, bulk archive/trash/mark-read operations, forwarding messages, or any Gmail operation beyond simple search/get/send. Includes auth and Gmail tools only.
---

# gogcli-mcp-gmail

Extended Gmail MCP server via [gogcli](https://github.com/openclaw/gogcli) — 32 tools: auth + 4 base Gmail + 23 extra dedicated Gmail tools.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-gmail": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-gmail"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra Gmail Tools

### Read
| Tool | What it does |
|------|-------------|
| `gog_gmail_raw` | Raw Gmail API JSON for a message |
| `gog_gmail_attachment` | Download a single attachment |
| `gog_gmail_url` | Print web URLs for threads |
| `gog_gmail_history` | List history events since a historyId |

### Threads
| Tool | What it does |
|------|-------------|
| `gog_gmail_thread_get` | Get a thread with all messages |
| `gog_gmail_thread_modify` | Modify labels on a thread |
| `gog_gmail_thread_attachments` | List/download all attachments in a thread |

### Labels
| Tool | What it does |
|------|-------------|
| `gog_gmail_labels_list` | List all labels |
| `gog_gmail_labels_get` | Get a label's details and counts |
| `gog_gmail_labels_create` | Create a new label |
| `gog_gmail_labels_rename` | Rename a label |
| `gog_gmail_labels_delete` | Delete a label |
| `gog_gmail_labels_modify` | Modify labels on one or more threads |

### Bulk operations
| Tool | What it does |
|------|-------------|
| `gog_gmail_archive` | Archive by IDs or query |
| `gog_gmail_mark_read` | Mark read by IDs or query |
| `gog_gmail_mark_unread` | Mark unread by IDs or query |
| `gog_gmail_trash` | Trash by IDs or query |
| `gog_gmail_message_modify` | Modify labels on a single message |
| `gog_gmail_batch_delete` | Permanently delete multiple messages |
| `gog_gmail_batch_modify` | Modify labels on multiple messages |

### Drafts
| Tool | What it does |
|------|-------------|
| `gog_gmail_drafts_list` | List drafts |
| `gog_gmail_drafts_get` | Get a draft |
| `gog_gmail_drafts_create` | Create a draft |
| `gog_gmail_drafts_update` | Update a draft |
| `gog_gmail_drafts_delete` | Delete a draft |
| `gog_gmail_drafts_send` | Send a draft |

### Write
| Tool | What it does |
|------|-------------|
| `gog_gmail_forward` | Forward a message |
| `gog_gmail_autoreply` | Reply once to all messages matching a query |

Plus 5 auth tools and 4 base Gmail tools (search, get, send, run). Use `gog_gmail_run` for advanced settings (`filters`, `delegates`, `forwarding`, `sendas`, `vacation`, `watch`) and email tracking (`track`).
