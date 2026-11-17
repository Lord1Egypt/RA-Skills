---
name: oo-xiaohongshu-store
description: "Xiaohongshu Store (ark.xiaohongshu.com). Use this skill for ANY Xiaohongshu Store request — reading, creating, and updating data. Whenever a task involves Xiaohongshu Store, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Xiaohongshu Store"
  author: "OOMOL"
  version: "1.0.2"
  services: ["xiaohongshu_store"]
  icon: "https://static.oomol.com/logo/third-party/xiaohongshu_store.jpg"
---

# Xiaohongshu Store

Operate **Xiaohongshu Store** through your OOMOL-connected account. This skill calls the `xiaohongshu_store` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Xiaohongshu Store. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "xiaohongshu_store" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "xiaohongshu_store" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `adjust_sku_stock` — Increase or decrease the sellable stock of a Xiaohongshu SKU. [write]
- `audit_after_sale` — Audit a Xiaohongshu after-sale request. Only callable while the after-sale is pending seller audit. [write]
- `confirm_after_sale_receive` — Confirm receipt of a buyer-returned package for a Xiaohongshu after-sale. Only callable while the after-sale waits for seller receipt. [write]
- `create_item` — Create a Xiaohongshu item with its SKUs after resolving its category, attributes, brand, freight template, logistics plan, and material URLs. [write]
- `deliver_order` — Ship a Xiaohongshu order with an express tracking number. Supports split shipments by passing the SKU IDs of one package. [write]
- `get_after_sale` — Get a Xiaohongshu after-sale record by its after-sale ID, including SKUs, amounts, and logistics.
- `get_category_attributes` — Get the attributes and validation rules of a leaf Xiaohongshu category.
- `get_item` — Get a Xiaohongshu item by its item ID, including its SKU list.
- `get_order` — Get a Xiaohongshu order by its order ID, including SKU, amount, and delivery package details.
- `get_order_declare_info` — Get the customs declaration identity information of a cross-border Xiaohongshu order.
- `get_order_receiver_info` — Get receiver addresses for Xiaohongshu orders. Only available while an order is pending shipment; call it right before printing shipping labels.
- `get_order_tracking` — Get the logistics tracking records of every package in a Xiaohongshu order.
- `get_sku_stock` — Get the sellable, total, and occupied stock of a Xiaohongshu SKU, including per-warehouse breakdowns.
- `list_address_records` — List shop address records, including return addresses used when accepting after-sale returns.
- `list_after_sale_reject_reasons` — List the reject reason options available when auditing or confirming receipt of a Xiaohongshu after-sale.
- `list_after_sales` — List Xiaohongshu after-sale records by order or by creation/update time. Pass an order ID, or a time window (24 hours by creation time, 30 minutes by update time).
- `list_carriage_templates` — List the freight templates configured for the Xiaohongshu shop.
- `list_categories` — List the Xiaohongshu item categories under a parent category, or the top-level categories.
- `list_express_companies` — List the express companies supported by Xiaohongshu for order shipment.
- `list_item_skus` — List Xiaohongshu items together with their full SKU details such as price, stock, and logistics plan.
- `list_items` — List Xiaohongshu items with basic fields using ID, time, stock, barcode, or availability filters.
- `list_logistics_plans` — List shop logistics plans whose IDs can be assigned to item SKUs.
- `list_materials` — List and filter files in the Xiaohongshu material center.
- `list_orders` — List Xiaohongshu orders by creation or update time. startTime and endTime are Unix timestamps in seconds, while the returned order times are in milliseconds. Creation-time windows are limited to 24 hours and update-time windows to 30 minutes.
- `list_supported_ports` — List the customs ports supported by Xiaohongshu for cross-border clearance.
- `modify_order_express` — Change the express tracking number of a shipped Xiaohongshu order. Only available after shipment and before receipt. [write]
- `modify_order_remark` — Modify the seller remark and flag of a Xiaohongshu order. [write]
- `refresh_token` — Refresh the access token using the refresh token stored in the connection credential. Xiaohongshu only issues new tokens when the access token has under 30 minutes left or has expired; otherwise it returns the current ones unchanged. A changed token set must be saved back to the connection, and the old access token stays valid for only 5 more minutes. Access tokens expire after 7 days. [write]
- `resend_payment_record` — Ask Xiaohongshu to notify the payment company to push the payment record to customs again for a bonded cross-border order. [write]
- `search_brands` — Search the brands available for a leaf Xiaohongshu category.
- `search_items` — Search Xiaohongshu items with full publish fields using keywords, item codes, or availability filters.
- `set_sku_availability` — List or delist a Xiaohongshu SKU. [write]
- `ship_after_sale_exchange` — Confirm receipt of the returned package and report the exchange shipment tracking number for a Xiaohongshu exchange after-sale. [write]
- `sync_sku_stock` — Set the total stock of a Xiaohongshu SKU. Xiaohongshu derives the sellable stock from the difference with occupied and channel stock. [write]
- `update_item` — Update a Xiaohongshu item and its SKU collection, including adding and removing SKUs. [write]
- `upload_material` — Upload an image or video to the Xiaohongshu material center and return its URL for item media fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Xiaohongshu Store state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Xiaohongshu Store is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/xiaohongshu_store
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Xiaohongshu Store homepage: https://ark.xiaohongshu.com/
- API documentation: https://s.apifox.cn/apidoc/docs-site/1103512/doc-2810935
