---
name: oo-speedtest-tracker
description: "Speedtest Tracker (speedtest-tracker.dev). Use this skill for ANY Speedtest Tracker request — reading, creating, and updating data. Whenever a task involves Speedtest Tracker, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Speedtest Tracker"
  author: "OOMOL"
  version: "1.0.3"
  services: ["speedtest_tracker"]
  icon: "https://static.oomol.com/logo/third-party/speedtest_tracker.png"
---

# Speedtest Tracker

Operate **Speedtest Tracker** through your OOMOL-connected account. This skill calls the `speedtest_tracker` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Speedtest Tracker. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "speedtest_tracker" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "speedtest_tracker" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_health` — Check that the Speedtest Tracker instance is reachable and running through its unauthenticated health check endpoint.
- `get_latest_result` — Retrieve the most recent speedtest result, optionally narrowed by the same filters as list_results, for example status `completed` for the last successful test. Requires a token with the Read Results ability.
- `get_result` — Retrieve one speedtest result by ID. Use it to poll a test queued by run_speedtest until its status leaves the in-progress states. Requires a token with the Read Results ability.
- `get_stats` — Retrieve aggregated ping, download, and upload statistics, optionally limited to a date range. Requires a token with the Read Results ability.
- `list_results` — List speedtest results with optional filters, sorting, and pagination. Requires a token with the Read Results ability.
- `list_servers` — List nearby Ookla speedtest servers as seen by the instance, for choosing a serverId for run_speedtest. Requires a token with the List Servers ability.
- `run_speedtest` — Queue a new Ookla speedtest on the instance and return the queued result immediately. Poll get_result with the returned ID until the status is completed, failed, or skipped. Requires a token with the Run Speedtest ability. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Speedtest Tracker state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Speedtest Tracker is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/speedtest_tracker
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Speedtest Tracker homepage: https://speedtest-tracker.dev/
- API documentation: https://docs.speedtest-tracker.dev/api
