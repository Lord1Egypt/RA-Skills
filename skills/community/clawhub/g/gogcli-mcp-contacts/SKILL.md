---
name: gogcli-mcp-contacts
description: Use when the user asks to look up, search, or manage Google Contacts and the broader People API (Workspace directory). Triggers for contact lookups by name/email/phone, Workspace user search, profile fields, manager/reports relations, or any People API query.
---

# gogcli-mcp-contacts

Extended Google Contacts MCP server via [gogcli](https://github.com/openclaw/gogcli) — 15 tools: auth + 5 base Contacts + 5 extra People API tools.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-contacts": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-contacts"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra People Tools

| Tool | What it does |
|------|-------------|
| `gog_people_me` | Show your own profile |
| `gog_people_get` | Get a profile by resource name |
| `gog_people_search` | Search the Workspace directory |
| `gog_people_relations` | Manager/reports relations |
| `gog_people_raw` | Raw People API JSON dump |

Plus 5 auth tools and 5 base Contacts tools (`gog_contacts_search/list/get/create/run`). The base `gog_contacts_search` only sees your personal contacts; use `gog_people_search` for the full Workspace directory.
