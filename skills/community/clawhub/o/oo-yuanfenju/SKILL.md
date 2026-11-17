---
name: oo-yuanfenju
description: "Yuanfenju (yuanfenju.com). Use this skill for ANY Yuanfenju request — searching and reading data. Whenever a task involves Yuanfenju, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Yuanfenju"
  author: "OOMOL"
  version: "1.0.2"
  services: ["yuanfenju"]
  icon: "https://static.oomol.com/logo/third-party/yuanfenju.png"
---

# Yuanfenju

Operate **Yuanfenju** through your OOMOL-connected account. This skill calls the `yuanfenju` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Yuanfenju. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "yuanfenju" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "yuanfenju" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `analyze_bazi_compatibility` — Analyze two people's Bazi charts for relationship or marriage entertainment using the official matching interface selected by the caller. Marriage uses firstPerson as the male partner and secondPerson as the female partner. Each lunar date in 1900-2100 adds a conversion call; other non-leap lunar dates use native input.
- `convert_calendar` — Convert Gregorian and Chinese lunar dates in either direction, including negative lunar month numbers for leap months.
- `find_auspicious_dates` — Find dates marked suitable for a selected traditional activity within the next 7 days, half month, month or three months, for cultural research and entertainment. Use get_almanac for a selected date's hourly details.
- `get_account` — Get the connected Yuanfenju account's membership, expiry and applicable remaining quota. This query does not consume call credits.
- `get_almanac` — Get the Chinese almanac for a Gregorian date within 90 days before or after today, for cultural research and entertainment.
- `get_annual_usage` — Get the current 24-hour cycle's used call count and reset timing for a Yuanfenju annual-plan account. This free query is only available to annual members.
- `get_bazi_chart` — Calculate a standard Bazi chart with four pillars, five elements and luck cycles for cultural research and entertainment. Lunar dates in 1900-2100 are converted first, including leap months, using an additional API call. Other non-leap lunar dates use native lunar input.
- `get_natal_chart` — Calculate a Western astrology natal chart from the original Gregorian local birth time for cultural research and entertainment. Returns celestial data, official interpretations and the SVG chart when provided. The provider handles timezone/DST and transport compression; no true solar time correction is applied.
- `get_solar_terms` — Get the year's 12 seasonal nodes or all 24 solar terms with Gregorian and lunar timestamps for the supplied date.
- `get_ziwei_chart` — Calculate a Ziwei Doushu chart with twelve palaces and star placements for cultural research and entertainment. Lunar dates in 1900-2100 are converted first using an additional call; other non-leap lunar dates use native input.
- `interpret_bazi` — Get Yuanfenju's official Bazi interpretation for cultural research and entertainment, including five-element, relationship, wealth and life interpretation text. Lunar dates in 1900-2100 are converted first using an additional call; other non-leap lunar dates use native input.
- `interpret_tarot` — Draw and interpret a full-deck tarot spread for entertainment using the current Yuanfenju interface. Drawing is automatic; paid membership is required.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Yuanfenju state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Yuanfenju is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/yuanfenju
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Yuanfenju homepage: https://yuanfenju.com/
- API documentation: https://doc.yuanfenju.com/
