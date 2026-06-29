---
name: oo-fireberry
description: "Fireberry (fireberry.com). Use this skill for ANY Fireberry request — reading, creating, updating, and deleting data. Whenever a task involves Fireberry, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Fireberry"
  author: "OOMOL"
  version: "1.0.0"
  services: ["fireberry"]
  icon: "https://static.oomol.com/logo/third-party/fireberry.svg"
---

# Fireberry

Operate **Fireberry** through your OOMOL-connected account. This skill calls the `fireberry` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Fireberry. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fireberry" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fireberry" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_account` — Create one Fireberry account record. [write]
- `create_contact` — Create one Fireberry contact record. [write]
- `delete_account` — Delete one Fireberry account record by GUID. [destructive]
- `delete_contact` — Delete one Fireberry contact record by GUID. [destructive]
- `get_account` — Get one Fireberry account record by GUID.
- `get_contact` — Get one Fireberry contact record by GUID.
- `list_accounts` — List Fireberry account records with simple page and page size controls.
- `list_contacts` — List Fireberry contact records with simple page and page size controls.
- `query_records` — Search, filter, sort, aggregate, and paginate Fireberry records using v3 query.
- `update_account` — Update one Fireberry account record by GUID. [write]
- `update_contact` — Update one Fireberry contact record by GUID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Fireberry state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Fireberry is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=fireberry
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Fireberry homepage: https://www.fireberry.com
