---
name: global-population-demographics-data
description: "Global Population & Demographics Data: Query population totals, growth rates, age structure, fertility rates, migration data, and urban-rural. Use when an agent needs global population & demographics data, population demographics, look up a country's total population and growth rate, compare age distributions across countries, analyze fertility rate trends over time, research migration patterns by country, query population data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/population-demographics
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/population-demographics"}}
---
# Global Population & Demographics Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Access detailed population and demographic data for every country on earth. Look up total population counts, growth rates, age distributions, fertility trends, migration patterns, and urban-rural splits. Build age pyramids, calculate dependency ratios, and compare demographic profiles across countries and regions — all from a comprehensive global data set.

## Product Instructions
### Population & Demographics Data

#### Overview

Query World Bank population and demographic indicators for any country or region. Access data on population size, growth rates, age structure, fertility and mortality, urban/rural splits, migration, dependency ratios, and demographic transition analysis. All data sourced from the World Bank Data360 API (World Development Indicators).

#### Actions

##### query_population_data

Query demographic indicators by country/region and demographic aspect.

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | Must be `"query_population_data"` |
| `country_or_region` | string | Country name, ISO3 code, or region. Examples: `"United States"`, `"USA"`, `"JPN"`, `"Kenya"`, `"India"` |

**Optional Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `demographic_aspect` | string | `"all"` | Category of indicators to return. One of: `"population"`, `"growth"`, `"age"`, `"fertility"`, `"migration"`, `"all"` |
| `calculate_dependency_ratios` | boolean | `true` | Automatically calculate dependency ratios from age structure data when aspect is `"all"` or `"age"` |
| `include_urban_rural` | boolean | `false` | Include urban vs rural population percentage breakdown |
| `time_period` | string | `"latest"` | Time period for data. Accepts: `"latest"`, a single year like `"2022"`, a range like `"2010:2023"`, or shorthand `"last5"` / `"last10"` |

**Demographic Aspects:**

- **`population`** -- Total population, population growth rate (annual %), population density (people per sq. km)
- **`growth`** -- Population growth rate, birth rate (per 1,000), death rate (per 1,000), net migration
- **`age`** -- Age groups (0-14, 15-64, 65+ as % of total), age dependency ratio, youth dependency, elderly dependency
- **`fertility`** -- Fertility rate (births per woman), birth rate (per 1,000)
- **`migration`** -- Net migration (number of people)
- **`all`** -- All available indicators combined

###### Example: Basic country population data

```json
{
  "action": "query_population_data",
  "country_or_region": "Japan"
}
```

###### Example: Age structure with dependency ratios

```json
{
  "action": "query_population_data",
  "country_or_region": "Germany",
  "demographic_aspect": "age",
  "calculate_dependency_ratios": true
}
```

###### Example: Growth indicators for a specific year

```json
{
  "action": "query_population_data",
  "country_or_region": "Nigeria",
  "demographic_aspect": "growth",
  "time_period": "2020"
}
```

###### Example: Full profile with urban/rural breakdown

```json
{
  "action": "query_population_data",
  "country_or_region": "Brazil",
  "demographic_aspect": "all",
  "include_urban_rural": true,
  "calculate_dependency_ratios": true,
  "time_period": "latest"
}
```

###### Example: Historical fertility data over a range

```json
{
  "action": "query_population_data",
  "country_or_region": "India",
  "demographic_aspect": "fertility",
  "time_period": "2000:2023"
}
```

###### Example: Migration data using ISO3 code

```json
{
  "action": "query_population_data",
  "country_or_region": "MEX",
  "demographic_aspect": "migration",
  "time_period": "last5"
}
```

#### Workflows

##### Demographic Profile Report
1. Call `query_population_data` with `demographic_aspect: "all"`, `include_urban_rural: true`, and `calculate_dependency_ratios: true` to get a full country profile.
2. The response includes indicators, dependency ratios, urban/rural split, demographic transition stage analysis, and age structure interpretation.

##### Country Comparison
1. Call `query_population_data` for each country with the same `demographic_aspect` and `time_period`.
2. Compare the returned indicator values, dependency ratios, and transition stages side by side.

##### Trend Analysis
1. Call `query_population_data` with a `time_period` range (e.g., `"2000:2023"`) and a specific `demographic_aspect`.
2. The response contains data points across the range for tracking changes over time.

