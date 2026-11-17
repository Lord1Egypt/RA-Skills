---
name: oo-wind
description: "Wind (market.windalice.com). Use this skill for ANY Wind request — reading, creating, and updating data. Whenever a task involves Wind, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Wind"
  author: "OOMOL"
  version: "1.0.3"
  services: ["wind"]
  icon: "https://static.oomol.com/logo/third-party/wind.png"
---

# Wind

Operate **Wind** through your OOMOL-connected account. This skill calls the `wind` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Wind. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wind" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wind" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `download_alice_report` — Download a Wind Alice report or spreadsheet with the connected API Key and return a transferable file URL. Accepts official Alice file URLs or project-relative references from an analysis result.
- `get_bond_basicinfo` — Query bond profiles and instrument attributes.
- `get_bond_financial_data` — Query bond issuer financial statements and ratios.
- `get_bond_issuer_info` — Query bond issuer profiles and information.
- `get_bond_market_data` — Query bond market prices, yields and valuations.
- `get_company_announcements` — Search company announcements, annual reports and regulatory disclosures; not media news.
- `get_financial_data` — Compute cross-entity aggregates, weighted averages, rankings and composite financial indicators; use dedicated tools for quotes and entity screening.
- `get_financial_news` — Search financial news by topic, entity and date; not issuer announcements or brokerage research reports.
- `get_fund_company_info` — Query fund management company profiles and business information.
- `get_fund_financials` — Query fund financial statements and financial indicators.
- `get_fund_holders` — Query fund holder structure and ownership information.
- `get_fund_holdings` — Query fund portfolio holdings and asset allocation by reporting period.
- `get_fund_info` — Query fund profiles, managers and product information.
- `get_fund_kline` — Get historical ETF or LOF OHLCV bars over an explicit date range.
- `get_fund_performance` — Query fund performance, returns and related evaluation metrics.
- `get_fund_price_indicators` — Get current exchange-traded fund price indicators for up to 50 funds; not historical time series.
- `get_fund_quote` — Get minute-level ETF or LOF quotes; omit dates for the latest trading day.
- `get_index_basicinfo` — Query index profiles, publishers, base dates and constituents.
- `get_index_fundamentals` — Query index or sector valuation and constituent-weighted fundamental metrics.
- `get_index_kline` — Get historical index OHLCV bars over an explicit date range.
- `get_index_price_indicators` — Get current price indicators for up to 50 indices; not historical time series.
- `get_index_quote` — Get minute-level index quotes; omit dates for the latest trading day.
- `get_index_technicals` — Query index or sector technical indicators and rolling returns.
- `get_risk_metrics` — Query stock risk metrics such as beta, volatility, Sharpe ratio and maximum drawdown.
- `get_stock_basicinfo` — Query stock identity, listing, industry and company profile information.
- `get_stock_equity_holders` — Query stock capital structure, major shareholders and institutional holdings.
- `get_stock_events` — Query structured corporate actions, dividends, financing, shareholder and regulatory events; not announcement text.
- `get_stock_fundamentals` — Query stock financial statements, ratios and valuation indicators by reporting or trading date.
- `get_stock_kline` — Get historical stock OHLCV bars over an explicit date range.
- `get_stock_price_indicators` — Get current stock price, valuation and market indicators for up to 50 stocks; not historical time series.
- `get_stock_quote` — Get minute-level stock quotes; omit dates for the latest trading day, and prefer K-line bars for long ranges.
- `get_stock_technicals` — Query stock technical indicators, rolling returns and technical patterns.
- `list_tools` — Discover current Wind tools and their live input and output schemas in one financial data domain.
- `query_economic_indicator_data` — Retrieve Wind EDB time series by question or indicator codes, using a date range or observation count.
- `resume_alice_analysis` — Resubscribe to an existing Wind Alice task after interruption without starting a new analysis. Returns within a 120-second subscription window. Retain previous window results and any error.data.partialResult because Wind does not guarantee prior output replay.
- `run_alice_analysis` — Run Wind Alice financial research, company memos, earnings reviews, peer comparisons, fact checks, fund analysis, macro and credit research. Returns within a 120-second subscription window with results and recovery identifiers; analysis may continue and consume Wind credits. If completed is false, retain this window and resume the same task instead of submitting again. [write]
- `search_economic_indicator` — Find Wind EDB economic indicators and their metadata; does not return time-series values.
- `search_funds` — Screen funds using natural-language conditions without requiring a specific fund.
- `search_stocks` — Screen A-share, Hong Kong and US stocks using natural-language conditions.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Wind state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Wind is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/wind
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Wind homepage: https://market.windalice.com/
- API documentation: https://github.com/Wind-Alice/AliceMarket/tree/main/skills/wind-mcp-skill/references
