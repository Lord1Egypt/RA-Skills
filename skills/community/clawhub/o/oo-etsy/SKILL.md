---
name: oo-etsy
description: "Etsy (etsy.com). Use this skill for ANY Etsy request — reading, creating, and updating data. Whenever a task involves Etsy, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Etsy"
  author: "OOMOL"
  version: "1.0.0"
  services: ["etsy"]
  icon: "https://static.oomol.com/logo/third-party/etsy.svg"
---

# Etsy

Operate **Etsy** through your OOMOL-connected account. This skill calls the `etsy` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Etsy. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "etsy" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "etsy" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_receipt_shipment` — Record an Etsy shipment and notify the buyer by email on every successful call. Omit tracking and carrier to mark shipped only; both are required for US domestic orders over $10 and shipments to India. Use carrier 'other' for unsupported carriers. Regional partner restrictions may apply even with valid credentials and scopes. [write]
- `get_listing` — Get an Etsy listing with optional associations and translation.
- `get_listing_inventory` — Read inventory for a listing you own. Listings without Etsy inventory records may have no inventory.
- `get_me` — Get the connected Etsy user ID and shop ID.
- `get_receipt` — Get an Etsy order receipt, including available shipping and payment details. Address availability depends on Etsy regional partner access.
- `get_shop` — Get an Etsy shop's public details.
- `get_shop_by_owner` — Get an Etsy shop by its owner's user ID.
- `list_receipt_transactions` — List the purchased items for an Etsy order receipt.
- `list_receipts` — List Etsy order receipts by dates, payment, shipping, delivery, and cancellation status. Address availability depends on Etsy regional partner access.
- `list_shop_listings` — List an Etsy shop's listings by state with limit/offset pagination.
- `list_shop_sections` — List the sections of an Etsy shop.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Etsy state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Etsy is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/etsy
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Etsy homepage: https://www.etsy.com
- API documentation: https://developers.etsy.com/documentation/
