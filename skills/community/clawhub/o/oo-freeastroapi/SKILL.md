---
name: oo-freeastroapi
description: "FreeAstroAPI (freeastroapi.com). Use this skill for ANY FreeAstroAPI request — searching and reading data. Whenever a task involves FreeAstroAPI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "FreeAstroAPI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["freeastroapi"]
  icon: "https://static.oomol.com/logo/third-party/freeastroapi.png"
---

# FreeAstroAPI

Operate **FreeAstroAPI** through your OOMOL-connected account. This skill calls the `freeastroapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected FreeAstroAPI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "freeastroapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "freeastroapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `analyze_bazi_constitution` — Analyze traditional BaZi and TCM constitution tendencies and timing patterns; this is not medical advice, diagnosis, or treatment.
- `calculate_bazi` — Calculate a complete BaZi chart with four pillars, Day Master, Ten Gods, luck cycles, and optional professional analysis.
- `calculate_bazi_flow` — Calculate annual and monthly BaZi flow pillars, interactions, and stars for one prediction year, with optional timezone and solar-time settings.
- `calculate_bazi_life_curve` — Calculate traditional Neijing Jing, Qi, and Shen age trajectories with BaZi luck-cycle adjustments.
- `calculate_bazi_synastry` — Analyze compatibility between two BaZi charts with independent calendar and time settings.
- `calculate_ephemeris` — Calculate celestial positions at an instant or over a date range, including optional aspects, houses, angles, fixed stars, Moon void-of-course data, and table outputs.
- `calculate_numerology_profile` — Calculate a Pythagorean, Chaldean, Kabbalah/Gematria, or Ank Jyotish profile with method-specific name, date, transliteration, and optional interpretation settings.
- `calculate_transit_timeline` — Calculate transit-to-natal intervals for a calendar month or a long-cycle range up to 366 days, with configurable planets, points, aspects, and orbs. Requires a High plan.
- `calculate_vedic_chart` — Run the V2 integrated Vedic calculation with optional divisional charts, Dasha, Yogas, Panchang, Shadbala, Ashtakavarga, and Avastha.
- `correct_bazi_time` — Convert local civil time to local mean and relative or absolute true solar time.
- `get_bazi_dictionary` — Get the stable ID mappings for BaZi interactions and symbolic stars.
- `get_chinese_calendar` — Convert a Gregorian date to the Chinese lunar calendar, zodiac, solar terms, and festivals.
- `get_current_pillars` — Get the four pillars and element balance at the current UTC instant.
- `get_moon_calendar` — Get a complete monthly moon calendar with optional SVG visuals, eclipses, forecasts, sign intervals, and ingress events. Requires an Entry or High plan.
- `get_moon_phase` — Get moon phase, illumination, and optional zodiac, rise/set, eclipse, forecasts, interpretation, and SVG visuals for a date or the current instant.
- `list_sky_events` — Get planetary ingresses, exact aspects, stations, and lunations for a local calendar date. This returns event data for downstream notifications.
- `search_cities` — Search cities and localities, including province-qualified queries, and return coordinates and IANA timezones for subsequent chart calculations.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change FreeAstroAPI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — FreeAstroAPI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/freeastroapi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- FreeAstroAPI homepage: https://www.freeastroapi.com/
- API documentation: https://www.freeastroapi.com/zh/docs
