---
name: global-agriculture-food-security-data
description: "Global Agriculture & Food Security Data: Query agricultural production, food security, malnutrition, land use, and productivity indicators for any. Use when an agent needs global agriculture & food security data, agriculture food security, research food security levels by country, track crop yield trends over time, analyze agricultural productivity across regions, study undernourishment and malnutrition rates, query agriculture data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/agriculture-food-security
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/agriculture-food-security"}}
---
# Global Agriculture & Food Security Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore agriculture and food security data for any country in the world. Look up crop yields, undernourishment rates, agricultural productivity, land use patterns, and rural development indicators. Compare food security outcomes across countries, track trends in agricultural output, and assess progress toward ending hunger — all from a comprehensive global data set.

## Product Instructions
### Agriculture & Food Security Data

Access comprehensive agricultural statistics and food security indicators from the World Bank's World Development Indicators database through a natural language interface.

#### Overview

This tool provides natural language access to World Bank agricultural data covering crop production, food security, land use, productivity metrics, and economic context. It supports 200+ countries and regional aggregations, with built-in trend analysis, regional comparisons, and SDG 2 (Zero Hunger) alignment tracking.

Data is sourced from the World Bank World Development Indicators and FAO databases.

#### Actions

##### query_agriculture_data

Query agricultural and food security indicators for any country or region.

###### Required Parameters

- **action** (string): Must be `"query_agriculture_data"`
- **country_or_region** (string): Country or region name in plain language
  - Country names: `"India"`, `"Brazil"`, `"Kenya"`, `"United States"`
  - Regions: `"Sub-Saharan Africa"`, `"Latin America"`, `"South Asia"`, `"East Asia"`, `"Middle East"`
  - Global: `"World"` or `"Global"`
  - Income groups: `"Low Income"`, `"Lower Middle Income"`, `"Upper Middle Income"`, `"High Income"`
  - ISO3 codes also accepted: `"USA"`, `"IND"`, `"KEN"`

###### Optional Parameters

- **agriculture_topic** (string, default: `"all"`): Topic filter for indicators
  - `"production"` - Cereal yield, crop production index, livestock production index, food production index
  - `"food_security"` - Undernourishment prevalence, food deficit, food production index, cereal import dependency
  - `"malnutrition"` - Undernourishment prevalence, food deficit (caloric deficits)
  - `"land_use"` - Agricultural land, arable land, arable land per person, forest area, irrigated land
  - `"productivity"` - Cereal yield, fertilizer consumption, agricultural machinery, agriculture value added growth
  - `"all"` - All available agricultural indicators (20 indicators)

- **time_period** (string, default: `"latest"`): Time period for data retrieval
  - `"latest"` - Most recent available data point
  - `"last_5_years"` - Last 5 years of data
  - `"last_10_years"` - Last 10 years of data
  - `"YYYY:YYYY"` - Specific year range (e.g., `"2015:2020"`), years must be between 1960 and current year
  - `"YYYY"` - Single specific year (e.g., `"2020"`)

- **include_rural_context** (boolean, default: `true`): Include rural population percentage and agricultural employment data for additional context

- **include_regional_comparison** (boolean, default: `true`): Include comparison data from World, Sub-Saharan Africa, South Asia, Latin America & Caribbean, East Asia & Pacific, and Middle East & North Africa

- **include_trends** (boolean, default: `true`): Include trend analysis with absolute and percentage change, direction assessment (improving/worsening/stable), when historical data is available

###### Example: Latest data for a country

```json
{
  "action": "query_agriculture_data",
  "country_or_region": "India",
  "agriculture_topic": "all",
  "time_period": "latest"
}
```

###### Example: Food security trends over time

```json
{
  "action": "query_agriculture_data",
  "country_or_region": "Kenya",
  "agriculture_topic": "food_security",
  "time_period": "last_10_years",
  "include_trends": true
}
```

###### Example: Regional productivity analysis

```json
{
  "action": "query_agriculture_data",
  "country_or_region": "Sub-Saharan Africa",
  "agriculture_topic": "productivity",
  "time_period": "last_5_years"
}
```

###### Example: Land use with minimal extras

```json
{
  "action": "query_agriculture_data",
  "country_or_region": "Brazil",
  "agriculture_topic": "land_use",
  "time_period": "2010:2020",
  "include_rural_context": false,
  "include_regional_comparison": false
}
```

###### Example: Malnutrition data for income group

```json
{
  "action": "query_agriculture_data",
  "country_or_region": "Low Income",
  "agriculture_topic": "malnutrition",
  "time_period": "latest"
}
```

#### Response Structure

Responses include:

- **data**: Indicator values with human-readable names, latest values, years, units, country name, and source attribution
- **productivity_metrics**: Derived metrics including cereal productivity assessment (Low/Moderate/Good/High with recommendations), agricultural efficiency ratio (GDP share vs employment share), and land productivity context
- **rural_context**: Rural population percentage and agricultural employment share (when `include_rural_context` is true)
- **trends**: For each indicator with historical data: oldest/newest values and years, absolute and percentage change, direction (improving/worsening/stable), and data point count
- **regional_comparison**: Comparison values from 6 major regions (when `include_regional_comparison` is true)
- **insights**: Human-readable analytical insights based on data values, trends, and regional comparisons
- **sdg_alignment**: SDG 2 Zero Hunger alignment information
- **data_notes**: Context notes about methodology and data quality

