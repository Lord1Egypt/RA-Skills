---
name: global-digital-economy-connectivity-data
description: "Global Digital Economy & Connectivity Data: Query internet penetration, mobile subscriptions, broadband access, e-government readiness, and. Use when an agent needs global digital economy & connectivity data, digital economy technology, research internet penetration rates by country, compare mobile subscription trends across regions, track broadband access growth over time, analyze e government readiness scores, query digital data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/digital-economy-technology
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/digital-economy-technology"}}
---
# Global Digital Economy & Connectivity Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore digital economy and technology adoption data for any country in the world. Look up internet penetration rates, mobile subscriptions, broadband access, e-government readiness scores, and ICT infrastructure indicators. Track digital growth, identify connectivity gaps, and compare how countries are progressing in the digital era — all from a comprehensive global data set.

## Product Instructions
### Digital Economy & Technology Data

Access comprehensive digital economy statistics from the World Bank's World Development Indicators database covering 200+ countries. Query internet penetration, mobile and broadband infrastructure, ICT trade metrics, digital divide analysis, and regional comparisons using natural language country names.

#### Actions

##### query_digital_data

Fetch digital economy and technology indicator data for a country or region.

**Required Parameters:**
- `action` (string): Must be `"query_digital_data"`
- `country_or_region` (string): Country or region name in plain language (e.g., `"South Korea"`, `"Kenya"`, `"World"`)

**Optional Parameters:**
- `digital_aspect` (string, default: `"all"`): Digital domain to query. One of:
  - `"internet"` - Internet users (% of population and total count)
  - `"mobile"` - Mobile cellular subscriptions (total and per 100 people) and fixed telephone subscriptions
  - `"broadband"` - Fixed broadband (total and per 100 people) and mobile broadband subscriptions
  - `"ict"` - ICT goods exports/imports, ICT service exports, high-tech exports (value and % of manufactured)
  - `"infrastructure"` - Secure internet servers, telephone subscriptions, fixed broadband
  - `"e_government"` - E-government context (limited; World Bank data does not include EGDI directly)
  - `"all"` - All available digital indicators
- `calculate_digital_divide` (boolean, default: `false`): Calculate digital access gaps (100% minus current access rates) for internet, broadband, and mobile
- `time_period` (string, default: `"latest"`): Time period for data. Options:
  - `"latest"` - Most recent available data
  - `"last_5_years"` - Last 5 years of data
  - `"last_10_years"` - Last 10 years of data
  - `"YYYY:YYYY"` - Specific year range (e.g., `"2015:2020"`). Years must be between 1960 and current year.
  - `"YYYY"` - A single year (e.g., `"2020"`)
- `include_regional_comparison` (boolean, default: `true`): Include comparison data with digital leaders (World average, High Income countries, South Korea, Singapore)
- `include_trends` (boolean, default: `true`): Include trend analysis with CAGR (Compound Annual Growth Rate) calculations when historical data is available

**Example - Latest internet data with digital divide:**
```json
{
  "action": "query_digital_data",
  "country_or_region": "Kenya",
  "digital_aspect": "internet",
  "time_period": "latest",
  "calculate_digital_divide": true
}
```

**Example - Broadband growth trends:**
```json
{
  "action": "query_digital_data",
  "country_or_region": "South Korea",
  "digital_aspect": "broadband",
  "time_period": "last_10_years",
  "include_trends": true
}
```

**Example - All digital indicators with comparison:**
```json
{
  "action": "query_digital_data",
  "country_or_region": "India",
  "digital_aspect": "all",
  "time_period": "latest",
  "calculate_digital_divide": true,
  "include_regional_comparison": true
}
```

**Example - ICT trade for a specific period:**
```json
{
  "action": "query_digital_data",
  "country_or_region": "China",
  "digital_aspect": "ict",
  "time_period": "2015:2020"
}
```

**Example - Mobile coverage for a region:**
```json
{
  "action": "query_digital_data",
  "country_or_region": "Sub-Saharan Africa",
  "digital_aspect": "mobile",
  "time_period": "latest"
}
```

#### Supported Countries and Regions

Accepts plain-language names. Examples of supported inputs:

- **Countries**: `"United States"`, `"USA"`, `"India"`, `"South Korea"`, `"Nigeria"`, `"Brazil"`, `"Singapore"`, `"Kenya"`, etc. (200+ countries)
- **Regions**: `"Sub-Saharan Africa"`, `"Latin America"`, `"Middle East"`, `"South Asia"`, `"East Asia"`, `"Europe"`
- **Income groups**: `"Low Income"`, `"Lower Middle Income"`, `"Upper Middle Income"`, `"High Income"`, `"OECD"`
- **Global**: `"World"` or `"Global"`
- **ISO3 codes**: 3-letter codes like `"USA"`, `"IND"`, `"KOR"` are also accepted

Country names support partial matching, so `"UK"` maps to United Kingdom and `"America"` maps to USA.

#### Available Indicators

##### Internet Access
- Internet Users (% of population)
- Internet Users (total number)

##### Mobile and Telephony
- Mobile Cellular Subscriptions (total)
- Mobile Subscriptions (per 100 people)
- Fixed Telephone Subscriptions

