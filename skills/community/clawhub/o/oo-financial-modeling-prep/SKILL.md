---
name: oo-financial-modeling-prep
description: "Financial Modeling Prep (financialmodelingprep.com). Use this skill for ANY Financial Modeling Prep request — searching and reading data. Whenever a task involves Financial Modeling Prep, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Financial Modeling Prep"
  author: "OOMOL"
  version: "1.0.2"
  services: ["financial_modeling_prep"]
  icon: "https://static.oomol.com/logo/third-party/financial_modeling_prep.svg"
---

# Financial Modeling Prep

Operate **Financial Modeling Prep** through your OOMOL-connected account. This skill calls the `financial_modeling_prep` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Financial Modeling Prep. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "financial_modeling_prep" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "financial_modeling_prep" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_analyst_estimates` — Retrieve analyst estimate rows for one stock symbol.
- `get_asset_quote` — Retrieve the latest quote for a commodity, cryptocurrency, forex pair, or index.
- `get_balance_sheet_statement` — Retrieve balance sheet statement rows for one stock symbol from Financial Modeling Prep.
- `get_calendar` — Retrieve Financial Modeling Prep market calendar rows.
- `get_cash_flow_statement` — Retrieve cash flow statement rows for one stock symbol from Financial Modeling Prep.
- `get_company_executives` — Retrieve company executive rows for one stock symbol.
- `get_company_notes` — Retrieve company note rows for one stock symbol.
- `get_company_peers` — Retrieve peer companies for one stock symbol.
- `get_company_profile` — Retrieve the company profile for one stock symbol from Financial Modeling Prep.
- `get_company_profile_by_cik` — Retrieve company profile rows by CIK from Financial Modeling Prep.
- `get_congressional_trades` — Retrieve senate or house trading disclosure rows.
- `get_dcf` — Retrieve discounted cash flow valuation rows for one stock symbol.
- `get_economic_indicators` — Retrieve economic indicator rows such as GDP, CPI, or unemployment.
- `get_enterprise_values` — Retrieve enterprise value rows for one stock symbol.
- `get_etf_holdings` — Retrieve ETF holding rows for one ETF symbol.
- `get_financial_ratios` — Retrieve financial ratios for one stock symbol.
- `get_financial_scores` — Retrieve financial score rows for one stock symbol.
- `get_financial_statement_growth` — Retrieve financial statement growth rows for income, balance sheet, cash flow, or combined financial statements.
- `get_historical_prices` — Retrieve historical daily OHLCV prices for one stock symbol from Financial Modeling Prep.
- `get_income_statement` — Retrieve income statement rows for one stock symbol from Financial Modeling Prep.
- `get_insider_trades` — Retrieve latest or searched insider trading disclosure rows.
- `get_intraday_prices` — Retrieve intraday OHLCV prices for one stock symbol.
- `get_key_metrics` — Retrieve key financial metrics for one stock symbol.
- `get_market_cap` — Retrieve latest market capitalization rows for one stock symbol.
- `get_market_movers` — Retrieve the current biggest gainers, losers, or most active stocks from Financial Modeling Prep.
- `get_market_performance` — Retrieve sector or industry market performance snapshot rows.
- `get_news` — Retrieve latest or symbol-filtered Financial Modeling Prep news.
- `get_quote` — Retrieve the latest quote for one stock symbol from Financial Modeling Prep.
- `get_quote_short` — Retrieve the latest compact quote for one stock symbol.
- `get_ratings` — Retrieve rating snapshot, historical rating, or historical grade rows.
- `get_sec_filings` — Search SEC filing rows by symbol, CIK, or form type.
- `get_shares_float` — Retrieve shares float rows for one stock symbol.
- `get_technical_indicator` — Retrieve technical indicator rows for one symbol.
- `list_directory` — List Financial Modeling Prep directory rows such as stocks, ETFs, and exchanges.
- `search_company_screener` — Search companies with Financial Modeling Prep screener filters.
- `search_names` — Search Financial Modeling Prep securities by company or security name.
- `search_symbols` — Search Financial Modeling Prep stock symbols by ticker fragment or company name.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Financial Modeling Prep state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Financial Modeling Prep is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=financial_modeling_prep
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Financial Modeling Prep homepage: https://financialmodelingprep.com
