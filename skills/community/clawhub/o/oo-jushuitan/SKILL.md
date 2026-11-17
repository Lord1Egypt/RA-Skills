---
name: oo-jushuitan
description: "Jushuitan ERP (jushuitan.com). Use this skill for ANY Jushuitan ERP request — reading, creating, updating, and deleting data. Whenever a task involves Jushuitan ERP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Jushuitan ERP"
  author: "OOMOL"
  version: "1.0.7"
  services: ["jushuitan"]
  icon: "https://static.oomol.com/logo/third-party/jushuitan.svg"
---

# Jushuitan ERP

Operate **Jushuitan ERP** through your OOMOL-connected account. This skill calls the `jushuitan` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Jushuitan ERP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "jushuitan" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "jushuitan" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

### Shipment records and tracking limits

**`list_shipments` returns shipment records, including shipment time, tracking number, and carrier; Jushuitan OpenWeb does not provide tracking events.** These records cannot establish pickup status, the current transit milestone, or the last tracking update. Shipment time is not pickup time, and a tracking number does not prove pickup. Information visible in the Jushuitan dashboard is not necessarily available through its open API.

- For shipment counts, carrier distributions, or shipment details, use the Jushuitan actions normally.
- For pickup status, transit progress, or stale-tracking alerts, explain that a separate tracking source is required. Use Kuaidi100 (快递100) for domestic courier tracking: first verify that the current environment exposes the service and that it is connected, discover its available actions, and read the latest action schema before calling it. Do not invent action names or assume account access.
- If the tracking service, connection, or required query parameters are missing, state exactly what is missing and still complete the independently deliverable Jushuitan shipment query. Do not count missing tracking events or failed queries as awaiting pickup. Do not default to scraping carrier websites or repeatedly solving CAPTCHAs for ongoing monitoring.
- A “no new tracking event for over 12 hours” alert requires the application to persist the latest valid event timestamp and check it on a schedule; event-change webhooks alone are insufficient. Display no tracking data, query failures, awaiting pickup, and stalled transit separately. Stop stale-tracking alerts for delivered shipments.

## Available actions

