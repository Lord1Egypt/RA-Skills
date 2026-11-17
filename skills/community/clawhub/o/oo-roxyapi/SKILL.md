---
name: oo-roxyapi
description: "RoxyAPI (roxyapi.com). Use this skill for ANY RoxyAPI request — searching and reading data. Whenever a task involves RoxyAPI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "RoxyAPI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["roxyapi"]
  icon: "https://static.oomol.com/logo/third-party/roxyapi.svg"
---

# RoxyAPI

Operate **RoxyAPI** through your OOMOL-connected account. This skill calls the `roxyapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected RoxyAPI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "roxyapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "roxyapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cast_career_tarot` — Career spread, 7 cards.
- `cast_celtic_cross_tarot` — Celtic Cross spread, 10 cards.
- `cast_custom_tarot` — Custom spread builder.
- `cast_iching` — Cast an I-Ching reading.
- `cast_love_tarot` — Love spread, 5 cards.
- `cast_three_card_tarot` — Three card spread, past present future.
- `cast_yes_no_tarot` — Yes or no answer.
- `convert_lunar_date` — Convert a Gregorian date OR a complete lunar date. Omit both for today in UTC. The calendar uses the UTC+8 reference meridian; isLeapMonth selects the repeated lunar month.
- `draw_tarot_cards` — Draw tarot cards.
- `find_auspicious_days` — Find days favored for an activity within a date range of at most 93 days, optionally excluding dates clashing with a zodiac animal.
- `get_almanac_day` — Get the Chinese almanac for a date in years 1900 through 2100, with lunar date, pillars, day officer, mansion, favored and avoided activities.
- `get_bazi_annual_forecast` — Read a Gregorian year against a natal BaZi chart, including Ten Gods and pillar interactions.
- `get_bazi_chart` — Generate BaZi chart. Resolve ambiguous places with search_cities first; prefer an IANA timezone for historical daylight saving.
- `get_bazi_compatibility` — Calculate BaZi compatibility. Resolve ambiguous places with search_cities first; prefer an IANA timezone for historical daylight saving.
- `get_bazi_day_master_strength` — Assess BaZi Day Master strength with factor scores and favorable and unfavorable elements.
- `get_bazi_luck_pillars` — Calculate BaZi ten-year luck pillars and the start age, with optional annual overlays.
- `get_bodygraph` — Generate full Human Design bodygraph. Resolve ambiguous places with search_cities first; prefer an IANA timezone for historical daylight saving.
- `get_daily_horoscope` — Daily horoscope by zodiac sign.
- `get_daily_tarot` — Daily tarot card.
- `get_forecast_digest` — Summarize personal forecast events into the next 24 hours, 7 days, 30 days, and 90 days. Preserve explicit domains, weights, and per-window top-event count.
- `get_forecast_timeline` — Build a personal, cross-domain forecast timeline. The provider clamps the window to at most 90 days and caps events at 200; use returned startDate and endDate as the resolved window.
- `get_human_design_connection` — Calculate Human Design connection chart. Resolve ambiguous places with search_cities first; prefer an IANA timezone for historical daylight saving.
- `get_monthly_horoscope` — Monthly horoscope by zodiac sign.
- `get_natal_chart` — Generate natal chart. Resolve ambiguous places with search_cities first; prefer an IANA timezone for historical daylight saving.
- `get_numerology_chart` — Generate numerology chart.
- `get_numerology_compatibility` — Calculate numerology compatibility.
- `get_synastry` — Calculate synastry. Resolve ambiguous places with search_cities first; prefer an IANA timezone for historical daylight saving.
- `get_tarot_card` — Get tarot card by id.
- `get_usage` — Get API usage statistics.
- `get_weekly_horoscope` — Weekly horoscope by zodiac sign.
- `get_yearly_horoscope` — Yearly horoscope by zodiac sign.
- `list_tarot_cards` — List all 78 tarot cards.
- `search_cities` — Search cities worldwide. Confirm province and country when multiple cities match; use timezone rather than today's utcOffset for birth charts.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change RoxyAPI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — RoxyAPI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/roxyapi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- RoxyAPI homepage: https://roxyapi.com/
- API documentation: https://roxyapi.com/docs/authentication
