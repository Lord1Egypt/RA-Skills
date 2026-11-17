---
name: oo-trendshift
description: "Trendshift (trendshift.io). Use this skill for ANY Trendshift request — searching and reading data. Whenever a task involves Trendshift, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Trendshift"
  author: "OOMOL"
  version: "1.0.4"
  services: ["trendshift"]
  icon: "https://static.oomol.com/logo/third-party/trendshift.svg"
---

# Trendshift

Operate **Trendshift** through your OOMOL-connected account. This skill calls the `trendshift` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Trendshift. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "trendshift" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "trendshift" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_github_trending_by_date` — Get Trendshift's captured GitHub Trending list for a specific scrape date.
- `get_trending_daily_by_date` — Get Trendshift's daily trending ranking for a specific UTC date.
- `get_trending_monthly_by_period` — Get Trendshift's trending ranking for a specific calendar year and month.
- `get_trending_weekly_by_period` — Get Trendshift's trending ranking for a specific ISO year and week.
- `get_trending_yearly_by_period` — Get Trendshift's trending ranking for a specific calendar year.
- `list_engagement_spikes` — List repositories whose engagement increased within a requested date window.
- `list_github_trending` — Get Trendshift's latest captured GitHub Trending list.
- `list_trending_daily` — List repositories in Trendshift's current daily trending ranking.
- `list_trending_monthly` — List repositories in Trendshift's current monthly trending ranking.
- `list_trending_weekly` — List repositories in Trendshift's current weekly trending ranking.
- `list_trending_yearly` — List repositories in Trendshift's current yearly trending ranking.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Trendshift state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Trendshift is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/trendshift
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Trendshift homepage: https://trendshift.io/
- API documentation: https://api.trendshift.io/docs
