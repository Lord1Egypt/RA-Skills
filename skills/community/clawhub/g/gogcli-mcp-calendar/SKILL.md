---
name: gogcli-mcp-calendar
description: Use when the user asks to manage Google Calendar events or Google Meet spaces. Triggers for scheduling, listing events, creating/updating/deleting events, responding to invitations, creating Meet spaces, ending conferences, listing meeting participants or call history.
---

# gogcli-mcp-calendar

Extended Google Calendar MCP server via [gogcli](https://github.com/openclaw/gogcli) — 18 tools: auth + 7 base Calendar + 6 extra Meet tools.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-calendar": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-calendar"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra Meet Tools

| Tool | What it does |
|------|-------------|
| `gog_meet_create` | Create a Meet space |
| `gog_meet_get` | Get a Meet space by code |
| `gog_meet_update` | Update Meet space config |
| `gog_meet_end` | End the active conference |
| `gog_meet_history` | List past calls in a space |
| `gog_meet_participants` | List call participants |

Plus 5 auth tools and 7 base Calendar tools (`gog_calendar_events/get/create/update/delete/respond/run`).
