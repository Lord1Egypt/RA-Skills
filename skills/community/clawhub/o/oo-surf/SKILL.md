---
name: oo-surf
description: "Surf (asksurf.ai). Use this skill for ANY Surf request — reading, creating, updating, and deleting data. Whenever a task involves Surf, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Surf"
  author: "OOMOL"
  version: "1.0.2"
  services: ["surf"]
  icon: "https://static.oomol.com/logo/third-party/surf.svg"
---

# Surf

Operate **Surf** through your OOMOL-connected account. This skill calls the `surf` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Surf. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "surf" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "surf" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `credit_balance` — Read the current API account credit balance.
- `dex_token_price` — DEX Token OHLCV Price.
- `equity_balance_sheet` — Equity Balance Sheet.
- `equity_candles` — Equity Price Candles.
- `equity_cash_flow` — Equity Cash Flow.
- `equity_company_profile` — Equity Profile.
- `equity_etf_holdings` — ETF Holdings.
- `equity_filings` — Equity SEC Filings.
- `equity_financial_metrics` — Equity Financial Metrics.
- `equity_income_statement` — Equity Income Statement.
- `equity_latest_filings` — Latest Equity Filings.
- `equity_latest_financials` — Latest Equity Financials.
- `equity_listings` — Equity Listings.
- `equity_meta` — Equity Metadata.
- `equity_overview` — Equity Financial Overview.
- `equity_segments` — Equity Segment Financials.
- `exchange_candles` — Exchange Historical Candles.
- `exchange_coverage` — Exchange Market Coverage.
- `exchange_depth` — Exchange Order Book Depth.
- `exchange_funding_history` — Exchange Funding Rate History.
- `exchange_klines` — Exchange OHLCV Candlesticks.
- `exchange_long_short_ratio` — Exchange Long/Short Ratio History.
- `exchange_markets` — Exchange Trading Pairs.
- `exchange_perp` — Exchange Perpetual Contract Snapshot.
- `exchange_price` — Exchange Ticker Price.
- `fund_detail` — Fund Profile Detail.
- `fund_portfolio` — Fund Portfolio.
- `fund_ranking` — Fund Ranking.
- `hyperliquid_account` — Account Portfolio.
- `hyperliquid_candles` — Market Candles.
- `hyperliquid_fills` — Fills.
- `hyperliquid_leaderboard` — Trader Leaderboard.
- `hyperliquid_orders` — Open & Recent Orders.
- `hyperliquid_performance` — Trading Performance.
- `hyperliquid_positions` — Open Positions.
- `hyperliquid_trade_context` — Closed Trade Funding and Leverage.
- `hyperliquid_trades` — Closed Trades.
- `hyperliquid_trades_aggregate` — Closed Trades Aggregate.
- `kalshi_events` — Kalshi Events.
- `kalshi_markets` — Kalshi Markets.
- `kalshi_open_interest` — Kalshi Open Interest History.
- `kalshi_orderbooks` — Kalshi Orderbook History.
- `kalshi_prices` — Kalshi Price History.
- `kalshi_trades` — Kalshi Trades.
- `kalshi_volumes` — Kalshi Volume History.
- `listing` — Exchange Listing Events.
- `market_etf` — ETF Flow History.
- `market_exchange_flow_exchanges` — Exchange Flow Exchanges.
- `market_fear_greed` — Fear & Greed Index History.
- `market_futures` — Futures Market Overview.
- `market_liquidation_chart` — Liquidation Chart.
- `market_liquidation_exchange_list` — Liquidation by Exchange.
- `market_liquidation_order` — Large Liquidation Orders.
- `market_onchain_indicator` — On-Chain Indicator.
- `market_options` — Options Market Data.
- `market_price` — Token Price History.
- `market_price_indicator` — Technical Indicator.
- `market_public_sale` — Public Sale / Crowdsale.
- `market_ranking` — Token Rankings.
- `market_tge` — Token Generation Event.
- `matching_market_daily` — Cross-Platform Daily Comparison (Polymarket <> Kalshi).
- `matching_market_pairs` — Cross-Platform Prediction Market Matcher (Polymarket <> Kalshi).
- `news_detail` — News Article Detail.
- `news_feed` — Crypto News Feed.
- `onchain_bridge_ranking` — Bridge Protocol Ranking.
- `onchain_dex_activity` — DEX Protocol Activity.
- `onchain_gas_price` — Current Gas Price.
- `onchain_schema` — On-Chain Table Schema.
- `onchain_sql` — Execute a read-only ClickHouse SELECT/WITH query against agent.<table> blockchain data. Discover tables with onchain_schema and filter large tables by block_date or block_number. Normalize address literals to lowercase without wrapping indexed address columns in lower(); use separate UNION ALL branches instead of OR for transfer from/to predicates. Resolve token symbols with search_token before querying contracts. The synchronous budget is 30 seconds; use prefer=respond-async and a stable idempotency_key for long queries. Do not automatically retry synchronous timeouts; submit an asynchronous job instead. [destructive]
- `onchain_sql_job_cancel` — Cancel Asynchronous Blockchain SQL Job. [destructive]
- `onchain_sql_job_create` — Submit a read-only ClickHouse SELECT/WITH query as a durable asynchronous job. Use agent.<table> names, partition filters, and resolved contract addresses as for onchain_sql. A retained job is reused for the same idempotency key or equivalent normalized SQL and max_rows. Poll onchain_sql_job_get, then read onchain_sql_job_results; results are retained for 24 hours. [destructive]
- `onchain_sql_job_get` — Get Asynchronous Blockchain SQL Job.
- `onchain_sql_job_results` — Download Asynchronous Blockchain SQL Results.
- `onchain_sql_preflight` — Preflight Blockchain SQL Query.
- `onchain_structured_query` — Query blockchain data with structured column, filter, and sort clauses. Discover agent.<table> sources with onchain_schema; always filter large tables by block_date. Resolve token symbols using search_token rather than filtering unindexed symbol columns. Transfer amount is decimal-adjusted, while amount_raw is in base units.
- `onchain_tx` — Transaction Details by Hash.
- `onchain_yield_ranking` — Yield Pool Ranking.
- `polymarket_events` — Polymarket Events.
- `polymarket_leaderboard` — Polymarket Leaderboard.
- `polymarket_markets` — Polymarket Markets.
- `polymarket_open_interest` — Polymarket Open Interest History.
- `polymarket_orderbooks` — Polymarket Orderbook History.
- `polymarket_positions` — Polymarket Wallet Positions.
- `polymarket_price_ohlcv` — Polymarket OHLCV Candlesticks.
- `polymarket_prices` — Polymarket Price History.
- `polymarket_smart_money` — Polymarket Smart Money.
- `polymarket_trades` — Polymarket Trades.
- `polymarket_volume_split` — Polymarket Volume Split (YES/NO).
- `polymarket_volumes` — Polymarket Volume History.
- `portfolio_wallets` — Current User Portfolio Wallets.
- `prediction_market_analytics` — Prediction Market Analytics.
- `prediction_market_correlations` — Market Correlations.
- `project_ai_news` — Project AI News.
- `project_defi_metrics` — Project DeFi Metrics.
- `project_defi_ranking` — DeFi Protocol Ranking.
- `project_detail` — Aggregated Project Detail.
- `project_pulse` — Project Pulse [Deprecated].
- `research` — Research crypto and equity markets with Surf Research 2.0 and return non-streaming Responses JSON. Use previous_response_id to continue a response chain. surf-2.0-instant favors latency; surf-2.0 supports optional nested reasoning.effort for deeper analysis, with higher latency and credit cost. [write]
- `search_airdrop` — Airdrop Search.
- `search_airdrop_activities` — Airdrop Activities.
- `search_events` — Project Event Search.
- `search_fund` — Fund Search.
- `search_fundraising` — Fundraising Event Search.
- `search_news` — News Article Search.
- `search_prediction_market` — Search Prediction Markets.
- `search_project` — Project Search.
- `search_token` — Token Symbol Resolution.
- `search_wallet` — Wallet Search.
- `search_web` — Web Search.
- `signal_detail` — Signal Detail.
- `signal_projects` — Signal Projects.
- `signal_token_of_the_day` — Signal Token Of The Day.
- `signal_token_of_week` — Signal Token Of The Week.
- `social_mindshare` — Project Mindshare Time Series.
- `token_dex_trades` — Token DEX Trade History.
- `token_holders` — Token Holders.
- `token_tokenomics` — Token Unlock Schedule.
- `token_transfer_counterparties` — Top Transfer Counterparties.
- `token_transfer_stats` — Token Transfer Activity Summary.
- `token_transfers` — Token Transfer History.
- `wallet_detail` — Aggregated Wallet Detail.
- `wallet_history` — Wallet Transaction History.
- `wallet_labels_batch` — Wallet Labels (Batch).
- `wallet_net_worth` — Wallet Net Worth History.
- `wallet_protocols` — Wallet DeFi Protocol Positions.
- `wallet_transfers` — Wallet Transfer History.
- `web_fetch` — Web Page Fetch.
- `x_tweets` — X Tweets by IDs.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Surf state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Surf is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/surf
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Surf homepage: https://asksurf.ai
- API documentation: https://docs.asksurf.ai/data-api/overview
