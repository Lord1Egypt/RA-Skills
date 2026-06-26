# InvestToday Financial Data Skill

Fetch Chinese financial-market data with coverage across A-shares, Hong Kong stocks, indices, market data, research reports, news, real-time quotes, macroeconomics, and related datasets.

Use when: the user asks for stock trends, fund NAV, ETF performance, index quotes, financial statements, valuation metrics, announcements, research reports, institutional views, macro data, sectors, themes, industry chains, market statistics, or structured financial data export and comparison.

Do not use when: the user asks for direct buy/sell advice, automated trading, order execution, non-financial data, system operations troubleshooting, or conclusions that would require inventing missing data.

## What This Skill Is For

Common tasks for this skill:

- Review recent price action for stocks, Hong Kong stocks, indices, funds, and ETFs
- Check company profile, financial trends, valuation, and operating performance
- Gather announcements, research reports, news, and institutional views
- Inspect sectors, themes, industry chains, and market heat
- Read macroeconomic and market datasets
- Export structured datasets for later analysis, comparison, or backtesting

Start from the user's research goal, then decide whether to browse categories, search APIs, or call a known endpoint directly.

## When To Use

Prefer this skill when the user's intent matches one of these:

- Price action / trend: recent moves, relative strength, turnover, market activity
- Financials / valuation: reports, profit trends, valuation, cash flow, dividends, metrics
- Announcements / research / news: recent filings, catalysts, institutional views, report summaries
- Funds / ETFs / indices: NAV, quotes, constituents, fund profile, performance
- Sectors / themes / industry chains: strongest sectors, theme heat, industry relationships
- Macro / market: CPI, PPI, PMI, rates, market statistics, macro indicators
- Data export / research prep: pull structured datasets for downstream analysis or comparison

Typical user phrasing:

- Check how this stock has been doing recently
- Show me fund NAV or ETF performance
- I want to export financial data
- Find recent announcements, research reports, or institutional views
- Compare financial metrics for several companies
- Which sector has been stronger recently
- Pull macroeconomic or market statistics

## What This Skill Is Not For

This skill is not for:

- Giving direct trading advice or replacing an investment advisor
- Automated trading or order execution
- Querying non-financial data, system ports, server status, or other operations issues
- Inventing conclusions when data is unavailable, incomplete, or out of scope
- Building a backtesting engine, optimizer, or trading system itself

If data access, time range, or endpoint capability is limited, say so clearly.

## Decision Flow

Use this order:

1. First decide whether the user needs quotes, financials, announcements and research, funds and indices, macro data, data export, or something outside this skill.
2. If the endpoint is unclear, use `investoday-api list` to browse groups or `investoday-api search-api` to search by keyword.
3. If the endpoint is clear but parameters are unclear, use `investoday-api search-api` to inspect usage, parameters, and examples.
4. If both endpoint and parameters are clear, call `investoday-api <endpoint> [key=value ...]`.
5. If results are empty or unavailable, state the query scope, time range, permission, or network limitation instead of inventing conclusions.

When the user speaks in natural language, interpret the task first instead of jumping to endpoint names. Prefer to treat:

- "recently" as a reasonable time window
- "financials" as recent quarters or recent annual periods
- "strong or weak" as trend, relative performance, and activity
- "catalyst" as announcements, reports, news, or policy signals

## Installation & Usage

Requires Node.js 18+ and the Node package `@investoday/investoday-api`.

`investoday-api init` initializes the CLI's local runtime configuration and may create or update local config files used by the CLI.

## CLI Command Reference

```bash
# Initialize runtime
investoday-api init

# Non-interactive one-shot initialization
investoday-api init --api-key "<API_KEY>" --auto-update --skip-verify

# Browse multi-level groups and leaf categories
investoday-api list <group/subgroup/leaf>

# Search APIs by keyword or tool id.
# query and tool_ids can contain multiple values separated by English commas.
investoday-api search-api query=<query> tool_ids=<tool_ids>

# Fetch data
investoday-api <endpoint> [key=value ...]

# For POST endpoints where references separate Query parameters and Body JSON parameters:
# pass Query parameters as key=value and Body JSON parameters with --body-json.
investoday-api <endpoint> --method POST [queryKey=value ...] --body-json '{"bodyKey":[]}'
```

Examples:

```bash
# Initialize runtime
investoday-api init

# Non-interactive one-shot initialization
investoday-api init --api-key "<API_KEY>" --auto-update --skip-verify

# List categories
investoday-api list
investoday-api list 沪深京数据
investoday-api list 沪深京数据/公司行为/基本信息

# Keyword search
investoday-api search-api query=股票,基本面分析

# Tool-id search
investoday-api search-api tool_ids=list_stock_violation_penalt,list_stock_report_schema

# Fetch data
investoday-api search key=贵州茅台 type=11
investoday-api stock/basic-info stockCode=600519
investoday-api fund/daily-quotes --method POST fundCode=000001 beginDate=2024-01-01 endDate=2024-12-31
investoday-api industry-quote/realtime-v2 --method POST industryLevel=1 industryType=SW sortColumn=changeRatio order=desc pageSize=10 --body-json '{"industryCodes":[]}'
```

## Usage Strategy

- If the endpoint is unclear, use `list` or `search-api` to find it.
- If the endpoint is clear but parameters are unclear, use `search-api` to get the usage details.
- If both the endpoint and usage are clear, call it directly.
- For POST endpoints where references separate `Query parameters` and `Body JSON parameters`, pass Query as `key=value` and Body as `--body-json`; do not pass array or object Body values as plain string parameters.

## Failure Handling

- If `investoday-api init` has not been run or local runtime configuration is missing, ask to run `investoday-api init` before continuing the data query.
- If required inputs such as stock code, fund code, time range, or market type are missing, state which inputs are missing and provide the minimum inputs needed to continue.
- If an endpoint returns no data, explain that the current query scope, time range, or data coverage may not support the request; do not treat an empty result as a definitive market conclusion.
- If network, permission, or service access is unavailable, state that the data cannot currently be fetched and stop any inference that depends on it.

## Supporting Docs

- API reference index: `docs/references-index.en.md`
