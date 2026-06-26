# Bls

BLS MCP — Bureau of Labor Statistics public data API (v2)

## bls_get_series

Fetch historical time series data for employment, inflation, wages, productivity, or housing. Return

## bls_search

Search BLS economic data series by keyword. Returns matching series IDs and titles. Use bls_get_seri

## bls_latest

Get the most recent data point for a BLS series. Returns latest value and date. Use when you need cu

## bls_popular_series

Browse popular BLS series by category: employment, inflation, wages, housing, productivity. Returns 

```json
{
  "mcpServers": {
    "bls": {
      "url": "https://gateway.pipeworx.io/bls/mcp"
    }
  }
}
```
