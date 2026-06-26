---
name: mcp-company-search
description: Search corporate registries across multiple jurisdictions via L402 API. Find companies by name and jurisdiction for due diligence, compliance, and business research.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
      env:
        - L402_API_BASE_URL
    emoji: 🏢
---

# Company Search (L402)

Search corporate registries across jurisdictions — find companies by name for due diligence and compliance.

## Setup

```json
{
  "mcpServers": {
    "company-search": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-company-search"],
      "env": {
        "L402_API_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

## Tools

### `search_companies`
Search companies by name within a jurisdiction.

| Parameter    | Type   | Required | Description |
|-------------|--------|----------|-------------|
| name        | string | yes      | Company name to search |
| jurisdiction| string | yes      | Jurisdiction code |

### `list_jurisdictions`
List all supported jurisdictions and their codes.

## When to Use

- KYC / due diligence checks
- Business partner verification
- Compliance research
- Corporate registry lookups
