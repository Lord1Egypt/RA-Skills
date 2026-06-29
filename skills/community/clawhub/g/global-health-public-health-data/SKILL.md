---
name: global-health-public-health-data
description: "Global Health & Public Health Data: Query life expectancy, mortality rates, immunization coverage, health expenditure, infectious disease. Use when an agent needs global health & public health data, healthcare demographics data, research life expectancy by country, compare infant and child mortality rates across regions, track immunization coverage trends, analyze health expenditure as percentage of gdp, query health data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/healthcare-demographics-data
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/healthcare-demographics-data"}}
---
# Global Health & Public Health Data

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore health and public health data for any country in the world. Look up life expectancy, mortality rates, immunization coverage, health expenditure, infectious disease prevalence, and demographic health indicators. Compare health outcomes across countries, benchmark against WHO targets, and track progress on global health goals — all from a comprehensive global data set.

## Product Instructions
### Health and Public Health Data Hub

Access health and demographic data for any country from the World Bank. Query mortality rates, life expectancy, immunization coverage, health expenditure, infectious disease prevalence, and demographic indicators with WHO benchmarks and SDG 3 target comparisons.

#### Actions

##### query_health_data

Fetch health and demographic data for a country or region from the World Bank World Development Indicators database. Uses the World Bank countries API for fuzzy country name resolution.

**Required fields:**
- `action` — `"query_health_data"`
- `country_or_region` (string) — Country or region name in plain English (e.g., `"Japan"`, `"Kenya"`, `"United States"`, `"South Asia"`, `"Sub-Saharan Africa"`). The tool searches the World Bank countries API for exact and partial matches.

**Optional fields:**
- `health_topic` (string) — Health topic to query. Default: `"all"`.
  - `"mortality"` — Maternal mortality, under-5 mortality, infant mortality, neonatal mortality, death rate
  - `"life_expectancy"` — Overall life expectancy, male life expectancy, female life expectancy
  - `"immunization"` — Measles, DPT, and Hepatitis B immunization coverage rates
  - `"expenditure"` — Health expenditure per capita and as % of GDP, physicians per 1,000, hospital beds per 1,000, nurses/midwives per 1,000
  - `"infectious_disease"` — Tuberculosis incidence, HIV prevalence
  - `"demographics"` — Birth rate, death rate, fertility rate, total population, population ages 0-14, population ages 65+, urban population percentage
  - `"all"` — All health indicators listed above
- `time_period` (string) — Time period for data. Default: `"latest"`.
  - `"latest"` — Most recent available data point
  - `"YYYY"` — Specific year (e.g., `"2020"`)
  - `"YYYY:YYYY"` — Year range (e.g., `"2015:2020"`)
  - `"last5"` — Last 5 years of data
  - `"last10"` — Last 10 years of data
  - Also accepts `"last_5_years"` and `"last_10_years"`
- `include_who_benchmarks` (boolean) — Include WHO benchmarks and SDG 3 target comparisons for applicable indicators. Shows target value, current value, difference, and whether the target is met. Default: `true`.
- `include_demographic_context` (boolean) — Include population context (total population, age distribution under 14 and over 65) alongside health data. Automatically skipped when the topic is already `"demographics"`. Default: `true`.
- `include_regional_comparison` (boolean) — Include a note about regional comparison data availability. Default: `false`.

**Example — Life expectancy for a country:**
```json
{
  "action": "query_health_data",
  "country_or_region": "Japan",
  "health_topic": "life_expectancy",
  "time_period": "latest"
}
```

**Example — Mortality data with WHO benchmarks:**
```json
{
  "action": "query_health_data",
  "country_or_region": "Kenya",
  "health_topic": "mortality",
  "include_who_benchmarks": true
}
```

**Example — All health data over a time range:**
```json
{
  "action": "query_health_data",
  "country_or_region": "India",
  "health_topic": "all",
  "time_period": "2015:2020"
}
```

**Example — Immunization coverage with demographic context:**
```json
{
  "action": "query_health_data",
  "country_or_region": "Nigeria",
  "health_topic": "immunization",
  "include_demographic_context": true,
  "include_who_benchmarks": true
}
```

**Example — Health expenditure without benchmarks:**
```json
{
  "action": "query_health_data",
  "country_or_region": "United States",
  "health_topic": "expenditure",
  "include_who_benchmarks": false,
  "time_period": "last5"
}
```

#### Response Format

Responses include:

- **country** — Resolved country name from World Bank metadata.
- **iso_code** — ISO country code.
- **region** — World Bank region name.
- **income_level** — World Bank income classification.
- **query** — Echo of the topic and time period requested.
- **indicators** — Per-indicator results, each with:
  - `name` — Human-readable indicator name
  - `data` — Array of data points with year, value, and unit
  - `latest_value` — Most recent value
  - `latest_year` — Year of most recent value
- **who_benchmarks** — When enabled, per-indicator comparison to WHO/SDG targets:
  - `target` — WHO target value
  - `current_value` — Country's current value
  - `difference` — Gap from target
  - `unit` — Measurement unit
  - `sdg` — Related SDG target (e.g., SDG 3.1, SDG 3.2, SDG 3.b, SDG 3.3)
  - `assessment` — "Meets target" or "Above/Below target"
  - `meets_target` — Boolean
