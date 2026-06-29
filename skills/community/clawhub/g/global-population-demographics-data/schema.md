# Global Population & Demographics Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `population-demographics`

x402 availability: not enabled for this product.

## `query_population_data`

Action slug: `query-population-data`

Price: `10` credits

Query World Bank population and demographic indicators by country/region and demographic aspect. Returns data on population size, growth rates, age structure, fertility/mortality, urban-rural splits, migration, dependency ratios, and demographic transition analysis.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_dependency_ratios` | `boolean` | no | Automatically calculate dependency ratios from age structure data when aspect is 'all' or 'age' |
| `country_or_region` | `string` | yes | Country name, ISO3 code (e.g., 'USA', 'JPN'), or region (e.g., 'East Asia') |
| `demographic_aspect` | `string` | no | Demographic category to query: 'population' (total, growth, density), 'growth' (birth/death rates, migration), 'age' (age groups, dependency ratios), 'fertility' (fertility/birth rates), 'migration' (net migration), 'all' (all indicators) |
| `include_urban_rural` | `boolean` | no | Include urban vs rural population percentage breakdown |
| `time_period` | `string` | no | Time period for data: 'latest', a year like '2022', a range like '2010:2023', or shorthand 'last5'/'last10' |

Sample parameters:

```json
{
  "calculate_dependency_ratios": true,
  "country_or_region": "example country or region",
  "demographic_aspect": "all",
  "include_urban_rural": false,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_dependency_ratios": {
    "default": true,
    "description": "Automatically calculate dependency ratios from age structure data when aspect is 'all' or 'age'",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country name, ISO3 code (e.g., 'USA', 'JPN'), or region (e.g., 'East Asia')",
    "required": true,
    "type": "string"
  },
  "demographic_aspect": {
    "default": "all",
    "description": "Demographic category to query: 'population' (total, growth, density), 'growth' (birth/death rates, migration), 'age' (age groups, dependency ratios), 'fertility' (fertility/birth rates), 'migration' (net migration), 'all' (all indicators)",
    "enum": [
      "population",
      "growth",
      "age",
      "fertility",
      "migration",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_urban_rural": {
    "default": false,
    "description": "Include urban vs rural population percentage breakdown",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period for data: 'latest', a year like '2022', a range like '2010:2023', or shorthand 'last5'/'last10'",
    "required": false,
    "type": "string"
  }
}
```
