---
name: oo-mixpanel
description: "Mixpanel (mixpanel.com). Use this skill for ANY Mixpanel request — searching and reading data. Whenever a task involves Mixpanel, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mixpanel"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mixpanel"]
  icon: "https://static.oomol.com/logo/third-party/Mixpanel.svg"
---

# Mixpanel

Operate **Mixpanel** through your OOMOL-connected account. This skill calls the `mixpanel` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mixpanel. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mixpanel" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mixpanel" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `export_events` — Export raw Mixpanel events for a project and date range.
- `list_funnels` — List saved funnels available in a Mixpanel project.
- `list_saved_cohorts` — List saved cohorts available in a Mixpanel project.
- `profile_event_activity` — Get event activity for one or more Mixpanel profiles over a date range.
- `query_frequency_report` — Query how frequently users perform an event in Mixpanel.
- `query_funnel` — Query a saved Mixpanel funnel report over a date range.
- `query_numeric_average` — Average a numeric expression for a Mixpanel event over time.
- `query_numeric_sum` — Sum a numeric expression for a Mixpanel event over time.
- `query_profiles` — Query Mixpanel profiles with optional filters, paging, and selected properties.
- `query_retention_report` — Query a Mixpanel retention report over a date range.
- `query_saved_report` — Query a saved Mixpanel report by bookmark ID.
- `query_segmentation_report` — Query a Mixpanel segmentation report for one event over a date range.
- `query_top_events` — Get today's top Mixpanel events with counts and percent change from yesterday.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mixpanel state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mixpanel is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mixpanel
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Mixpanel homepage: https://mixpanel.com
