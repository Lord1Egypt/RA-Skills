---
name: global-financial-inclusion-banking-data
description: "Global Financial Inclusion & Banking Data: Query bank account ownership, credit access, financial inclusion gender gaps, stock market. Use when an agent needs global financial inclusion & banking data, financial sector banking, research bank account ownership rates by country, compare financial inclusion across regions, analyze credit access and lending conditions, study gender gaps in financial services, query financial data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/financial-sector-banking
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/financial-sector-banking"}}
---
# Global Financial Inclusion & Banking Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore financial inclusion and banking data for any country in the world. Look up bank account ownership rates, credit access, gender gaps in financial services, stock market capitalization, and remittance flows. Compare how countries stack up on financial access, track progress toward universal banking, and identify where financial gaps remain — all from a comprehensive global data set.

## Product Instructions
### Financial Sector & Banking Data

Access comprehensive World Bank financial indicators including bank account ownership, credit access, financial inclusion metrics, stock market data, remittances, and mobile money adoption through a natural language query interface with gender gap analysis and global comparisons.

#### Overview

This tool provides natural language access to World Bank financial sector data covering financial inclusion (Global Findex), banking infrastructure, credit and lending rates, stock markets, remittances, and mobile money adoption. It supports automatic gender gap calculations, global average comparisons, and SDG alignment tracking (SDG 1, 5, 8.10, 10).

Data is sourced from the World Bank Data API including the Global Findex Database, Financial Sector Indicators, International Debt Statistics, and World Development Indicators.

#### Actions

##### query_financial_data

Query financial sector indicators for any country or region.

###### Required Parameters

- **action** (string): Must be `"query_financial_data"`

###### Optional Parameters

- **country_or_region** (string, default: `"World"`): Country name or ISO3 code
  - Country names: `"United States"`, `"India"`, `"Kenya"`, `"Nigeria"`
  - ISO3 codes: `"USA"`, `"IND"`, `"KEN"`
  - Global: `"World"`
  - If not provided, defaults to World (WLD) data
  - Maximum 100 characters

- **financial_aspect** (string, default: `"all"`): Financial category to query
  - `"banking"` - Account ownership, bank branches per 100k adults, ATM density, bank deposit ratios
  - `"credit"` - Domestic credit to private sector (% GDP), borrowing rates, lending interest rate
  - `"inclusion"` - Account ownership by gender (male/female), mobile money accounts, savings at financial institutions
  - `"markets"` - Stock market capitalization (% GDP), trading volume, turnover ratio
  - `"remittances"` - Remittances received (% GDP and USD), remittances sent (USD)
  - `"all"` - All financial indicators (19 indicators)
  - If an unrecognized value is provided, defaults to all indicators

- **calculate_gender_gaps** (boolean, default: `true`): Calculate gender disparities in financial inclusion. Returns male/female values, gap in percentage points, relative gap percentage, and status (male advantage/female advantage/equal). Only applies when `financial_aspect` is `"inclusion"`, `"all"`, or null.

- **time_period** (string, default: `"latest"`): Time period for data retrieval
  - `"latest"` - Fetches the last 10 years and returns the most recent non-null value
  - `"YYYY"` - Single specific year (e.g., `"2021"`), must be between 1960 and current year
  - `"YYYY:YYYY"` - Year range (e.g., `"2017:2021"`), both years must be between 1960 and current year

- **include_targets** (boolean, default: `true`): Include Global Findex targets (Universal Financial Access by 2030, 80% account ownership target, gender gap elimination) and SDG alignment information (SDG 1, 5, 8.10, 10) in the response

###### Example: Financial inclusion with gender analysis

```json
{
  "action": "query_financial_data",
  "country_or_region": "Nigeria",
  "financial_aspect": "inclusion",
  "calculate_gender_gaps": true
}
```

###### Example: Banking infrastructure

```json
{
  "action": "query_financial_data",
  "country_or_region": "Switzerland",
  "financial_aspect": "banking"
}
```

###### Example: Stock market overview

```json
{
  "action": "query_financial_data",
  "country_or_region": "United States",
  "financial_aspect": "markets"
}
```

###### Example: Remittance flows

```json
{
  "action": "query_financial_data",
  "country_or_region": "Philippines",
  "financial_aspect": "remittances"
}
```

###### Example: Global financial overview

```json
{
  "action": "query_financial_data",
  "country_or_region": "World",
  "financial_aspect": "all",
  "include_targets": true
}
```

###### Example: Gender gap study over time

```json
{
  "action": "query_financial_data",
  "country_or_region": "India",
  "financial_aspect": "inclusion",
  "calculate_gender_gaps": true,
  "time_period": "2017:2021"
}
```

#### Response Structure

Responses include:

- **country**: The queried country or region name
- **country_code**: Resolved ISO3 country code
- **aspect**: The financial aspect queried
- **time_period**: The time period used
- **data**: Object with each indicator containing:
  - `value`: The numeric value (null if no data available)
  - `date`: Year of the data point
  - `country`: Country name from API
  - `indicator`: Full indicator description
  - `unit`: Unit of measurement
  - `global_comparison` (for non-World queries): global_average, difference_absolute, difference_pct, comparison ("above global average"/"below global average")
  - `error`: Error message if data fetch failed
