# @blue-trianon/mcp-crypto-data

MCP tool for cryptocurrency data — real-time prices, network fees, and Lightning Network statistics via the L402 API.

## Features

- Real-time cryptocurrency prices
- Network transaction fee estimates
- Lightning Network statistics (nodes, channels, capacity)
- Configurable base URL via environment variable
- Powered by L402 micropayments

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "crypto-data": {
      "command": "npx",
      "args": ["-y", "@blue-trianon/mcp-crypto-data"],
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
    "crypto-data": {
      "command": "mcp-crypto-data"
    }
  }
}
```

## Tools

### price

Get the current price for a cryptocurrency.

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| coin      | string | yes      | Cryptocurrency identifier (e.g. bitcoin, ethereum) |

### fees

Get current network transaction fees across major cryptocurrencies.

No parameters required.

### lightning_stats

Get current Lightning Network statistics.

No parameters required.

## Pricing

Requests are metered via L402 micropayments. See [Blue-Trianon-Ventures](https://github.com/Blue-Trianon-Ventures) for pricing details.

## License

MIT
