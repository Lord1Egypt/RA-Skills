# Infrastructure, Mobility, and Housing Data Hub Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `infrastructure-urban-development`

x402 action routes are enabled for this product through `https://www.agentpmt.com/api/external`.

## `query_infrastructure_data`

Action slug: `query-infrastructure-data`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/infrastructure-urban-development/actions/query-infrastructure-data/invoke`

Price: `5` credits

Fetch infrastructure and urban development data for a country or region from the World Bank. Returns electricity access, internet penetration, water/sanitation access, road infrastructure, urbanization indicators, with SDG progress tracking, access gap calculations, and urban-rural divide analysis.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'Kenya', 'United States', 'South Asia'). Uses natural language matching against the World Bank country list. |
| `include_access_gaps` | `boolean` | no | Calculate access gaps (100% minus current access) for coverage indicators. |
| `include_logistics_performance` | `boolean` | no | Include Logistics Performance Index (LPI) data. Only applies when infrastructure_type is 'roads' or 'all'. |
| `include_regional_comparison` | `boolean` | no | Include regional averages for comparison. |
| `include_sdg_targets` | `boolean` | no | Include SDG 9 and SDG 11 targets and progress assessment. |
| `infrastructure_type` | `string` | no | Infrastructure type to query. Options: electricity, internet, water, roads, urban, or all. |
| `time_period` | `string` | no | Time period: 'latest' (most recent year), 'YYYY' (specific year), 'YYYY:YYYY' (range), or 'last5' (last 5 years). |
| `urban_rural_breakdown` | `boolean` | no | Include urban/rural disaggregation where available (electricity, water, sanitation). |

Sample parameters:

```json
{
  "country_or_region": "example country or region",
  "include_access_gaps": true,
  "include_logistics_performance": true,
  "include_regional_comparison": true,
  "include_sdg_targets": true,
  "infrastructure_type": "all",
  "time_period": "latest",
  "urban_rural_breakdown": true
}
```

Generated JSON parameter schema:

```json
{
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'Kenya', 'United States', 'South Asia'). Uses natural language matching against the World Bank country list.",
    "required": true,
    "type": "string"
  },
  "include_access_gaps": {
    "default": true,
    "description": "Calculate access gaps (100% minus current access) for coverage indicators.",
    "required": false,
    "type": "boolean"
  },
  "include_logistics_performance": {
    "description": "Include Logistics Performance Index (LPI) data. Only applies when infrastructure_type is 'roads' or 'all'.",
    "required": false,
    "type": "boolean"
  },
  "include_regional_comparison": {
    "description": "Include regional averages for comparison.",
    "required": false,
    "type": "boolean"
  },
  "include_sdg_targets": {
    "default": true,
    "description": "Include SDG 9 and SDG 11 targets and progress assessment.",
    "required": false,
    "type": "boolean"
  },
  "infrastructure_type": {
    "default": "all",
    "description": "Infrastructure type to query. Options: electricity, internet, water, roads, urban, or all.",
    "enum": [
      "electricity",
      "internet",
      "water",
      "roads",
      "urban",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' (most recent year), 'YYYY' (specific year), 'YYYY:YYYY' (range), or 'last5' (last 5 years).",
    "required": false,
    "type": "string"
  },
  "urban_rural_breakdown": {
    "description": "Include urban/rural disaggregation where available (electricity, water, sanitation).",
    "required": false,
    "type": "boolean"
  }
}
```
