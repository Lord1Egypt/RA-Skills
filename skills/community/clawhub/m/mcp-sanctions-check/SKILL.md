---
name: mcp-sanctions-check
description: Check names against the OFAC SDN (Specially Designated Nationals) sanctions list via MCP. Downloads and caches official SDN CSV, auto-refreshes every 24h. Case-insensitive token matching with optional country filter. Use when agents need compliance screening before financial transactions.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: 🛡️
---

# Sanctions Check (OFAC SDN)

Screen names against the US Treasury OFAC Specially Designated Nationals list.

## Setup

```json
{
  "mcpServers": {
    "sanctions-check": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-sanctions-check"]
    }
  }
}
```

## Tool: `check_sanctions`

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| name      | string | yes      | Name to check against SDN list |
| country   | string | no       | Country to narrow results |

### Example

Check "John Doe" → returns match status, matched entries with type/programs/remarks, and timestamp.

## How It Works

- Downloads official OFAC SDN CSV on first call
- Caches locally, refreshes every 24 hours
- Case-insensitive, token-based matching (handles name variations)
- Returns structured JSON with match boolean, entries array, and check timestamp

## When to Use

- Before processing payments or financial transactions
- Customer onboarding / KYC screening
- Compliance checks for international business
- Charter booking verification (BVI, international waters)
