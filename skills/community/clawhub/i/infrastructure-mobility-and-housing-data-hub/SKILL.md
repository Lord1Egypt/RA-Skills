---
name: infrastructure-mobility-and-housing-data-hub
description: "Infrastructure, Mobility, and Housing Data Hub: Query World Bank infrastructure data by country or region name. Use when an agent needs infrastructure, mobility, and housing data hub, infrastructure urban development, mobility and transit analysis, infrastructure access benchmarking, housing and permit trend analysis, urban planning support, query infrastructure data, country or region through AgentPMT-hosted remote tool calls. Discovery terms: infrastructure, mobility, and housing data hub."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/infrastructure-urban-development
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/infrastructure-urban-development"}}
---
# Infrastructure, Mobility, and Housing Data Hub

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Find out how well a country's basic systems are working for its people. Look up electricity and internet access rates, safe water and sanitation coverage, road networks, rail lines, port traffic, and urbanization trends for 200+ countries. See how city and rural access compare side by side, identify where the biggest gaps remain, and track progress toward universal coverage goals. Includes logistics performance scores, urban growth rates, slum population data, and alignment with UN Sustainable Development Goals for infrastructure and sustainable cities.

## Product Instructions
### Infrastructure, Mobility, and Housing Data Hub

#### Overview
Natural language interface to World Bank infrastructure and urban development data. Query electricity access, internet penetration, water and sanitation access, road infrastructure, and urbanization indicators by country or region. No indicator codes needed -- just provide a country name and infrastructure type.

Data sourced from the World Bank API. Covers electricity access (total, urban, rural), internet and mobile connectivity, water and sanitation, urban development (population, growth, slum population), transport and logistics (roads, rail, air, ports, LPI), and energy infrastructure. Includes SDG 9 (Industry/Infrastructure) and SDG 11 (Sustainable Cities) progress tracking, access gap calculations, urban-rural divide analysis, and country metadata (region, income level).

#### Actions

##### query_infrastructure_data
Fetches infrastructure and urban development data for a country or region from the World Bank.

**Required parameters:**
- `country_or_region` (string): Country or region name in plain language (e.g., "Kenya", "United States", "South Asia"). Uses natural language matching against the full World Bank country list.

**Optional parameters:**
- `infrastructure_type` (string): One of "electricity", "internet", "water", "roads", "urban", or "all". Defaults to "all" if omitted or not provided.
- `urban_rural_breakdown` (boolean): Include urban/rural disaggregation where available (electricity, water, sanitation). Defaults to false.
- `time_period` (string): "latest" (most recent year), a specific year "2020", a range "2015:2020", or "last5" (last 5 years). Defaults to "latest".
- `include_sdg_targets` (boolean): Include SDG 9 and SDG 11 targets and progress assessment. Defaults to true.
- `include_access_gaps` (boolean): Calculate access gaps (100% minus current access) for coverage indicators. Defaults to true.
- `include_logistics_performance` (boolean): Include Logistics Performance Index (LPI) data. Only applies when infrastructure_type is "roads" or "all". Defaults to false.
- `include_regional_comparison` (boolean): Include a note about regional averages for comparison. Defaults to false.

**Example -- Electricity access in Kenya with urban/rural breakdown:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "Kenya",
  "infrastructure_type": "electricity",
  "urban_rural_breakdown": true
}
```

**Example -- All infrastructure data for India:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "India",
  "infrastructure_type": "all"
}
```

**Example -- Internet connectivity in South Asia over the last 5 years:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "South Asia",
  "infrastructure_type": "internet",
  "time_period": "last5"
}
```

**Example -- Water and sanitation access with SDG targets and access gaps:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "Nigeria",
  "infrastructure_type": "water",
  "include_sdg_targets": true,
  "include_access_gaps": true
}
```

**Example -- Roads and logistics for Germany with LPI data:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "Germany",
  "infrastructure_type": "roads",
  "include_logistics_performance": true
}
```

**Example -- Urban development data for Brazil with regional comparison:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "Brazil",
  "infrastructure_type": "urban",
  "include_regional_comparison": true
}
```

**Example -- Specific year range for United States:**
```json
{
  "action": "query_infrastructure_data",
  "country_or_region": "United States",
  "infrastructure_type": "electricity",
  "time_period": "2015:2020"
}
```

#### Workflows

##### Country Infrastructure Profile
1. Call `query_infrastructure_data` with a country and `infrastructure_type: "all"` to get a complete infrastructure overview.
2. Review the `sdg_progress` section for SDG 9 and SDG 11 target tracking.
3. Check `access_gaps` to see where coverage is lacking.

##### Urban-Rural Divide Analysis
1. Call `query_infrastructure_data` with `urban_rural_breakdown: true` and `infrastructure_type` set to "electricity", "water", or "all".
2. Review the `urban_rural_divide` section for analysis of the divide (minimal, moderate, significant, or severe).
3. Use the interpretation text for reporting.

