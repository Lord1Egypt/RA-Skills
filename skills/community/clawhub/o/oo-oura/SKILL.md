---
name: oo-oura
description: "Oura (ouraring.com). Use this skill for ANY Oura request — searching and reading data. Whenever a task involves Oura, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Oura"
  author: "OOMOL"
  version: "1.0.4"
  services: ["oura"]
  icon: "https://static.oomol.com/logo/third-party/oura.svg"
---

# Oura

Operate **Oura** through your OOMOL-connected account. This skill calls the `oura` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Oura. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "oura" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "oura" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_daily_activity` — Get one daily activity summary document from Oura by document ID.
- `get_daily_cardiovascular_age` — Get one daily cardiovascular age document from Oura by document ID.
- `get_daily_readiness` — Get one daily readiness summary document from Oura by document ID.
- `get_daily_resilience` — Get one daily resilience summary document from Oura by document ID.
- `get_daily_sleep` — Get one daily sleep summary document from Oura by document ID.
- `get_daily_spo2` — Get one daily SpO2 summary document from Oura by document ID.
- `get_daily_stress` — Get one daily stress summary document from Oura by document ID.
- `get_enhanced_tag` — Get one enhanced tag document from Oura by document ID.
- `get_personal_info` — Get personal information for the authenticated Oura account.
- `get_rest_mode_period` — Get one rest mode period document from Oura by document ID.
- `get_ring_configuration` — Get one ring configuration document from Oura by document ID.
- `get_session` — Get one guided or unguided session document from Oura by document ID.
- `get_sleep` — Get one sleep period document from Oura by document ID.
- `get_sleep_time` — Get one recommended bedtime window document from Oura by document ID.
- `get_tag` — Get one tag document from Oura by document ID. Oura has superseded this collection by enhanced tags.
- `get_vo2_max` — Get one VO2 max measurement document from Oura by document ID.
- `get_workout` — Get one workout document from Oura by document ID.
- `list_daily_activity` — List daily activity summary documents from Oura.
- `list_daily_cardiovascular_age` — List daily cardiovascular age documents from Oura.
- `list_daily_readiness` — List daily readiness summary documents from Oura.
- `list_daily_resilience` — List daily resilience summary documents from Oura.
- `list_daily_sleep` — List daily sleep summary documents from Oura.
- `list_daily_spo2` — List daily SpO2 summary documents from Oura.
- `list_daily_stress` — List daily stress summary documents from Oura.
- `list_enhanced_tag` — List enhanced tag documents from Oura.
- `list_heartrate` — List heart rate sample documents from Oura.
- `list_rest_mode_period` — List rest mode period documents from Oura.
- `list_ring_battery_level` — List ring battery level sample documents from Oura.
- `list_ring_configuration` — List ring configuration documents from Oura.
- `list_session` — List guided or unguided session documents from Oura.
- `list_sleep` — List sleep period documents from Oura.
- `list_sleep_time` — List recommended bedtime window documents from Oura.
- `list_tag` — List tag documents from Oura. Oura has superseded this collection by enhanced tags.
- `list_vo2_max` — List VO2 max measurement documents from Oura.
- `list_workout` — List workout documents from Oura.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Oura state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Oura is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/oura
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Oura homepage: https://ouraring.com
- API documentation: https://developer.ouraring.com/