#### Key Indicators Reference

| Indicator | Unit | Description |
|-----------|------|-------------|
| cereal_yield | kg per hectare | Cereal productivity (global avg ~4,000) |
| crop_production_index | index (2014-2016=100) | Overall crop production level |
| livestock_production_index | index (2014-2016=100) | Livestock production level |
| agricultural_land | % of land area | Land used for agriculture |
| arable_land | % of land area | Land suitable for crops |
| arable_land_per_person | hectares per person | Per capita arable land |
| forest_area | % of land area | Forest coverage |
| irrigated_land | % of agricultural land | Irrigated portion of farmland |
| undernourishment_prevalence | % of population | Population unable to acquire enough food |
| food_production_index | index (2014-2016=100) | Overall food production level |
| food_deficit | kcal/person/day | Depth of caloric food deficit |
| fertilizer_consumption | kg/ha of arable land | Fertilizer use intensity |
| agricultural_machinery | number of tractors | Mechanization level |
| agricultural_methane | % of total emissions | Agriculture's methane contribution |
| agriculture_value_added | % of GDP | Agriculture's share of economy |
| agriculture_value_added_growth | annual % growth | Agriculture GDP growth rate |
| employment_agriculture | % of total employment | Agricultural workforce share |
| rural_population | % of total population | Rural population share |
| cereal_import_dependency | % | Reliance on cereal imports |

#### Productivity Assessments

Cereal yield classifications used in productivity_metrics:
- **Low productivity**: Below 2,000 kg/ha - significant improvement potential
- **Moderate productivity**: 2,000-4,000 kg/ha - room for improvement
- **Good productivity**: 4,000-6,000 kg/ha - above average
- **High productivity**: Above 6,000 kg/ha - excellent yields

#### Workflows

1. **Country Agricultural Profile**: Query with `agriculture_topic: "all"` and `time_period: "latest"` to get a comprehensive snapshot of a country's agricultural sector
2. **Food Security Monitoring**: Query `agriculture_topic: "food_security"` with `time_period: "last_10_years"` and `include_trends: true` to track food security progress
3. **Cross-Country Comparison**: Run separate queries for multiple countries with `include_regional_comparison: true` to compare against regional benchmarks
4. **Productivity Gap Analysis**: Query `agriculture_topic: "productivity"` to get yield assessments and efficiency ratios with recommendations

#### Notes

- Data sourced from World Bank World Development Indicators and FAO
- Most recent data is typically 1-3 years behind current year due to collection/processing delays
- Data availability varies by country and indicator; some countries may have gaps
- Production indices use 2014-2016 as the base period (value of 100)
- Cereal yield is based on harvested area, not planted area
- Undernourishment is based on minimum dietary energy requirements
- When a country name is not recognized, a descriptive error is returned with guidance
- If no country_or_region is provided, returns an error requesting the parameter
- The tool supports partial name matching for country lookups (e.g., "korea" matches "south korea")
- Trend direction for undernourishment and food deficit is inverted (decrease = improving)
- Regional comparison fetches the top 5 key indicators (not all) for performance reasons

#### Pricing

$0.05 per request

## When To Use
- Use this skill for `Global Agriculture & Food Security Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global agriculture & food security data, agriculture food security, research food security levels by country, track crop yield trends over time, analyze agricultural productivity across regions, study undernourishment and malnutrition rates, query agriculture data, country or region.
- Supported action names: `query_agriculture_data`.

## Use Cases
- Research food security levels by country
- Track crop yield trends over time
- Analyze agricultural productivity across regions
- Study undernourishment and malnutrition rates
- Compare land use patterns between countries
- Monitor rural population and agricultural employment
- Assess progress toward SDG 2 zero hunger targets
- Research agricultural value added as percentage of GDP
- Evaluate food production capacity by region
- Support policy research on rural development

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_agriculture_data` (action slug: `query-agriculture-data`): Fetch agricultural and food security indicator data for a country or region, including crop yields, undernourishment rates, land use, productivity metrics, and rural development context. Price: `5` credits. Parameters: `agriculture_topic`, `country_or_region`, `include_regional_comparison`, `include_rural_context`, `include_trends`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "agriculture-food-security"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "agriculture-food-security"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "agriculture-food-security"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "agriculture-food-security"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "agriculture-food-security"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "agriculture-food-security"
  }
}
```

## Call This Tool
Product slug: `agriculture-food-security`

Marketplace page: https://www.agentpmt.com/marketplace/agriculture-food-security

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
    "name": "Global-Agriculture--Food-Security-Data",
    "arguments": {
      "action": "query_agriculture_data",
      "agriculture_topic": "all",
      "country_or_region": "example country or region",
      "include_regional_comparison": true,
      "include_rural_context": true,
      "include_trends": true,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "agriculture-food-security",
  "parameters": {
    "action": "query_agriculture_data",
    "agriculture_topic": "all",
    "country_or_region": "example country or region",
    "include_regional_comparison": true,
    "include_rural_context": true,
    "include_trends": true,
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
- If `query_agriculture_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/agriculture-food-security
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
