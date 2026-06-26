# World Bank

Access the World Bank's development indicators: GDP, population, CO2 emissions, literacy rates, mortality rates, and hundreds more metrics for every country, going back decades.

## Tools

**get_country** -- Basic country info. Pass an ISO code (e.g., `US`, `GBR`, `IN`) and get the full name, region, income level, capital city, and coordinates.

**get_indicator** -- Time-series data for any World Bank indicator. Specify a country code, indicator code, and optional date range (default 2015-2024).

**get_population** -- Shortcut for total population over time (indicator SP.POP.TOTL).

**get_gdp** -- Shortcut for GDP in current USD over time (indicator NY.GDP.MKTP.CD).

## Common indicator codes

| Code | Metric |
|------|--------|
| NY.GDP.MKTP.CD | GDP (current USD) |
| SP.POP.TOTL | Population, total |
| EN.ATM.CO2E.KT | CO2 emissions (kt) |
| SE.ADT.LITR.ZS | Literacy rate, adult (%) |
| SH.DYN.MORT | Under-5 mortality rate |
| SI.POV.GINI | Gini index |

## Example: India's GDP over the last decade

```bash
curl -X POST https://gateway.pipeworx.io/worldbank/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_gdp","arguments":{"country_code":"IN"}}}'
```

```json
{
  "mcpServers": {
    "worldbank": {
      "url": "https://gateway.pipeworx.io/worldbank/mcp"
    }
  }
}
```
