---
name: pipeworx-jokes
description: Jokes MCP — wraps JokeAPI v2 (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/jokes
---

# pipeworx-jokes

Jokes MCP — wraps JokeAPI v2 (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_joke`
- `search_jokes`
- `get_joke_categories`
- `get_joke_flags`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-jokes": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/jokes/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/jokes](https://pipeworx.io/packs/jokes)
