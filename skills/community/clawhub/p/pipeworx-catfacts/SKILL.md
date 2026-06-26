---
name: pipeworx-catfacts
description: Random cat facts and breed information from the Cat Facts API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🐱"
    homepage: https://pipeworx.io/packs/catfacts
---

# Cat Facts

Did you know cats spend 70% of their lives sleeping? Pull random feline trivia, batch multiple facts, or browse cat breeds with details on country of origin, coat type, and temperament.

## Tools

- **`get_fact`** — One random cat fact
- **`get_facts`** — Multiple random cat facts (default 5)
- **`list_breeds`** — Cat breeds with country, origin, coat, and pattern info

## Great for

- Spicing up a chatbot with fun cat trivia
- Building a "cat fact of the day" notification
- Educational apps about different cat breeds
- Testing or prototyping when you need harmless sample data

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/catfacts/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_facts","arguments":{"count":3}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-catfacts": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/catfacts/mcp"]
    }
  }
}
```
