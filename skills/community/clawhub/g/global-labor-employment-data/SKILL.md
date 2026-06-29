---
name: global-labor-employment-data
description: "Global Labor & Employment Data: Query labor force participation, unemployment rates, sector employment breakdowns, gender gaps, and youth employment for. Use when an agent needs global labor & employment data, labor market employment, research labor force participation rates by country, compare unemployment rates across regions, analyze employment by sector breakdown, study gender gaps in workforce participation, query labor data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/labor-market-employment
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/labor-market-employment"}}
---
# Global Labor & Employment Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Access workforce and employment data for any country in the world. Look up labor force participation rates, unemployment figures, sector breakdowns, gender employment gaps, and youth employment trends. Compare workforce metrics across countries, track labor market shifts over time, and benchmark regional performance — all from a comprehensive global data set.

## Product Instructions
### Labor Market & Employment Data

Access comprehensive labor market and employment statistics from the World Bank's World Development Indicators database covering 200+ countries. Query labor force participation, unemployment rates, employment by sector, gender gap analysis, employment quality metrics, and regional comparisons using natural language country names.

#### Actions

##### query_labor_data

Fetch labor market and employment indicator data for a country or region.

**Required Parameters:**
- `action` (string): Must be `"query_labor_data"`
- `country_or_region` (string): Country or region name in plain language (e.g., `"Kenya"`, `"South Korea"`, `"World"`)

**Optional Parameters:**
- `demographic_filter` (string, default: `null`): Filter indicators by demographic category. One of:
  - `"gender"` - Male/female labor force participation and unemployment rates, plus total rates
  - `"youth"` - Youth unemployment (ages 15-24) by gender, plus total unemployment and labor force participation
  - `"sector"` - Employment by economic sector (agriculture, industry, services), plus total labor force and unemployment
  - `"total"` - Overall labor force participation, unemployment, wage/salaried workers, and vulnerable employment
  - `null` or `"all"` - All available labor market indicators
- `calculate_gender_gaps` (boolean, default: `true`): Calculate gender gaps as male rate minus female rate for labor force participation, unemployment, and youth unemployment. Positive gap means males higher, negative means females higher.
- `include_sector_employment` (boolean, default: `true`): Include employment by sector breakdown (agriculture, industry, services) even when a different demographic filter is selected
- `time_period` (string, default: `"latest"`): Time period for data. Options:
  - `"latest"` - Most recent available data
  - `"last_5_years"` - Last 5 years of data
  - `"last_10_years"` - Last 10 years of data
  - `"YYYY:YYYY"` - Specific year range (e.g., `"2015:2020"`). Years must be between 1960 and current year.
  - `"YYYY"` - A single year (e.g., `"2020"`)
- `include_regional_comparison` (boolean, default: `true`): Include comparison data with World average, High Income countries, East Asia & Pacific, and Latin America & Caribbean
- `include_trends` (boolean, default: `true`): Include trend analysis with CAGR (Compound Annual Growth Rate) calculations when historical data is available

**Example - Gender-disaggregated data with gap analysis:**
```json
{
  "action": "query_labor_data",
  "country_or_region": "Kenya",
  "demographic_filter": "gender",
  "calculate_gender_gaps": true,
  "time_period": "latest"
}
```

**Example - Youth unemployment trends:**
```json
{
  "action": "query_labor_data",
  "country_or_region": "Spain",
  "demographic_filter": "youth",
  "time_period": "last_10_years",
  "include_trends": true
}
```

**Example - All labor indicators with full analysis:**
```json
{
  "action": "query_labor_data",
  "country_or_region": "India",
  "demographic_filter": "all",
  "calculate_gender_gaps": true,
  "include_sector_employment": true,
  "time_period": "latest",
  "include_regional_comparison": true
}
```

**Example - Sector employment breakdown:**
```json
{
  "action": "query_labor_data",
  "country_or_region": "Vietnam",
  "demographic_filter": "sector",
  "include_sector_employment": true,
  "time_period": "latest"
}
```

**Example - Regional labor market overview:**
```json
{
  "action": "query_labor_data",
  "country_or_region": "Sub-Saharan Africa",
  "demographic_filter": "total",
  "time_period": "last_5_years",
  "include_regional_comparison": true
}
```

#### Supported Countries and Regions

Accepts plain-language names. Examples of supported inputs:

- **Countries**: `"United States"`, `"USA"`, `"India"`, `"South Korea"`, `"Nigeria"`, `"Brazil"`, `"Spain"`, `"Kenya"`, etc. (200+ countries)
- **Regions**: `"Sub-Saharan Africa"`, `"Latin America"`, `"Middle East"`, `"South Asia"`, `"East Asia"`, `"Europe"`
- **Income groups**: `"Low Income"`, `"Lower Middle Income"`, `"Upper Middle Income"`, `"High Income"`, `"OECD"`
- **Global**: `"World"` or `"Global"`
- **ISO3 codes**: 3-letter codes like `"USA"`, `"IND"`, `"KOR"` are also accepted

Country names support partial matching, so `"UK"` maps to United Kingdom and `"America"` maps to USA.

#### Available Indicators

##### Labor Force Participation
- Labor Force Participation Rate, Total (% of population ages 15+)
- Labor Force Participation Rate, Male (% of male population ages 15+)
- Labor Force Participation Rate, Female (% of female population ages 15+)

