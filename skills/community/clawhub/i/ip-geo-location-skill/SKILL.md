---
name: ip-geo-location-skill
description: "IP geolocation lookup via MCP. Use when users ask IP location, IP geolocation, where an IP is from, IP lookup, ASN, IP to country/city, IP 地理位置查询, IP 归属地, 批量 IP 查询."
argument-hint: "Provide one or more IPs (IPv4/IPv6), e.g. 8.8.8.8, 1.1.1.1"
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# IP Geolocation Skill

Use this skill to query geographic and ASN information from IP addresses through the `mcp-geoip-server` MCP service.

This skill is designed for:

- Single IP lookup
- Multi-IP batch lookup
- Domain-to-IP then geolocation workflow
- Structured result output for quick user reading

## MCP Server

- Name: `mcp-geoip-server`
- URL: `https://ip.api4claw.com/mcp`
- Transport: Streamable HTTP

### VS Code MCP Configuration

Add to `.vscode/mcp.json` (workspace) or user MCP settings:

```json
{
  "servers": {
    "mcp-geoip-server": {
      "type": "http",
      "url": "https://ip.api4claw.com/mcp"
    }
  }
}
```

## Tools

### `get_ip_geolocation`

Look up geolocation information for one IP.

Input:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ip_address` | string | Yes | IPv4 or IPv6 address to look up (e.g. `8.8.8.8` or `2001:4860:4860::8888`) |

Output fields:

| Field | Description |
|-------|-------------|
| `ip` | The queried IP address |
| `country` | Country name |
| `country_code` | ISO country code (e.g. `US`, `CN`) |
| `province` | Province or state |
| `city` | City name |
| `asn` | Autonomous System Number |
| `asn_org` | ASN organization name |

Detailed tool schema and protocol notes: [API reference](./references/api.md)

## Execution Workflow

1. Extract query targets from user input.
2. Classify each target as IPv4, IPv6, or domain.
3. If target is a domain, resolve to IP first using [resolve script](./scripts/resolve-domain.js).
4. Call `get_ip_geolocation` for each IP.
5. Return concise and structured results.
6. If multiple IPs are provided, present results in a table for easy comparison.

## Input Handling Rules

- Trim whitespace and punctuation around candidate IPs.
- Keep duplicates out during batch lookup.
- Support both IPv4 and IPv6.
- If input is neither valid IP nor resolvable domain, return a clear validation error.
- For script-based calls, only valid IP literals are sent to remote MCP (invalid inputs are rejected locally).
- Private/reserved IP ranges (for example `127.0.0.1`, `10.x.x.x`, `192.168.x.x`, `fc00::/7`) must not be sent to external MCP.

## Security and Privacy

- This skill sends queried IP addresses to an external MCP service (`ip.api4claw.com`).
- The default endpoint uses HTTPS transport to encrypt traffic in transit.
- The script implementation is restricted to a fixed HTTPS endpoint (`https://ip.api4claw.com/mcp`) to reduce misuse risk.
- Private/internal IPs are blocked in the script implementation to reduce privacy leakage risk.

## Output Format

Use this format by default:

| IP | Country | Province/State | City | Country Code | ASN | ASN Org |
|---|---|---|---|---|---|---|
| 8.8.8.8 | United States | - | - | US | 15169 | Google LLC |

If a field is empty, display `-`.

## Error Handling

- MCP unavailable/timeout: explain temporary service issue and suggest retry.
- Invalid IP format: ask user to confirm/correct the IP.
- Private or reserved IP: explain that local/private addresses are intentionally blocked from external lookup.
- Empty/unknown location fields: keep response transparent and do not fabricate values.
- Encoding anomalies (for example garbled country text): include `country_code` and raw value.
- Session timeout/invalid session ID: re-run MCP `initialize` to get a new `Mcp-Session-Id`, then retry the failed tool call once.

## Domain-to-IP Flow

When user asks for a domain location (for example `example.com`):

1. Resolve A/AAAA records with [resolve script](./scripts/resolve-domain.js).
2. Query each resolved IP using `get_ip_geolocation`.
3. Summarize domain-level findings and list per-IP differences.

## Implementation Scripts

- [invoke MCP lookup](./scripts/invoke-geoip-mcp.js): includes `initialize` before calls and auto re-initialize on session expiration.
- [resolve domain](./scripts/resolve-domain.js): resolves domain to unique A/AAAA addresses.

## Example: Single IP

User: `8.8.8.8 在哪里?`

Call:

`get_ip_geolocation({ "ip_address": "8.8.8.8" })`

Response (example):

```json
{
  "ip": "8.8.8.8",
  "country": "美国",
  "country_code": "US",
  "province": "",
  "city": "",
  "asn": 15169,
  "asn_org": "Google LLC"
}
```

## Example: Batch IPs

User: `帮我查 8.8.8.8 和 1.1.1.1 的地理位置`

Execution:

1. Call `get_ip_geolocation` with `8.8.8.8`
2. Call `get_ip_geolocation` with `1.1.1.1`
3. Return merged table with both records

## Success Criteria

- Every valid input IP returns one result row.
- Invalid targets are explicitly marked with reason.
- No inferred or fabricated geographic values.
- Response is readable for both Chinese and English users.
