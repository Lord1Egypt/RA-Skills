---
name: oo-home-assistant
description: "Home Assistant (home-assistant.io). Use this skill for ANY Home Assistant request — reading, creating, updating, and deleting data. Whenever a task involves Home Assistant, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Home Assistant"
  author: "OOMOL"
  version: "1.0.8"
  services: ["home_assistant"]
  icon: "https://static.oomol.com/logo/third-party/home_assistant.svg"
---

# Home Assistant

Operate **Home Assistant** through your OOMOL-connected account. This skill calls the `home_assistant` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Home Assistant. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "home_assistant" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "home_assistant" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_service` — Call a Home Assistant service to control entities, such as light.turn_on or switch.turn_off. [destructive]
- `check_config` — Ask Home Assistant to validate its own configuration files and report errors and warnings. Requires an admin access token.
- `delete_automation_config` — Delete one Home Assistant automation. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found. [destructive]
- `delete_scene_config` — Delete one Home Assistant scene. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found. [destructive]
- `delete_script_config` — Delete one Home Assistant script. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found. [destructive]
- `execute_script` — Run a Home Assistant script sequence containing service calls, delays, and conditions. [write]
- `fire_event` — Fire one Home Assistant event with optional event data. [destructive]
- `get_automation_config` — Fetch the stored configuration for one Home Assistant automation. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found.
- `get_config` — Fetch the Home Assistant instance configuration.
- `get_error_log` — Fetch the Home Assistant error log for the current session as plain text. Home Assistant serves this only when the instance runs with file logging enabled, so it can report not found on an otherwise healthy instance.
- `get_history` — Fetch recorded state history for one or more Home Assistant entities over a time period, for answering questions about how a value changed.
- `get_logbook` — Fetch the Home Assistant logbook: the human-readable timeline of what happened and what triggered it, for diagnosing why something changed.
- `get_registries` — List Home Assistant entity, device, area, floor, and label registries over the WebSocket API.
- `get_scene_config` — Fetch the stored configuration for one Home Assistant scene. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found.
- `get_script_config` — Fetch the stored configuration for one Home Assistant script. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found.
- `get_state` — Fetch the current state for one Home Assistant entity.
- `list_calendar_events` — List the events on one Home Assistant calendar between a start and end time.
- `list_calendars` — List the calendar entities exposed by Home Assistant.
- `list_device_automations` — List the triggers, conditions, and actions supported by one Home Assistant device.
- `list_events` — List Home Assistant event types currently known by the instance.
- `list_services` — List Home Assistant service domains and their available services.
- `list_states` — List all current Home Assistant entity states.
- `render_template` — Render a Home Assistant template against the connected instance.
- `save_automation_config` — Create or replace one Home Assistant automation. Posting to an unused id creates the automation. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found. [destructive]
- `save_scene_config` — Create or replace one Home Assistant scene. Posting to an unused id creates the scene. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found. [destructive]
- `save_script_config` — Create or replace one Home Assistant script. Posting to an unused key creates the script. Requires an admin access token, and only covers entries stored in the Home Assistant UI-editable config; entries defined in other YAML files return not found. [destructive]
- `search_related` — Find Home Assistant items related to an entity, device, area, automation, or configuration entry.
- `validate_config` — Validate Home Assistant trigger, condition, and action configurations before storing an automation.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Home Assistant state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Home Assistant is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/home_assistant
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Home Assistant homepage: https://www.home-assistant.io
- API documentation: https://developers.home-assistant.io/docs/api/rest
