---
name: global-debt-fiscal-explorer
description: "Global Debt & Fiscal Explorer: Query national debt, government revenue, public expenditure, fiscal balance, and debt service data for any country or region. Use when an agent needs global debt & fiscal explorer, debt fiscal management, research a country's national debt level, compare government debt across countries, analyze tax revenue trends over time, check fiscal balance and budget deficits, query fiscal data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/debt-fiscal-management
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/debt-fiscal-management"}}
---
# Global Debt & Fiscal Explorer

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore the financial health of any country in the world. Look up national debt levels, government spending, tax revenue, and fiscal balances — all expressed as easy-to-understand ratios and percentages of GDP. Compare countries, track trends over time, and assess debt sustainability at a glance.

## Product Instructions
### Global Debt & Fiscal Explorer

Query national debt levels, government spending, tax revenue, fiscal balances, and debt sustainability indicators for any country from the World Bank World Development Indicators database.

#### Actions

##### query_fiscal_data

Fetch fiscal and debt data for a country or region with optional debt sustainability assessment.

**Optional fields (all have defaults):**
- `country_or_region` (string) — Country name or region in plain English (e.g., `"United States"`, `"Greece"`, `"Kenya"`, `"World"`). Defaults to `"World"` if not provided. Supports plain English names or ISO3 codes.
- `fiscal_aspect` (string) — Which category of fiscal data to query. Default: `"all"`.
  - `"debt"` — External debt stocks, external debt/GNI ratio, central government debt/GDP, short-term and long-term debt, debt service/exports ratio
  - `"balance"` — Cash surplus/deficit (% of GDP), primary balance (% of GDP)
  - `"revenue"` — Tax revenue (% of GDP), government revenue excluding grants (% of GDP)
  - `"expenditure"` — Government expense (% of GDP), education/health/military expenditure (% of GDP)
  - `"debt_service"` — Total debt service, debt service/exports ratio, interest payments (% of revenue), multilateral and bilateral debt
  - `"all"` — All fiscal indicators combined
- `calculate_debt_ratios` (boolean) — Calculate debt sustainability ratios and compare against IMF/World Bank Debt Sustainability Framework thresholds. Default: `true`.
- `time_period` (string) — Default: `"latest"`.
  - `"latest"` — Most recent 10 data points (returns the most recent non-null value)
  - `"YYYY"` — Specific year (e.g., `"2020"`)
  - `"YYYY:YYYY"` — Year range (e.g., `"2015:2020"`)

**Example — All fiscal data for a country:**
```json
{
  "country_or_region": "Kenya",
  "fiscal_aspect": "all",
  "time_period": "latest"
}
```

**Example — Debt sustainability analysis:**
```json
{
  "country_or_region": "Greece",
  "fiscal_aspect": "debt",
  "calculate_debt_ratios": true,
  "time_period": "latest"
}
```

**Example — Government revenue over time:**
```json
{
  "country_or_region": "United States",
  "fiscal_aspect": "revenue",
  "time_period": "2015:2023"
}
```

**Example — Expenditure breakdown:**
```json
{
  "country_or_region": "Nigeria",
  "fiscal_aspect": "expenditure",
  "time_period": "latest"
}
```

**Example — Fiscal balance for a specific year:**
```json
{
  "country_or_region": "Brazil",
  "fiscal_aspect": "balance",
  "time_period": "2022"
}
```

**Example — Debt service analysis:**
```json
{
  "country_or_region": "Sri Lanka",
  "fiscal_aspect": "debt_service",
  "calculate_debt_ratios": true,
  "time_period": "2018:2023"
}
```

#### Response Format

Responses include:

- **data** — Per-indicator results with value, date, country name, indicator description, and unit. For time-range queries, includes a `time_series` array of date/value pairs.
- **debt_sustainability_assessment** — When `calculate_debt_ratios` is true and debt data is available:
  - `overall_risk_level` — low, moderate, high, or critical
  - `sustainability_indicators` — Individual ratio assessments against IMF/World Bank thresholds
  - `risk_factors` — List of identified debt risks
