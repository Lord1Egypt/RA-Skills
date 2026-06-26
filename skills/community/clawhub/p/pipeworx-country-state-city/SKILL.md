# Country State City

CountryStateCity MCP — wraps CountryStateCity API (api.countrystatecity.in/v1)

## list_countries

List all countries with ISO codes, capitals, phone codes, currencies, and regions. Returns ~250 coun

## get_states

Get all states or provinces for a country by ISO2 code (e.g., "US", "IN", "BR"). Returns state names

## get_cities

Get cities for a country, optionally filtered by state. Pass country_code (e.g., "US") and optionall

```json
{
  "mcpServers": {
    "country-state-city": {
      "url": "https://gateway.pipeworx.io/country-state-city/mcp"
    }
  }
}
```
