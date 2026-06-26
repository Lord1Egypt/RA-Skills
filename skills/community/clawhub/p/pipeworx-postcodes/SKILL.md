# Postcodes

UK postcode geographic lookup. Get coordinates, administrative districts, parliamentary constituencies, and NHS regions for any postcode in the United Kingdom.

## What you get

- **lookup_postcode** -- Full geographic and administrative details for a UK postcode
- **nearest_postcodes** -- Find neighbouring postcodes to a given one
- **validate_postcode** -- Check if a postcode string is valid
- **random_postcode** -- Grab a random valid postcode with full details

## Try it

Look up 10 Downing Street's postcode:

```bash
curl -X POST https://gateway.pipeworx.io/postcodes/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"lookup_postcode","arguments":{"postcode":"SW1A 2AA"}}}'
```

## Good to know

Postcodes are case-insensitive and spaces are optional -- `SW1A1AA` works the same as `sw1a 1aa`. The response includes ONS codes, lat/lon coordinates, and full administrative geography down to ward and parish level.

## MCP config

```json
{
  "mcpServers": {
    "postcodes": {
      "url": "https://gateway.pipeworx.io/postcodes/mcp"
    }
  }
}
```
