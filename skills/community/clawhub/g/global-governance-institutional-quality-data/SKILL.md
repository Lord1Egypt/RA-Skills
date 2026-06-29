---
name: global-governance-institutional-quality-data
description: "Global Governance & Institutional Quality Data: Query governance indicators including corruption control, rule of law, government. Use when an agent needs global governance & institutional quality data, governance institutional quality, research corruption control scores by country, compare rule of law rankings across regions, track government effectiveness over time, analyze political stability indicators, query governance data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/governance-institutional-quality
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/governance-institutional-quality"}}
---
# Global Governance & Institutional Quality Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore governance and institutional quality data for any country in the world. Look up corruption control scores, rule of law rankings, government effectiveness, political stability, regulatory quality, and civic voice indicators. Compare how countries rank on governance, track institutional improvement over time, and benchmark against regional peers — all from a comprehensive global data set.

## Product Instructions
### Governance & Institutional Quality Data

Access comprehensive governance data from the World Bank's Worldwide Governance Indicators (WGI) database covering 200+ countries. Query six core governance dimensions with WGI scores, percentile rankings, historical trends, and peer comparisons using natural language country names.

#### Actions

##### query_governance_data

Fetch governance indicator data for a country or region.

**Required Parameters:**
- `action` (string): Must be `"query_governance_data"`
- `country_or_region` (string): Country or region name in plain language (e.g., `"United States"`, `"India"`, `"Sub-Saharan Africa"`)

**Optional Parameters:**
- `governance_aspect` (string, default: `"all"`): Governance dimension to query. One of:
  - `"corruption"` - Control of corruption indicators
  - `"rule_of_law"` - Rule of law and legal institutions
  - `"effectiveness"` - Government effectiveness and service delivery
  - `"stability"` - Political stability and absence of violence
  - `"regulatory"` - Regulatory quality and business environment
  - `"voice"` - Voice and accountability, democratic participation
  - `"all"` - All 6 WGI dimensions
- `include_percentile_ranks` (boolean, default: `true`): Include percentile rankings (0-100 scale) for international comparison
- `include_historical_trends` (boolean, default: `true`): Include historical trends showing improvement or deterioration over time
- `time_period` (string, default: `"latest"`): Time period for data. Options:
  - `"latest"` - Most recent available data
  - `"last_5_years"` - Last 5 years of data
  - `"last_10_years"` - Last 10 years of data
  - `"YYYY:YYYY"` - Specific year range (e.g., `"2015:2020"`). Years must be between 1960 and current year.
  - `"YYYY"` - A single year (e.g., `"2020"`)
- `include_peer_comparison` (boolean, default: `true`): Include comparison with regional and income group peers (World, High Income, Upper Middle Income, Lower Middle Income, Low Income)

**Example - Latest governance for a country:**
```json
{
  "action": "query_governance_data",
  "country_or_region": "United States",
  "governance_aspect": "all",
  "time_period": "latest"
}
```

**Example - Corruption trends over time:**
```json
{
  "action": "query_governance_data",
  "country_or_region": "India",
  "governance_aspect": "corruption",
  "time_period": "last_10_years",
  "include_historical_trends": true
}
```

**Example - Rule of law with peer comparison:**
```json
{
  "action": "query_governance_data",
  "country_or_region": "Kenya",
  "governance_aspect": "rule_of_law",
  "time_period": "latest",
  "include_peer_comparison": true
}
```

**Example - Political stability for a specific range:**
```json
{
  "action": "query_governance_data",
  "country_or_region": "Brazil",
  "governance_aspect": "stability",
  "time_period": "2015:2020",
  "include_percentile_ranks": true
}
```

**Example - Regional aggregate data:**
```json
{
  "action": "query_governance_data",
  "country_or_region": "Sub-Saharan Africa",
  "governance_aspect": "effectiveness",
  "time_period": "latest"
}
```

#### Supported Countries and Regions

Accepts plain-language names. Examples of supported inputs:

- **Countries**: `"United States"`, `"USA"`, `"India"`, `"Germany"`, `"Nigeria"`, `"Brazil"`, `"Japan"`, `"Kenya"`, `"Singapore"`, `"South Africa"`, etc. (200+ countries)
- **Regions**: `"Sub-Saharan Africa"`, `"Latin America"`, `"Middle East"`, `"South Asia"`, `"East Asia"`, `"Europe"`
- **Income groups**: `"Low Income"`, `"Lower Middle Income"`, `"Upper Middle Income"`, `"High Income"`, `"OECD"`
- **Global**: `"World"` or `"Global"`
- **ISO3 codes**: 3-letter codes like `"USA"`, `"IND"`, `"GBR"` are also accepted

Country names support partial matching, so `"UK"` maps to United Kingdom and `"America"` maps to USA.

#### Six Governance Dimensions (WGI)

1. **Voice and Accountability** (`"voice"`): Citizen participation, freedom of expression, media independence
2. **Political Stability** (`"stability"`): Likelihood of political instability and violence/terrorism
3. **Government Effectiveness** (`"effectiveness"`): Quality of public services, civil service, policy formulation and implementation
4. **Regulatory Quality** (`"regulatory"`): Government ability to formulate and implement sound policies promoting private sector development
5. **Rule of Law** (`"rule_of_law"`): Confidence in rules of society, contract enforcement, property rights, courts, likelihood of crime/violence
6. **Control of Corruption** (`"corruption"`): Extent to which public power is exercised for private gain

