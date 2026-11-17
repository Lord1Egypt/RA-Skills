---
name: oo-coingecko
description: "CoinGecko (coingecko.com). Use this skill for ANY CoinGecko request — searching and reading data. Whenever a task involves CoinGecko, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CoinGecko"
  author: "OOMOL"
  version: "1.0.4"
  services: ["coingecko"]
  icon: "https://static.oomol.com/logo/third-party/coingecko.svg"
---

# CoinGecko

Operate **CoinGecko** through your OOMOL-connected account. This skill calls the `coingecko` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CoinGecko. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "coingecko" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "coingecko" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_coin` — Get coin metadata and optional market data, tickers and seven-day sparkline.
- `get_coin_by_contract` — Resolve CoinGecko coin details and coin ID from an asset platform ID and token contract address.
- `get_coin_history` — Get a coin market snapshot at 00:00 UTC on a specified date, not that day's closing price. Demo history is limited to 365 days; paid historical access depends on plan.
- `get_coin_ohlc` — Get coin OHLC candles without volume. Timestamps are candle close times in UNIX milliseconds. Demo supports up to 365 days with automatic granularity; max and explicit hourly/daily intervals require paid access.
- `get_global_market_data` — Get global cryptocurrency market capitalization, trading volume and market share.
- `get_market_chart` — Get historical price, market capitalization and volume series by number of days. Historical access and interval availability depend on your CoinGecko plan.
- `get_market_chart_range` — Get historical price, market capitalization and volume series within a date or UNIX timestamp range. Historical access and interval availability depend on your CoinGecko plan.
- `get_onchain_pool` — Get prices, reserves and activity for one explicitly selected DEX pool, with optional token and DEX resources, composition and volume breakdown.
- `get_onchain_token` — Get token price, supply, volume and token reserve value across pools, with optional top pools. Prices follow the upstream selected pool; unavailable market capitalization remains null.
- `get_onchain_token_info` — Get token project metadata and available GeckoTerminal verification, holder and authority signals. Field availability varies by network and does not constitute a safety assessment.
- `get_pool_ohlcv` — Get OHLCV candles for an explicit pool and token direction. Timestamps are UNIX seconds. Empty intervals are omitted unless requested. Each request covers at most six months; accessible history depends on plan and pool tracking. Second timeframes require eligible paid access.
- `get_prices` — Get current coin prices by ID, name or symbol, with optional market metrics. At least one selector is required; CoinGecko prioritizes IDs, then names, then symbols.
- `get_token_prices` — Get global average prices and optional metrics for CoinGecko-listed tokens by asset platform and contract addresses. Supports up to 515 addresses per request.
- `get_trending` — Get trending coins, NFTs and categories by CoinGecko search volume over the last 24 hours. The show_max option requires an eligible plan.
- `list_asset_platforms` — List CoinGecko asset platform IDs for contract-address lookups. These differ from onchain network IDs.
- `list_category_markets` — List CoinGecko category market capitalization, 24-hour changes and volume. Use returned category IDs with list_coin_markets.
- `list_coin_markets` — List paginated coin prices, market capitalization, volume and price changes. Plan-specific filters are enforced by CoinGecko.
- `list_coin_tickers` — List a page of up to 100 CEX and DEX tickers for a coin, with exchange filters and optional 2-percent orderbook depth. Quotes are market observations, not execution guarantees.
- `list_coins` — List CoinGecko coin IDs, symbols and names, optionally including platform contract addresses.
- `list_onchain_networks` — List a page of GeckoTerminal network IDs and their CoinGecko asset platform mappings. Use network IDs such as eth for onchain actions.
- `list_pool_trades` — List the latest 300 trades within the past 24 hours for a pool, optionally filtered by USD volume and token direction. This is not complete transaction history or a complete capital-flow dataset.
- `list_supported_currencies` — List supported quote currencies for CoinGecko price and market queries.
- `list_token_pools` — List up to 20 pools for a token per page, with sorting and related resources. The default sort combines 24-hour volume and liquidity; pages beyond 10 require Analyst or above.
- `search` — Search coins, categories, exchanges and NFTs listed on CoinGecko.
- `search_onchain_pools` — Search DEX pools by pool address, token address, name or symbol, optionally filtered by network. Returns up to 20 pools per page; pages beyond 10 require Analyst or above.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CoinGecko state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CoinGecko is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/coingecko
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- CoinGecko homepage: https://www.coingecko.com
- API documentation: https://docs.coingecko.com/reference/authentication
