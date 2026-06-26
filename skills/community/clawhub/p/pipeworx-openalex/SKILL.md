---
name: pipeworx-openalex
description: OpenAlex MCP — wraps the OpenAlex API (scholarly works, free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/openalex
---

# pipeworx-openalex

OpenAlex MCP — wraps the OpenAlex API (scholarly works, free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_works`
- `search_authors`
- `search_institutions`
- `get_concept`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-openalex": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/openalex/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/openalex](https://pipeworx.io/packs/openalex)
