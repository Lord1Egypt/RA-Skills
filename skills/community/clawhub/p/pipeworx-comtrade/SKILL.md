# Comtrade

Comtrade MCP — UN Comtrade API for international bilateral trade data

## comtrade_trade_data

Get bilateral trade data between two countries (e.g., "840" for US, "156" for China). Returns trade 

## comtrade_top_partners

Find a country's top trading partners ranked by trade volume. Returns partner countries and total tr

## comtrade_top_commodities

Find top commodities traded between two countries ranked by value. Returns product categories and tr

## comtrade_country_codes

Look up country ISO numeric codes for trade queries (e.g., "840" = US, "156" = China). Returns code 

```json
{
  "mcpServers": {
    "comtrade": {
      "url": "https://gateway.pipeworx.io/comtrade/mcp"
    }
  }
}
```