#### Response Structure

Responses include:
- **WGI scores** on a -2.5 (weak) to +2.5 (strong) scale with score category and interpretation
- **Percentile ranks** from 0 (lowest) to 100 (highest) for global positioning
- **Overall governance score** (average of the 6 dimensions)
- **Historical trends** with direction (improving/deteriorating/stable), magnitude, and absolute change
- **Peer comparisons** against World, High Income, Upper Middle Income, Lower Middle Income, and Low Income group averages
- **Insights** including strongest/weakest dimensions, corruption analysis, political stability assessment, trajectory assessment
- **SDG 16 alignment** (Peace, Justice and Strong Institutions)

##### WGI Score Interpretation
| Score Range | Category | Meaning |
|---|---|---|
| +1.5 to +2.5 | Very Strong | Excellent governance performance |
| +0.5 to +1.5 | Strong | Good governance performance |
| -0.5 to +0.5 | Moderate | Average governance performance |
| -1.5 to -0.5 | Weak | Below-average governance performance |
| -2.5 to -1.5 | Very Weak | Poor governance performance |

##### Percentile Rank Interpretation
| Rank Range | Meaning |
|---|---|
| 90-100 | Top 10% globally |
| 75-89 | Top quartile globally |
| 50-74 | Above median globally |
| 25-49 | Below median globally |
| 10-24 | Bottom quartile globally |
| 0-9 | Bottom 10% globally |

#### Workflows

1. **Country Risk Assessment**: Query all governance indicators for a country, review overall score and weakest dimensions, compare against peer income group
2. **Anti-Corruption Analysis**: Use `governance_aspect: "corruption"` with `time_period: "last_10_years"` to track corruption control trends
3. **Regional Comparison**: Query the same aspect for multiple countries or regions to compare governance performance
4. **Democratic Governance Monitoring**: Focus on `"voice"` aspect with historical trends to track democratic participation over time
5. **Investment Due Diligence**: Query `"all"` aspects with peer comparison enabled to benchmark a country against its income group

#### Notes

- Data sourced from the World Bank Worldwide Governance Indicators (WGI), based on 30+ underlying data sources from diverse institutions
- Indicators reflect perceptions from citizen surveys, businesses, and experts -- they are not objective measurements
- Data updated annually with approximately a 1-year lag
- Standard error indicators are available internally for confidence intervals
- When `include_percentile_ranks` is set to `false`, rank indicators are filtered out from the response
- If an unrecognized country name is provided, the tool returns an error with guidance on valid inputs
- Data coverage varies by country; some may have limited historical data
- When querying with `time_period: "latest"`, only the single most recent data point is returned per indicator
- Trend analysis requires at least 2 valid data points; trends are classified by magnitude (Significant >= 1.0, Moderate >= 0.5, Slight < 0.5)
- Peer comparison fetches data for World, High Income, Upper Middle Income, Lower Middle Income, and Low Income groups for the core (non-rank, non-standard-error) indicators

## When To Use
- Use this skill for `Global Governance & Institutional Quality Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global governance & institutional quality data, governance institutional quality, research corruption control scores by country, compare rule of law rankings across regions, track government effectiveness over time, analyze political stability indicators, query governance data, country or region.
- Supported action names: `query_governance_data`.

## Use Cases
- Research corruption control scores by country
- Compare rule of law rankings across regions
- Track government effectiveness over time
- Analyze political stability indicators
- Study regulatory quality benchmarks
- Monitor voice and accountability metrics
- Assess governance improvement or decline trends
- Compare institutional quality with regional peers
- Support risk profiling for investment decisions
- Research progress on good governance targets

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_governance_data` (action slug: `query-governance-data`): Fetch governance and institutional quality data for a country or region from the World Bank Worldwide Governance Indicators (WGI). Returns six governance dimensions with WGI scores, percentile rankings, historical trends, peer comparisons, and SDG 16 alignment. Price: `10` credits. Parameters: `country_or_region`, `governance_aspect`, `include_historical_trends`, `include_peer_comparison`, `include_percentile_ranks`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "governance-institutional-quality"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "governance-institutional-quality"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "governance-institutional-quality"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "governance-institutional-quality"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "governance-institutional-quality"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "governance-institutional-quality"
  }
}
```

## Call This Tool
Product slug: `governance-institutional-quality`

Marketplace page: https://www.agentpmt.com/marketplace/governance-institutional-quality

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
    "name": "Global-Governance--Institutional-Quality-Data",
    "arguments": {
      "action": "query_governance_data",
      "country_or_region": "example country or region",
      "governance_aspect": "all",
      "include_historical_trends": true,
      "include_peer_comparison": true,
      "include_percentile_ranks": true,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "governance-institutional-quality",
  "parameters": {
    "action": "query_governance_data",
    "country_or_region": "example country or region",
    "governance_aspect": "all",
    "include_historical_trends": true,
    "include_peer_comparison": true,
    "include_percentile_ranks": true,
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
- If `query_governance_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/governance-institutional-quality
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