##### Unemployment
- Unemployment Rate, Total (% of total labor force)
- Unemployment Rate, Male (% of male labor force)
- Unemployment Rate, Female (% of female labor force)
- Youth Unemployment Rate (% of total labor force ages 15-24)
- Youth Unemployment Rate, Male (% ages 15-24)
- Youth Unemployment Rate, Female (% ages 15-24)

##### Employment by Sector
- Employment in Agriculture (% of total employment)
- Employment in Industry (% of total employment)
- Employment in Services (% of total employment)

##### Employment Quality
- Wage and Salaried Workers (% of total employment) -- proxy for formal employment
- Vulnerable Employment (% of total employment) -- own-account workers + contributing family workers
- Self-Employed (% of total employment)

##### Employment by Gender
- Employment to Population Ratio, Male (%)
- Employment to Population Ratio, Female (%)

##### Other
- Part-Time Employment (% of total employment)

#### Response Structure

Responses include:
- **Indicator data** with latest values, units (% of labor force, % of population ages 15+, %), year, country name, and source
- **Trend analysis** with absolute change, percent change, direction (increasing/decreasing/stable), data point count, and CAGR when applicable
- **Gender gap analysis** (when enabled): labor force participation gap, unemployment gap, and youth unemployment gap with interpretation of gap direction and magnitude
- **Regional comparison** benchmarked against World average, High Income countries, East Asia & Pacific, and Latin America & Caribbean
- **Insights** covering participation levels, unemployment severity, youth unemployment, gender gaps, sector composition (agriculture-dependent vs service-based vs industrial), vulnerable employment, formal employment levels, and SDG 8 progress
- **SDG 8.5 alignment** (Full and productive employment and decent work for all)

#### Gender Gap Analysis

When `calculate_gender_gaps` is `true`, the response includes:
- **Labor force participation gap**: Male rate minus female rate with interpretation
- **Unemployment gap**: Male rate minus female rate with interpretation
- **Youth unemployment gap**: Male youth rate minus female youth rate

Positive gap = males higher. Negative gap = females higher.

#### Workflows

1. **Gender Equity Assessment**: Use `demographic_filter: "gender"` with `calculate_gender_gaps: true` to analyze male-female disparities in labor force participation and unemployment
2. **Youth Employment Crisis**: Use `demographic_filter: "youth"` with `time_period: "last_10_years"` to track youth unemployment trends
3. **Economic Structure Analysis**: Use `demographic_filter: "sector"` to understand whether a country is agriculture-dependent, service-based, or industrial
4. **Job Quality Assessment**: Query all indicators and review vulnerable employment and wage/salaried worker percentages as proxies for informal vs formal employment
5. **SDG 8 Monitoring**: Query total labor indicators with regional comparison to assess progress toward decent work goals

#### Notes

- Data sourced from World Bank World Development Indicators
- Labor force participation = % of population ages 15+ that is economically active
- Unemployment = % of labor force without work but available and seeking employment
- Youth unemployment covers ages 15-24
- Vulnerable employment = own-account workers + contributing family workers (proxy for job insecurity)
- Wage/salaried workers serves as a proxy for formal employment
- Employment by sector percentages should sum to approximately 100% (agriculture + industry + services)
- Gender gaps are calculated as male rate minus female rate
- When `demographic_filter` is unrecognized, the tool defaults to total labor force indicators
- When `include_sector_employment` is `true` and the demographic filter is not already `"sector"`, sector indicators are appended to the results
- Regional comparison uses lfp_total, lfp_female, unemployment_total, and unemployment_youth as key benchmarking indicators
- Data availability varies by country; some developing countries may have limited labor force survey coverage
- Most recent data is typically 1-2 years behind the current year
- Trend CAGR is only calculated for multi-year periods where both start and end values are positive

## When To Use
- Use this skill for `Global Labor & Employment Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global labor & employment data, labor market employment, research labor force participation rates by country, compare unemployment rates across regions, analyze employment by sector breakdown, study gender gaps in workforce participation, query labor data, country or region.
- Supported action names: `query_labor_data`.

## Use Cases
- Research labor force participation rates by country
- Compare unemployment rates across regions
- Analyze employment by sector breakdown
- Study gender gaps in workforce participation
- Track youth unemployment trends
- Benchmark formal vs informal employment
- Monitor wage and labor market shifts
- Support workforce equity research
- Assess progress toward SDG 8 decent work targets
- Compare regional labor market performance

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_labor_data` (action slug: `query-labor-data`): Fetch labor market and employment indicator data for a country or region, including labor force participation, unemployment rates, sector employment, gender gap analysis, and employment quality metrics. Price: `5` credits. Parameters: `calculate_gender_gaps`, `country_or_region`, `demographic_filter`, `include_regional_comparison`, `include_sector_employment`, `include_trends`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "labor-market-employment"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "labor-market-employment"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "labor-market-employment"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "labor-market-employment"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "labor-market-employment"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "labor-market-employment"
  }
}
```

## Call This Tool
Product slug: `labor-market-employment`

Marketplace page: https://www.agentpmt.com/marketplace/labor-market-employment

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
    "name": "Global-Labor--Employment-Data",
    "arguments": {
      "action": "query_labor_data",
      "calculate_gender_gaps": true,
      "country_or_region": "example country or region",
      "demographic_filter": "gender",
      "include_regional_comparison": true,
      "include_sector_employment": true,
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
  "name": "labor-market-employment",
  "parameters": {
    "action": "query_labor_data",
    "calculate_gender_gaps": true,
    "country_or_region": "example country or region",
    "demographic_filter": "gender",
    "include_regional_comparison": true,
    "include_sector_employment": true,
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
- If `query_labor_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/labor-market-employment
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
