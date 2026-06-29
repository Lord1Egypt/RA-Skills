# Global Debt & Fiscal Explorer Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `debt-fiscal-management`

x402 availability: not enabled for this product.

## `query_fiscal_data`

Action slug: `query-fiscal-data`

Price: `30` credits

Query national debt, government revenue, public expenditure, fiscal balance, and debt service data for any country or region from the World Bank.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_debt_ratios` | `boolean` | no | Calculate debt sustainability ratios and compare against IMF/World Bank thresholds. |
| `country_or_region` | `string` | no | Country name or region (e.g., 'United States', 'Greece', 'Kenya', 'World'). Defaults to 'World' if not provided. |
| `fiscal_aspect` | `string` | no | Fiscal aspect to query: 'debt', 'balance', 'revenue', 'expenditure', 'debt_service', or 'all'. Defaults to 'all'. |
| `time_period` | `string` | no | Time period: 'latest' for most recent data, a specific year like '2020', or a range like '2015:2020'. |

Sample parameters:

```json
{
  "calculate_debt_ratios": true,
  "country_or_region": "example country or region",
  "fiscal_aspect": "all",
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_debt_ratios": {
    "default": true,
    "description": "Calculate debt sustainability ratios and compare against IMF/World Bank thresholds.",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country name or region (e.g., 'United States', 'Greece', 'Kenya', 'World'). Defaults to 'World' if not provided.",
    "required": false,
    "type": "string"
  },
  "fiscal_aspect": {
    "default": "all",
    "description": "Fiscal aspect to query: 'debt', 'balance', 'revenue', 'expenditure', 'debt_service', or 'all'. Defaults to 'all'.",
    "enum": [
      "debt",
      "balance",
      "revenue",
      "expenditure",
      "debt_service",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' for most recent data, a specific year like '2020', or a range like '2015:2020'.",
    "required": false,
    "type": "string"
  }
}
```
