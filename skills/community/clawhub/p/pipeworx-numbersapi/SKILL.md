---
name: pipeworx-numbersapi
description: NumbersAPI MCP — wraps numbersapi.com (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/numbersapi
---

# pipeworx-numbersapi

NumbersAPI MCP — wraps numbersapi.com (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `number_fact`
- `date_fact`
- `math_fact`
- `random_fact`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-numbersapi": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/numbersapi/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/numbersapi](https://pipeworx.io/packs/numbersapi)
