---
name: oo-zyhub
description: "Sina Finance ZYHub (zyhub.finance.sina.cn). Use this skill for ANY Sina Finance ZYHub request — searching and reading data. Whenever a task involves Sina Finance ZYHub, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sina Finance ZYHub"
  author: "OOMOL"
  version: "1.0.2"
  services: ["zyhub"]
  icon: "https://static.oomol.com/logo/third-party/zyhub.png"
---

# Sina Finance ZYHub

Operate **Sina Finance ZYHub** through your OOMOL-connected account. This skill calls the `zyhub` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sina Finance ZYHub. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zyhub" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zyhub" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_batch_forex_quotes` — Get current quotes for multiple target currencies against one base currency.
- `get_block_trades` — Get block trades for an A-share company.
- `get_company_profile` — Get Sina Finance profile and reference data for an A-share company.
- `get_daily_kline` — Get daily Sina Finance candlesticks for a stock or global index.
- `get_financial_report` — Get one A-share financial statement or indicator report for a reporting date.
- `get_forex_quote` — Get the latest Sina Finance quote for a currency pair.
- `get_fund_asset_allocation` — Get a fund's asset allocation.
- `get_fund_industry_allocation` — Get a fund's industry allocation and changes from the prior reporting period.
- `get_fund_manager` — Get the background and historical average return of a fund manager.
- `get_fund_metrics` — Get core performance and risk metrics for a fund.
- `get_fund_net_values` — Get historical unit and cumulative net values for a fund.
- `get_fund_profile` — Get a fund's profile, classification, manager, scale, and investment mandate.
- `get_fund_returns` — Get cumulative returns and peer rankings for a fund.
- `get_fund_stock_holdings` — Get the major stock holdings of a fund.
- `get_futures_quote` — Get the latest quote for a domestic, global, or Chinese financial futures contract.
- `get_intraday_kline` — Get minute-level candlesticks for an A-share, index, or virtual sector.
- `get_major_events` — Get major corporate events for an A-share, Hong Kong, or US-listed company.
- `get_margin_trading` — Get historical margin-financing and securities-lending data for an A-share.
- `get_news_article` — Get the title, publication time, and body of one Sina Finance article.
- `get_revenue_composition` — Get an A-share company's revenue, cost, and gross-margin composition.
- `get_sector_constituents` — Get and rank the constituents of an A-share index or virtual sector.
- `get_stock_industry` — Get the Shenwan level-one, level-two, and level-three industries for an A-share.
- `get_stock_quote` — Get the latest Sina Finance quote for a stock or global index.
- `get_valuation_history` — Get historical valuation data for an A-share, its industry, and the broad market.
- `list_consecutive_limit_up_stocks` — List A-shares currently in the consecutive-limit-up pool.
- `list_financial_report_dates` — List available financial-report dates for an A-share company.
- `list_flash_news` — List the latest Sina Finance market flashes or page around a known document ID.
- `list_hot_stocks` — List daily or hourly popular stocks and funds.
- `list_limit_up_stocks` — List the current A-share limit-up pool.
- `list_sector_rankings` — Rank A-share industries, concepts, or regions by market and fund-flow metrics.
- `list_stock_connect_holdings` — List Shanghai, Shenzhen, or Hong Kong Stock Connect holdings.
- `list_strong_sectors` — List strong A-share concept, industry, or regional sectors.
- `search_flash_news` — Search Sina Finance market flashes by one or more keywords.
- `search_news` — Search Sina Finance news by one or more keywords.
- `search_stock_news` — Search news for one A-share, Hong Kong, or US-listed stock.
- `search_symbols` — Search Sina Finance instrument symbols across one or more markets.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sina Finance ZYHub state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sina Finance ZYHub is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zyhub
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sina Finance ZYHub homepage: https://zyhub.finance.sina.cn/
- API documentation: https://zyhub.finance.sina.cn/help/interface
