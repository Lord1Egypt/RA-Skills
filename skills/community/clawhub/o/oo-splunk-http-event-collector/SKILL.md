---
name: oo-splunk-http-event-collector
description: "Splunk HTTP Event Collector (splunk.com). Use this skill for ANY Splunk HTTP Event Collector request — reading, creating, and updating data. Whenever a task involves Splunk HTTP Event Collector, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Splunk HTTP Event Collector"
  author: "OOMOL"
  version: "1.0.4"
  services: ["splunk_http_event_collector"]
  icon: "https://static.oomol.com/logo/third-party/splunk_http_event_collector.png"
---

# Splunk HTTP Event Collector

Operate **Splunk HTTP Event Collector** through your OOMOL-connected account. This skill calls the `splunk_http_event_collector` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Splunk HTTP Event Collector. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "splunk_http_event_collector" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "splunk_http_event_collector" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `send_event` — Send one structured event to the connected Splunk HTTP Event Collector. [write]
- `send_raw_event` — Send one raw text event to the connected Splunk HTTP Event Collector. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Splunk HTTP Event Collector state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Splunk HTTP Event Collector is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/splunk_http_event_collector
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Splunk HTTP Event Collector homepage: https://www.splunk.com
- API documentation: https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.4/input-endpoints/input-endpoint-descriptions
