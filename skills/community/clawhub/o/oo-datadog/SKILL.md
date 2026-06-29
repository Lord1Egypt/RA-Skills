---
name: oo-datadog
description: "Datadog (datadoghq.com). Use this skill for ANY Datadog request — searching and reading data. Whenever a task involves Datadog, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Datadog"
  author: "OOMOL"
  version: "1.0.1"
  services: ["datadog"]
  icon: "https://static.oomol.com/logo/third-party/datadog.png"
---

# Datadog

Operate **Datadog** through your OOMOL-connected account. This skill calls the `datadog` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Datadog. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "datadog" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "datadog" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_metric_metadata` — Retrieve Datadog metadata for one metric.
- `get_monitor` — Retrieve one Datadog monitor by ID.
- `list_metrics` — List Datadog metric names active since a given Unix timestamp.
- `list_monitors` — List Datadog monitors with optional group state and tag filters.
- `query_timeseries_points` — Query Datadog timeseries points for a metric expression and time window.
- `search_monitors` — Search Datadog monitors by query, page, and sort options.
- `validate_api_key` — Validate the configured Datadog API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Datadog state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Datadog is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=datadog
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Datadog homepage: https://www.datadoghq.com/
