---
name: oo-ringover
description: "Ringover (ringover.com). Use this skill for ANY Ringover request — searching and reading data. Whenever a task involves Ringover, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ringover"
  author: "OOMOL"
  version: "1.0.4"
  services: ["ringover"]
  icon: "https://static.oomol.com/logo/third-party/ringover.svg"
---

# Ringover

Operate **Ringover** through your OOMOL-connected account. This skill calls the `ringover` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ringover. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ringover" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ringover" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_call` — Get Ringover call log entries for one call ID.
- `get_group` — Get a Ringover call group by ID, optionally paginating its users array.
- `get_ivr` — Get a Ringover IVR by ID.
- `get_number` — Get Ringover phone number details by E.164 number without the plus prefix.
- `get_tag` — Get a Ringover call tag by ID.
- `get_team` — Retrieve the Ringover team object with nested numbers, users, IVRs, conferences, tags, and groups allowed by the API key.
- `get_user` — Get a Ringover user by ID.
- `list_calls` — List terminated Ringover calls with optional date, pagination, and call type filters.
- `list_groups` — List Ringover call groups with offset pagination.
- `list_ivrs` — List Ringover IVR configurations visible to the API key.
- `list_numbers` — List Ringover phone numbers with assignment-type filters.
- `list_tags` — List Ringover call tags.
- `list_users` — List Ringover users visible to the API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ringover state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ringover is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ringover
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Ringover homepage: https://www.ringover.com/
- API documentation: https://developer.ringover.com/
