---
name: global-poverty-inequality-data
description: "Global Poverty & Inequality Data: Query World Bank poverty and inequality data by country or region name. Returns poverty headcount at $2.15/$3.65/$6.85 thresholds, Gini index, income shares by quintile/decile, and extreme poverty metrics. Use when an agent needs global poverty & inequality data, global poverty inequality data, development analysis, poverty research, inequality studies, sdg monitoring, query poverty data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/global-poverty-inequality-data
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/global-poverty-inequality-data"}}
---
# Global Poverty & Inequality Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore how poverty and wealth are distributed across 200+ countries using data from the World Bank. Find out what share of a nation's population lives below the international poverty line, how income is split between the richest and poorest households, and whether conditions are improving or getting worse over time. Compare any country against its region or the world, track progress toward ending extreme poverty, and uncover the story behind the numbers with built-in trend analysis and contextual insights.

## Product Instructions
### Global Poverty & Inequality Data

Access poverty rates, Gini coefficients, income distribution, and inequality metrics for 200+ countries from World Bank data. Query by country name in plain language with optional trend analysis and regional comparisons.

#### Actions

##### query_poverty_data

Fetch poverty and inequality data for a country or region from the World Bank World Development Indicators database.

**Required fields:**
- `action` — `"query_poverty_data"`
- `country_or_region` (string) — Country or region name in plain English. Supports 200+ countries (e.g., `"India"`, `"Kenya"`, `"Brazil"`), regional aggregations (e.g., `"Sub-Saharan Africa"`, `"South Asia"`, `"Latin America and Caribbean"`, `"East Asia and Pacific"`, `"Middle East"`), income groups (e.g., `"Low Income"`, `"Upper Middle Income"`, `"High Income"`, `"OECD"`), and global (`"World"` or `"Global"`). Common abbreviations like `"USA"`, `"UK"`, `"UAE"` are accepted. Names longer than 100 characters are rejected.

**Optional fields:**
- `metric_type` (string) — Type of metric to query. Default: `"all"`.
  - `"poverty_headcount"` — Poverty rates at $2.15, $3.65, and $6.85/day thresholds (2017 PPP)
  - `"extreme_poverty"` — $2.15/day poverty line plus poverty gap analysis
  - `"gini_index"` — Gini coefficient (0 = perfect equality, 100 = perfect inequality)
  - `"gini"` — Alias for `gini_index`
  - `"inequality"` — Gini coefficient plus income share held by lowest 20% and highest 20%
  - `"income_distribution"` — Income shares by lowest 10%, lowest 20%, highest 20%, and highest 10%
  - `"all"` — All available metrics including multidimensional poverty headcount
- `time_period` (string) — Time period for data retrieval. Default: `"latest"`.
  - `"latest"` — Most recent complete year
  - `"last_5_years"` — Data from past 5 years
  - `"last_10_years"` — Data from past 10 years
  - `"YYYY:YYYY"` — Specific year range (e.g., `"2015:2020"`, `"2010:2022"`). A dash-separated range like `"2015-2020"` is also accepted and converted automatically.
- `include_regional_comparison` (boolean) — Include regional and global averages (World, Sub-Saharan Africa, South Asia, Latin America & Caribbean, East Asia & Pacific, Middle East & North Africa) for context. Default: `true`. Only the first 3 indicators are compared per region.
- `include_trends` (boolean) — Include trend analysis showing direction (improving/worsening/stable), absolute and percent change, and data point count when historical data is available. Default: `true`. For poverty and inequality indicators, a decrease is classified as "improving."

**Example — Latest poverty data for a country:**
```json
{
  "action": "query_poverty_data",
  "country_or_region": "India",
  "metric_type": "all",
  "time_period": "latest"
}
```

**Example — Inequality trends over a decade:**
```json
{
  "action": "query_poverty_data",
  "country_or_region": "Brazil",
  "metric_type": "inequality",
  "time_period": "2010:2022",
  "include_trends": true
}
```

**Example — Regional poverty overview:**
```json
{
  "action": "query_poverty_data",
  "country_or_region": "Sub-Saharan Africa",
  "metric_type": "poverty_headcount",
  "time_period": "latest",
  "include_regional_comparison": true
}
```

**Example — Gini coefficient lookup:**
```json
{
  "action": "query_poverty_data",
  "country_or_region": "South Africa",
  "metric_type": "gini_index",
  "time_period": "latest"
}
```

