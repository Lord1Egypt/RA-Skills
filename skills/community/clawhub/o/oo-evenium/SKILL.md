---
name: oo-evenium
description: "Evenium (corp.evenium.com). Use this skill for ANY Evenium request — reading, creating, and updating data. Whenever a task involves Evenium, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Evenium"
  author: "OOMOL"
  version: "1.0.1"
  services: ["evenium"]
  icon: "https://static.oomol.com/logo/third-party/evenium.svg"
---

# Evenium

Operate **Evenium** through your OOMOL-connected account. This skill calls the `evenium` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Evenium. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "evenium" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "evenium" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_event` — Get one Evenium event by event ID or external event ID.
- `get_guest` — Get one Evenium guest by contact ID or guest code for a given event.
- `get_guest_post_status` — Get the current post-event attendance status for one Evenium guest. [write]
- `get_guest_status` — Get the current RSVP status for one Evenium guest.
- `list_events` — List Evenium events with optional title, status, date filters, and pagination.
- `list_guests` — List guests for one Evenium event with optional attendee filters, expansions, and pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Evenium state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Evenium is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=evenium
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Evenium homepage: https://corp.evenium.com
