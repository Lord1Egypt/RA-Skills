---
name: oo-taxjar
description: "TaxJar (taxjar.com). Use this skill for ANY TaxJar request — reading, creating, updating, and deleting data. Whenever a task involves TaxJar, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TaxJar"
  author: "OOMOL"
  version: "1.0.1"
  services: ["taxjar"]
  icon: "https://static.oomol.com/logo/third-party/Taxjar.svg"
---

# TaxJar

Operate **TaxJar** through your OOMOL-connected account. This skill calls the `taxjar` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TaxJar. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "taxjar" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "taxjar" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `calculate_sales_tax_for_order` — Calculate TaxJar sales tax for an order. [write]
- `create_customer` — Create a TaxJar customer for exemption management. [write]
- `create_order_transaction` — Create a TaxJar order transaction for reporting and filing. [write]
- `create_refund_transaction` — Create a TaxJar refund transaction. [write]
- `delete_customer` — Delete a TaxJar customer by identifier. [destructive]
- `delete_order_transaction` — Delete a TaxJar order transaction by identifier. [destructive]
- `delete_refund_transaction` — Delete a TaxJar refund transaction by identifier. [destructive]
- `list_customers` — List TaxJar customer identifiers.
- `list_nexus_regions` — List TaxJar nexus regions for the account.
- `list_order_transactions` — List TaxJar order transaction identifiers within a date range. [write]
- `list_refund_transactions` — List TaxJar refund transaction identifiers within a date range.
- `list_tax_categories` — List TaxJar product tax categories and codes.
- `show_customer` — Retrieve a TaxJar customer by identifier.
- `show_order_transaction` — Retrieve a TaxJar order transaction by identifier. [write]
- `show_refund_transaction` — Retrieve a TaxJar refund transaction by identifier.
- `show_tax_rates_for_location` — Retrieve TaxJar sales tax rates for a location.
- `summarize_tax_rates_for_all_regions` — Retrieve TaxJar minimum and average sales tax rates by region.
- `update_customer` — Update an existing TaxJar customer. [write]
- `update_order_transaction` — Update an existing TaxJar order transaction. [write]
- `update_refund_transaction` — Update an existing TaxJar refund transaction. [write]
- `validate_vat_number` — Validate a VAT identification number with TaxJar.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TaxJar state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TaxJar is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=taxjar
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- TaxJar homepage: https://www.taxjar.com/
