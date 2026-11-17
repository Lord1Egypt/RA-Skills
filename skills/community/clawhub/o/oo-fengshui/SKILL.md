---
name: oo-fengshui
description: "Feng Shui API (fengshui-api.com). Use this skill for ANY Feng Shui API request — searching and reading data. Whenever a task involves Feng Shui API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Feng Shui API"
  author: "OOMOL"
  version: "1.0.2"
  services: ["fengshui"]
  icon: "https://static.oomol.com/logo/third-party/fengshui.svg"
---

# Feng Shui API

Operate **Feng Shui API** through your OOMOL-connected account. This skill calls the `fengshui` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Feng Shui API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fengshui" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fengshui" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_lucky_dimension` — Check a positive length on the Lu Ban ruler and get nearest auspicious ranges when the length is inauspicious.
- `get_compatibility` — Score traditional love or business compatibility from 1 (challenging) to 4 (excellent), using birth dates or zodiac animals.
- `get_eight_mansions` — Calculate the house trigram and traditional Eight Mansions stars for the eight compass sectors.
- `get_flying_star` — Calculate the natal Flying Star chart for the nine palaces using the building facing and construction year or period. Replacement (Ti Gua) charts are not computed.
- `get_key_status` — Get the current API key status and hourly request quota without accessing personal data.
- `get_kua` — Calculate the personal Kua number, East or West group, and traditional favorable and unfavorable directions.
- `get_zodiac_allies` — Get the two zodiac animals forming the traditional three-harmony group with a sign.
- `get_zodiac_day` — Get the day zodiac animal and stem-branch pillar for a date.
- `get_zodiac_enemy` — Get the opposite, traditionally clashing zodiac animal for a sign.
- `get_zodiac_hour` — Get the zodiac animal and earthly branch for a local two-hour period; this does not calculate a full hour pillar.
- `get_zodiac_month` — Get the lunar month or solar-term month zodiac and pillar for a date.
- `get_zodiac_peach_blossom` — Get the traditional Peach Blossom zodiac animal and compass direction for a sign.
- `get_zodiac_secret_friend` — Get the zodiac animal forming a traditional six-harmony pair with a sign.
- `get_zodiac_year` — Get the Chinese year zodiac animal, element and stem-branch pillar for a date.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Feng Shui API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Feng Shui API is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/fengshui
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Feng Shui API homepage: https://fengshui-api.com/
- API documentation: https://fengshui-api.com/docs
