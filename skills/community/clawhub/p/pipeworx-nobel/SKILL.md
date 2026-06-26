---
name: pipeworx-nobel
description: Nobel Prize laureates and awards — search by name or category and browse prizes by year since 1901
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🏅"
    homepage: https://pipeworx.io/packs/nobel
---

# Nobel Prizes

Over a century of Nobel Prize data. Search laureates by name, filter by category (Physics, Chemistry, Medicine, Literature, Peace, Economics), or list all prizes awarded in a given year.

## Tools

- **`search_laureates`** — Search Nobel laureates by name and optionally filter by category
- **`get_prizes_by_year`** — All Nobel Prizes awarded in a specific year (1901 onward)

## Ideal for

- "Who won the Nobel Peace Prize in 2023?"
- Educational tools about scientific achievement and history
- Research on prize distribution by country, gender, or field
- Trivia and quiz content about Nobel laureates

## Example: search for Einstein

```bash
curl -s -X POST https://gateway.pipeworx.io/nobel/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_laureates","arguments":{"name":"Einstein"}}}'
```

```json
{
  "laureates": [{
    "name": "Albert Einstein",
    "full_name": "Albert Einstein",
    "prizes": [{
      "year": 1921,
      "category": "Physics",
      "motivation": "for his services to Theoretical Physics, and especially for his discovery of the law of the photoelectric effect"
    }]
  }]
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-nobel": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/nobel/mcp"]
    }
  }
}
```
