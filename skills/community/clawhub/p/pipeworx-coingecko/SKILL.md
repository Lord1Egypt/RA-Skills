# Coingecko

CoinGecko MCP — wraps CoinGecko free API (no auth required)

## get_coin

Get detailed information about a cryptocurrency including price, market cap, volume, and description

## search_coins

Search for cryptocurrencies by name or symbol. Returns matching coins with their IDs. Example: searc

## get_market_data

Get top cryptocurrencies ranked by market cap with current prices, 24h changes, and volume. Example:

## get_trending

Get currently trending cryptocurrencies on CoinGecko based on user search activity. No parameters ne

```json
{
  "mcpServers": {
    "coingecko": {
      "url": "https://gateway.pipeworx.io/coingecko/mcp"
    }
  }
}
```
