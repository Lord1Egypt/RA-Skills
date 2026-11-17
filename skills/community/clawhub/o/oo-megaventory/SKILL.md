---
name: oo-megaventory
description: "Megaventory (megaventory.com). Use this skill for ANY Megaventory request — reading, creating, and updating data. Whenever a task involves Megaventory, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Megaventory"
  author: "OOMOL"
  version: "1.0.4"
  services: ["megaventory"]
  icon: "https://static.oomol.com/logo/third-party/megaventory.svg"
---

# Megaventory

Operate **Megaventory** through your OOMOL-connected account. This skill calls the `megaventory` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Megaventory. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "megaventory" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "megaventory" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `list_document_types` — List Megaventory document types for sales and purchase orders.
- `list_inventory_locations` — List Megaventory inventory locations for order lookups.
- `list_products` — List Megaventory products using documented structured filters.
- `list_purchase_orders` — List Megaventory purchase orders using documented structured filters.
- `list_sales_orders` — List Megaventory sales orders using documented structured filters.
- `list_supplier_clients` — List Megaventory suppliers and clients for order lookups.
- `upsert_product` — Insert a new Megaventory product or update its non-empty fields by SKU. [write]
- `upsert_purchase_order` — Insert or update a Megaventory purchase order with one or more order lines. [write]
- `upsert_sales_order` — Insert or update a Megaventory sales order with one or more order lines. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Megaventory state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Megaventory is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/megaventory
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Megaventory homepage: https://www.megaventory.com/
- API documentation: https://help.megaventory.com/en/articles/74873-how-do-i-get-started-with-the-api