##### Broadband
- Fixed Broadband Subscriptions (total)
- Fixed Broadband (per 100 people)
- Mobile Broadband Subscriptions

##### ICT Trade
- ICT Goods Exports (% of total goods exports)
- ICT Goods Imports (% of total goods imports)
- ICT Service Exports (% of service exports)
- High-Technology Exports (current US$)
- High-Tech Exports (% of manufactured exports)

##### Infrastructure and R&D
- Secure Internet Servers (per million people)
- Researchers in R&D (per million people)
- R&D Expenditure (% of GDP)

#### Response Structure

Responses include:
- **Indicator data** with latest values, proper units (%, per 100 people, total numbers, current US$), year, and source
- **Trend analysis** with absolute change, percent change, direction (increasing/decreasing/stable), data point count, and CAGR when applicable
- **Digital divide analysis** (when enabled): internet access gap, fixed broadband gap, mobile coverage status
- **Regional comparison** benchmarked against World average, High Income countries, South Korea, and Singapore
- **Insights** covering internet penetration levels, mobile adoption, broadband infrastructure, ICT export significance, digital expansion rates, and SDG 9.c progress
- **SDG 9.c alignment** (Universal and affordable access to internet)

#### Digital Divide Analysis

When `calculate_digital_divide` is `true`, the response includes:
- **Internet access gap**: Current access percentage and the gap (100% minus access)
- **Fixed broadband gap**: Current subscriptions per 100 people and gap to universal access
- **Mobile coverage**: Subscriptions per 100 people and whether coverage exceeds population (multiple devices per person)

#### Workflows

1. **Digital Readiness Assessment**: Query all digital indicators for a country with regional comparison to benchmark against digital leaders
2. **Digital Divide Analysis**: Enable `calculate_digital_divide` for internet and broadband aspects to quantify access gaps
3. **ICT Trade Research**: Use `digital_aspect: "ict"` with trends to track technology export growth over time
4. **Infrastructure Planning**: Query broadband and infrastructure aspects over the last 10 years to identify growth patterns
5. **SDG 9.c Monitoring**: Query internet penetration with regional comparison to assess progress toward universal access

#### Notes

- Data sourced from World Bank World Development Indicators
- Mobile subscriptions can exceed 100 per 100 people due to multiple SIMs/devices per person
- Fixed broadband means wired broadband subscriptions, not mobile broadband
- Mobile broadband refers to internet via mobile networks (3G, 4G, 5G)
- ICT goods include computers, telecom equipment, and consumer electronics
- High-tech exports include aerospace, computers, pharmaceuticals, and instruments
- Secure internet servers are measured per 1 million people
- The E-Government Development Index (EGDI) is not available in World Bank data; the `"e_government"` aspect returns an empty indicator set
- Data availability varies by country and indicator; most recent data may be 1-2 years old
- When an unrecognized `digital_aspect` is provided, the tool defaults to internet and mobile indicators
- Regional comparison benchmarks against World, High Income, South Korea, and Singapore using internet_users, mobile_subscriptions_per100, and fixed_broadband_per100
- Trend CAGR is only calculated for multi-year periods where both start and end values are positive

## When To Use
- Use this skill for `Global Digital Economy & Connectivity Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global digital economy & connectivity data, digital economy technology, research internet penetration rates by country, compare mobile subscription trends across regions, track broadband access growth over time, analyze e government readiness scores, query digital data, country or region.
- Supported action names: `query_digital_data`.

## Use Cases
- Research internet penetration rates by country
- Compare mobile subscription trends across regions
- Track broadband access growth over time
- Analyze e-government readiness scores
- Study the digital divide between countries
- Monitor ICT infrastructure development
- Assess digital adoption rates by region
- Research technology access gaps
- Support policy research on digital inclusion
- Compare connectivity metrics across income groups

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_digital_data` (action slug: `query-digital-data`): Fetch digital economy and technology indicator data for a country or region, including internet penetration, mobile subscriptions, broadband access, ICT trade metrics, and digital divide analysis. Price: `5` credits. Parameters: `calculate_digital_divide`, `country_or_region`, `digital_aspect`, `include_regional_comparison`, `include_trends`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "digital-economy-technology"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "digital-economy-technology"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "digital-economy-technology"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "digital-economy-technology"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "digital-economy-technology"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "digital-economy-technology"
  }
}
```

## Call This Tool
Product slug: `digital-economy-technology`

Marketplace page: https://www.agentpmt.com/marketplace/digital-economy-technology

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
    "name": "Global-Digital-Economy--Connectivity-Data",
    "arguments": {
      "action": "query_digital_data",
      "calculate_digital_divide": false,
      "country_or_region": "example country or region",
      "digital_aspect": "all",
      "include_regional_comparison": true,
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
  "name": "digital-economy-technology",
  "parameters": {
    "action": "query_digital_data",
    "calculate_digital_divide": false,
    "country_or_region": "example country or region",
    "digital_aspect": "all",
    "include_regional_comparison": true,
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
- If `query_digital_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/digital-economy-technology
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
