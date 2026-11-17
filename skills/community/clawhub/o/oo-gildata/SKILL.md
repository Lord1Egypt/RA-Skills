---
name: oo-gildata
description: "Gildata Data Map (gildata.com). Use this skill for ANY Gildata Data Map request — searching and reading data. Whenever a task involves Gildata Data Map, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gildata Data Map"
  author: "OOMOL"
  version: "1.0.4"
  services: ["gildata"]
  icon: "https://static.oomol.com/logo/third-party/gildata.png"
---

# Gildata Data Map

Operate **Gildata Data Map** through your OOMOL-connected account. This skill calls the `gildata` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gildata Data Map. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gildata" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gildata" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a current Gildata Data Map financial MCP tool with JSON arguments after checking its live schema with list_tools.
- `compare_stocks` — Compare two or more stocks across business fundamentals, growth, profitability, cash flow, valuation, industry position, and market performance.
- `get_company_news_and_announcements` — Find recent company news, exchange announcements, and earnings guidance with source and publication timestamps.
- `get_macro_data` — Find macroeconomic or industry indicators for China, local regions, or global economies and return the relevant time-series data.
- `get_stock_overview` — Get a user-oriented stock overview covering the company, core business, recent market data, financial performance, valuation, peers, and consensus expectations.
- `list_tools` — Discover the current Gildata Data Map financial tools and live input schemas from the high-level tool service or the detailed API service.
- `query_financial_data` — Answer a natural-language financial data question across securities, funds, bonds, indices, market data, and company information.
- `screen_funds` — Screen funds or ETFs with natural-language conditions covering returns, risk, holdings, fund managers, categories, or overall evaluation.
- `screen_stocks` — Screen stocks or listed companies with natural-language conditions covering industries, trading metrics, financials, valuation, or technical patterns.
- `search_research_reports` — Search brokerage research about macroeconomics, industries, listed companies, funds, or market trends.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gildata Data Map state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gildata Data Map is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gildata
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gildata Data Map homepage: https://www.gildata.com/products/datamap
