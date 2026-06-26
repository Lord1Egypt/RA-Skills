---
name: otto-travel-local
description: OpenClaw plugin for Otto Travel — search, compare, and book flights and hotels via Otto's MCP endpoint.
---

# Otto Travel Local

OpenClaw plugin for Otto Travel — search, compare, and book flights and hotels via Otto's MCP endpoint.

## Install

`openclaw plugins install ./openclaw-otto-travel`

## Configuration

In your `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "openclaw-otto-travel": {
        "config": {
          "serverUrl": "https://api.ottotheagent.com/mcp"
        }
      }
    }
  }
}
```

## Tools

Tools are discovered dynamically from the MCP server:

- `search_flights` / `book_flight`
- `search_hotels` / `book_hotel`
- `get_bookings`
- Preference and loyalty program management

## Security

Uses OAuth 2.1; tokens stored securely at `~/.openclaw/.otto-tokens.json`.
