---
name: global-energy-power-grid-data
description: "Global Energy & Power Grid Data: Query electricity access rates, renewable vs fossil energy mix, per capita consumption, energy intensity, and clean. Use when an agent needs global energy & power grid data, energy access production, research electricity access rates by country, compare renewable energy adoption across regions, track fossil fuel vs clean energy trends, analyze urban vs rural electricity gaps, query energy data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/energy-access-production
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/energy-access-production"}}
---
# Global Energy & Power Grid Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore energy production and access data for any country in the world. Look up electricity access rates, renewable energy adoption, fossil fuel usage, energy efficiency metrics, and power grid coverage. Compare energy mixes across countries, track the shift toward clean energy, and identify urban-rural electricity gaps — all from a comprehensive global data set.

## Product Instructions
### Energy Access & Production Data

Access World Bank energy indicators including electricity access, renewable energy mix, fossil fuel consumption, energy efficiency, and clean cooking access through a natural language interface.

#### Overview

This tool provides natural language access to World Bank energy data covering electricity access rates (total, urban, rural), energy mix breakdowns (renewable, fossil, nuclear), per capita consumption, energy efficiency metrics, and clean cooking fuel access. It supports SDG 7 (Affordable and Clean Energy) tracking with built-in urban/rural gap analysis and energy mix calculations.

Data is sourced from the World Bank Data API (World Development Indicators).

#### Actions

##### query_energy_data

Query energy indicators for any country or region.

###### Required Parameters

- **action** (string): Must be `"query_energy_data"`
- **country_or_region** (string): Country name, ISO3 code, or region
  - Country names: `"Kenya"`, `"India"`, `"United States"`, `"Germany"`
  - ISO3 codes: `"USA"`, `"KEN"`, `"IND"`
  - If not provided or empty, defaults to `"WLD"` (World)

###### Optional Parameters

- **energy_type** (string, default: `"all"`): Energy category to query
  - `"electricity"` - Electricity access rates: total population, urban, and rural
  - `"renewable"` - Renewable energy share in total final energy consumption and electricity output
  - `"fossil"` - Fossil fuel energy consumption as percentage of total
  - `"efficiency"` - Energy intensity (MJ per $2017 PPP GDP) and energy use per capita
  - `"cooking"` - Clean cooking fuel access as percentage of population
  - `"all"` - All available energy indicators (11 indicators)

- **include_urban_rural_gaps** (boolean, default: `false`): Calculate urban/rural electricity access gap analysis. Returns urban access %, rural access %, and the gap in percentage points. Most useful with `energy_type: "electricity"` or `"all"`.

- **include_energy_mix** (boolean, default: `true`): Calculate energy mix breakdown showing renewable, fossil fuel, and nuclear percentages with an "other" category for the remainder. Applies when `energy_type` is `"all"`, `"renewable"`, or `"fossil"`.

- **time_period** (string, default: `"latest"`): Time period for data retrieval
  - `"latest"` - Most recent available data point
  - `"YYYY"` - Single specific year (e.g., `"2020"`), must be between 1960 and current year
  - `"YYYY:YYYY"` - Year range (e.g., `"2015:2023"`), both years must be between 1960 and current year

###### Example: Electricity access for a country

```json
{
  "action": "query_energy_data",
  "country_or_region": "Kenya",
  "energy_type": "electricity",
  "include_urban_rural_gaps": true
}
```

###### Example: Renewable energy overview

```json
{
  "action": "query_energy_data",
  "country_or_region": "Germany",
  "energy_type": "renewable",
  "time_period": "latest"
}
```

###### Example: Full energy profile with mix breakdown

```json
{
  "action": "query_energy_data",
  "country_or_region": "India",
  "energy_type": "all",
  "include_energy_mix": true,
  "include_urban_rural_gaps": true
}
```

###### Example: Energy efficiency comparison

```json
{
  "action": "query_energy_data",
  "country_or_region": "Japan",
  "energy_type": "efficiency",
  "time_period": "2015:2023"
}
```

###### Example: Clean cooking access

```json
{
  "action": "query_energy_data",
  "country_or_region": "Ethiopia",
  "energy_type": "cooking"
}
```

#### Response Structure

Responses include:

- **country**: Resolved country name from the data
- **energy_type**: The energy category queried
- **indicators**: Object with each indicator containing:
  - `value`: The numeric value
  - `date`: Year of the data point
  - `unit`: Unit of measurement (e.g., "% of population", "kg of oil equivalent per capita")
