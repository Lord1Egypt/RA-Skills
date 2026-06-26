---
name: pipeworx-chucknorris
description: Chuck Norris jokes — random, by category, or keyword search from chucknorris.io
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "👊"
    homepage: https://pipeworx.io/packs/chucknorris
---

# Chuck Norris Jokes

The internet's definitive Chuck Norris joke database. Pull random jokes, search by keyword, browse categories, or get a joke from a specific category like "dev", "science", or "sport".

## Tools

- **`random_joke`** — A random Chuck Norris joke
- **`search_jokes`** — Search jokes containing a keyword
- **`list_categories`** — All available joke categories
- **`joke_by_category`** — Random joke from a specific category

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/chucknorris/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"joke_by_category","arguments":{"category":"dev"}}}'
```

```json
{
  "id": "elgv2wkvt8ioag6xywykbq",
  "value": "Chuck Norris writes code that optimizes itself.",
  "categories": ["dev"]
}
```

## Categories

animal, career, celebrity, dev, explicit, fashion, food, history, money, movie, music, political, religion, science, sport, travel

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-chucknorris": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/chucknorris/mcp"]
    }
  }
}
```
