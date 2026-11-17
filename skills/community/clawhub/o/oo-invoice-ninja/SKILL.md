---
name: oo-invoice-ninja
description: "Invoice Ninja (invoiceninja.com). Use this skill for ANY Invoice Ninja request — reading, creating, updating, and deleting data. Whenever a task involves Invoice Ninja, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Invoice Ninja"
  author: "OOMOL"
  version: "1.0.5"
  services: ["invoice_ninja"]
  icon: "https://static.oomol.com/logo/third-party/invoice_ninja.png"
---

# Invoice Ninja

Operate **Invoice Ninja** through your OOMOL-connected account. This skill calls the `invoice_ninja` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Invoice Ninja. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "invoice_ninja" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "invoice_ninja" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_client` — Create an Invoice Ninja client. [write]
- `create_invoice` — Create an Invoice Ninja invoice for a client. [write]
- `create_payment` — Record a payment in Invoice Ninja and optionally apply it to invoices. [write]
- `get_client` — Retrieve one Invoice Ninja client by hashed ID.
- `get_invoice` — Retrieve one Invoice Ninja invoice by hashed ID.
- `get_payment` — Retrieve one Invoice Ninja payment by hashed ID.
- `list_clients` — List Invoice Ninja clients with optional search and pagination filters.
- `list_invoices` — List Invoice Ninja invoices with optional client, status, date, and search filters.
- `list_payments` — List Invoice Ninja payments with optional client and search filters.
- `update_client` — Update an Invoice Ninja client while replacing its complete contact list. [destructive]
- `update_invoice` — Update documented fields or status actions on an Invoice Ninja invoice. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Invoice Ninja state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Invoice Ninja is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/invoice_ninja
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Invoice Ninja homepage: https://invoiceninja.com
- API documentation: https://invoiceninja.github.io/docs/api-reference/invoice-ninja-api-reference