- **demographic_context** — When enabled, population total, ages 0-14 percentage, and ages 65+ percentage.
- **regional_comparison_note** — When enabled, notes the region for which comparison data is available.

If a country name is not found, the response returns an error with a suggestion to try the full country name.

#### WHO Benchmarks & SDG Targets

| Indicator | SDG Target | WHO Target |
|---|---|---|
| Maternal mortality | SDG 3.1 | < 70 per 100,000 live births |
| Under-5 mortality | SDG 3.2 | < 25 per 1,000 live births |
| Infant mortality | SDG 3.2 | < 12 per 1,000 live births |
| Neonatal mortality | SDG 3.2 | < 12 per 1,000 live births |
| Measles immunization | SDG 3.b | >= 95% coverage |
| DPT immunization | SDG 3.b | >= 95% coverage |
| HIV prevalence | SDG 3.3 | End epidemic by 2030 |
| TB incidence | SDG 3.3 | End epidemic by 2030 |

For mortality and disease indicators, lower values are better (below target = meets target). For immunization, higher values are better (above target = meets target).

#### Health Indicators by Topic

| Topic | Indicators |
|---|---|
| mortality | Maternal mortality, Under-5 mortality, Infant mortality, Neonatal mortality, Death rate |
| life_expectancy | Life expectancy (overall), Life expectancy (male), Life expectancy (female) |
| immunization | Measles immunization, DPT immunization, Hepatitis B immunization |
| expenditure | Health expenditure per capita (USD), Health expenditure (% GDP), Physicians per 1,000, Hospital beds per 1,000, Nurses/midwives per 1,000 |
| infectious_disease | Tuberculosis incidence (per 100,000), HIV prevalence (% population) |
| demographics | Birth rate, Death rate, Fertility rate, Total population, Population ages 0-14 (%), Population ages 65+ (%), Urban population (%) |

#### Common Workflows

1. **Country health profile** — Call with `health_topic: "all"` to get a complete health snapshot with WHO benchmark comparisons.
2. **SDG 3 progress check** — Query mortality and immunization topics with `include_who_benchmarks: true` to assess progress toward health SDG targets.
3. **Health system assessment** — Use `health_topic: "expenditure"` to review healthcare spending, physician density, and hospital capacity.
4. **Cross-country comparison** — Make separate calls for different countries with the same topic and time period, then compare results.
5. **Disease burden analysis** — Use `health_topic: "infectious_disease"` with `time_period: "last10"` to track TB and HIV trends.

#### Important Notes

- Data is sourced from the World Bank World Development Indicators database.
- `health_topic` must be one of: mortality, life_expectancy, immunization, expenditure, infectious_disease, demographics, all. Invalid values produce a validation error.
- `time_period` is validated and must be `"latest"`, a 4-digit year, a `YYYY:YYYY` range, or `"last5"`/`"last10"`/`"last_5_years"`/`"last_10_years"`. Invalid formats produce a validation error.
- Data availability varies by country and indicator; some countries may have gaps.
- Most recent data may be 1-3 years behind the current year.
- All indicator data is fetched concurrently for performance.
- Demographic context is automatically excluded when the health topic is already "demographics" to avoid duplicate data.

## When To Use
- Use this skill for `Global Health & Public Health Data` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: global health & public health data, healthcare demographics data, research life expectancy by country, compare infant and child mortality rates across regions, track immunization coverage trends, analyze health expenditure as percentage of gdp, query health data, country or region.
- Supported action names: `query_health_data`.

## Use Cases
- Research life expectancy by country
- Compare infant and child mortality rates across regions
- Track immunization coverage trends
- Analyze health expenditure as percentage of GDP
- Study infectious disease prevalence
- Monitor maternal mortality rates
- Benchmark health outcomes against WHO targets
- Compare healthcare access across countries
- Support public health policy research
- Assess progress toward health-related SDG targets

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_health_data` (action slug: `query-health-data`): Fetch health and demographic data for a country or region from the World Bank. Returns mortality rates, life expectancy, immunization coverage, health expenditure, infectious disease prevalence, and demographic indicators with WHO benchmarks and SDG target comparisons. Price: `10` credits. Parameters: `country_or_region`, `health_topic`, `include_demographic_context`, `include_regional_comparison`, `include_who_benchmarks`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "healthcare-demographics-data"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "healthcare-demographics-data"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "healthcare-demographics-data"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "healthcare-demographics-data"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "healthcare-demographics-data"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "healthcare-demographics-data"
  }
}
```

## Call This Tool
Product slug: `healthcare-demographics-data`

Marketplace page: https://www.agentpmt.com/marketplace/healthcare-demographics-data

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
    "name": "Global-Health--Public-Health-Data",
    "arguments": {
      "action": "query_health_data",
      "country_or_region": "example country or region",
      "health_topic": "all",
      "include_demographic_context": true,
      "include_regional_comparison": false,
      "include_who_benchmarks": true,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "healthcare-demographics-data",
  "parameters": {
    "action": "query_health_data",
    "country_or_region": "example country or region",
    "health_topic": "all",
    "include_demographic_context": true,
    "include_regional_comparison": false,
    "include_who_benchmarks": true,
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
- If `query_health_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/healthcare-demographics-data
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
