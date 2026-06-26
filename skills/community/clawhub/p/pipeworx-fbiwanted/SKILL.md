---
name: pipeworx-fbiwanted
description: Search the FBI's Most Wanted list — fugitives, missing persons, and wanted individuals with photos and case details
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🔎"
    homepage: https://pipeworx.io/packs/fbiwanted
---

# FBI Wanted

Access the FBI's official Wanted persons database. Search by name, crime type, or browse the full list. Each record includes photos, physical descriptions, charges, reward information, and case details.

## Tools

- **`search_wanted`** — Search the FBI Wanted list by keyword (name, crime type, description). Omit the keyword to browse all entries with pagination.
- **`get_wanted_person`** — Full details for a specific person by their unique identifier (UID).

## When to use

- Answering questions about FBI wanted fugitives or missing persons
- Building a crime awareness application with official data
- Journalism research on specific cases or crime categories
- Educational tools about law enforcement and criminal justice

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/fbiwanted/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_wanted","arguments":{"query":"cyber","page":1}}}'
```

Returns matching entries with title, description, charges, reward, images, and status.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-fbiwanted": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/fbiwanted/mcp"]
    }
  }
}
```
