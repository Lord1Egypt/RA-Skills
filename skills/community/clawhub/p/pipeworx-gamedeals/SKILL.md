---
name: pipeworx-gamedeals
description: PC game deals from 30+ stores — search sales, compare prices, and track cheapest-ever prices via CheapShark
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🎮"
    homepage: https://pipeworx.io/packs/gamedeals
---

# Game Deals (CheapShark)

Find the best PC game deals across 30+ digital storefronts including Steam, GOG, Humble Bundle, and Epic. Search by title, filter by price range, sort by savings percentage, and compare prices across stores for any game.

## Tools

| Tool | Description |
|------|-------------|
| `search_deals` | Search current deals with filters: title, max/min price, store, sort order |
| `search_games` | Search games by title and see the cheapest current price across all stores |
| `get_game_details` | Price history and current deals across all stores for a specific game |
| `list_stores` | All supported digital storefronts with IDs |

## When to use

- "What are the best game deals under $5 right now?"
- Checking if a specific game is on sale anywhere
- Comparing prices across Steam, GOG, and other stores
- Building a game deal alert system

## Example: deals under $5 sorted by savings

```bash
curl -s -X POST https://gateway.pipeworx.io/gamedeals/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_deals","arguments":{"upperPrice":5,"sortBy":"Savings","limit":5}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-gamedeals": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/gamedeals/mcp"]
    }
  }
}
```
