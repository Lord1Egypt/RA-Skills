---
name: oo-garmin-connect
description: "Garmin Connect (connect.garmin.com). Use this skill for ANY Garmin Connect request — searching and reading data. Whenever a task involves Garmin Connect, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Garmin Connect"
  author: "OOMOL"
  version: "1.0.0"
  services: ["garmin_connect"]
  icon: "https://static.oomol.com/logo/third-party/garmin_connect.svg"
---

# Garmin Connect

Operate **Garmin Connect** through your OOMOL-connected account. This skill calls the `garmin_connect` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Garmin Connect. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "garmin_connect" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "garmin_connect" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_activity` — Get one activity in full: summary measurements such as heart rate, pace, power, swim strokes and training effect, plus device metadata and split summaries.
- `get_fitness_age` — Get the latest Garmin fitness age calculated on or before a date: the fitness age, the best fitness age within reach, the user's age when it was calculated, and the inputs it is based on (vigorous activity, resting heart rate, and BMI or body fat), each with its current value and, where Garmin sets one, a target.
- `get_heart_rate` — Get one day of heart rate: resting, minimum and maximum heart rate and the readings through the day.
- `get_heart_rate_zones` — Get the user's heart rate zones: the default zones and any sport-specific zones, with the method and the resting, maximum and threshold heart rates they are built on.
- `get_sleep` — Get one night of sleep in detail: duration, sleep stages, sleep scores, overnight SpO2, respiration and stress, and Garmin's sleep need estimate.
- `get_user_settings` — Get the Garmin Connect display name, time zone, locale and measurement units of the user. Use the time zone to read the local times that other actions return.
- `list_activities` — List the user's recorded activities, newest first by default, with optional date, type and text filters. Each item is a summary; use get_activity for the full detail of one activity.
- `list_activity_types` — List the activity type keys Garmin Connect uses. Keys without a parent can filter list_activities by activityType; keys with a parent filter it by activitySubType.
- `list_body_battery` — List Body Battery for a range of days: the energy charged and drained and the readings through each day. The range may span at most 31 days.
- `list_daily_summaries` — List all-day wellness summaries for a range of days: steps, calories, heart rate, intensity minutes, stress, Body Battery, respiration and pulse oximetry. The range may span at most 366 days.
- `list_hrv_summaries` — List overnight heart rate variability for a range of nights: the nightly average, the seven-day average, the personal baseline and the HRV status. Garmin lists only nights it holds an HRV record for, and the averages can still be null on such a night.
- `list_sleep_summaries` — List sleep summaries for a range of nights: duration, sleep stages and sleep need. The range may span at most 31 days; use get_sleep for the sleep scores of one night.
- `list_vo2_max` — List the user's VO2 max estimates for a range of days: the general estimate and the cycling and rowing estimates, each with the sport of the activity it came from. Garmin lists only days that have an estimate. The range may span at most 366 days.
- `list_weight` — List weigh-ins for a range of days with body composition from a smart scale, the range average, and the nearest weigh-ins before and after the range. Weights are in grams.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Garmin Connect state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Garmin Connect is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/garmin_connect
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Garmin Connect homepage: https://connect.garmin.com
- API documentation: https://developer.garmin.com/gc-developer-program/personal/
