---
name: oo-freshservice
description: "Freshservice (freshworks.com). Use this skill for ANY Freshservice request — reading, creating, and updating data. Whenever a task involves Freshservice, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Freshservice"
  author: "OOMOL"
  version: "1.0.1"
  services: ["freshservice"]
  icon: "https://static.oomol.com/logo/third-party/freshservice.svg"
---

# Freshservice

Operate **Freshservice** through your OOMOL-connected account. This skill calls the `freshservice` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Freshservice. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "freshservice" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "freshservice" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_service_request` — Create a Freshservice service request for one service catalog item. [write]
- `create_ticket` — Create a Freshservice ticket for an incident or service request workflow. [write]
- `get_ticket` — Get one Freshservice ticket by identifier with optional include expansions.
- `list_locations` — List Freshservice locations to help callers resolve account-level location metadata.
- `list_service_catalog_items` — List Freshservice service catalog items so callers can discover item display IDs before placing requests.
- `list_tickets` — List Freshservice tickets with optional filters, pagination, and include expansions.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Freshservice state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Freshservice is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=freshservice
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Freshservice homepage: https://www.freshworks.com/freshservice/
