---
name: oo-eodhd-apis
description: "EODHD APIs (eodhd.com). Use this skill for ANY EODHD APIs request — searching and reading data. Whenever a task involves EODHD APIs, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "EODHD APIs"
  author: "OOMOL"
  version: "1.0.1"
  services: ["eodhd_apis"]
  icon: "https://static.oomol.com/logo/third-party/eodhd_apis.svg"
---

# EODHD APIs

Operate **EODHD APIs** through your OOMOL-connected account. This skill calls the `eodhd_apis` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected EODHD APIs. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "eodhd_apis" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "eodhd_apis" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_eod` — Get historical end-of-day price data for an EODHD ticker.
- `get_id_mapping` — Map between EODHD ticker symbols and security identifiers.
- `get_macro_indicators` — Get macroeconomic indicator time series for a country from EODHD.
- `get_real_time_quote` — Get delayed real-time quote data for one or more EODHD symbols.
- `get_user_info` — Get EODHD account details and API usage for the authenticated user.
- `get_ust_yield_rates` — Get US Treasury yield curve rates from EODHD.
- `list_exchanges` — List exchanges supported by EODHD.
- `search_instruments` — Search EODHD instruments by ticker, company name, or ISIN.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change EODHD APIs state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — EODHD APIs is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=eodhd_apis
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- EODHD APIs homepage: https://eodhd.com
