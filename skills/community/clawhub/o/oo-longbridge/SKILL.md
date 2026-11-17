---
name: oo-longbridge
description: "Longbridge (longbridge.com). Use this skill for ANY Longbridge request — searching and reading data. Whenever a task involves Longbridge, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Longbridge"
  author: "OOMOL"
  version: "1.0.7"
  services: ["longbridge"]
  icon: "https://static.oomol.com/logo/third-party/longbridge.png"
---

# Longbridge

Operate **Longbridge** through your OOMOL-connected account. This skill calls the `longbridge` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Longbridge. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "longbridge" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "longbridge" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ah_premium` — List Longbridge A/H premium K-line records for a dual-listed security.
- `ah_premium_intraday` — List Longbridge intraday A/H premium records for a dual-listed security.
- `anomaly` — List Longbridge quote change and anomaly records.
- `broker_holding` — List top Longbridge broker holdings for a security.
- `broker_holding_daily` — List daily Longbridge broker holding history for a broker and security.
- `broker_holding_detail` — Get detailed Longbridge broker holdings for a security.
- `business_segments` — Get Longbridge business segment data for a security.
- `business_segments_history` — List Longbridge business segment history for a security.
- `buyback` — Get Longbridge buyback data for a security.
- `company` — Get Longbridge company overview and profile data for a security.
- `consensus` — Get Longbridge financial consensus estimates for a security.
- `constituent` — List Longbridge index constituents.
- `corp_action` — List Longbridge corporate actions for a security.
- `dividend` — List Longbridge dividend history for a security.
- `dividend_detail` — Get detailed Longbridge dividend information for a security.
- `estimate_max_buy_quantity` — Estimate the maximum Longbridge buy quantity for a security without submitting an order.
- `exchange_rate` — Get Longbridge exchange rates for supported currencies.
- `executive` — List Longbridge company executives and board members for a security.
- `finance_calendar` — List Longbridge finance calendar events.
- `financial_report` — Get Longbridge financial report data for a security.
- `financial_report_latest` — Get the latest Longbridge financial report summary for a security.
- `financial_report_snapshot` — Get Longbridge earnings snapshot data for a security.
- `financial_statement` — Get Longbridge company financial statement data for a security.
- `forecast_eps` — Get Longbridge EPS forecast data for a security.
- `fund_holder` — List Longbridge funds and ETFs holding a security.
- `get_market_temperature` — Get the current Longbridge market sentiment temperature for a market.
- `get_order_detail` — Get a Longbridge order detail record by order ID.
- `industry_peers` — List Longbridge industry peer securities for a security.
- `industry_valuation` — Get Longbridge industry peer valuation comparison for a security.
- `industry_valuation_dist` — Get Longbridge industry valuation distribution for a security.
- `institution_rating` — Get the latest Longbridge institution analyst rating summary for a security.
- `institution_rating_detail` — Get Longbridge institution analyst rating detail for a security.
- `institution_rating_history` — List Longbridge institution analyst rating history for a security.
- `institution_rating_industry_rank` — Get Longbridge institution rating industry rank for a security.
- `institutional_views` — List Longbridge institutional views for a security.
- `invest_relation` — List Longbridge investor relations records for a security.
- `list_account_cash` — List Longbridge account cash balances visible to the connected OAuth user.
- `list_cash_flow` — List Longbridge account cash flow records visible to the connected OAuth user.
- `list_filings` — List Longbridge regulatory filings and disclosure documents for a symbol.
- `list_fund_positions` — List Longbridge fund positions visible to the connected OAuth user.
- `list_history_executions` — List historical Longbridge execution records visible to the connected OAuth user.
- `list_history_orders` — List historical Longbridge orders visible to the connected OAuth user.
- `list_market_temperature` — List historical Longbridge market sentiment temperature values for a market and date range.
- `list_news` — List Longbridge news articles for a symbol.
- `list_securities` — List Longbridge tradable securities for a market and category.
- `list_stock_positions` — List Longbridge stock positions visible to the connected OAuth user.
- `list_today_executions` — List today's Longbridge execution records visible to the connected OAuth user.
- `list_today_orders` — List today's Longbridge orders visible to the connected OAuth user.
- `list_watchlist_groups` — List Longbridge watchlist groups for the connected OAuth user.
- `market_status` — Get Longbridge market trading status for supported markets.
- `market_stock_events` — List Longbridge market stock events.
- `news` — List Longbridge news articles for a symbol.
- `operating` — Get Longbridge operating metrics for a security.
- `option_volume` — List Longbridge real-time option volume statistics for an underlying security.
- `option_volume_daily` — List Longbridge historical daily option volume statistics for an underlying security.
- `profit_analysis` — Get Longbridge portfolio profit and loss analysis summary.
- `profit_analysis_by_market` — List Longbridge portfolio profit and loss analysis grouped by market.
- `profit_analysis_detail` — Get Longbridge portfolio profit and loss detail for a security.
- `profit_analysis_flows` — List Longbridge portfolio profit and loss flow records for a security.
- `profit_analysis_sublist` — List Longbridge portfolio profit and loss analysis sublist records.
- `rank_categories` — List Longbridge market ranking categories.
- `rank_list` — List Longbridge ranked securities for a market ranking category.
- `screener_indicators` — List Longbridge screener indicator definitions.
- `screener_recommend_strategies` — List Longbridge recommended screener strategies.
- `screener_search` — Search Longbridge securities with screener filters.
- `screener_strategy` — Get one Longbridge screener strategy by ID.
- `screener_user_strategies` — List Longbridge saved screener strategies for the connected user.
- `shareholder` — List Longbridge shareholder records for a security.
- `shareholder_detail` — Get Longbridge shareholder holding detail for a security and shareholder object.
- `shareholder_top` — List Longbridge top shareholder records for a security.
- `short_margin` — Get Longbridge short margin information for the connected account.
- `short_positions` — List Longbridge short interest records for a US or HK security.
- `short_trades` — List Longbridge short sale trade records for a US or HK security.
- `stock_rating_history` — List Longbridge stock rating history records for a security.
- `stock_ratings` — List Longbridge stock rating records for a security.
- `trade_stats` — Get Longbridge trade statistics for a security.
- `valuation` — Get Longbridge valuation metrics for a security.
- `valuation_comparison` — Compare Longbridge valuation metrics between a security and optional peers.
- `valuation_history` — List Longbridge historical valuation detail data for a security.
- `valuation_rank` — Get Longbridge valuation rank data for a security.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Longbridge state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Longbridge is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/longbridge
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Longbridge homepage: https://longbridge.com
- API documentation: https://open.longbridge.com/docs
