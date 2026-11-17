---
name: oo-fxmacrodata
description: "FXMacroData (fxmacrodata.com). Use this skill for ANY FXMacroData request — searching and reading data. Whenever a task involves FXMacroData, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "FXMacroData"
  author: "OOMOL"
  version: "1.0.2"
  services: ["fxmacrodata"]
  icon: "https://static.oomol.com/logo/third-party/fxmacrodata.png"
---

# FXMacroData

Operate **FXMacroData** through your OOMOL-connected account. This skill calls the `fxmacrodata` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected FXMacroData. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fxmacrodata" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fxmacrodata" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_announcements` — Get the official release history of one macroeconomic indicator for a currency, such as US CPI or the ECB deposit rate. Each row carries the reference period, the value and the time the publisher released it. USD works without an API key with limited recent history.
- `get_cot` — Get weekly CFTC Commitments of Traders positioning for a currency's futures. USD supports limited keyless history; other currencies require an API key.
- `get_data_catalogue` — List the indicators served for a currency, keyed by indicator slug, with name, unit, frequency, publisher and coverage. Works without an API key.
- `get_forex` — Get daily FX spot rates for a currency pair, such as EUR/USD. Requires an API key.
- `get_latest_announcements` — Get the most recent official release of every indicator for a currency in one call. USD works without an API key.
- `get_release_calendar` — Get scheduled official release times for a currency, such as the next CPI, payrolls or central bank decision. Calendars work without an API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change FXMacroData state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — FXMacroData is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/fxmacrodata
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- FXMacroData homepage: https://fxmacrodata.com
- API documentation: https://fxmacrodata.com/docs