- **gender_gap_analysis** (when `calculate_gender_gaps` is true and inclusion data available): male_value, female_value, gap_percentage_points, gap_relative_pct, status
- **financial_access_gap** (when account_ownership data available): population_with_accounts_pct, population_without_accounts_pct, progress_to_universal_access_pct
- **mobile_money_insight** (when mobile money data available): mobile_money_adoption_pct with significance note
- **global_findex_targets** (when `include_targets` is true): Universal Financial Access by 2030 target, 80% account ownership target, gender gap elimination target
- **sdg_alignment** (when `include_targets` is true): SDG 1, 5, 8.10, and 10 alignment descriptions
- **summary**: total_indicators_requested, indicators_with_data, data_availability_pct

#### Key Indicators Reference

##### Financial Inclusion (Global Findex)
| Indicator | Unit | Description |
|-----------|------|-------------|
| account_ownership | % age 15+ | Population with financial account |
| account_male | % age 15+ | Male account ownership |
| account_female | % age 15+ | Female account ownership |
| mobile_money_account | % age 15+ | Mobile money service adoption |
| saved_financial_institution | % age 15+ | Saved at a bank or financial institution |
| borrowed_financial_institution | % age 15+ | Borrowed from formal financial sources |

##### Banking Infrastructure
| Indicator | Unit | Description |
|-----------|------|-------------|
| bank_branches | per 100,000 adults | Commercial bank branch density |
| atm_per_100k | per 100,000 adults | ATM density |
| bank_deposits_gdp | % | Bank liquid reserves to assets ratio |

##### Credit & Lending
| Indicator | Unit | Description |
|-----------|------|-------------|
| domestic_credit_private | % of GDP | Domestic credit to private sector |
| lending_rate | % | Lending interest rate |
| deposit_rate | % | Deposit interest rate |
| real_interest_rate | % | Real interest rate |

##### Stock Markets
| Indicator | Unit | Description |
|-----------|------|-------------|
| stock_market_cap | % of GDP | Market capitalization |
| stock_traded | % of GDP | Total value of stocks traded |
| stock_turnover | ratio | Stocks traded turnover ratio |

##### Remittances
| Indicator | Unit | Description |
|-----------|------|-------------|
| remittances_received | % of GDP | Personal remittances received |
| remittances_received_usd | current US$ | Remittances received absolute |
| remittances_sent | current US$ | Personal remittances sent |

#### Workflows

1. **Financial Inclusion Assessment**: Query `financial_aspect: "inclusion"` with `calculate_gender_gaps: true` to get account ownership rates, gender disparities, mobile money adoption, and financial access gaps
2. **Banking Sector Analysis**: Query `financial_aspect: "banking"` to assess bank branch density, ATM availability, and compare against global averages
3. **Credit Market Research**: Query `financial_aspect: "credit"` to analyze lending rates, domestic credit levels, and borrowing access
4. **Remittance Economy Analysis**: Query `financial_aspect: "remittances"` for countries with significant diaspora to understand remittance flows as percentage of GDP
5. **SDG Progress Tracking**: Query `financial_aspect: "all"` with `include_targets: true` to track progress toward Universal Financial Access 2030 targets

#### Notes

- Financial inclusion data (Global Findex) is updated every 3 years via surveys; most recent data is from 2021
- Banking infrastructure data is updated annually
- Stock market data is updated monthly/annually
- Gender-disaggregated data availability varies by country
- Mobile money data is particularly relevant for Sub-Saharan Africa and South Asia
- Some indicators may not be available for all countries or time periods
- When `time_period` is `"latest"`, the tool fetches the last 10 years and returns the most recent non-null value
- Global comparisons are automatically included for non-World queries when indicator data is available
- The tool fetches all requested indicators concurrently for performance
- If no data is available for any indicator, the response returns `success: false` with a message
- Country names longer than 100 characters are rejected
- Unrecognized country names raise a ValueError with guidance on accepted formats
- The summary section shows data availability percentage to help assess data completeness

#### Pricing

$0.05 per request

## When To Use
- Use this skill for `Global Financial Inclusion & Banking Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global financial inclusion & banking data, financial sector banking, research bank account ownership rates by country, compare financial inclusion across regions, analyze credit access and lending conditions, study gender gaps in financial services, query financial data, country or region.
- Supported action names: `query_financial_data`.

## Use Cases
- Research bank account ownership rates by country
- Compare financial inclusion across regions
- Analyze credit access and lending conditions
- Study gender gaps in financial services
- Track stock market capitalization trends
- Monitor remittance flows between countries
- Assess progress toward universal financial access
- Benchmark banking sector development
- Support financial policy research
- Evaluate Global Findex indicators and SDG 8 alignment

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_financial_data` (action slug: `query-financial-data`): Fetch financial sector indicators for a country or region, including bank account ownership, credit access, financial inclusion gender gaps, stock market data, remittances, and mobile money adoption with global comparisons. Price: `20` credits. Parameters: `calculate_gender_gaps`, `country_or_region`, `financial_aspect`, `include_targets`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "financial-sector-banking"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "financial-sector-banking"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "financial-sector-banking"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "financial-sector-banking"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "financial-sector-banking"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "financial-sector-banking"
  }
}
```

## Call This Tool
Product slug: `financial-sector-banking`

Marketplace page: https://www.agentpmt.com/marketplace/financial-sector-banking

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
    "name": "Global-Financial-Inclusion--Banking-Data",
    "arguments": {
      "action": "query_financial_data",
      "calculate_gender_gaps": true,
      "country_or_region": "World",
      "financial_aspect": "all",
      "include_targets": true,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "financial-sector-banking",
  "parameters": {
    "action": "query_financial_data",
    "calculate_gender_gaps": true,
    "country_or_region": "World",
    "financial_aspect": "all",
    "include_targets": true,
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
- If `query_financial_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/financial-sector-banking
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
