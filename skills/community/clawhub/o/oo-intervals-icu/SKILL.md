---
name: oo-intervals-icu
description: "Intervals.icu (intervals.icu). Use this skill for ANY Intervals.icu request — searching and reading data. Whenever a task involves Intervals.icu, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Intervals.icu"
  author: "OOMOL"
  version: "1.0.0"
  services: ["intervals_icu"]
  icon: "https://static.oomol.com/logo/third-party/intervals_icu.svg"
---

# Intervals.icu

Operate **Intervals.icu** through your OOMOL-connected account. This skill calls the `intervals_icu` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Intervals.icu. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "intervals_icu" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "intervals_icu" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_activity` — Get one activity in full: every summary measurement Intervals.icu holds for it, the list of recorded streams, and optionally its intervals (laps and efforts).
- `get_activity_streams` — Get the recorded data series of one activity, such as heart rate or power, sample by sample. Ask only for the streams you need: a long activity holds thousands of samples per stream.
- `get_athlete` — Get the Intervals.icu athlete profile of the API key: id, name, time zone and location. Use the time zone to read the local dates and times that other actions return.
- `get_event` — Get one calendar entry in full. For a planned workout this includes its structured steps with their durations and targets.
- `list_activities` — List the athlete's completed activities between two local dates, newest first, with distance, time, heart rate and training load. It returns at most limit activities (30 by default); when the list is full, call again with newest set to the start_date_local of the oldest activity returned and skip the activities already seen. Intervals.icu does not share data synced from Strava through its API.
- `list_events` — List the athlete's calendar between two local dates: planned workouts, races, notes and other entries. Without dates it lists today and the next six days in the athlete's time zone.
- `list_sport_settings` — List the athlete's settings for each group of sports: the FTP, threshold and maximum heart rate, and the power and heart rate zones Intervals.icu uses for training load.
- `list_wellness` — List daily wellness records between two local dates: fitness (ctl), fatigue (atl) and ramp rate, plus weight, resting heart rate, HRV, sleep, readiness and the athlete's notes where recorded.
- `search_activities` — Find the athlete's activities by name, or by tag when the query starts with #. Returns short summaries; use get_activity for the detail of one activity.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Intervals.icu state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Intervals.icu is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/intervals_icu
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Intervals.icu homepage: https://intervals.icu
- API documentation: https://intervals.icu/api-docs.html
