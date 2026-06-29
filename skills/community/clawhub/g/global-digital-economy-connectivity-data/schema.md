# Global Digital Economy & Connectivity Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `digital-economy-technology`

x402 availability: not enabled for this product.

## `query_digital_data`

Action slug: `query-digital-data`

Price: `5` credits

Fetch digital economy and technology indicator data for a country or region, including internet penetration, mobile subscriptions, broadband access, ICT trade metrics, and digital divide analysis.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_digital_divide` | `boolean` | no | Calculate digital access gaps (100% minus current access rates) for internet, broadband, and mobile |
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'South Korea', 'Kenya', 'World') |
| `digital_aspect` | `string` | no | Digital aspect to query: 'internet', 'mobile', 'broadband', 'e_government', 'ict', 'infrastructure', or 'all' |
| `include_regional_comparison` | `boolean` | no | Include comparison data with digital leaders (World average, High Income, South Korea, Singapore) |
| `include_trends` | `boolean` | no | Include trend analysis with CAGR calculations when historical data is available |
| `time_period` | `string` | no | Time period: 'latest', 'last_5_years', 'last_10_years', 'YYYY:YYYY' range, or single 'YYYY' year |

Sample parameters:

```json
{
  "calculate_digital_divide": false,
  "country_or_region": "example country or region",
  "digital_aspect": "all",
  "include_regional_comparison": true,
  "include_trends": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_digital_divide": {
    "default": false,
    "description": "Calculate digital access gaps (100% minus current access rates) for internet, broadband, and mobile",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'South Korea', 'Kenya', 'World')",
    "required": true,
    "type": "string"
  },
  "digital_aspect": {
    "default": "all",
    "description": "Digital aspect to query: 'internet', 'mobile', 'broadband', 'e_government', 'ict', 'infrastructure', or 'all'",
    "enum": [
      "internet",
      "mobile",
      "broadband",
      "e_government",
      "ict",
      "infrastructure",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_regional_comparison": {
    "default": true,
    "description": "Include comparison data with digital leaders (World average, High Income, South Korea, Singapore)",
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
