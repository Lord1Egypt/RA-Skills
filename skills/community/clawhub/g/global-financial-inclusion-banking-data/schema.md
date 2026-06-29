# Global Financial Inclusion & Banking Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `financial-sector-banking`

x402 availability: not enabled for this product.

## `query_financial_data`

Action slug: `query-financial-data`

Price: `20` credits

Fetch financial sector indicators for a country or region, including bank account ownership, credit access, financial inclusion gender gaps, stock market data, remittances, and mobile money adoption with global comparisons.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_gender_gaps` | `boolean` | no | Calculate gender disparities in financial inclusion (male/female account ownership gap). Applies when aspect is 'inclusion', 'all', or not specified. |
| `country_or_region` | `string` | no | Country name or ISO3 code (e.g., 'United States', 'India', 'World'). Defaults to 'World' if not provided. |
| `financial_aspect` | `string` | no | Financial category: 'banking', 'credit', 'inclusion', 'markets', 'remittances', or 'all' |
| `include_targets` | `boolean` | no | Include Global Findex targets (Universal Financial Access 2030) and SDG alignment (SDG 1, 5, 8.10, 10) in response |
| `time_period` | `string` | no | Time period: 'latest' for most recent 10 years, single year 'YYYY', or range 'YYYY:YYYY' |

Sample parameters:

```json
{
  "calculate_gender_gaps": true,
  "country_or_region": "World",
  "financial_aspect": "all",
  "include_targets": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_gender_gaps": {
    "default": true,
    "description": "Calculate gender disparities in financial inclusion (male/female account ownership gap). Applies when aspect is 'inclusion', 'all', or not specified.",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "default": "World",
    "description": "Country name or ISO3 code (e.g., 'United States', 'India', 'World'). Defaults to 'World' if not provided.",
    "required": false,
    "type": "string"
  },
  "financial_aspect": {
    "default": "all",
    "description": "Financial category: 'banking', 'credit', 'inclusion', 'markets', 'remittances', or 'all'",
    "enum": [
      "banking",
      "credit",
      "inclusion",
      "markets",
      "remittances",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_targets": {
    "default": true,
    "description": "Include Global Findex targets (Universal Financial Access 2030) and SDG alignment (SDG 1, 5, 8.10, 10) in response",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' for most recent 10 years, single year 'YYYY', or range 'YYYY:YYYY'",
    "required": false,
    "type": "string"
  }
}
```
