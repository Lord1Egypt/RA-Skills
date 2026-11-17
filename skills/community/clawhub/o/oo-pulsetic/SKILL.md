---
name: oo-pulsetic
description: "Pulsetic (pulsetic.com). Use this skill for ANY Pulsetic request — searching and reading data. Whenever a task involves Pulsetic, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pulsetic"
  author: "OOMOL"
  version: "1.0.2"
  services: ["pulsetic"]
  icon: "https://static.oomol.com/logo/third-party/pulsetic.svg"
---

# Pulsetic

Operate **Pulsetic** through your OOMOL-connected account. This skill calls the `pulsetic` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pulsetic. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pulsetic" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pulsetic" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_monitor` — Get one Pulsetic monitor by ID.
- `get_monitor_downtime` — Get total Pulsetic downtime for a monitor over an optional lookback window.
- `get_monitor_stats` — Get Pulsetic uptime, downtime, and response-time statistics for a monitor.
- `list_monitor_checks` — List Pulsetic checks for a monitor and time range.
- `list_monitor_events` — List Pulsetic online and offline events for a monitor and time range.
- `list_monitor_snapshots` — List hourly Pulsetic snapshots for a monitor and time range.
- `list_monitors` — List Pulsetic monitors with optional pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pulsetic state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pulsetic is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pulsetic
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Pulsetic homepage: https://pulsetic.com
- API documentation: https://help.pulsetic.com/category/275-api
