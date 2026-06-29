# Global Agriculture & Food Security Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `agriculture-food-security`

x402 availability: not enabled for this product.

## `query_agriculture_data`

Action slug: `query-agriculture-data`

Price: `5` credits

Fetch agricultural and food security indicator data for a country or region, including crop yields, undernourishment rates, land use, productivity metrics, and rural development context.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agriculture_topic` | `string` | no | Topic filter: 'production', 'food_security', 'malnutrition', 'land_use', 'productivity', or 'all' |
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'India', 'Sub-Saharan Africa', 'Brazil', 'World') |
| `include_regional_comparison` | `boolean` | no | Include comparison data from World, Sub-Saharan Africa, South Asia, Latin America, East Asia, and Middle East |
| `include_rural_context` | `boolean` | no | Include rural population percentage and agricultural employment data for additional context |
| `include_trends` | `boolean` | no | Include trend analysis with change direction (improving/worsening/stable) when historical data is available |
| `time_period` | `string` | no | Time period: 'latest', 'last_5_years', 'last_10_years', 'YYYY:YYYY' range, or single 'YYYY' year |

Sample parameters:

```json
{
  "agriculture_topic": "all",
  "country_or_region": "example country or region",
  "include_regional_comparison": true,
  "include_rural_context": true,
  "include_trends": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "agriculture_topic": {
    "default": "all",
    "description": "Topic filter: 'production', 'food_security', 'malnutrition', 'land_use', 'productivity', or 'all'",
    "enum": [
      "production",
      "food_security",
      "malnutrition",
      "land_use",
      "productivity",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'India', 'Sub-Saharan Africa', 'Brazil', 'World')",
    "required": true,
    "type": "string"
  },
  "include_regional_comparison": {
    "default": true,
    "description": "Include comparison data from World, Sub-Saharan Africa, South Asia, Latin America, East Asia, and Middle East",
    "required": false,
    "type": "boolean"
  },
  "include_rural_context": {
    "default": true,
    "description": "Include rural population percentage and agricultural employment data for additional context",
    "required": false,
    "type": "boolean"
  },
  "include_trends": {
    "default": true,
    "description": "Include trend analysis with change direction (improving/worsening/stable) when historical data is available",
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
