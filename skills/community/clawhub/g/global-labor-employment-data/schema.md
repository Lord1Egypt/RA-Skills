# Global Labor & Employment Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `labor-market-employment`

x402 availability: not enabled for this product.

## `query_labor_data`

Action slug: `query-labor-data`

Price: `5` credits

Fetch labor market and employment indicator data for a country or region, including labor force participation, unemployment rates, sector employment, gender gap analysis, and employment quality metrics.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_gender_gaps` | `boolean` | no | Calculate gender gaps (male rate minus female rate) for participation, unemployment, and youth unemployment |
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'Kenya', 'South Korea', 'World') |
| `demographic_filter` | `string` | no | Filter indicators by demographic: 'gender', 'youth', 'sector', 'total', or 'all' for all indicators |
| `include_regional_comparison` | `boolean` | no | Include comparison with World average, High Income, East Asia & Pacific, and Latin America & Caribbean |
| `include_sector_employment` | `boolean` | no | Include employment by sector breakdown (agriculture, industry, services) even when a different demographic filter is selected |
| `include_trends` | `boolean` | no | Include trend analysis with CAGR calculations when historical data is available |
| `time_period` | `string` | no | Time period: 'latest', 'last_5_years', 'last_10_years', 'YYYY:YYYY' range, or single 'YYYY' year |

Sample parameters:

```json
{
  "calculate_gender_gaps": true,
  "country_or_region": "example country or region",
  "demographic_filter": "gender",
  "include_regional_comparison": true,
  "include_sector_employment": true,
  "include_trends": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_gender_gaps": {
    "default": true,
    "description": "Calculate gender gaps (male rate minus female rate) for participation, unemployment, and youth unemployment",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'Kenya', 'South Korea', 'World')",
    "required": true,
    "type": "string"
  },
  "demographic_filter": {
    "description": "Filter indicators by demographic: 'gender', 'youth', 'sector', 'total', or 'all' for all indicators",
    "enum": [
      "gender",
      "youth",
      "sector",
      "total",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_regional_comparison": {
    "default": true,
    "description": "Include comparison with World average, High Income, East Asia & Pacific, and Latin America & Caribbean",
    "required": false,
    "type": "boolean"
  },
  "include_sector_employment": {
    "default": true,
    "description": "Include employment by sector breakdown (agriculture, industry, services) even when a different demographic filter is selected",
    "required": false,
    "type": "boolean"
  },
  "include_trends": {
    "default": true,
    "description": "Include trend analysis with CAGR calculations when historical data is available",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest', 'last_5_years', 'last_10_years', 'YYYY:YYYY' range, or single 'YYYY' year",
    "required": false,
    "type": "string"
  }
}
```
