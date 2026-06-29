# Global Governance & Institutional Quality Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `governance-institutional-quality`

x402 availability: not enabled for this product.

## `query_governance_data`

Action slug: `query-governance-data`

Price: `10` credits

Fetch governance and institutional quality data for a country or region from the World Bank Worldwide Governance Indicators (WGI). Returns six governance dimensions with WGI scores, percentile rankings, historical trends, peer comparisons, and SDG 16 alignment.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'United States', 'India', 'Sub-Saharan Africa'). Accepts partial matches and 3-letter ISO codes. |
| `governance_aspect` | `string` | no | Governance dimension to query. Options: corruption, rule_of_law, effectiveness, stability, regulatory, voice, or all. |
| `include_historical_trends` | `boolean` | no | Include historical trends showing improvement or deterioration over time. |
| `include_peer_comparison` | `boolean` | no | Include comparison with regional and income group peers (World, High Income, Upper Middle Income, Lower Middle Income, Low Income). |
| `include_percentile_ranks` | `boolean` | no | Include percentile rankings (0-100 scale) for international comparison. |
| `time_period` | `string` | no | Time period: 'latest' (most recent), 'last_5_years', 'last_10_years', a single year 'YYYY', or a range 'YYYY:YYYY'. |

Sample parameters:

```json
{
  "country_or_region": "example country or region",
  "governance_aspect": "all",
  "include_historical_trends": true,
  "include_peer_comparison": true,
  "include_percentile_ranks": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'United States', 'India', 'Sub-Saharan Africa'). Accepts partial matches and 3-letter ISO codes.",
    "required": true,
    "type": "string"
  },
  "governance_aspect": {
    "default": "all",
    "description": "Governance dimension to query. Options: corruption, rule_of_law, effectiveness, stability, regulatory, voice, or all.",
    "enum": [
      "corruption",
      "rule_of_law",
      "effectiveness",
      "stability",
      "regulatory",
      "voice",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_historical_trends": {
    "default": true,
    "description": "Include historical trends showing improvement or deterioration over time.",
    "required": false,
    "type": "boolean"
  },
  "include_peer_comparison": {
    "default": true,
    "description": "Include comparison with regional and income group peers (World, High Income, Upper Middle Income, Lower Middle Income, Low Income).",
    "required": false,
    "type": "boolean"
  },
  "include_percentile_ranks": {
    "default": true,
    "description": "Include percentile rankings (0-100 scale) for international comparison.",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' (most recent), 'last_5_years', 'last_10_years', a single year 'YYYY', or a range 'YYYY:YYYY'.",
    "required": false,
    "type": "string"
  }
}
```
