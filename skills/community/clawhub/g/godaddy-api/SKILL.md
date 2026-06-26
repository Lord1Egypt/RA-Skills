---
name: godaddy
description: Complete GoDaddy API skill with shell scripts + MCP server for domains, DNS, certificates, shoppers, subscriptions, agreements, countries, and aftermarket listings.
homepage: https://developer.godaddy.com/doc
metadata: {"openclaw": {"emoji": "🌐", "requires": {"bins": ["bash", "curl", "jq", "node", "npm"]}}}
---

# GoDaddy API

## Setup

```bash
export GODADDY_API_BASE_URL="https://api.godaddy.com"  # or https://api.ote-godaddy.com
export GODADDY_API_KEY="your-key"
export GODADDY_API_SECRET="your-secret"
```

Keys: <https://developer.godaddy.com/keys>

## Shell scripts

- `scripts/gd-domains.sh` — list/get/availability, validate purchase, purchase, renew, transfer, update, update contacts, delete, privacy on/off, domain agreements get/accept
- `scripts/gd-dns.sh` — get all/type/name, patch add, replace all/type/type+name, delete type+name
- `scripts/gd-certs.sh` — create/validate/get/actions/download/renew/reissue/revoke/verify domain control
- `scripts/gd-shoppers.sh` — get/update/delete shopper
- `scripts/gd-subscriptions.sh` — list/get/cancel subscription
- `scripts/gd-agreements.sh` — list legal agreements
- `scripts/gd-countries.sh` — list countries
- `scripts/gd-aftermarket.sh` — list/get aftermarket listings

Destructive/financial actions prompt for confirmation.

## MCP server

Path: `scripts/mcp-server/`

```bash
cd scripts/mcp-server
npm install
npm run build
node dist/index.js
```

Exposes MCP tools for all skill operations (domains, DNS, certs, shoppers, subscriptions, agreements, countries, aftermarket).

Example MCP config:

```json
{
  "mcpServers": {
    "godaddy": {
      "command": "node",
      "args": ["path/to/mcp-server/dist/index.js"],
      "env": {
        "GODADDY_API_BASE_URL": "https://api.godaddy.com",
        "GODADDY_API_KEY": "",
        "GODADDY_API_SECRET": ""
      }
    }
  }
}
```

## References

- `references/endpoints.md` — complete endpoint map
- `references/auth-and-env.md` — auth/env setup
- `references/request-bodies.md` — payload examples
- `references/error-handling.md` — troubleshooting
- `references/safety-playbook.md` — safe operation patterns