**Example — Extreme poverty with no comparisons:**
```json
{
  "action": "query_poverty_data",
  "country_or_region": "Nigeria",
  "metric_type": "extreme_poverty",
  "time_period": "last_5_years",
  "include_regional_comparison": false,
  "include_trends": true
}
```

#### Response Format

Responses include:

- **data** — Per-indicator results with indicator name, latest value, year, unit (% of population, index 0-100, or % of total income), country name, and source attribution.
- **trends** — When enabled, shows oldest/newest year and value, absolute change, percent change, direction (improving/worsening/stable), and data point count.
- **regional_comparison** — When enabled, latest values for the same indicators across World, Sub-Saharan Africa, South Asia, Latin America & Caribbean, East Asia & Pacific, and Middle East & North Africa.
- **insights** — Auto-generated observations such as poverty level severity, inequality classification, trend direction, and comparison to global averages.
- **sdg_alignment** — SDG 1: No Poverty alignment note.
- **data_notes** — Contextual notes about PPP, indicator interpretation, and data freshness.

If a country name is not recognized, the response returns an error with a hint to use full English country names.

#### Supported Metric Indicators

| Metric Type | Indicators Included |
|---|---|
| poverty_headcount | Poverty at $2.15/day, $3.65/day, $6.85/day |
| extreme_poverty | Poverty at $2.15/day, Poverty gap at $2.15/day |
| gini_index / gini | Gini coefficient |
| inequality | Gini coefficient, Income share lowest 20%, Income share highest 20% |
| income_distribution | Income share lowest 10%, lowest 20%, highest 20%, highest 10% |
| all | All of the above plus Multidimensional poverty headcount |

#### Common Workflows

1. **Country poverty profile** — Call with `metric_type: "all"` and `time_period: "latest"` to get a complete snapshot of a country's poverty and inequality status.
2. **Track progress over time** — Use `time_period: "2010:2022"` with `include_trends: true` to see whether poverty is improving or worsening.
3. **Cross-country comparison** — Make separate calls for different countries with the same metric and time period, then compare the results.
4. **Regional benchmarking** — Set `include_regional_comparison: true` to see how a country compares to its region and the world.

#### Important Notes

- Data is sourced from the World Bank World Development Indicators database.
- PPP values are in constant 2017 international dollars.
- Most recent data is typically 1-3 years behind the current year due to collection and processing delays.
- Data availability varies by country and indicator; some countries may have gaps.
- Boolean fields must be actual booleans (`true`/`false`), not strings.
- If an unrecognized `metric_type` is provided, the tool defaults to returning all metrics.
- Aligns with SDG 1 (No Poverty) and SDG 10 (Reduced Inequalities) monitoring.

## When To Use
- Use this skill for `Global Poverty & Inequality Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global poverty & inequality data, global poverty inequality data, development analysis, poverty research, inequality studies, sdg monitoring, query poverty data, country or region.
- Supported action names: `query_poverty_data`.

## Use Cases
- Development analysis
- poverty research
- inequality studies
- SDG monitoring
- policy research

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_poverty_data` (action slug: `query-poverty-data`): Fetch poverty and inequality data for a country or region from the World Bank World Development Indicators database. Price: `5` credits. Parameters: `country_or_region`, `include_regional_comparison`, `include_trends`, `metric_type`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "global-poverty-inequality-data"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "global-poverty-inequality-data"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "global-poverty-inequality-data"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "global-poverty-inequality-data"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "global-poverty-inequality-data"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "global-poverty-inequality-data"
  }
}
```

## Call This Tool
Product slug: `global-poverty-inequality-data`

Marketplace page: https://www.agentpmt.com/marketplace/global-poverty-inequality-data

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
    "name": "Global-Poverty--Inequality-Data",
    "arguments": {
      "action": "query_poverty_data",
      "country_or_region": "example country or region",
      "include_regional_comparison": true,
      "include_trends": true,
      "metric_type": "all",
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "global-poverty-inequality-data",
  "parameters": {
    "action": "query_poverty_data",
    "country_or_region": "example country or region",
    "include_regional_comparison": true,
    "include_trends": true,
    "metric_type": "all",
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
- If `query_poverty_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/global-poverty-inequality-data
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
