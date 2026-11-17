---
name: oo-sage-sales-management
description: "Sage Sales Management (forcemanager.com). Use this skill for ANY Sage Sales Management request — reading, creating, updating, and deleting data. Whenever a task involves Sage Sales Management, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sage Sales Management"
  author: "OOMOL"
  version: "1.0.4"
  services: ["sage_sales_management"]
  icon: "https://static.oomol.com/logo/third-party/sage_sales_management.svg"
---

# Sage Sales Management

Operate **Sage Sales Management** through your OOMOL-connected account. This skill calls the `sage_sales_management` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sage Sales Management. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sage_sales_management" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sage_sales_management" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_account` — Create one Sage Sales Management account. [write]
- `create_contact` — Create one Sage Sales Management contact. [write]
- `create_opportunity` — Create one Sage Sales Management opportunity. [write]
- `delete_account` — Delete one Sage Sales Management account by ID. [destructive]
- `delete_contact` — Delete one Sage Sales Management contact by ID. [destructive]
- `delete_opportunity` — Delete one Sage Sales Management opportunity by ID. [destructive]
- `get_account` — Get one Sage Sales Management account by ID.
- `get_accounts_schema` — Get the Sage Sales Management Accounts schema metadata.
- `get_contact` — Get one Sage Sales Management contact by ID.
- `get_contacts_schema` — Get the Sage Sales Management Contacts schema metadata.
- `get_opportunities_schema` — Get the Sage Sales Management Opportunities schema metadata.
- `get_opportunity` — Get one Sage Sales Management opportunity by ID.
- `list_accounts` — List Sage Sales Management accounts with optional filters and pagination.
- `list_contacts` — List Sage Sales Management contacts with optional filters and pagination.
- `list_opportunities` — List Sage Sales Management opportunities with optional filters and pagination.
- `update_account` — Update one Sage Sales Management account by ID. [write]
- `update_contact` — Update one Sage Sales Management contact by ID. [write]
- `update_opportunity` — Update one Sage Sales Management opportunity by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sage Sales Management state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sage Sales Management is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/sage_sales_management
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sage Sales Management homepage: https://www.forcemanager.com/
- API documentation: https://developer.forcemanager.com/
