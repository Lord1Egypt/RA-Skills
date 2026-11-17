---
name: oo-shopee
description: "Shopee (shopee.com). Use this skill for ANY Shopee request — reading, creating, updating, and deleting data. Whenever a task involves Shopee, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Shopee"
  author: "OOMOL"
  version: "1.0.2"
  services: ["shopee"]
  icon: "https://static.oomol.com/logo/third-party/shopee.svg"
---

# Shopee

Operate **Shopee** through your OOMOL-connected account. This skill calls the `shopee` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Shopee. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "shopee" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "shopee" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_global_item` — Create a Shopee global product draft for a mainland China CNSC merchant. [write]
- `get_global_attribute_tree` — Get Shopee global product attributes for up to 20 category IDs.
- `get_global_items` — Get details for up to 20 Shopee global products.
- `get_item_models` — Get variation tiers, model prices, and model stock for a Shopee shop item.
- `get_merchant_info` — Get the identity, region, currency, and authorization status of a Shopee merchant.
- `get_order_escrow` — Get Shopee accounting and fee details for one order.
- `get_orders` — Get detailed information for up to 50 Shopee orders from one shop.
- `get_return` — Get the details and current workflow state of a Shopee return.
- `get_shipping_parameters` — Get the pickup, drop-off, or non-integrated shipping options for an order package.
- `get_shop_info` — Get the profile, region, authorization, and cross-border status of a Shopee shop.
- `get_shop_items` — Get base information for up to 50 Shopee shop items.
- `get_tracking_info` — Get logistics tracking events for a Shopee order package.
- `get_tracking_number` — Get carrier tracking numbers for a shipped Shopee order package.
- `list_global_brands` — List Shopee brands available for a global product category.
- `list_global_categories` — List the Shopee global product category tree for a cross-border merchant.
- `list_global_items` — List global products owned by a Shopee cross-border merchant.
- `list_merchant_shops` — List shops authorized and bound to a Shopee merchant.
- `list_orders` — List Shopee shop orders created or updated in a time range of at most 15 days.
- `list_returns` — List Shopee returns by creation time, update time, and workflow status.
- `list_shop_items` — List Shopee shop items by listing status and update time.
- `ship_order` — Arrange pickup, drop-off, or non-integrated shipment for a Shopee order package. [write]
- `update_item_prices` — Replace prices for up to 50 models of one Shopee shop item. [destructive]
- `update_item_stocks` — Replace seller stock for up to 50 models of one Shopee shop item. [destructive]
- `upload_product_image` — Download a public image URL and upload it to Shopee Media Space for products. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Shopee state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Shopee is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/shopee
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Shopee homepage: https://www.shopee.com/
- API documentation: https://open.shopee.cn/developer-guide/14
