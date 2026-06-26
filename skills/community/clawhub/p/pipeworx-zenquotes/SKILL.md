---
name: pipeworx-zenquotes
description: Inspirational quotes — random, daily quote of the day, or batch 50 at once from ZenQuotes
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🧘"
    homepage: https://pipeworx.io/packs/zenquotes
---

# ZenQuotes

Inspirational and motivational quotes for any occasion. Pull a single random quote, get the consistent quote of the day, or batch 50 quotes at once for collections and displays.

## Tools

| Tool | Description |
|------|-------------|
| `random_quote` | A single random inspirational quote with author |
| `today_quote` | Quote of the day — same for all users within a given day |
| `list_quotes` | Batch of 50 random quotes in one call |

## When to use

- Starting a meeting or newsletter with an inspiring quote
- "Quote of the day" widgets and notifications
- Building a motivational content feed
- Populating a quotes collection for a journaling app

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/zenquotes/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"random_quote","arguments":{}}}'
```

```json
{
  "quote": "The only way to do great work is to love what you do.",
  "author": "Steve Jobs"
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-zenquotes": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/zenquotes/mcp"]
    }
  }
}
```
