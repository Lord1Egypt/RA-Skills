---
name: oo-woocommerce
description: "WooCommerce (woocommerce.com). Use this skill for ANY WooCommerce request — reading, creating, and updating data. Whenever a task involves WooCommerce, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WooCommerce"
  author: "OOMOL"
  version: "1.0.1"
  services: ["woocommerce"]
  icon: "https://static.oomol.com/logo/third-party/woocommerce.svg"
---

# WooCommerce

Operate **WooCommerce** through your OOMOL-connected account. This skill calls the `woocommerce` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WooCommerce. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "woocommerce" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "woocommerce" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_order_note` — Add an administrator or customer-visible note to one WooCommerce order. [write]
- `create_coupon` — Create a WooCommerce coupon. [write]
- `create_order` — Create a WooCommerce order with customer, address, line item, and coupon fields. [write]
- `create_product` — Create a WooCommerce product with catalog, price, stock, image, and attribute fields. [write]
- `create_product_variation` — Create a variation for one WooCommerce variable product. [write]
- `get_coupon` — Fetch one WooCommerce coupon by coupon ID.
- `get_customer` — Fetch one WooCommerce customer by customer ID.
- `get_order` — Fetch one WooCommerce order by order ID. [write]
- `get_product` — Fetch one WooCommerce product by product ID.
- `get_product_variation` — Fetch one WooCommerce product variation by product and variation ID.
- `list_coupons` — List WooCommerce coupons with common code search and pagination metadata.
- `list_customers` — List WooCommerce customers with common filters and pagination metadata.
- `list_order_notes` — List notes for one WooCommerce order. [write]
- `list_orders` — List WooCommerce orders with common status, customer, and date filters.
- `list_product_attribute_terms` — List terms for one WooCommerce product attribute.
- `list_product_attributes` — List WooCommerce product attributes.
- `list_product_categories` — List WooCommerce product categories with filters and pagination metadata.
- `list_product_tags` — List WooCommerce product tags with filters and pagination metadata.
- `list_product_variations` — List variations for one WooCommerce variable product.
- `list_products` — List WooCommerce products with common catalog filters and pagination metadata.
- `update_coupon` — Update a WooCommerce coupon by coupon ID. [write]
- `update_order` — Update a WooCommerce order by order ID. [write]
- `update_order_status` — Update the status of one WooCommerce order. [write]
- `update_product` — Update a WooCommerce product by product ID. [write]
- `update_product_variation` — Update one WooCommerce product variation. [write]
- `upload_media` — Upload one media file to the WordPress media library used by WooCommerce. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WooCommerce state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WooCommerce is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=woocommerce
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- WooCommerce homepage: https://woocommerce.com
