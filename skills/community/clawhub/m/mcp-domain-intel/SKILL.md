---
name: mcp-domain-intel
description: Domain intelligence — WHOIS lookups and domain availability checks via L402 API. Use for brand research, cybersecurity investigations, and domain acquisition planning.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
      env:
        - L402_API_BASE_URL
    emoji: 🔍
---

# Domain Intel (L402)

WHOIS lookups and domain availability checks — fast domain intelligence for agents.

## Setup

```json
{
  "mcpServers": {
    "domain-intel": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-domain-intel"],
      "env": {
        "L402_API_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

## Tools

### `whois_lookup`
Full WHOIS/DNS intelligence for a domain.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| domain    | string | yes      | Domain to look up |

### `check_availability`
Check if a domain is available for registration.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| domain    | string | yes      | Domain to check |

## When to Use

- Brand protection and monitoring
- Domain acquisition research
- Cybersecurity investigations
- Competitor analysis
