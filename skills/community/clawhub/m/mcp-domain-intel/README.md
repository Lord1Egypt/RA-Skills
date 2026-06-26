# @blue-trianon/mcp-domain-intel

MCP tool for domain intelligence — WHOIS lookups and domain availability checks via the L402 API.

## Features

- WHOIS and DNS intelligence lookups
- Domain availability checking
- Configurable base URL via environment variable
- Powered by L402 micropayments

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "domain-intel": {
      "command": "npx",
      "args": ["-y", "@blue-trianon/mcp-domain-intel"],
      "env": {
        "NAUTDEV_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "domain-intel": {
      "command": "mcp-domain-intel"
    }
  }
}
```

## Tools

### lookup

Look up WHOIS and DNS intelligence for a domain name.

| Parameter | Type   | Required | Description                        |
|-----------|--------|----------|------------------------------------|
| domain    | string | yes      | Domain name (e.g. example.com)    |

### available

Check if a domain name is available for registration.

| Parameter | Type   | Required | Description                        |
|-----------|--------|----------|------------------------------------|
| domain    | string | yes      | Domain name (e.g. example.com)    |

## Pricing

Requests are metered via L402 micropayments. See [Blue-Trianon-Ventures](https://github.com/Blue-Trianon-Ventures) for pricing details.

## License

MIT
