---
name: oo-google-analytics
description: "Google Analytics (analytics.google.com). Use this skill for ANY Google Analytics request — reading, creating, and updating data. Whenever a task involves Google Analytics, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Analytics"
  author: "OOMOL"
  version: "1.0.1"
  services: ["google_analytics"]
  icon: "https://static.oomol.com/logo/third-party/google_analytics.svg"
---

# Google Analytics

Operate **Google Analytics** through your OOMOL-connected account. This skill calls the `google_analytics` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Analytics. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "google_analytics" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "google_analytics" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_custom_dimension` — Archive a Google Analytics custom dimension that should no longer be available for reporting configuration. [write]
- `archive_custom_metric` — Archive a Google Analytics custom metric that should no longer be available for reporting configuration. [write]
- `batch_run_pivot_reports` — Run up to five Google Analytics Data API pivot reports in one batch request for a single property.
- `batch_run_reports` — Run up to five Google Analytics Data API reports in one batch request for a single property.
- `check_compatibility` — Check whether selected Google Analytics dimensions and metrics can be queried together.
- `create_custom_dimension` — Create a Google Analytics custom dimension so reporting can use a business-specific event, user, or item attribute. [write]
- `create_custom_metric` — Create a Google Analytics custom metric so reports can measure business-specific event values. [write]
- `get_metadata` — Get available dimensions and metrics for a Google Analytics property before building reports.
- `get_property_overview` — Get the key setup details for a Google Analytics property before choosing reports.
- `get_property_quotas_snapshot` — Get the Google Analytics Data API quota snapshot for a property without running a report.
- `list_account_summaries` — List Google Analytics accounts and property summaries visible to the connected Google account.
- `list_custom_dimensions` — List custom dimensions configured on a Google Analytics property.
- `list_custom_metrics` — List custom metrics configured on a Google Analytics property.
- `list_data_streams` — List data streams configured on a Google Analytics property.
- `list_properties` — List Google Analytics properties visible to the connected account as user-selectable options. Use this first when the user does not know their GA4 propertyId.
- `list_properties_filtered` — List Google Analytics properties matching a known Admin API filter such as parent:accounts/123. Use list_properties first when the account or propertyId is unknown.
- `run_acquisition_report` — Run a Google Analytics acquisition report showing where sessions and users came from.
- `run_engagement_report` — Run a Google Analytics engagement trend report for users, sessions, and engagement quality.
- `run_events_report` — Run a Google Analytics events report for event volume, users, key events, and value.
- `run_geography_report` — Run a Google Analytics geography report for users, sessions, and key events by location.
- `run_key_events_report` — Run a Google Analytics key events report for key event volume and conversion rates.
- `run_pages_report` — Run a Google Analytics pages report for page views, users, sessions, and engagement.
- `run_pivot_report` — Run a Google Analytics Data API pivot report for cross-tabbed reporting views.
- `run_realtime_report` — Run a Google Analytics realtime report for currently active users and events.
- `run_report` — Run a Google Analytics Data API report for selected dimensions, metrics, and date ranges.
- `run_technology_report` — Run a Google Analytics technology report for device, browser, and operating system performance.
- `update_data_retention_settings` — Update Google Analytics property data retention settings for event data and user activity reset behavior. [write]
- `update_property` — Update Google Analytics property settings such as display name, industry category, time zone, or currency. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Analytics state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Analytics is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=google_analytics
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Analytics homepage: https://analytics.google.com
