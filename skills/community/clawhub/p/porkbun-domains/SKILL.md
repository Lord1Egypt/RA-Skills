---
name: porkbun-domains
description: Manage domains and DNS via the Porkbun API. Use when asked to list domains, check domain availability, manage DNS records (A, AAAA, CNAME, MX, TXT, etc.), update nameservers, set up URL forwarding, retrieve SSL certificates, check pricing, or toggle auto-renew. Covers all Porkbun API v3 endpoints. NOT for other registrars (Cloudflare, Namecheap, GoDaddy). Requires PORKBUN_API_KEY and PORKBUN_SECRET_KEY in env or workspace .env file.
---

# Porkbun Domains & DNS

Manage domains and DNS records via the Porkbun API v3.

## Setup

API keys: `PORKBUN_API_KEY` and `PORKBUN_SECRET_KEY` in environment or `~/.openclaw/workspace/.env`.

Get keys at: https://porkbun.com/account/api

## Shell Script

All operations via `scripts/porkbun.sh`. Run with `bash <skill-dir>/scripts/porkbun.sh <command>`.

### Domain Commands

```bash
porkbun.sh ping                    # Test API connection
porkbun.sh list                    # List all domains (status, expiry, auto-renew)
porkbun.sh check example.com       # Check availability + pricing
porkbun.sh ns example.com          # Get current nameservers
porkbun.sh ns-update example.com ns1.cf.com ns2.cf.com  # Update nameservers
porkbun.sh auto-renew example.com on|off
porkbun.sh pricing                 # All TLD pricing (no auth needed)
```

### DNS Commands

```bash
porkbun.sh dns-list example.com                        # List all records
porkbun.sh dns-create example.com A @ 76.76.21.21 600  # Create A record
porkbun.sh dns-create example.com CNAME www cname.vercel-dns.com
porkbun.sh dns-create example.com MX @ mail.example.com 300
porkbun.sh dns-create example.com TXT @ "v=spf1 include:_spf.google.com ~all"
porkbun.sh dns-delete example.com <record-id>
porkbun.sh dns-delete-type example.com A www            # Delete by type+name
```

### URL Forwarding

```bash
porkbun.sh forward-add example.com https://target.com          # Root forward
porkbun.sh forward-add example.com https://target.com www      # Subdomain
porkbun.sh forward-add example.com https://target.com "" permanent
porkbun.sh forward-list example.com
porkbun.sh forward-delete example.com <id>
```

### SSL

```bash
porkbun.sh ssl example.com         # Retrieve SSL cert bundle
```

## Common Workflows

### Point domain to Vercel
```bash
porkbun.sh dns-create example.com A @ 76.76.21.21
porkbun.sh dns-create example.com CNAME www cname.vercel-dns.com
```

### Point domain to Cloudflare (DNS proxy)
```bash
porkbun.sh ns-update example.com adam.ns.cloudflare.com betty.ns.cloudflare.com
```

### Redirect domain to another
```bash
porkbun.sh forward-add old-domain.com https://new-domain.com "" permanent
```

## API Details

- Base URL: `https://api.porkbun.com/api/json/v3`
- All requests: HTTP POST with JSON body containing `apikey` + `secretapikey`
- Rate limits apply — avoid tight loops, serialize requests
- Domain registration via API is supported but use the dashboard for purchases
- `.de` domains do not support WHOIS privacy (DENIC limitation)

## Response Parsing

All responses include `"status": "SUCCESS"` or `"status": "ERROR"`. Parse with `jq`:

```bash
porkbun.sh list | jq '.domains[] | {domain, status, expireDate}'
porkbun.sh dns-list example.com | jq '.records[] | {id, type, name, content}'
```
