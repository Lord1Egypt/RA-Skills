---
name: pipeworx-advice
description: Crowdsourced life advice — search, browse, or grab a random slip of wisdom from the Advice Slip API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "💡"
    homepage: https://pipeworx.io/packs/advice
---

# Advice Slip

Sometimes you just need a nudge in the right direction. This pack taps the Advice Slip API — a crowd-curated collection of short, practical life advice — and lets you pull random slips, search by topic, or fetch a specific one by ID.

## Tools

| Tool | What it does |
|------|-------------|
| `random_advice` | Returns a single random piece of advice |
| `search_advice` | Full-text search across all advice slips by keyword |
| `get_advice` | Retrieve a specific advice slip by its numeric ID |

## When to reach for this

- A user asks for motivation or a pick-me-up during a conversation
- Building a "tip of the day" widget or notification
- Searching for advice on a specific topic like "money", "friendship", or "patience"
- Populating placeholder content with real human-written sentences

## Quick example

Searching for advice about sleep:

```bash
curl -s -X POST https://gateway.pipeworx.io/advice/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_advice","arguments":{"query":"sleep"}}}'
```

Response shape:

```json
{
  "total_results": 3,
  "slips": [
    { "id": 87, "advice": "Get enough sleep." },
    { "id": 143, "advice": "Don't use your phone before bed..." }
  ]
}
```

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-advice": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/advice/mcp"]
    }
  }
}
```

## Good to know

- The API caches random results for 2 seconds, so rapid consecutive calls to `random_advice` may return the same slip
- Search is case-insensitive and matches partial words
- No auth needed, free for everyone
