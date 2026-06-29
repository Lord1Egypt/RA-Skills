---
name: oo-fathom
description: "Fathom Analytics (usefathom.com). Use this skill for ANY Fathom Analytics request — reading, creating, and updating data. Whenever a task involves Fathom Analytics, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Fathom Analytics"
  author: "OOMOL"
  version: "1.0.0"
  services: ["fathom"]
  icon: "https://static.oomol.com/logo/third-party/fathom.svg"
---

# Fathom Analytics

Operate **Fathom Analytics** through your OOMOL-connected account. This skill calls the `fathom` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Fathom Analytics. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fathom" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fathom" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_event` — Create a Fathom event for a site. [write]
- `create_milestone` — Create a Fathom milestone for a site. [write]
- `create_site` — Create a Fathom site. [write]
- `get_account` — Retrieve the Fathom account that owns the API key.
- `get_current_visitors` — Fetch the current visitor count and optional detailed breakdown for a Fathom site.
- `get_event` — Retrieve a single Fathom event by site ID and event ID.
- `get_milestone` — Retrieve a single Fathom milestone by site ID and milestone ID.
- `get_site` — Retrieve a single Fathom site by site ID.
- `list_events` — List events for a Fathom site.
- `list_milestones` — List milestones for a Fathom site.
- `list_sites` — List Fathom sites available to the API key.
- `run_aggregation` — Generate a Fathom analytics aggregation report.
- `update_event` — Update a Fathom event. [write]
- `update_milestone` — Update a Fathom milestone. [write]
- `update_site` — Update a Fathom site. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Fathom Analytics state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Fathom Analytics is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=fathom
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Fathom Analytics homepage: https://usefathom.com
