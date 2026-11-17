---
name: oo-tianapi
description: "TianAPI (tianapi.com). Use this skill for ANY TianAPI request — searching and reading data. Whenever a task involves TianAPI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TianAPI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["tianapi"]
  icon: "https://static.oomol.com/logo/third-party/tianapi.png"
---

# TianAPI

Operate **TianAPI** through your OOMOL-connected account. This skill calls the `tianapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TianAPI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tianapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tianapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_usage` — Query TianAPI account membership, remaining TianDou credits, and usage for an API ID. Enable the Account Information API (96) first; this request consumes its quota or TianDou credits.
- `get_almanac` — Query the traditional Chinese almanac, including auspicious activities, taboos, lunar dates, zodiac animals, and heavenly stems. Supports Gregorian dates or Unix timestamps, and lunar dates when calendar is lunar. Omitted dates use today. Years 1970-2038. Enable TianAPI Chinese Almanac (45).
- `get_birthday_personality` — Query the personality interpretation for a birthday's month and day; no birth year is required. Enable TianAPI Birthday Personality (27). For entertainment only.
- `get_blood_type_compatibility` — Query a traditional ABO blood-type pairing interpretation. Enable TianAPI Blood Type Pairing (84). For entertainment only, not a medical compatibility assessment.
- `get_constellation_compatibility` — Query a single constellation's interpretation, a pair of constellations, or its compatibility with all constellations. Omit otherSign for the single mode or set compareWithAll for all pairings. Enable TianAPI Constellation Pairing (42). For entertainment only.
- `get_daily_horoscope` — Query a constellation's horoscope for a date, defaulting to today when omitted. Includes overall, love, work, wealth, health, and lucky attributes. Enable TianAPI Star Horoscope (78). For entertainment only.
- `get_full_almanac` — Query the full Chinese almanac for a Gregorian date, defaulting to today. Includes lunar dates, zodiac animals, auspicious and inauspicious gods, directions, and seasonal information. Years 1900-2100. This endpoint does not accept lunar-date input. Enable TianAPI Chinese Almanac (45).
- `get_number_fortune` — Query a traditional numerology interpretation for a number such as a phone, room, or vehicle number. Preserve leading zeros by passing a string. Enable TianAPI Number Fortune (105). For entertainment only.
- `get_solar_term` — Query one of the 24 Chinese solar terms, including its meaning, customs, poetry, and foods. An optional year requests exact Gregorian and lunar date information. Enable TianAPI Solar Terms (86).
- `get_zodiac_compatibility` — Query compatibility interpretations for two Chinese zodiac animals, preserving the different gender combinations. Enable TianAPI Chinese Zodiac Pairing (83). For entertainment only.
- `list_baidu_trending` — List Baidu trending search keywords, summaries, popularity indexes, and trends through TianAPI. Enable the Baidu Trending API (68) first.
- `list_douyin_trending` — List Douyin trending search topics, labels, and popularity indexes through TianAPI. Enable the Douyin Trending API (155) first. TianAPI documents a 3-minute update interval.
- `list_netease_trending` — List NetEase news trending topics through TianAPI. This endpoint belongs to the Network Trending API (223), which must be enabled first.
- `list_network_trending` — List aggregated trending topics across Chinese platforms with titles, summaries, and popularity indexes. Enable the Network Trending API (223) in TianAPI first.
- `list_phoenix_trending` — List Phoenix news trending topics through TianAPI. This endpoint belongs to the Network Trending API (223), which must be enabled first.
- `list_tencent_trending` — List Tencent ecosystem trending topics and ordering indexes through TianAPI. Enable the Tencent Trending API (196) first. TianAPI documents a 10-to-30-minute update interval.
- `list_toutiao_trending` — List Toutiao trending news topics and popularity indexes through TianAPI. Enable the Toutiao Trending API (244) first. TianAPI documents a 20-minute update interval.
- `list_weibo_trending` — List Weibo trending search topics, tags, and popularity indexes through TianAPI. Enable the Weibo Trending API (100) first. TianAPI documents a 30-minute update interval.
- `list_zodiac_compatibilities` — Compare one Chinese zodiac animal with the other 11 animals, optionally including itself. The connector makes 11 or 12 official pairing requests, consuming that many calls, with requests spaced below the ordinary-account 3 QPS limit. Enable TianAPI Chinese Zodiac Pairing (83). For entertainment only.
- `query_holidays` — Query Chinese holidays, working days, make-up working days, lunar information, and optional international festivals. Supports dates, a month, a date range, or annual official holidays. Non-annual queries contain at most 31 dates. Enable TianAPI Holidays (139).
- `search_dream_interpretations` — Search traditional Zhou Gong dream interpretations by keyword with pagination. Enable TianAPI Dream Interpretation (24). For entertainment only.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TianAPI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TianAPI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tianapi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TianAPI homepage: https://www.tianapi.com/
- API documentation: https://www.tianapi.com/apiview/96
