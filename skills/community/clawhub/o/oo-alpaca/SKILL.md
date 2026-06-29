---
name: oo-alpaca
description: "Alpaca (alpaca.markets). Use this skill for ANY Alpaca request — reading, creating, and updating data. Whenever a task involves Alpaca, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Alpaca"
  author: "OOMOL"
  version: "1.0.0"
  services: ["alpaca"]
  icon: "https://static.oomol.com/logo/third-party/alpaca.svg"
---

# Alpaca

Operate **Alpaca** through your OOMOL-connected account. This skill calls the `alpaca` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Alpaca. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "alpaca" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "alpaca" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account` — Get Alpaca Trading API account details for the connected paper or live account.
- `get_account_config` — Get Alpaca account configuration values.
- `get_account_portfolio_history` — Get Alpaca account equity and profit/loss time series.
- `get_asset` — Get one Alpaca asset by symbol or asset ID.
- `get_crypto_bars` — Get historical OHLC crypto bars from Alpaca Market Data API.
- `get_crypto_snapshots` — Get latest crypto snapshots from Alpaca Market Data API.
- `get_market_calendar` — Get Alpaca Trading API US market calendar days.
- `get_market_clock` — Get Alpaca Trading API US market clock information.
- `get_option_contract` — Get one Alpaca option contract by contract symbol or ID.
- `get_order` — Get one Alpaca order by order ID or client order ID. [write]
- `get_position` — Get one open Alpaca position by symbol or asset ID.
- `get_stock_bars` — Get historical OHLC stock bars from Alpaca Market Data API.
- `get_stock_snapshots` — Get latest stock snapshots from Alpaca Market Data API.
- `get_watchlist` — Get one Alpaca watchlist by watchlist ID or user-defined name.
- `list_account_activities` — List Alpaca account activities with optional type, category, date, and pagination filters.
- `list_assets` — List Alpaca assets with optional status, asset class, and attribute filters.
- `list_corporate_actions` — List Alpaca corporate actions for symbols, CUSIPs, types, or IDs.
- `list_news` — List latest Alpaca news articles across stocks and crypto.
- `list_option_contracts` — List Alpaca option contracts with optional underlying and contract filters.
- `list_orders` — List Alpaca orders for the connected account with optional filters.
- `list_positions` — List open positions for the connected Alpaca trading account.
- `list_watchlists` — List Alpaca watchlists registered under the connected trading account.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Alpaca state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Alpaca is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=alpaca
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Alpaca homepage: https://alpaca.markets/
