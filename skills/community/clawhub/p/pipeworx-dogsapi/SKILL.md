---
name: pipeworx-dogsapi
description: Detailed dog breed encyclopedia — weight ranges, life spans, temperament, and breed groups from dogapi.dog
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🐶"
    homepage: https://pipeworx.io/packs/dogsapi
---

# Dogs API — Breed Encyclopedia

A structured database of dog breeds with detailed attributes: weight ranges, life spans, hypoallergenic status, temperament descriptions, and breed group classifications. Also includes random dog facts.

## Tools

- **`list_breeds`** — Paginated list of breeds with weight, life span, and hypoallergenic flag
- **`get_breed`** — Full details for a specific breed by ID
- **`list_facts`** — Random dog facts (default 10, max 100)
- **`get_groups`** — All breed groups (Sporting, Herding, Terrier, etc.)

## Use cases

- "Is a Poodle hypoallergenic?" — look up the breed and check the flag
- Building a breed comparison tool for prospective dog owners
- Enriching a pet adoption platform with breed data
- Fun facts for a pet-themed chatbot or newsletter

## Example: browse breeds

```bash
curl -s -X POST https://gateway.pipeworx.io/dogsapi/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_breeds","arguments":{"page":1}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-dogsapi": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dogsapi/mcp"]
    }
  }
}
```
