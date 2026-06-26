---
name: dns-lookup
description: DNS record lookups, reverse DNS, WHOIS via RDAP, and IP geolocation.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌐"
    homepage: https://dns.agentutil.net
    always: false
---

# dns-lookup

DNS record lookups (A, AAAA, MX, TXT, CNAME, NS, SOA), reverse DNS (PTR), WHOIS/RDAP domain info, and IP geolocation.

## Data Handling

This skill sends domain names and IP addresses to an external API. The service does not store or log input data beyond the immediate response.

## Endpoints

### DNS Lookup

```bash
curl -X POST https://dns.agentutil.net/v1/lookup \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "type": "MX"}'
```

Types: A, AAAA, MX, TXT, CNAME, NS, SOA, ANY. Default: A.

### Reverse DNS

```bash
curl -X POST https://dns.agentutil.net/v1/reverse \
  -H "Content-Type: application/json" \
  -d '{"ip": "8.8.8.8"}'
```

### WHOIS

```bash
curl -X POST https://dns.agentutil.net/v1/whois \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

### IP Geolocation

```bash
curl -X POST https://dns.agentutil.net/v1/geoip \
  -H "Content-Type: application/json" \
  -d '{"ip": "8.8.8.8"}'
```

## Response Format

```json
{
  "records": [{"type": "A", "value": "93.184.216.34", "ttl": 300}],
  "domain": "example.com",
  "query_type": "A",
  "request_id": "abc-123",
  "service": "https://dns.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

No authentication required for free tier. No personal data collected. Rate limiting uses IP hashing only.
