# Global Poverty & Inequality Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `global-poverty-inequality-data`

x402 availability: not enabled for this product.

## `query_poverty_data`

Action slug: `query-poverty-data`

Price: `5` credits

Fetch poverty and inequality data for a country or region from the World Bank World Development Indicators database.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country_or_region` | `string` | yes | Country or region name in plain English. Supports 200+ countries (e.g., India, Kenya, Brazil), regional aggregations (e.g., Sub-Saharan Africa, South Asia, Latin America and Caribbean), income groups (e.g., Low Income, High Income, OECD), and global (World or Global). Common abbreviations like USA, UK, UAE are accepted. |
| `include_regional_comparison` | `boolean` | no | Include regional and global averages (World, Sub-Saharan Africa, South Asia, Latin America & Caribbean, East Asia & Pacific, Middle East & North Africa) for context. |
| `include_trends` | `boolean` | no | Include trend analysis showing direction, absolute change, percent change, and data point count when historical data is available. |
| `metric_type` | `string` | no | Type of poverty/inequality metric to query. |
| `time_period` | `string` | no | Time period for data retrieval: 'latest' for most recent year, 'last_5_years', 'last_10_years', or a specific range like '2015:2020'. |

Sample parameters:

```json
{
  "country_or_region": "example country or region",
  "include_regional_comparison": true,
  "include_trends": true,
  "metric_type": "all",
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "country_or_region": {
    "description": "Country or region name in plain English. Supports 200+ countries (e.g., India, Kenya, Brazil), regional aggregations (e.g., Sub-Saharan Africa, South Asia, Latin America and Caribbean), income groups (e.g., Low Income, High Income, OECD), and global (World or Global). Common abbreviations like USA, UK, UAE are accepted.",
    "required": true,
    "type": "string"
  },
  "include_regional_comparison": {
    "default": true,
    "description": "Include regional and global averages (World, Sub-Saharan Africa, South Asia, Latin America & Caribbean, East Asia & Pacific, Middle East & North Africa) for context.",
    "required": false,
    "type": "boolean"
  },
  "include_trends": {
    "default": true,
    "description": "Include trend analysis showing direction, absolute change, percent change, and data point count when historical data is available.",
    "required": false,
    "type": "boolean"
  },
  "metric_type": {
    "default": "all",
    "description": "Type of poverty/inequality metric to query.",
    "enum": [
      "poverty_headcount",
      "extreme_poverty",
      "gini_index",
      "gini",
      "inequality",
      "income_distribution",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period for data retrieval: 'latest' for most recent year, 'last_5_years', 'last_10_years', or a specific range like '2015:2020'.",
    "required": false,
    "type": "string"
  }
}
```
