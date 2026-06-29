---
name: global-gender-equality-data
description: "Global Gender Equality Data: Access gender equality indicators for any country or region. Use when an agent needs global gender equality data, gender equality women s empowerment, analyze gender gaps in labor force participation, compare education parity across countries, research women's political representation, track maternal health outcomes by region, query gender data, country or region through AgentPMT-hosted remote tool calls. Discovery terms: global gender equality data."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/gender-equality-women-s-empowerment
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/gender-equality-women-s-empowerment"}}
---
# Global Gender Equality Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Dive into gender equality data for any country in the world. Explore labor force participation gaps, education parity, political representation, legal rights scores, and maternal health outcomes. Compare male and female indicators side by side, track progress over time, and see how countries measure up on gender parity — all from a comprehensive global data set.

## Product Instructions
### Gender Equality Data

#### Overview

Query World Bank gender equality and women's empowerment indicators for any country or region. Access data on labor force participation gaps, education parity indices, political representation, legal framework scores, maternal health, economic empowerment, and attitudes toward violence against women. All indicators are aligned with SDG 5 (Achieve gender equality and empower all women and girls). Data sourced from the World Bank Data360 API and Women, Business and the Law Database.

#### Actions

##### query_gender_data

Query gender equality indicators by country/region and gender aspect.

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | Must be `"query_gender_data"` |
| `country_or_region` | string | Country name or region. Examples: `"Rwanda"`, `"India"`, `"United States"`, `"Africa"`, `"Latin America"` |

**Optional Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `gender_aspect` | string | `"all"` | Specific gender dimension to query. One of: `"labor"`, `"education"`, `"political"`, `"legal"`, `"health"`, `"economic"`, `"violence"`, `"all"` |
| `calculate_gaps` | boolean | `true` | Automatically calculate gender gaps (male minus female) where male/female pairs exist |
| `time_period` | string | `"latest"` | Time period for data. Accepts: `"latest"`, a single year like `"2020"`, a range like `"2010:2020"`, or shorthand `"last5"` / `"last10"` |

**Gender Aspects:**

- **`labor`** -- Female and male labor force participation rates, female-to-male ratio, employment rates by gender
- **`education`** -- Female and male adult literacy rates, Gender Parity Index (GPI) for primary, secondary, and tertiary education enrollment
- **`political`** -- Proportion of parliamentary seats held by women (%), proportion of women in ministerial positions (%)
- **`legal`** -- Women, Business and the Law Index (0-100 scale measuring legal protections and economic opportunities)
- **`health`** -- Maternal mortality ratio (per 100,000 live births), adolescent fertility rate, contraceptive prevalence, antenatal care coverage, skilled birth attendance
- **`economic`** -- Financial account ownership by gender (%), female firm ownership (%)
- **`violence`** -- Attitudes toward intimate partner violence (% of women who believe husband is justified in beating wife)
- **`all`** -- All available indicators combined

###### Example: Political representation in Rwanda

```json
{
  "action": "query_gender_data",
  "country_or_region": "Rwanda",
  "gender_aspect": "political",
  "time_period": "latest"
}
```

###### Example: Labor force gender gaps in India

```json
{
  "action": "query_gender_data",
  "country_or_region": "India",
  "gender_aspect": "labor",
  "calculate_gaps": true,
  "time_period": "latest"
}
```

###### Example: Education parity trends in Sweden

```json
{
  "action": "query_gender_data",
  "country_or_region": "Sweden",
  "gender_aspect": "education",
  "time_period": "2010:2023"
}
```

###### Example: Full gender equality profile for Africa

```json
{
  "action": "query_gender_data",
  "country_or_region": "Africa",
  "gender_aspect": "all",
  "time_period": "latest"
}
```

###### Example: Maternal health in the United States

```json
{
  "action": "query_gender_data",
  "country_or_region": "United States",
  "gender_aspect": "health",
  "time_period": "latest"
}
```

###### Example: Legal framework without gap calculations

```json
{
  "action": "query_gender_data",
  "country_or_region": "Saudi Arabia",
  "gender_aspect": "legal",
  "calculate_gaps": false
}
```

###### Example: Economic empowerment for a specific year

```json
{
  "action": "query_gender_data",
  "country_or_region": "Kenya",
  "gender_aspect": "economic",
  "time_period": "2021"
}
```

#### Workflows

##### Comprehensive Gender Equality Report
1. Call `query_gender_data` with `gender_aspect: "all"` and `calculate_gaps: true` for a full country profile.
2. The response includes indicators across all dimensions, gender gap calculations, contextual interpretations, and SDG 5 alignment summary.

##### Cross-Country Comparison
1. Call `query_gender_data` for each country with the same `gender_aspect` and `time_period`.
2. Compare gender gaps, interpretation levels (e.g., parliamentary representation thresholds), and indicator values side by side.

##### Gender Gap Trend Analysis
1. Call `query_gender_data` with a `time_period` range (e.g., `"2005:2023"`) and `calculate_gaps: true`.
2. For time-series requests, the response includes year-by-year data points for tracking gap evolution.

