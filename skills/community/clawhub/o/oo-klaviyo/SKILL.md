---
name: oo-klaviyo
description: "Klaviyo (klaviyo.com). Use this skill for ANY Klaviyo request — reading, creating, and updating data. Whenever a task involves Klaviyo, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Klaviyo"
  author: "OOMOL"
  version: "1.0.1"
  services: ["klaviyo"]
  icon: "https://static.oomol.com/logo/third-party/klaviyo.svg"
---

# Klaviyo

Operate **Klaviyo** through your OOMOL-connected account. This skill calls the `klaviyo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Klaviyo. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "klaviyo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "klaviyo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_event` — Create a Klaviyo event for a profile using a metric name and JSON event properties. [write]
- `get_campaign` — Get one Klaviyo campaign by campaign ID.
- `get_profile` — Get one Klaviyo profile by profile ID.
- `list_campaigns` — List Klaviyo campaigns with the required channel filter plus optional sorting and cursor pagination.
- `list_events` — List Klaviyo events with optional filtering, sorting, and cursor pagination.
- `list_profiles` — List Klaviyo profiles with optional filtering, sorting, and cursor pagination.
- `validate_account` — Validate a Klaviyo private API key by reading account metadata.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Klaviyo state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Klaviyo is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=klaviyo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Klaviyo homepage: https://www.klaviyo.com
