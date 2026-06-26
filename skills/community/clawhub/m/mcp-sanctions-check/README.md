# @velocibot/mcp-sanctions-check

MCP tool that checks names against the OFAC SDN (Specially Designated Nationals) sanctions list.

## Features

- Downloads and caches the official OFAC SDN CSV list
- Automatic cache refresh every 24 hours
- Case-insensitive, token-based name matching
- Optional country filtering
- Returns structured match results

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "sanctions-check": {
      "command": "npx",
      "args": ["-y", "@velocibot/mcp-sanctions-check"]
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "sanctions-check": {
      "command": "mcp-sanctions-check"
    }
  }
}
```

## Tool: check_sanctions

**Input:**
| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| name      | string | yes      | The name to check against the SDN list |
| country   | string | no       | Optional country to narrow results   |

**Output:**
```json
{
  "match": true,
  "entries": [
    {
      "name": "DOE, John",
      "type": "individual",
      "programs": "SDGT",
      "remarks": "DOB 01 Jan 1970; nationality USA"
    }
  ],
  "checked_at": "2026-03-19T12:00:00.000Z"
}
```

## License

MIT