##### SDG 5 Progress Assessment
1. Call `query_gender_data` with `gender_aspect: "all"` to get all SDG 5-aligned indicators.
2. Review the interpretations against SDG targets (e.g., maternal mortality below 70 per 100,000, parliamentary parity).

##### Regional Gender Landscape
1. Call `query_gender_data` with a region name (e.g., `"Africa"`, `"Latin America"`, `"Middle East"`) and `gender_aspect: "all"`.
2. The response provides regional aggregate indicators weighted by population.

#### Notes

- **Gender gap calculation**: When `calculate_gaps` is true, the tool calculates absolute gap (male - female), percentage gap ((gap / male) * 100), and interpretation: "Near parity" (gap < 1 point), "Male advantage" (male > female), or "Female advantage" (female > male). Gaps are calculated for labor force participation, adult literacy, and financial inclusion.
- **Gender Parity Index (GPI)**: For education indicators, GPI values of 0.97-1.03 are interpreted as "Gender parity achieved". Values below 0.97 indicate female disadvantage; above 1.03 indicate female advantage. GPI is reported for primary, secondary, and tertiary enrollment.
- **Parliamentary representation thresholds**: Interpreted as "Gender parity achieved" (>= 50%), "Strong representation" (40-50%), "Approaching critical mass" (30-40%), "Moderate representation" (20-30%), "Low representation" (10-20%), or "Very low representation" (< 10%).
- **Women, Business and the Law Index**: Scored 0-100 (higher is better). Interpreted as "Excellent legal framework" (90-100), "Strong legal protections" (80-90), "Good protections" (70-80), "Moderate protections" (60-70), "Weak protections" (50-60), "Very weak legal framework" (< 50).
- **Maternal mortality interpretation**: "SDG target achieved" (< 70 per 100,000), "Above target but relatively low" (70-140), "Moderate" (140-300), "High" (300-500), "Very high" (> 500). SDG 3.1 target is below 70 per 100,000 live births.
- **Country input**: Accepts common country names (e.g., `"United States"`, `"South Korea"`), and supports partial matching. Unrecognized countries return a descriptive error.
- **Supported regions**: `"World"`, `"Africa"`, `"Asia"`, `"Europe"`, `"Latin America"`, `"Middle East"`, `"North America"`.
- **Supported countries**: 190+ World Bank member countries including all major economies, African nations, Asian countries, European countries, Latin American countries, and Middle Eastern countries.
- **SDG 5 alignment**: Every response includes an `sdg_alignment` section referencing SDG 5 and its targets (5.1 through 5.c) on gender equality, violence elimination, and women's empowerment.
- **time_period validation**: Accepts `"latest"`, `"last5"`, `"last10"`, a 4-digit year, or a `YYYY:YYYY` range. Invalid formats return a validation error.
- **Concurrency**: Indicator fetches are batched concurrently (up to 10 simultaneous API calls) for performance.
- **Data availability**: World Bank data may lag 1-3 years behind the current year. Some indicators are not collected in all countries. Regional aggregates are weighted by population.
- **Values are rounded** to 2 decimal places where applicable.
- **Data source**: World Bank Data360 (World Development Indicators) and Women, Business and the Law Database, updated regularly.

## When To Use
- Use this skill for `Global Gender Equality Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global gender equality data, gender equality women s empowerment, analyze gender gaps in labor force participation, compare education parity across countries, research women's political representation, track maternal health outcomes by region, query gender data, country or region.
- Supported action names: `query_gender_data`.

## Use Cases
- Analyze gender gaps in labor force participation
- Compare education parity across countries
- Research women's political representation
- Track maternal health outcomes by region
- Evaluate legal rights and Women Business and Law scores
- Study economic inclusion and financial access by gender
- Monitor progress toward SDG 5 targets
- Assess attitudes toward violence against women
- Compare male vs female employment rates
- Research reproductive health indicators

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_gender_data` (action slug: `query-gender-data`): Query World Bank gender equality and women's empowerment indicators by country/region and gender aspect. Returns data on labor force participation gaps, education parity indices, political representation, legal framework scores, maternal health, economic empowerment, and attitudes toward violence. Includes automatic gender gap calculations and SDG 5 alignment. Price: `100` credits. Parameters: `calculate_gaps`, `country_or_region`, `gender_aspect`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "gender-equality-women-s-empowerment"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "gender-equality-women-s-empowerment"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "gender-equality-women-s-empowerment"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "gender-equality-women-s-empowerment"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "gender-equality-women-s-empowerment"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "gender-equality-women-s-empowerment"
  }
}
```

## Call This Tool
Product slug: `gender-equality-women-s-empowerment`

Marketplace page: https://www.agentpmt.com/marketplace/gender-equality-women-s-empowerment

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
    "name": "Global-Gender-Equality-Data",
    "arguments": {
      "action": "query_gender_data",
      "calculate_gaps": true,
      "country_or_region": "example country or region",
      "gender_aspect": "all",
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "gender-equality-women-s-empowerment",
  "parameters": {
    "action": "query_gender_data",
    "calculate_gaps": true,
    "country_or_region": "example country or region",
    "gender_aspect": "all",
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
- If `query_gender_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/gender-equality-women-s-empowerment
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
