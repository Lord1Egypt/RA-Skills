---
name: pipeworx-dns
description: DNS record lookups via Google DNS-over-HTTPS — A, AAAA, MX, NS, TXT, CNAME, and reverse DNS
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🔍"
    homepage: https://pipeworx.io/packs/dns
---

# DNS Lookup

Query DNS records for any domain using Google's DNS-over-HTTPS service. Supports all common record types (A, AAAA, MX, NS, TXT, CNAME) plus batch multi-type lookups and reverse DNS.

## Tools

- **`dns_lookup`** — Query a specific record type for a domain (e.g., MX records for "gmail.com")
- **`dns_lookup_all`** — Query A, AAAA, MX, NS, TXT, and CNAME all at once for a domain
- **`reverse_dns`** — Reverse-lookup an IPv4 address to find its hostname (e.g., "8.8.8.8" -> "dns.google")

## When this helps

- Debugging email delivery issues by checking MX records
- Verifying DNS propagation after making changes
- Checking if a domain has SPF/DKIM/DMARC records (TXT)
- Identifying what server an IP address belongs to via reverse DNS
- Auditing a domain's complete DNS configuration

## Example: check MX records for gmail.com

```bash
curl -s -X POST https://gateway.pipeworx.io/dns/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"dns_lookup","arguments":{"domain":"gmail.com","type":"MX"}}}'
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-dns": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dns/mcp"]
    }
  }
}
```
