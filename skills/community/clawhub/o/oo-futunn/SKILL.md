---
name: oo-futunn
description: "Futunn (open.futunn.com). Use this skill for ANY Futunn request — searching and reading data. Whenever a task involves Futunn, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Futunn"
  author: "OOMOL"
  version: "1.0.3"
  services: ["futunn"]
  icon: "https://static.oomol.com/logo/third-party/futunn.svg"
---

# Futunn

Operate **Futunn** through your OOMOL-connected account. This skill calls the `futunn` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Futunn. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "futunn" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "futunn" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_funds` — Get account assets, cash, buying power and margin balances in the requested currency.
- `get_capital_distribution` — Get current-day capital inflow and outflow distribution by order size.
- `get_capital_flow` — Get intraday capital flow by order size and trading session.
- `get_capital_flow_history` — Get daily, weekly or monthly capital flows; move end earlier to retrieve preceding data.
- `get_financial_statements` — Get financial statements or key metrics by reporting period.
- `get_history_kline` — Get a page of historical candlesticks, retaining the next-page timestamp and volume precision.
- `get_market_snapshot` — Get real-time market snapshots and valuation metrics for up to 400 securities.
- `get_market_state` — Get trading-session states for a batch of securities.
- `get_operational_efficiency` — Get historical employee counts and per-employee financial metrics.
- `get_order_details` — Get details of fewer than 50 orders from the same exchange.
- `get_revenue_breakdown` — Get revenue composition by product, industry, region or business.
- `get_security_info` — Get basic security information, including listing date and lot size.
- `get_valuation` — Get PE, PB or PS valuation history and market or sector comparisons.
- `list_accounts` — List trading accounts authorized by the connected user.
- `list_history_deals` — List historical execution fills filtered by update time in microseconds.
- `list_history_orders` — List historical orders filtered by creation time in microseconds.
- `list_open_orders` — List recent orders, including pending orders and orders filled or cancelled in the last 24 hours.
- `list_positions` — List account positions, optionally filtered by security code and profit/loss ratio.
- `list_today_deals` — List today's execution fills for a trading account.
- `list_trading_days` — List trading days for a market within an inclusive date range.
- `screen_stocks` — Screen securities with combined market, financial and technical conditions.
- `search_community` — Search community discussions, topics and live streams by keyword.
- `search_news` — Search news, announcements and research reports by keyword.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Futunn state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Futunn is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/futunn
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Futunn homepage: https://open.futunn.com
- API documentation: https://open.futunn.com/zh-cn/api/overview/getting-started
