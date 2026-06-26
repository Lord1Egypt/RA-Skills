# MCP API Reference: mcp-geoip-server

## Endpoint

- URL: `https://ip.api4claw.com/mcp`
- Transport: Streamable HTTP
- Server name: `mcp-geoip-server`
- Server version: `1.0.0`
- Protocol version (initialize result): `2024-11-05`

## Tool List

### `get_ip_geolocation`

Look up geolocation information for an IP address.

Input schema:

```json
{
  "type": "object",
  "properties": {
    "ip_address": {
      "type": "string",
      "description": "IPv4 or IPv6 address to look up (e.g. \"8.8.8.8\" or \"2001:4860:4860::8888\")"
    }
  },
  "required": ["ip_address"]
}
```

Typical output fields:

- `ip`: queried IP
- `country`: country name
- `country_code`: ISO country code
- `province`: province/state
- `city`: city
- `asn`: ASN number
- `asn_org`: ASN org name

## Notes

- The endpoint requires an MCP session workflow (`initialize` -> get `Mcp-Session-Id` -> `tools/list` / `tools/call`).
- Country field text may sometimes show encoding issues in non-UTF8 clients; keep raw data and present `country_code` together for reliability.
- The script implementation uses a fixed HTTPS endpoint (`https://ip.api4claw.com/mcp`) and does not expose arbitrary endpoint override.