- **energy_mix** (when `include_energy_mix` is true): Breakdown with renewable_percent, fossil_percent, nuclear_percent, other_percent, and corresponding dates
- **urban_rural_gap** (when `include_urban_rural_gaps` is true): urban_access_percent, rural_access_percent, access_gap_percentage_points, and date
- **sdg_7_context**: SDG 7 tracking with target values, current values, and gap-to-universal for electricity access and clean cooking; renewable energy share note; energy intensity assessment

#### Key Indicators Reference

| Indicator | Unit | Description |
|-----------|------|-------------|
| electricity_access | % of population | Total population with electricity access |
| electricity_urban | % of urban population | Urban electricity access rate |
| electricity_rural | % of rural population | Rural electricity access rate |
| clean_cooking_access | % of population | Access to clean cooking fuels |
| renewable_energy | % of total final energy | Renewable share in energy consumption |
| fossil_fuel_energy | % of total energy | Fossil fuel share of energy |
| renewable_electricity | % of total electricity output | Renewable share in electricity generation |
| alternative_nuclear | % of total energy use | Alternative and nuclear energy share |
| energy_use_per_capita | kg of oil equivalent per capita | Per capita energy consumption |
| electric_power_consumption | kWh per capita | Per capita electricity consumption |
| energy_intensity | MJ/$2017 PPP GDP | Energy intensity (lower = more efficient) |

#### Workflows

1. **Energy Access Assessment**: Query `energy_type: "electricity"` with `include_urban_rural_gaps: true` to identify electrification gaps between urban and rural areas
2. **Energy Transition Tracking**: Query `energy_type: "all"` with `include_energy_mix: true` to see the renewable/fossil/nuclear breakdown and track transition progress
3. **SDG 7 Progress Monitoring**: Query `energy_type: "all"` to get the full sdg_7_context with gap-to-universal calculations for electricity and clean cooking
4. **Efficiency Benchmarking**: Query `energy_type: "efficiency"` for multiple countries to compare energy intensity and per capita consumption

#### Notes

- Data sourced from World Bank World Development Indicators
- Most recent data may be 1-3 years behind the current year due to collection delays
- Data availability varies by country; some indicators may return null for certain countries
- Energy mix percentages may not sum to exactly 100% due to data collection timing differences across indicators
- The "other" category in energy mix is calculated as 100 minus the sum of renewable, fossil, and nuclear
- Urban/rural gap analysis requires both urban and rural data to be available; returns null if either is missing
- SDG 7 context is always included in responses regardless of parameters
- When a country name is not recognized, a ValueError is raised with guidance
- If country_or_region is empty or null, defaults to World (WLD) data
- Country codes that are already 3 uppercase letters pass through directly

#### Pricing

$0.05 per request

## When To Use
- Use this skill for `Global Energy & Power Grid Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global energy & power grid data, energy access production, research electricity access rates by country, compare renewable energy adoption across regions, track fossil fuel vs clean energy trends, analyze urban vs rural electricity gaps, query energy data, country or region.
- Supported action names: `query_energy_data`.

## Use Cases
- Research electricity access rates by country
- Compare renewable energy adoption across regions
- Track fossil fuel vs clean energy trends
- Analyze urban vs rural electricity gaps
- Study energy consumption per capita
- Monitor energy efficiency and intensity metrics
- Assess progress toward SDG 7 clean energy targets
- Compare energy mix breakdowns between countries
- Research clean cooking fuel access
- Evaluate energy transition progress over time

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_energy_data` (action slug: `query-energy-data`): Fetch energy indicators for a country or region, including electricity access rates, renewable and fossil energy mix, per capita consumption, energy efficiency, and clean cooking access with SDG 7 tracking. Price: `10` credits. Parameters: `country_or_region`, `energy_type`, `include_energy_mix`, `include_urban_rural_gaps`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "energy-access-production"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "energy-access-production"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "energy-access-production"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "energy-access-production"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "energy-access-production"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "energy-access-production"
  }
}
```

## Call This Tool
Product slug: `energy-access-production`

Marketplace page: https://www.agentpmt.com/marketplace/energy-access-production

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
    "name": "Global-Energy--Power-Grid-Data",
    "arguments": {
      "action": "query_energy_data",
      "country_or_region": "example country or region",
      "energy_type": "all",
      "include_energy_mix": true,
      "include_urban_rural_gaps": false,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "energy-access-production",
  "parameters": {
    "action": "query_energy_data",
    "country_or_region": "example country or region",
    "energy_type": "all",
    "include_energy_mix": true,
    "include_urban_rural_gaps": false,
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
- If `query_energy_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/energy-access-production
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
