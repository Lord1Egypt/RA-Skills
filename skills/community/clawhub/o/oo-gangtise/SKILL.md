---
name: oo-gangtise
description: "Gangtise (gangtise.com). Use this skill for ANY Gangtise request — searching and reading data. Whenever a task involves Gangtise, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gangtise"
  author: "OOMOL"
  version: "1.0.4"
  services: ["gangtise"]
  icon: "https://static.oomol.com/logo/third-party/gangtise.png"
---

# Gangtise

Operate **Gangtise** through your OOMOL-connected account. This skill calls the `gangtise` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gangtise. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gangtise" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gangtise" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_company_indicators` — Get Gangtise A-share company indicator values as a time series or a single-date cross section.
- `get_daily_kline` — Get Gangtise unadjusted daily K-line market data for exact security codes in one supported market.
- `get_earnings_forecast` — Get Gangtise broker-consensus earnings forecasts for exact security codes.
- `get_financial_statements` — Get Gangtise income statements, balance sheets, or cash-flow statements for exact security codes.
- `get_fund_flow` — Get historical A-share daily small, medium, large, extra-large, total, and main-fund net inflows.
- `get_main_business_breakdown` — Get a company's main-business revenue and profitability breakdown by product, industry, or region.
- `get_minute_kline` — Get historical minute K-line data for one or more exact A-share security codes.
- `get_realtime_quotes` — Get current Gangtise market snapshots for one or more exact security codes.
- `get_top_shareholders` — Get the top ten shareholders or top ten floating shareholders for exact security codes.
- `get_valuation_metrics` — Get Gangtise valuation metrics and their percentile ranks over a requested date range.
- `search_announcements` — Search Gangtise company announcement indexes without downloading source files.
- `search_company_indicators` — Search Gangtise A-share company indicators before requesting time-series or cross-section values.
- `search_meeting_summaries` — Search Gangtise meeting and research summaries without downloading source files.
- `search_reports` — Search Gangtise domestic broker research reports without downloading report files.
- `search_securities` — Search Gangtise securities by name, code, abbreviation, or pinyin before requesting market data.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gangtise state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gangtise is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gangtise
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gangtise homepage: https://www.gangtise.com
- API documentation: https://github.com/gangtise-ai/gangtise-mcp
