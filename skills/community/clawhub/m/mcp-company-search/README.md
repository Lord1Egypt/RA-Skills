# @blue-trianon/mcp-company-search

MCP tool for corporate registry search — find companies by jurisdiction and name via the L402 API.

## Features

- Search companies across multiple jurisdictions
- List all supported jurisdictions
- Configurable base URL via environment variable
- Powered by L402 micropayments

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "company-search": {
      "command": "npx",
      "args": ["-y", "@blue-trianon/mcp-company-search"],
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
    "company-search": {
      "command": "mcp-company-search"
    }
  }
}
```

## Tools

### search

Search for companies by jurisdiction and name.

| Parameter     | Type   | Required | Description                              |
|---------------|--------|----------|------------------------------------------|
| jurisdiction  | string | yes      | Jurisdiction code (e.g. us_de, gb, sg)  |
| name          | string | yes      | Company name or partial name to search   |

### jurisdictions

List all available jurisdictions for company search.

No parameters required.

## Pricing

Requests are metered via L402 micropayments. See [Blue-Trianon-Ventures](https://github.com/Blue-Trianon-Ventures) for pricing details.

## License

MIT
