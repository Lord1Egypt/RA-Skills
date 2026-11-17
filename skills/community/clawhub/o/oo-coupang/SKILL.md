---
name: oo-coupang
description: "Coupang (coupang.com). Use this skill for ANY Coupang request — reading, creating, updating, and deleting data. Whenever a task involves Coupang, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Coupang"
  author: "OOMOL"
  version: "1.0.5"
  services: ["coupang"]
  icon: "https://static.oomol.com/logo/third-party/coupang.svg"
---

# Coupang

Operate **Coupang** through your OOMOL-connected account. This skill calls the `coupang` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Coupang. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "coupang" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "coupang" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_item_inventory` — Get the stock quantity, sale price, and sale status of one Coupang item.
- `get_order` — Get current purchase-order and receiver details for one Coupang order.
- `get_product` — Get the registered details of one Coupang seller product.
- `list_orders` — List Coupang purchase orders for a date range and fulfillment status.
- `list_products` — List seller products in Coupang with optional filters and cursor pagination.
- `list_return_requests` — List Coupang return or cancellation requests submitted in a time range.
- `update_item_price` — Replace the selling price and optional auto-pricing settings of one Coupang item. [destructive]
- `update_item_quantity` — Replace the available inventory quantity of one Coupang item. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Coupang state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Coupang is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/coupang
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Coupang homepage: https://www.coupang.com
- API documentation: https://developers.coupang.com/en/api
