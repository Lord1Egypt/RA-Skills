# openclaw-otto-travel

OpenClaw plugin for Otto Travel — search, compare, and book flights and hotels via Otto's MCP endpoint.

## Install

```bash
openclaw plugins install ./openclaw-otto-travel
```

## First Run

On first use, the plugin runs an OAuth Device Authorization flow:

1. A URL and code are printed to your terminal
2. Visit the URL and enter the code
3. Log in to your Otto account and approve
4. The plugin stores tokens locally at `~/.openclaw/.otto-tokens.json`

Subsequent runs use the stored tokens. Refresh is automatic.

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

`serverUrl` defaults to `https://api.ottotheagent.com/mcp` if omitted.

## Tools

Tools are discovered dynamically from the MCP server. Currently available:

- `read_skill` — Read a skill guide (required before using other tools)
- `search_flights` — Search flights by route and date
- `query_flights` — Query search results with SQL
- `book_flight` — Book a flight
- `search_hotels` — Search hotels by location
- `get_hotel_rooms` — Get room options for a hotel
- `book_hotel` — Book a hotel room
- `get_bookings` — View your bookings
- `read_preferences` / `write_preference` — Manage travel preferences
- `read_loyalty_programs` / `write_loyalty_program` — Manage loyalty programs

## Architecture

```
OpenClaw Gateway
  └─ otto-travel plugin (this repo)
       └─ StreamableHTTP → https://api.ottotheagent.com/mcp
            with Authorization: Bearer <oauth_token>
```

No stdio proxy. No API keys. Direct HTTP with OAuth 2.1.
