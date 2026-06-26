---
name: oo-twelve-data
description: "Twelve Data (twelvedata.com). Use this skill for ANY Twelve Data request — searching and reading data. Whenever a task involves Twelve Data, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Twelve Data"
  author: "OOMOL"
  version: "1.0.1"
  services: ["twelve_data"]
  icon: "https://static.oomol.com/logo/third-party/Twelve%20Data.svg"
---

# Twelve Data

Operate **Twelve Data** through your OOMOL-connected account. This skill calls the `twelve_data` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Twelve Data. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "twelve_data" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "twelve_data" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `earliest_timestamp` — Fetch the earliest available historical timestamp for an instrument at a given interval.
- `eod` — Fetch the end-of-day close price for a specific instrument.
- `exchanges` — List equity exchanges and their timezone and access metadata.
- `forex_pairs` — List available forex pairs with base and quote currency metadata.
- `market_movers` — Fetch the top gaining or losing instruments for a market family such as stocks, forex, or crypto.
- `market_state` — List the current open or closed state of exchanges together with timing data.
- `price` — Fetch the latest available market price for a specific instrument.
- `profile` — Fetch the company profile for an instrument, including sector and contact fields.
- `quote` — Fetch a real-time quote snapshot with price, change, volume, and 52-week range fields.
- `stocks` — List stock symbols and metadata from the Twelve Data stock catalog with optional filters.
- `symbol_search` — Search financial instruments by symbol or name and return the most relevant matches.
- `time_series` — Fetch historical OHLCV time-series data with metadata for a specific instrument and interval.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Twelve Data state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Twelve Data is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=twelve_data
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Twelve Data homepage: https://twelvedata.com
