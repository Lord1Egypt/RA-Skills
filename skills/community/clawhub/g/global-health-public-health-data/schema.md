# Global Health & Public Health Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `healthcare-demographics-data`

x402 availability: not enabled for this product.

## `query_health_data`

Action slug: `query-health-data`

Price: `10` credits

Fetch health and demographic data for a country or region from the World Bank. Returns mortality rates, life expectancy, immunization coverage, health expenditure, infectious disease prevalence, and demographic indicators with WHO benchmarks and SDG target comparisons.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'Japan', 'Kenya', 'United States', 'South Asia', 'Sub-Saharan Africa'). Uses fuzzy matching against the World Bank countries API. |
| `health_topic` | `string` | no | Health topic to query. Options: mortality, life_expectancy, immunization, expenditure, infectious_disease, demographics, or all. |
| `include_demographic_context` | `boolean` | no | Include population and demographic context (total population, age distribution). Automatically skipped when health_topic is 'demographics'. |
| `include_regional_comparison` | `boolean` | no | Include a note about regional comparison data availability. |
| `include_who_benchmarks` | `boolean` | no | Include WHO benchmarks and SDG 3 target comparisons for applicable indicators. |
| `time_period` | `string` | no | Time period for data. Use 'latest' for most recent, 'YYYY' for a specific year, 'YYYY:YYYY' for a range, 'last5' or 'last10' for recent years. |

Sample parameters:

```json
{
  "country_or_region": "example country or region",
  "health_topic": "all",
  "include_demographic_context": true,
  "include_regional_comparison": false,
  "include_who_benchmarks": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'Japan', 'Kenya', 'United States', 'South Asia', 'Sub-Saharan Africa'). Uses fuzzy matching against the World Bank countries API.",
    "required": true,
    "type": "string"
  },
  "health_topic": {
    "default": "all",
    "description": "Health topic to query. Options: mortality, life_expectancy, immunization, expenditure, infectious_disease, demographics, or all.",
    "enum": [
      "mortality",
      "life_expectancy",
      "immunization",
      "expenditure",
      "infectious_disease",
      "demographics",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_demographic_context": {
    "default": true,
    "description": "Include population and demographic context (total population, age distribution). Automatically skipped when health_topic is 'demographics'.",
    "required": false,
    "type": "boolean"
  },
  "include_regional_comparison": {
    "default": false,
    "description": "Include a note about regional comparison data availability.",
    "required": false,
    "type": "boolean"
  },
  "include_who_benchmarks": {
    "default": true,
    "description": "Include WHO benchmarks and SDG 3 target comparisons for applicable indicators.",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period for data. Use 'latest' for most recent, 'YYYY' for a specific year, 'YYYY:YYYY' for a range, 'last5' or 'last10' for recent years.",
    "required": false,
    "type": "string"
  }
}
```