##### SDG Progress Monitoring
1. Call `query_infrastructure_data` with `include_sdg_targets: true`.
2. Review the `sdg_progress` section which shows current value, target, gap, progress percentage, and whether the target is being met.
3. SDG targets tracked: SDG 7.1 (electricity), SDG 9.c (internet/broadband), SDG 6.1 (water), SDG 6.2 (sanitation), SDG 11.1 (housing/slums), SDG 9.1 (logistics).

##### Logistics and Trade Infrastructure
1. Call `query_infrastructure_data` with `infrastructure_type: "roads"` and `include_logistics_performance: true`.
2. Review road density, paved roads, rail lines, air transport, container port traffic, and LPI score.
3. LPI score ranges from 1 (low) to 5 (high) and covers customs, infrastructure, shipments, competence, tracking, and timeliness.

#### Notes
- **Country matching:** Uses the World Bank country/region API for natural language matching. Tries exact match first, then partial match. Works with full country names and standard region names.
- **Infrastructure types and their indicators:**
  - `electricity`: electricity access (total, urban, rural), electric power consumption, renewable energy %
  - `internet`: internet users %, mobile subscriptions, broadband subscriptions, fixed broadband, secure internet servers
  - `water`: water access (total, urban, rural), sanitation access (total, urban, rural)
  - `urban`: urban population %, urban growth rate, total urban population, slum population %
  - `roads`: road density, paved roads %, rail lines, logistics performance (LPI), air transport passengers, container port traffic
  - `all`: all indicators across all types
- **Access gap calculation:** For percentage-based access indicators (electricity, internet, water, sanitation), calculates 100% minus current access. Shows current access, gap, and interpretation.
- **SDG target comparison:** Compares current values against SDG 2030 targets. For slum population, lower is better. For access indicators, higher is better. Non-numeric targets show "See SDG target for goal".
- **Urban-rural divide assessment thresholds:** less than 5pp = minimal, 5-15pp = moderate, 15-30pp = significant, over 30pp = severe.
- **Response includes:** country metadata (name, ISO code, region, income level, capital city, coordinates), indicator data with latest value and year, and optional sections for access gaps, SDG progress, urban-rural divide, logistics notes, and regional comparison notes.
- If `infrastructure_type` is not one of the valid options, a validation error is returned listing valid options.
- If `country_or_region` is missing for `query_infrastructure_data`, a validation error is returned.
- Data availability varies by country and indicator. Some indicators may have no data for certain countries or time periods.

## When To Use
- Use this skill for `Infrastructure, Mobility, and Housing Data Hub` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: infrastructure, mobility, and housing data hub, infrastructure urban development, mobility and transit analysis, infrastructure access benchmarking, housing and permit trend analysis, urban planning support, query infrastructure data, country or region.
- Supported action names: `query_infrastructure_data`.

## Use Cases
- Mobility and transit analysis
- Infrastructure access benchmarking
- Housing and permit trend analysis
- Urban planning support
- Regional development comparisons

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 action routes are enabled and listed in `./schema.md`.

- `query_infrastructure_data` (action slug: `query-infrastructure-data`): Fetch infrastructure and urban development data for a country or region from the World Bank. Returns electricity access, internet penetration, water/sanitation access, road infrastructure, urbanization indicators, with SDG progress tracking, access gap calculations, and urban-rural divide analysis. Price: `5` credits. Parameters: `country_or_region`, `include_access_gaps`, `include_logistics_performance`, `include_regional_comparison`, `include_sdg_targets`, `infrastructure_type`, `time_period`, `urban_rural_breakdown`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "infrastructure-urban-development"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "infrastructure-urban-development"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "infrastructure-urban-development"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "infrastructure-urban-development"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "infrastructure-urban-development"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "infrastructure-urban-development"
  }
}
```

## Call This Tool
Product slug: `infrastructure-urban-development`

Marketplace page: https://www.agentpmt.com/marketplace/infrastructure-urban-development

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- No-account AgentAddress/x402 route: first use `../agentpmt-no-account-agentaddress-x402` for the canonical payment and wallet setup instructions.
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
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
  - OpenClaw install: `openclaw skills install agentpmt-no-account-agentaddress-x402`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Infrastructure-Mobility-and-Housing-Data-Hub",
    "arguments": {
      "action": "query_infrastructure_data",
      "country_or_region": "example country or region",
      "include_access_gaps": true,
      "include_logistics_performance": true,
      "include_regional_comparison": true,
      "include_sdg_targets": true,
      "infrastructure_type": "all",
      "time_period": "latest",
      "urban_rural_breakdown": true
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "infrastructure-urban-development",
  "parameters": {
    "action": "query_infrastructure_data",
    "country_or_region": "example country or region",
    "include_access_gaps": true,
    "include_logistics_performance": true,
    "include_regional_comparison": true,
    "include_sdg_targets": true,
    "infrastructure_type": "all",
    "time_period": "latest",
    "urban_rural_breakdown": true
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `query_infrastructure_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402 (ClawHub: `agentpmt-no-account-agentaddress-x402`, page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`)
- Marketplace product: https://www.agentpmt.com/marketplace/infrastructure-urban-development
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
