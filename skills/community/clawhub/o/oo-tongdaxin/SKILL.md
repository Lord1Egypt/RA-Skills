---
name: oo-tongdaxin
description: "Tongdaxin (vip.tdx.com.cn). Use this skill for ANY Tongdaxin request — reading, creating, updating, and deleting data. Whenever a task involves Tongdaxin, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tongdaxin"
  author: "OOMOL"
  version: "1.0.5"
  services: ["tongdaxin"]
  icon: "https://static.oomol.com/logo/third-party/tongdaxin.png"
---

# Tongdaxin

Operate **Tongdaxin** through your OOMOL-connected account. This skill calls the `tongdaxin` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tongdaxin. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tongdaxin" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tongdaxin" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a Tongdaxin MCP tool with arguments matching its input schema. [destructive]
- `get_board_and_industry_data` — Get Tongdaxin board profiles, returns, market statistics, industry chains, or important industry events.
- `get_capital_and_trading_data` — Get Tongdaxin capital flow, northbound holdings, block trades, margin data, refinancing, limit analysis, or shareholder-change events.
- `get_company_profile` — Get a Tongdaxin company overview, basic profile, issuance history, executives, or affiliates.
- `get_dividends_and_financing` — Get Tongdaxin dividend, payout, yield, rights-issue, placement, or refinancing data.
- `get_financial_statements` — Get structured A-share income statements, balance sheets, or cash-flow statements from Tongdaxin F10.
- `get_hk_financials` — Get Tongdaxin Hong Kong income statements, balance sheets, or cash-flow statements.
- `get_hot_topics` — Get Tongdaxin board-family, theme-library, event-driven, or information-overview data for a stock.
- `get_institutional_holdings` — Get Tongdaxin institutional-holding periods, summaries, distributions, details, northbound holdings, or price comparisons.
- `get_kline` — Get Tongdaxin historical OHLCV data for a security, index, board, or futures contract.
- `get_quotes` — Get a real-time Tongdaxin market snapshot with optional order-book, valuation, financial, and ranking data.
- `get_share_capital` — Get Tongdaxin share-capital structure, historical changes, restricted-share unlocks, or stock buybacks.
- `get_shareholder_research` — Get Tongdaxin controlling-shareholder, shareholder-count, ranking, or top-shareholder data.
- `get_valuation_and_ranking` — Get Tongdaxin valuation history, industry rankings, financial-sector indicators, or board valuation comparisons.
- `list_tools` — Discover the Tongdaxin MCP tools available to this connection with their live input schemas.
- `lookup_security` — Resolve a security, fund, index, futures contract, or option underlying to Tongdaxin codes and market parameters.
- `query_indicators` — Query Tongdaxin valuation, financial, company, shareholder, market, concept, or industry-chain indicators for named entities.
- `query_macro_data` — Query Tongdaxin macroeconomic data such as GDP, CPI, PPI, social financing, money supply, interest rates, exchange rates, trade, employment, and population.
- `screen_fund_managers` — Screen fund managers with natural-language experience, performance, product, or risk criteria.
- `screen_funds` — Screen funds with natural-language performance, manager, risk, holding, or allocation criteria.
- `screen_hk_stocks` — Screen Hong Kong stocks with natural-language technical, capital-flow, and fundamental criteria.
- `screen_indices` — Screen indices with natural-language market, valuation, performance, or technical criteria.
- `screen_stocks` — Screen A-share securities with natural-language technical, capital-flow, and fundamental criteria.
- `search_announcements` — Search Tongdaxin company announcements, regulatory filings, and periodic reports.
- `search_news` — Search current Tongdaxin financial news, market briefs, themes, and company-related information.
- `search_reports` — Search Tongdaxin broker research, rating changes, target prices, and opinion summaries.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tongdaxin state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tongdaxin is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tongdaxin
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tongdaxin homepage: https://vip.tdx.com.cn/site/app/pc-mall/main.html#/page_product_mcp
- API documentation: https://help.tdx.com.cn/tdxclaw/docs/markdown/tdxclaw-api-key-data.html
