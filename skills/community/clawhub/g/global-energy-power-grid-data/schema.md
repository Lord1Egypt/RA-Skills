# Global Energy & Power Grid Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `energy-access-production`

x402 availability: not enabled for this product.

## `query_energy_data`

Action slug: `query-energy-data`

Price: `10` credits

Fetch energy indicators for a country or region, including electricity access rates, renewable and fossil energy mix, per capita consumption, energy efficiency, and clean cooking access with SDG 7 tracking.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country_or_region` | `string` | yes | Country name, ISO3 code (e.g., 'USA', 'KEN'), or region (e.g., 'Sub-Saharan Africa') |
| `energy_type` | `string` | no | Energy category: 'electricity', 'renewable', 'fossil', 'efficiency', 'cooking', or 'all' |
| `include_energy_mix` | `boolean` | no | Calculate energy mix breakdown showing renewable, fossil, nuclear, and other percentages |
| `include_urban_rural_gaps` | `boolean` | no | Calculate urban/rural electricity access gap analysis with percentage points difference |
| `time_period` | `string` | no | Time period: 'latest', single year 'YYYY' (e.g., '2020'), or range 'YYYY:YYYY' (e.g., '2015:2023') |

Sample parameters:

```json
{
  "country_or_region": "example country or region",
  "energy_type": "all",
  "include_energy_mix": true,
  "include_urban_rural_gaps": false,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "country_or_region": {
    "description": "Country name, ISO3 code (e.g., 'USA', 'KEN'), or region (e.g., 'Sub-Saharan Africa')",
    "required": true,
    "type": "string"
  },
  "energy_type": {
    "default": "all",
    "description": "Energy category: 'electricity', 'renewable', 'fossil', 'efficiency', 'cooking', or 'all'",
    "enum": [
      "electricity",
      "renewable",
      "fossil",
      "efficiency",
      "cooking",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_energy_mix": {
    "default": true,
    "description": "Calculate energy mix breakdown showing renewable, fossil, nuclear, and other percentages",
    "required": false,
    "type": "boolean"
  },
  "include_urban_rural_gaps": {
    "default": false,
    "description": "Calculate urban/rural electricity access gap analysis with percentage points difference",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest', single year 'YYYY' (e.g., '2020'), or range 'YYYY:YYYY' (e.g., '2015:2023')",
    "required": false,
    "type": "string"
  }
}
```
