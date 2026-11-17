---
name: oo-hithink-finance
description: "Tonghuashun Financial Data (fuyao.aicubes.cn). Use this skill for ANY Tonghuashun Financial Data request — searching and reading data. Whenever a task involves Tonghuashun Financial Data, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tonghuashun Financial Data"
  author: "OOMOL"
  version: "1.0.4"
  services: ["hithink_finance"]
  icon: "https://static.oomol.com/logo/third-party/hithink_finance.png"
---

# Tonghuashun Financial Data

Operate **Tonghuashun Financial Data** through your OOMOL-connected account. This skill calls the `hithink_finance` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tonghuashun Financial Data. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hithink_finance" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hithink_finance" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `export_full_market_daily_history` — Download the full A-share ten-year daily-price Parquet dataset and upload it to transit storage.
- `export_market_adjustment_factors` — Download the full A-share adjustment-event Parquet dataset and upload it to transit storage.
- `export_recent_market_daily_history` — Download the latest ten trading days of A-share daily-price data and upload it to transit storage.
- `get_adjustment_factors` — Get dividend and bonus-share adjustment events for one A-share security.
- `get_auction_short_term_benchmark` — Get the Tonghuashun short-term opening-auction benchmark for one date.
- `get_auction_snapshot` — Get live or final opening-auction snapshots for selected A-share securities.
- `get_balance_sheets` — Get recent consolidated balance sheets for one A-share company.
- `get_cash_flow_statements` — Get recent consolidated cash-flow statements for one A-share company.
- `get_dragon_tiger_list` — Get the Tonghuashun Dragon-Tiger list for all, institutional, or hot-money activity.
- `get_financial_indicators` — Get growth, profitability, solvency, operation, and cash-flow indicators for one report.
- `get_fund_asset_allocation` — Get disclosed stock, bond, deposit, and other asset allocation for one public fund.
- `get_fund_balance_sheets` — Get disclosed balance sheets for one public fund.
- `get_fund_bond_holdings_history` — Get disclosed historical bond holdings for one fund report period.
- `get_fund_company` — Get profile and scale information for one fund company.
- `get_fund_diagnostics` — Get Tonghuashun diagnostic dimensions and peer comparisons for one public fund.
- `get_fund_dividends` — Get dividend history and dividend summary data for one public fund.
- `get_fund_drawdowns` — Get fixed-range drawdown data for one public fund.
- `get_fund_financial_indicators` — Get the disclosed financial indicators for one public fund.
- `get_fund_holder_structure` — Get the latest institutional, personal, and staff holder structure for one public fund.
- `get_fund_holdings` — Get the latest periodically disclosed major holdings for one public fund.
- `get_fund_income_statements` — Get disclosed income statements for one public fund.
- `get_fund_industry_allocation` — Get the periodically disclosed industry allocation for one public fund.
- `get_fund_manager` — Get profile, resume, returns, and radar comparisons for one fund manager.
- `get_fund_manager_experience` — Get awards, major assets, and investment history for one fund manager.
- `get_fund_manager_investment_style` — Get investment ideas and industry preferences for one fund manager.
- `get_fund_manager_performance` — Get one fund manager's return, peer return, and benchmark return series for a fixed range.
- `get_fund_market_history` — Get up to five years of daily market history for one ETF.
- `get_fund_market_snapshot` — Get the latest exchange-market snapshot for one ETF or LOF.
- `get_fund_nav` — Get the latest or fixed-range unit and adjusted NAV series for one public fund.
- `get_fund_performance_indicators` — Get historical daily performance indicators for one public fund over a window of up to five years.
- `get_fund_profile` — Get the basic profile, company, managers, rules, and fees for one public fund.
- `get_fund_returns` — Get fixed-range returns, peer averages, and peer ranks for one public fund.
- `get_fund_stock_holdings_history` — Get disclosed historical stock holdings for one fund report period.
- `get_fund_top_holders` — Get up to ten top disclosed holders for one public fund.
- `get_hot_stock_history` — Get the Tonghuashun hot-stock ranking for one date in the latest year.
- `get_hot_stock_rank_trend` — Get one A-share security's hot-stock rank trend over a date range.
- `get_income_statements` — Get recent consolidated income statements for one A-share company.
- `get_index_constituents` — Get the current constituents of one Tonghuashun sector or standard index.
- `get_index_history` — Get daily historical prices for one index or sector over a specified window.
- `get_index_snapshot` — Get the latest market snapshot for a limited set of indexes or sectors.
- `get_limit_up_ladder` — Get the fixed 30-trading-day Tonghuashun consecutive-limit-up ladder.
- `get_stock_anomalies` — Get today's anomaly explanations for up to 50 selected A-share securities.
- `get_stock_history` — Get daily historical prices for one A-share security over a specified window.
- `get_stock_snapshot` — Get selected-security or paginated all-market A-share snapshots.
- `get_valuation_snapshot` — Get the latest fixed set of valuation ratios for up to 100 A-share securities.
- `list_fund_bond_report_dates` — List valid bond-holdings report periods for one public fund.
- `list_fund_news` — List public fund news metadata using the upstream opaque cursor.
- `list_fund_offerings` — List active or upcoming public-fund offerings.
- `list_fund_stock_report_dates` — List valid stock-holdings report periods for one public fund.
- `list_hot_stocks` — List the current Tonghuashun hot-stock ranking.
- `list_limit_break_stocks` — List stocks that touched their limit-up price and subsequently reopened.
- `list_limit_down_stocks` — List stocks in the Tonghuashun A-share limit-down pool.
- `list_limit_up_stocks` — List stocks in the Tonghuashun limit-up and consecutive-limit-up pool.
- `list_skyrocketing_stocks` — List the current Tonghuashun skyrocketing-stock ranking.
- `list_stock_anomalies` — List today's A-share anomaly explanations with optional anomaly-tag filters.
- `list_ths_indexes` — List Tonghuashun concepts, regions, special indexes, or industry sectors.
- `list_tickers` — List a bounded page of Tonghuashun instruments by exchange and asset category.
- `list_trading_days` — List A-share trading days in the service's latest one-year window.
- `search_tickers` — Search Tonghuashun instruments by code or Chinese or English name.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tonghuashun Financial Data state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tonghuashun Financial Data is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/hithink_finance
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tonghuashun Financial Data homepage: https://fuyao.aicubes.cn/
- API documentation: https://fuyao.aicubes.cn/docs/
