---
name: oo-xingpan
description: "Xingpan API (xingpan.vip). Use this skill for ANY Xingpan API request — searching and reading data. Whenever a task involves Xingpan API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Xingpan API"
  author: "OOMOL"
  version: "1.0.2"
  services: ["xingpan"]
  icon: "https://static.oomol.com/logo/third-party/xingpan.png"
---

# Xingpan API

Operate **Xingpan API** through your OOMOL-connected account. This skill calls the `xingpan` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Xingpan API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "xingpan" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "xingpan" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `calculate_comparison_chart` — Calculate a comparison chart for two people, including both planetary sets and their relationship to the houses.
- `calculate_composite_chart` — Calculate a composite midpoint relationship chart for two people.
- `calculate_lunar_return_chart` — Calculate a lunar return chart from birth details and a reference date, time, and return location.
- `calculate_natal_chart` — Calculate a personal natal chart from birth time and location, with optional SVG, interpretation corpus, and aspect patterns.
- `calculate_solar_return_chart` — Calculate a solar return chart from birth details and a reference date, time, and location. In verified upstream probes, changing the reference location did not change the birth-location houses; relocated solar returns remain unverified.
- `calculate_synastry_chart` — Calculate Xingpan's pairing (synastry) chart for two people.
- `calculate_transit_chart` — Calculate a transit chart against a natal chart for a specified local date and time at the birthplace, accounting for date-specific UTC offsets.
- `get_chart_config` — Get Xingpan planet, asteroid, fixed star, virtual point, zodiac, and house configuration.
- `get_daily_horoscope` — Get daily zodiac horoscopes for one sign or all twelve signs, including overall, love, career, health, scores, and lucky items.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Xingpan API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Xingpan API is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/xingpan
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Xingpan API homepage: https://xingpan.vip/
- API documentation: https://www.xingpan.vip/astrology/Apiinterface
