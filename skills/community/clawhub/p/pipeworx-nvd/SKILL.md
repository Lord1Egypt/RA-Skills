---
name: pipeworx-nvd
description: NVD MCP — wraps the NIST National Vulnerability Database API (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/nvd
---

# pipeworx-nvd

NVD MCP — wraps the NIST National Vulnerability Database API (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_cves`
- `get_cve`
- `recent_cves`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-nvd": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/nvd/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/nvd](https://pipeworx.io/packs/nvd)
