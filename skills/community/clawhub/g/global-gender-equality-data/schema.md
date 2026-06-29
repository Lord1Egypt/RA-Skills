# Global Gender Equality Data Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `gender-equality-women-s-empowerment`

x402 availability: not enabled for this product.

## `query_gender_data`

Action slug: `query-gender-data`

Price: `100` credits

Query World Bank gender equality and women's empowerment indicators by country/region and gender aspect. Returns data on labor force participation gaps, education parity indices, political representation, legal framework scores, maternal health, economic empowerment, and attitudes toward violence. Includes automatic gender gap calculations and SDG 5 alignment.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_gaps` | `boolean` | no | Automatically calculate gender gaps (absolute and percentage differences between male and female indicators) |
| `country_or_region` | `string` | yes | Country or region name (e.g., 'Rwanda', 'India', 'United States', 'Africa', 'Latin America') |
| `gender_aspect` | `string` | no | Gender dimension to query: 'labor' (participation, employment), 'education' (literacy, parity indices), 'political' (parliament, ministerial), 'legal' (WBL index), 'health' (maternal mortality, reproductive), 'economic' (financial inclusion, firm ownership), 'violence' (attitudes toward IPV), 'all' (all indicators) |
| `time_period` | `string` | no | Time period for data: 'latest', a year like '2020', a range like '2010:2020', or shorthand 'last5'/'last10' |

Sample parameters:

```json
{
  "calculate_gaps": true,
  "country_or_region": "example country or region",
  "gender_aspect": "all",
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_gaps": {
    "default": true,
    "description": "Automatically calculate gender gaps (absolute and percentage differences between male and female indicators)",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country or region name (e.g., 'Rwanda', 'India', 'United States', 'Africa', 'Latin America')",
    "required": true,
    "type": "string"
  },
  "gender_aspect": {
    "default": "all",
    "description": "Gender dimension to query: 'labor' (participation, employment), 'education' (literacy, parity indices), 'political' (parliament, ministerial), 'legal' (WBL index), 'health' (maternal mortality, reproductive), 'economic' (financial inclusion, firm ownership), 'violence' (attitudes toward IPV), 'all' (all indicators)",
    "enum": [
      "labor",
      "education",
      "political",
      "legal",
      "health",
      "economic",
      "violence",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period for data: 'latest', a year like '2020', a range like '2010:2020', or shorthand 'last5'/'last10'",
    "required": false,
    "type": "string"
  }
}
```