##### Aging Population Assessment
1. Call `query_population_data` with `demographic_aspect: "age"` and `calculate_dependency_ratios: true`.
2. Review the age structure interpretation (young, balanced, mature, aging), estimated median age range, and policy implications in the response.

#### Notes

- **Country input**: Accepts common country names (e.g., `"United States"`, `"South Korea"`), short forms (e.g., `"USA"`, `"UK"`), and ISO3 codes (e.g., `"GBR"`, `"JPN"`). If no country is provided, defaults to world (`"WLD"`).
- **Supported countries**: Major economies, African nations (Kenya, Nigeria, South Africa, Ethiopia, etc.), Asian countries (Indonesia, Pakistan, Bangladesh, etc.), European countries (Netherlands, Poland, Sweden, etc.), Latin America (Argentina, Colombia, Chile, etc.), and Middle East (Saudi Arabia, UAE, Israel, etc.).
- **Supported regions**: Use ISO3 codes or common names. No separate region aggregation endpoint; individual country queries only.
- **Demographic transition analysis**: Automatically included when aspect is `"all"`, `"growth"`, or `"fertility"`. Classifies countries into 5 stages: Stage 1 (High Stationary), Stage 2 (Early Expanding), Stage 3 (Late Expanding), Stage 4 (Low Stationary), Stage 5 (Declining).
- **Dependency ratios**: When `calculate_dependency_ratios` is true and aspect is `"all"` or `"age"`, the tool returns age dependency ratio, youth dependency ratio, and elderly dependency ratio (dependents per 100 working-age persons). If API-provided ratios are unavailable, they are calculated from age structure percentages.
- **Urban/rural split**: When `include_urban_rural` is true, returns urban and rural percentages plus an urbanization level classification (Highly urbanized >= 80%, Moderately urbanized >= 60%, Partially urbanized >= 40%, Predominantly rural < 40%).
- **Age structure interpretation**: Included when aspect is `"all"` or `"age"`. Categorizes population as "Very young" (youth > 40%), "Young" (youth > 30%), "Aging" (elderly > 20%), "Mature" (elderly > 14%), or "Balanced", with estimated median age range and policy implications.
- **Replacement fertility**: The tool flags whether the fertility rate is below the replacement level of 2.1 births per woman.
- **Data availability**: World Bank data may lag 1-3 years behind the current year. Some indicators may not be available for all countries or years.
- **Values are rounded** to 2 decimal places where applicable.
- **time_period validation**: Accepts `"latest"`, `"last5"`, `"last10"`, a 4-digit year, or a `YYYY:YYYY` range. Invalid formats return a validation error.
- **Unrecognized countries** return a descriptive error suggesting valid country names or ISO3 codes.
- **Data source**: World Bank Data360 API (World Development Indicators), updated regularly.

## When To Use
- Use this skill for `Global Population & Demographics Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global population & demographics data, population demographics, look up a country's total population and growth rate, compare age distributions across countries, analyze fertility rate trends over time, research migration patterns by country, query population data, country or region.
- Supported action names: `query_population_data`.

## Use Cases
- Look up a country's total population and growth rate
- Compare age distributions across countries
- Analyze fertility rate trends over time
- Research migration patterns by country
- Calculate dependency ratios from age structure
- Compare urban vs rural population splits
- Build demographic profiles for market research
- Study population aging trends
- Support academic demographic research
- Track population projections and forecasts

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_population_data` (action slug: `query-population-data`): Query World Bank population and demographic indicators by country/region and demographic aspect. Returns data on population size, growth rates, age structure, fertility/mortality, urban-rural splits, migration, dependency ratios, and demographic transition analysis. Price: `10` credits. Parameters: `calculate_dependency_ratios`, `country_or_region`, `demographic_aspect`, `include_urban_rural`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "population-demographics"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "population-demographics"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "population-demographics"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "population-demographics"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "population-demographics"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "population-demographics"
  }
}
```

## Call This Tool
Product slug: `population-demographics`

Marketplace page: https://www.agentpmt.com/marketplace/population-demographics

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Global-Population--Demographics-Data",
    "arguments": {
      "action": "query_population_data",
      "calculate_dependency_ratios": true,
      "country_or_region": "example country or region",
      "demographic_aspect": "all",
      "include_urban_rural": false,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "population-demographics",
  "parameters": {
    "action": "query_population_data",
    "calculate_dependency_ratios": true,
    "country_or_region": "example country or region",
    "demographic_aspect": "all",
    "include_urban_rural": false,
    "time_period": "latest"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `query_population_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/population-demographics
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