- `add_package_serial_numbers` — Add unique package serial numbers in batches. [write]
- `add_product_serial_numbers` — Add unique product serial numbers in batches. [write]
- `adjust_inventory_by_count` — Adjust product inventory through an inventory count operation. [destructive]
- `append_wms_workload` — Append a WMS workload record. [write]
- `assign_order_shipping_warehouse` — Assign a shipping warehouse to an order. [destructive]
- `assign_wave_to_robot` — Assign a picking wave to a specified warehouse robot. [destructive]
- `batch_off_shelf_products` — Move products off warehouse shelves in batches. [destructive]
- `batch_shelve_products` — Place products onto warehouse shelves in batches. [destructive]
- `bind_seeding_bin_to_cart` — Bind a seeding cabinet identifier to a seeding cart. [destructive]
- `bind_seeding_cart` — Bind a seeding cart to a warehouse picking or seeding workflow. [destructive]
- `cancel_allocation` — Cancel an inventory allocation document. [destructive]
- `cancel_cost_upload_batch` — Cancel a profitability data upload batch. [destructive]
- `cancel_order_by_internal_id` — Cancel an order by its Jushuitan internal order number. [destructive]
- `cancel_purchase_receipt` — Cancel a purchase receipt document. [destructive]
- `cancel_purchase_return` — Cancel a purchase return outbound document. [destructive]
- `check_seeding_cart_availability` — Check whether a seeding cart is currently available for use.
- `complete_seeding_with_stock_out` — Submit seeding results and complete the associated stock-out operation. [destructive]
- `complete_seeding_without_stock_out` — Submit seeding results without completing a stock-out operation. [destructive]
- `confirm_after_sale` — Confirm an after-sale document. [destructive]
- `confirm_after_sale_goods_received` — Confirm receipt of after-sale goods, including partial confirmations. [destructive]
- `confirm_after_sale_receipt_by_serial_numbers` — Confirm after-sale goods receipt in batches by product serial number. [destructive]
- `confirm_allocation` — Confirm an inventory allocation document. [destructive]
- `create_allocation_difference` — Create an allocation difference document. [write]
- `create_cost_upload_batch` — Create a batch identifier for profitability data uploads. [write]
- `create_cross_border_first_leg` — Create a first-leg cross-border logistics document. [write]
- `create_cross_warehouse_allocation` — Create a cross-warehouse inventory allocation. [write]
- `create_intra_warehouse_allocation` — Create an inventory allocation within a warehouse. [write]
- `create_other_stock_movement` — Create a miscellaneous inbound or outbound stock document. [write]
- `create_production_batch` — Create a production batch management record. [write]
- `create_purchase_receipts` — Create purchase receipt documents in batches. [write]
- `create_purchase_returns` — Create purchase return documents in batches. [write]
- `create_virtual_warehouse_allocation` — Create a virtual-warehouse inventory allocation document. [write]
- `create_virtual_warehouse_operation` — Create a virtual-warehouse allocation or return document. [write]
- `force_confirm_and_stock_in_shortage_order` — Force-confirm a single-item shortage order and receive it into inventory. [destructive]
- `force_confirm_shortage_order_for_shipping` — Force-confirm single-item shortage orders for shipment. [destructive]
- `generate_fast_moving_labels` — Generate unique labels for fast-moving products. [write]
- `get_allocation_first_leg_fee` — Get first-leg logistics fees for an allocation document.
- `get_cost_upload_batch_status` — Get status information for a profitability data upload batch.
- `get_fast_delivery_order_count` — Get the number of orders eligible for expedited shipment.
- `get_fast_moving_serial_number` — Get unique serial-number information for a fast-moving product.
- `get_product_by_sku` — Get ordinary product details by SKU code.
- `get_product_historical_cost` — Get the historical cost price for a product at the requested point in time.
- `get_recommended_bin_by_package` — Get recommended warehouse bins for products in a specified package.
- `get_recommended_product_bin` — Get recommended warehouse bins for a product.
- `get_returned_warehouse_package` — Get return-to-warehouse information for a delivery package.
- `get_robot_picking_wave` — Get a picking wave available to a warehouse robot.
- `get_seeding_wave` — Get seeding wave information, including supported third-party warehouse data.
- `get_serial_number_trace` — Get tracking history for a unique product serial number.
- `list_after_sale_receipts` — List actual warehouse receipts for sales returns.
- `list_after_sales` — List after-sale return and refund records visible through OpenWeb.
- `list_allocations` — List inventory allocation documents.
- `list_bundle_products` — List bundle products and their component product definitions.
- `list_company_users` — List users belonging to the authorized Jushuitan merchant company.
- `list_cost_upload_batch_errors` — List rejected or invalid records from a profitability data upload batch.
- `list_cross_border_after_sales` — List cross-border after-sale documents.
- `list_cross_border_logistics_channels` — List cross-border logistics providers and channels enabled for the merchant.
- `list_cross_border_orders` — List cross-border orders.
- `list_drp_distributors` — List distributors linked to the merchant in the Jushuitan distribution network.
- `list_drp_suppliers` — List suppliers linked to the merchant in the Jushuitan distribution network.
- `list_express_registrations` — List registered express shipment records.
- `list_finance_projects` — List finance expense projects configured for the merchant.
- `list_inventory` — List product inventory by warehouse and product filters.
- `list_inventory_counts` — List inventory count documents and their recorded quantities.
- `list_logistics_companies` — List logistics companies and carrier codes available to the merchant.
- `list_manufacturing_orders` — List manufacturing orders and their details.
- `list_operating_expenses` — List operating expense records from the Jushuitan finance module.
- `list_orders` — List orders visible through the standard Jushuitan OpenWeb channel.
- `list_other_stock_movements` — List miscellaneous inbound and outbound stock documents.
- `list_package_bin_inventory` — List inventory contained in packages and warehouse bins.
- `list_payables` — List payable documents from the Jushuitan finance module.
- `list_payments` — List payment documents from the Jushuitan finance module.
- `list_picking_waves` — List picking waves matching the requested filters.
- `list_product_boms` — List product bills of materials and their component relationships.
- `list_product_categories` — List product categories configured for the merchant.
- `list_product_customs_declarations` — List customs declaration information for products.
- `list_product_historical_costs` — List paginated historical cost-price records for products.
- `list_product_models` — List ordinary products grouped and filtered by product model.
- `list_product_restore_history` — List product operation history used to recover product data.
- `list_product_suppliers` — List supplier relationships configured for products.
- `list_profit_statement_items` — List available profit-statement cost and revenue items.
- `list_purchase_bookings` — List scheduled purchase receiving bookings.
- `list_purchase_orders` — List purchase orders and their line items.
- `list_purchase_receipts` — List purchase receipt documents and their line items.
- `list_purchase_requests` — List purchase requests across virtual and physical warehouses.
- `list_purchase_returns` — List purchase return outbound documents.
- `list_sales_outbounds` — List sales outbound documents visible through OpenWeb.
- `list_serial_number_stock_movements` — List inbound and outbound movements for unique product serial numbers.
- `list_shipments` — List one page of shipment records visible through Jushuitan OpenWeb, including shipment times, tracking numbers, and courier companies. The /open/logistic/query endpoint does not provide parcel tracking events or pickup status. Use a separate carrier tracking service to check pickup, delivery progress, or time since the last tracking event.
- `list_shop_products` — List shop product records and their mappings to Jushuitan products.
- `list_shops` — List shops available to the authorized Jushuitan merchant account.
- `list_suppliers` — List supplier master records.
- `list_virtual_warehouse_allocations` — List virtual-warehouse allocation documents with pagination.
- `list_virtual_warehouse_inventory` — List product inventory held in virtual warehouses.
- `list_virtual_warehouse_operations` — List virtual-warehouse allocation and return documents with pagination.
- `list_virtual_warehouses` — List virtual warehouses available to the merchant.
- `list_warehouses` — List warehouses available to the authorized merchant account.
- `list_wms_stock_movements` — List WMS inbound and outbound stock movement records.
- `list_wms_work_logs` — List WMS work logs for authorized warehouses.
- `mark_orders_exception` — Move orders into the exception-order workflow. [destructive]
- `mark_orders_shipped` — Mark orders as shipped and submit their shipment details. [destructive]
- `pack_shipment` — Record packing details for a shipment. [destructive]
- `recalculate_wave_inventory_reservation` — Recalculate inventory reservations for a picking wave. [destructive]
- `record_fast_moving_arrival` — Record arrival of fast-moving products in the WMS workflow. [destructive]
- `register_express_shipments` — Register express shipment records in batches. [write]
- `save_1688_product_mapping` — Create or update mappings for products sourced from 1688. [write]
- `save_packing_video_record` — Save a packing-machine video record for a package or shipment. [write]
- `save_product_categories` — Create or update product categories in Jushuitan. [write]
- `save_product_suppliers` — Create or modify supplier relationships for products. [destructive]
- `save_products_batch` — Create or update ordinary product records in batches using the current API. [write]
- `save_virtual_warehouse_purchase_request` — Create or update a virtual-warehouse purchase request. [destructive]
- `set_after_sale_labels` — Set labels on after-sale documents. [destructive]
- `ship_sales_outbounds` — Complete shipment for sales outbound documents. [destructive]
- `split_order` — Split an order into separate fulfillment orders. [destructive]
- `unbind_outbound_from_seeding_cart` — Unbind outbound documents from a seeding cart. [destructive]
- `unbind_wave_cart` — Unbind a picking or seeding cart from a wave. [destructive]
- `uncancel_orders` — Reverse cancellation for eligible orders. [destructive]
- `unconfirm_after_sale` — Reverse confirmation of an after-sale document. [destructive]
- `update_cross_border_order_forwarding` — Update cross-border forwarding and logistics information for an order. [destructive]
- `update_last_mile_shipping_fee` — Write back the last-mile shipping fee for a cross-border shipment. [destructive]
- `update_order_invoice` — Update invoice information attached to an order. [destructive]
- `update_order_labels` — Add or remove labels on orders. [destructive]
- `update_order_logistics_company` — Change the logistics company assigned to an order. [destructive]
- `update_order_offline_note` — Update an order note or offline remark by order number. [destructive]
- `update_order_remark_flag` — Update an order remark flag and synchronize the change to its platform. [destructive]
- `update_order_seller_remark_by_internal_id` — Update an order seller remark using the Jushuitan internal order number. [destructive]
- `update_order_seller_remark_by_online_id` — Update an order seller remark using its online order number. [destructive]
- `update_other_stock_movement_status` — Change the status of a miscellaneous inbound or outbound stock document. [destructive]
- `update_product_bin_capacity` — Update warehouse bin-capacity information for products. [destructive]
- `update_product_invoice_profile` — Update basic invoicing information for products. [destructive]
- `update_product_mappings` — Bind or unbind product mapping relationships. [destructive]
- `update_product_models` — Update product model information. [destructive]
- `update_purchase_order` — Modify an existing purchase order. [destructive]
- `update_purchase_order_labels` — Add or remove labels on purchase and manufacturing orders. [destructive]
- `update_purchase_order_status` — Change the business status of a purchase order. [destructive]
- `update_self_store_order_recipient` — Update recipient information for an order from a merchant-owned shop. [destructive]
- `update_virtual_inventory` — Import or update virtual inventory quantities in batches. [destructive]
- `update_wave_picking_status` — Update the picking status of a WMS wave. [destructive]
- `upload_after_sales` — Upload after-sale return or refund records. [write]
- `upload_bundle_products` — Upload bundle product definitions in batches. [write]
- `upload_external_purchase_order_costs` — Upload cost data for externally purchased orders. [write]
- `upload_manufacturing_orders` — Upload manufacturing orders to Jushuitan. [write]
- `upload_order_expenses` — Upload order expense data for profitability accounting. [write]
- `upload_orders` — Upload orders from merchant-owned shops or offline cross-border channels. [write]
- `upload_product_boms` — Upload product bill-of-material definitions. [write]
- `upload_product_costs` — Upload multiple product cost values for profitability accounting. [write]
- `upload_product_historical_costs` — Upload historical cost-price records for products. [write]
- `upload_purchase_bookings` — Upload scheduled purchase receiving bookings. [write]
- `upload_purchase_orders` — Upload purchase orders to Jushuitan. [write]
- `upload_shop_products` — Upload product records for a merchant-owned online shop. [write]
- `upload_suppliers` — Upload supplier master records to Jushuitan. [write]
- `upload_unidentified_after_sales` — Upload after-sale records for returned parcels without matching order information. [write]
- `void_after_sale` — Void an after-sale document. [destructive]
- `void_purchase_documents` — Void purchase orders, manufacturing orders, or receiving bookings. [destructive]
- `weigh_sort_and_ship_orders` — Record order weights, sort express parcels, and mark orders as shipped. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Jushuitan ERP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Jushuitan ERP is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/jushuitan
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Jushuitan ERP homepage: https://www.jushuitan.com/
- API documentation: https://openweb.jushuitan.com/dev-doc
- [Jushuitan official FAQ: the open platform has no shipment tracking API](https://openweb.jushuitan.com/qaCenter?groupId=12&postId=39); tracking requires a separate carrier integration.
