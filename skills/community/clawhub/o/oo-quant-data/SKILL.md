---
name: oo-quant-data
description: "Quant Data (quantdata.us). Use this skill for ANY Quant Data request — searching and reading data. Whenever a task involves Quant Data, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Quant Data"
  author: "OOMOL"
  version: "1.0.2"
  services: ["quant_data"]
  icon: "https://static.oomol.com/logo/third-party/quant_data.svg"
---

# Quant Data

Operate **Quant Data** through your OOMOL-connected account. This skill calls the `quant_data` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Quant Data. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "quant_data" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "quant_data" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_dark_flow` — Get time-bucketed off-exchange notional value, share count, trade count, and stock price.
- `get_dark_pool_levels` — Get off-exchange print activity aggregated by price level for one ticker.
- `get_equity_prints` — List individual lit and dark US equity prints with cursor pagination.
- `get_exposure_by_expiration` — Get dealer Greek exposure aggregated by strike and expiration for one ticker.
- `get_exposure_by_strike` — Get dealer Greek exposure aggregated by expiration and strike for one ticker.
- `get_gainers_losers` — Rank optionable tickers by bullish and bearish premium, volume, and trade activity.
- `get_iv_rank` — Get historical implied-volatility rank for one ticker and maturity window.
- `get_net_drift` — Get time-bucketed net call and put premium and volume with the underlying stock price.
- `get_net_flow` — Get total call and put premium or volume over time.
- `get_news_articles` — List ticker-tagged market news with topics and per-ticker sentiment using cursor pagination.
- `get_order_flow_consolidated` — List consolidated option blocks, splits, sweeps, and multi-leg trades with cursor pagination.
- `get_volatility_skew` — Get the implied-volatility surface across expirations and strikes for one ticker.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Quant Data state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Quant Data is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/quant_data
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Quant Data homepage: https://quantdata.us/
- API documentation: https://quantdata.us/api/docs