- **fiscal_balance_assessment** — Fiscal position analysis:
  - `fiscal_position` — surplus or deficit
  - `sustainability_level` — strong, sustainable, warning, or critical
  - Maastricht criterion comparison (-3% GDP threshold)
- **fiscal_space_analysis** — Revenue vs. expenditure analysis:
  - Revenue and expense as % of GDP
  - Interest burden assessment
  - Revenue mobilization assessment (weak/moderate/strong/very strong)
- **expenditure_allocation** — Education, health, and military spending as % of GDP
- **sdg_alignment** — SDG 8, 16, and 17 alignment information
- **summary** — Data availability statistics

#### Fiscal Indicators by Aspect

| Aspect | Indicators |
|---|---|
| debt | External debt stocks (US$), External debt/GNI %, Central govt debt/GDP %, Short-term debt, Long-term debt, Debt service/exports % |
| balance | Cash surplus/deficit (% GDP), Primary balance (% GDP) |
| revenue | Tax revenue (% GDP), Government revenue excl. grants (% GDP) |
| expenditure | Government expense (% GDP), Education spending (% GDP), Health spending (% GDP), Military spending (% GDP) |
| debt_service | Total debt service (US$), Debt service/exports %, Interest payments (% revenue), Multilateral debt, Bilateral debt |

#### Debt Sustainability Thresholds (IMF/World Bank DSF)

| Indicator | Low Risk | Moderate Risk | High Risk |
|---|---|---|---|
| External debt/GNI | < 30% | 30-40% | > 55% |
| Debt service/exports | < 15% | 15-20% | > 25% |
| Government debt/GDP | < 50% | 50-70% | > 90% |

#### Important Notes

- Data is sourced from the World Bank World Development Indicators database.
- Country names are resolved against a built-in mapping; use common English names or ISO3 codes.
- Data availability varies significantly by country; developing countries may have more gaps.
- Most recent data may be 1-3 years behind the current year.
- Percentage indicators with suspiciously small values are automatically corrected for a known World Bank API scaling bug.
- Years must be between 1960 and the current year.

## When To Use
- Use this skill for `Global Debt & Fiscal Explorer` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global debt & fiscal explorer, debt fiscal management, research a country's national debt level, compare government debt across countries, analyze tax revenue trends over time, check fiscal balance and budget deficits, query fiscal data, country or region.
- Supported action names: `query_fiscal_data`.

## Use Cases
- Research a country's national debt level
- Compare government debt across countries
- Analyze tax revenue trends over time
- Check fiscal balance and budget deficits
- Evaluate debt sustainability ratios
- Study public expenditure patterns
- Track debt service costs
- Support academic research on fiscal policy
- Assess sovereign credit risk indicators
- Monitor government revenue as a percentage of GDP

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_fiscal_data` (action slug: `query-fiscal-data`): Query national debt, government revenue, public expenditure, fiscal balance, and debt service data for any country or region from the World Bank. Price: `30` credits. Parameters: `calculate_debt_ratios`, `country_or_region`, `fiscal_aspect`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "debt-fiscal-management"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "debt-fiscal-management"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "debt-fiscal-management"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "debt-fiscal-management"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "debt-fiscal-management"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "debt-fiscal-management"
  }
}
```

## Call This Tool
Product slug: `debt-fiscal-management`

Marketplace page: https://www.agentpmt.com/marketplace/debt-fiscal-management

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
    "name": "Global-Debt--Fiscal-Explorer",
    "arguments": {
      "action": "query_fiscal_data",
      "calculate_debt_ratios": true,
      "country_or_region": "example country or region",
      "fiscal_aspect": "all",
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "debt-fiscal-management",
  "parameters": {
    "action": "query_fiscal_data",
    "calculate_debt_ratios": true,
    "country_or_region": "example country or region",
    "fiscal_aspect": "all",
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
- If `query_fiscal_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/debt-fiscal-management
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
