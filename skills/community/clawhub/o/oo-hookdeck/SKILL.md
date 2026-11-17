---
name: oo-hookdeck
description: "Hookdeck (hookdeck.com). Use this skill for ANY Hookdeck request — reading, creating, updating, and deleting data. Whenever a task involves Hookdeck, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Hookdeck"
  author: "OOMOL"
  version: "1.0.4"
  services: ["hookdeck"]
  icon: "https://static.oomol.com/logo/third-party/hookdeck.svg"
---

# Hookdeck

Operate **Hookdeck** through your OOMOL-connected account. This skill calls the `hookdeck` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Hookdeck. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hookdeck" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hookdeck" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_connection` — Create a Hookdeck connection and optionally create or bind its source and destination. [write]
- `create_destination` — Create a Hookdeck destination. [write]
- `create_source` — Create a Hookdeck source. [write]
- `delete_connection` — Delete a Hookdeck connection by ID. [destructive]
- `delete_destination` — Delete a Hookdeck destination by ID. [destructive]
- `delete_source` — Delete a Hookdeck source by ID. [destructive]
- `get_connection` — Get one Hookdeck connection by ID.
- `get_destination` — Get one Hookdeck destination by ID.
- `get_source` — Get one Hookdeck source by ID.
- `list_connections` — List Hookdeck connections with optional filters and cursor pagination.
- `list_destinations` — List Hookdeck destinations with optional filters and cursor pagination.
- `list_sources` — List Hookdeck sources with optional filters and cursor pagination.
- `update_connection` — Update a Hookdeck connection by ID. [write]
- `update_destination` — Update a Hookdeck destination by ID. [write]
- `update_source` — Update a Hookdeck source by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Hookdeck state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Hookdeck is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/hookdeck
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Hookdeck homepage: https://hookdeck.com
- API documentation: https://hookdeck.com/docs/api
