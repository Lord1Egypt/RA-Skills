---
name: oo-1688
description: "1688 (1688.com). Use this skill for ANY 1688 request — reading, creating, updating, and deleting data. Whenever a task involves 1688, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "1688"
  author: "OOMOL"
  version: "1.0.2"
  services: ["1688"]
  icon: "https://static.oomol.com/logo/third-party/1688.png"
---

# 1688

Operate **1688** through your OOMOL-connected account. This skill calls the `1688` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected 1688. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "1688" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "1688" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_products_to_category` — Add up to 50 products to a seller-defined category. [write]
- `agree_refund_exchange` — Agree to an exchange refund and provide the return address; only exchange disputes are supported. [write]
- `agree_refund_reshipping` — Agree to reship goods for a reshipping dispute. [write]
- `agree_return_goods` — Agree to a return-of-goods refund and provide the seller's return address. [write]
- `auto_refund_returned_order` — Trigger an automatic refund after returned goods enter the warehouse. [write]
- `cancel_ae_pickup_order` — Cancel an AliExpress JIT pickup order. [destructive]
- `cancel_order` — Cancel an eligible unpaid order as buyer or seller; orders less than ten seconds old may reject cancellation. [destructive]
- `cancel_waybill` — Cancel a Cainiao electronic waybill. [destructive]
- `check_ae_shipping_addresses` — Check whether AliExpress JIT orders share the same shipping address.
- `check_multi_package_shipping` — Check support for multi-package shipping.
- `check_products_modifiable` — Check whether the specified products can be edited.
- `check_video_capacity` — Check video-center capacity for supported Work shop videos.
- `count_logistics_exceptions` — Count logistics monitoring exceptions.
- `create_ae_pickup_order` — Create an AliExpress JIT pickup order for the specified trade orders. [write]
- `create_album` — Create a photo album with private, public or password-protected access. [write]
- `create_order` — Create a wholesale or distribution purchase order. Omit tradeType to let 1688 select an available payment method; use outOrderId for idempotency. [write]
- `create_product` — Publish a product using the current category schema returned by get_product_schema. [write]
- `create_seller_contract` — Create a seller contract with payment, freight and order agreements. [write]
- `create_user_category` — Create a seller-defined product category; parentID 0 creates a root category. [write]
- `create_waybill` — Allocate a Cainiao electronic waybill number and print data. [write]
- `decrypt_invoice` — Get invoice information for an order authorized to the current user.
- `decrypt_order_recipient` — Resolve buyer recipient information using the authorized order ID and caid.
- `delete_album` — Delete a photo album. [destructive]
- `delete_invoice` — Delete a seller invoice. [destructive]
- `delete_photo` — Delete a photo. [destructive]
- `delete_photos` — Delete at most 20 photos in one request. [destructive]
- `delete_product` — Move a product to the recycle bin; permanent deletion or restoration is performed on the website. [destructive]
- `delete_video` — Delete a video from the 1688 video center. [destructive]
- `edit_product` — Edit a product using its current category publishing schema. [write]
- `encrypt_login_id` — Convert a login ID to OpenUID for a manually initiated operation; 1688 prohibits automated batch use of this endpoint.
- `encrypt_login_ids` — Batch-convert login IDs to OpenUIDs for ERP order management; null entries are ignored by 1688.
- `expire_offers` — Mark the seller's specified offers expired using the legacy offer endpoint. [destructive]
- `expire_products` — Take the specified products off sale by marking them expired. [destructive]
- `extend_order_confirmation` — Extend the buyer's confirmation period as the seller. [write]
- `find_orders_by_recipient` — Find seller-side order IDs by recipient information.
- `find_supplier_products` — Find a supplier's products by cargo number or product ID; the supplier ID is required.
- `get_account` — Get basic information for the authorized 1688 account.
- `get_address_code` — Get an address code and its immediate children.
- `get_ae_order_addresses` — Get shipping and receiving addresses for an AliExpress JIT order.
- `get_ae_pickup_orders` — Get pickup information for AliExpress JIT orders.
- `get_buyer_logistics_trace` — Get buyer-side logistics tracking; dedicated API permission is required and updates may be delayed.
- `get_buyer_order` — Get buyer-side order details with selectable information fields using version 1.
- `get_buyer_order_v2` — Get buyer-side order details using version 2.
- `get_buyer_protection` — Get buyer-protection services available or enabled for a product.
- `get_buyer_refund` — Get buyer-side refund details and optional operation history.
- `get_category` — Get a category and its children; use categoryID 0 to list root categories.
- `get_company` — Get company information for a 1688 member.
- `get_customization_services` — Get customization services by category and optional product.
- `get_enterprise_sku_mapping` — Map an authorized supplier's product IDs to enterprise procurement SKU IDs.
- `get_freight_templates` — Get the seller's freight template details; template 0 denotes a freight description and 1 seller-paid freight.
- `get_fulfillment_data` — Get the user's fulfillment data.
- `get_invoice_related_orders` — Find merged-order relationships by trade order or invoice application.
- `get_member_categories` — Get a supplier's seller-defined product categories.
- `get_mixed_batch_settings` — Get a seller's mixed-batch purchasing settings.
- `get_mybank_service` — Get MyBank receiving-service enrollment status and information.
- `get_order_waybills` — Query waybill details by order identifiers.
- `get_other_account` — Get another account's basic information by login ID or shop domain; restricted to approved ISVs.
- `get_other_seller_product` — Get another seller's product using specifically approved API permissions; Lingshoutong products are unsupported.
- `get_payment_urls` — Get checkout links for orders; payment is completed by the user at checkout.
- `get_photo_storage` — Get photo-album storage details.
- `get_photos` — Get photos by image IDs or URLs.
- `get_processing_category` — Get processing/customization categories and their children.
- `get_product` — Get detailed information for a product owned by the authorized seller.
- `get_product_quality_advice` — Get product quality-star improvement advice when editing a product.
- `get_product_schema` — Get category-specific product publishing rules and current product data.
- `get_product_sub_schema` — Get cascading component rules for a publishing component with supportLevelProp enabled.
- `get_product_user_categories` — Get seller-defined category IDs for the specified products.
- `get_products` — Get the authorized seller's products by product ID list.
- `get_products_quality_advice` — Get quality-star improvement advice for at most 100 products.
- `get_relabeling_address` — Get the seller's private-label and relabeling service address.
- `get_repurchase_contract` — Get a repurchase contract.
- `get_seller_invoice` — Get an order's invoice information in the encrypted-data scenario; partner permission is required.
- `get_seller_logistics` — Get seller-side shipment details in the encrypted-data scenario.
- `get_seller_logistics_trace` — Get seller-side logistics tracking; tracking updates may be delayed.
- `get_seller_order` — Get seller-side order details in the encrypted-data scenario.
- `get_seller_refund` — Get seller-side refund details and optional operation history.
- `get_supplier_freight_templates` — Get a supplier's freight templates for an established distribution relationship.
- `get_system_time` — Get 1688 system time for clock synchronization.
- `get_tdd_logistics_trace` — Get Tao Da Dian logistics tracking by order ID.
- `get_tdd_order` — Get a Tao Da Dian order.
- `get_user_category_enabled` — Check whether a member has enabled seller-defined product categories.
- `get_video` — Get a video from the authorized user's video center.
- `get_waybill_subscriptions` — Query electronic waybill service subscriptions.
- `get_waybills` — Query waybill details by waybill numbers.
- `group_orders_by_recipient` — Group orders with matching recipient addresses by caid without modifying the orders.
- `list_address_codes` — List child address codes; omit areaCode for the root level.
- `list_ae_shipping_addresses` — List seller shipping addresses for AliExpress JIT.
- `list_albums` — List photo albums.
- `list_app_orders` — List service-market orders for the calling platform application.
- `list_authorized_brands` — List the seller's authorized brands for the specified leaf categories.
- `list_buyer_order_refunds` — Get in-sale refunds for an order from the buyer's perspective.
- `list_buyer_orders` — List the authorized buyer's orders; use order details for logistics and invoices.
- `list_buyer_refund_operations` — List refund operation history from the buyer's perspective.
- `list_carriers` — List all logistics companies.
- `list_display_order_tags` — List order tags available for display.
- `list_expert_products` — List expert-selection products or products facing removal for failing performance criteria.
- `list_expiring_app_orders` — List the application's service orders expiring around the specified date.
- `list_freight_templates` — List freight templates; freight descriptions and seller-paid template 1 are not returned.
- `list_invoice_applications` — List seller-side invoice applications by page.
- `list_legacy_orders` — List orders through the deprecated internal business-assistant API; prefer list_seller_orders for new integrations.
- `list_logistics_exceptions` — List logistics monitoring exceptions.
- `list_offline_carriers` — List carriers supported for seller-arranged shipping.
- `list_order_invoices` — List invoices associated with a trade order through the seller-view endpoint.
- `list_photos` — List photos in an album.
- `list_potential_expert_products` — List potential expert-selection products or products removed from expert selection.
- `list_related_suppliers` — Find suppliers related to the buyer through purchases or follows; dedicated API permission is required.
- `list_search_order_tags` — List order tags available for search filtering.
- `list_seller_order_refunds` — Get in-sale refunds for an order from the seller's perspective.
- `list_seller_orders` — List seller-side orders in the encrypted-data scenario; details provide logistics and invoices.
- `list_seller_products` — List the authorized seller's products. Use ID sorting when traversing all products; simple products are excluded.
- `list_seller_refunds` — List seller-side refunds by order or filters; data may be delayed.
- `list_shipping_addresses` — List the authorized user's shipping addresses.
- `list_subscription_orders` — List service-market subscription orders.
- `list_supply_products` — List supply products by product, audit, bidding and supply-status filters.
- `list_tdd_carriers` — List Tao Da Dian carriers.
- `list_tdd_orders` — List Tao Da Dian orders.
- `list_tdd_shipping_addresses` — List Tao Da Dian seller shipping addresses.
- `list_user_categories` — List the authorized user's seller-defined product categories.
- `list_videos` — List videos in the authorized user's video center.
- `list_waybill_templates` — List electronic waybill print templates.
- `parse_address_code` — Resolve region codes from an address.
- `patch_product` — Apply an incremental product edit using the category publishing schema. [write]
- `preview_order` — Preview pricing, promotions, stock and purchasing eligibility for products from one supplier.
- `print_ae_pickup_labels` — Get pickup-order, carton or product label print data for AliExpress JIT.
- `query_product_publishing_data` — Query publishing suggestions such as brands, categories and titles using the schema query type.
- `rate_orders` — Submit seller-to-buyer ratings for at most ten orders; ratings below four stars require a comment. [write]
- `recommend_carriers` — Recommend logistics companies for a receiving location.
- `redeem_receiving_code` — Redeem a goods-receipt verification code as the seller. [write]
- `remove_products_from_category` — Remove up to 50 product memberships from a seller-defined category without deleting the products. [write]
- `republish_products` — Republish offline products, subject to the seller's daily publishing quota and category restrictions. [write]
- `request_receiving_code` — Request a goods-receipt verification code as the seller. [write]
- `resolve_wangwang_nickname` — Resolve an OpenUID solely for a user-initiated Wangwang launch. Automated bulk decryption or displaying plaintext for other purposes is prohibited by 1688.
- `retry_invoice` — Retry a failed seller invoice submission. [write]
- `save_product_customization` — Save standard customization services for the specified products. [write]
- `save_seller_customization_values` — Save the seller's customization service values. [write]
- `search_categories` — Search leaf publishing categories by keyword.
- `search_distribution_products` — Search domestic distribution products by keyword and filters.
- `set_user_category_enabled` — Enable or disable the display of seller-defined product categories. [destructive]
- `set_waybill_enabled` — Report whether the seller has enabled or terminated downstream electronic waybill service for a channel. [destructive]
- `ship_order_official` — Request official logistics pickup for whole orders; merged and repeated partial shipments are unsupported. [write]
- `ship_order_offline` — Ship orders using a carrier arranged by the seller, including supported merged or line-item shipments. [write]
- `ship_order_without_logistics` — Mark supported orders or order lines shipped without logistics, providing the applicable reason and evidence. [write]
- `ship_tdd_order` — Ship a Tao Da Dian order using seller-arranged logistics. [write]
- `submit_exchange_tracking` — Submit the replacement shipment tracking number for an exchange dispute. [write]
- `submit_invoice` — Submit a seller's blue invoice. [write]
- `submit_red_invoice` — Submit a seller's red invoice. [write]
- `submit_reshipping_tracking` — Submit the tracking number for a reshipment. [write]
- `update_album` — Update the authorized user's photo album and optional access password. [write]
- `update_buyer_protection` — Update a product's buyer-protection services; category and seller requirements still apply. [write]
- `update_order_memo` — Replace the authorized buyer's or seller's order memo. [write]
- `update_order_price` — Update shipping and line discounts relative to original order prices, replacing existing discounts. [write]
- `update_order_recipient` — Update an order's receiving address as the seller. [write]
- `update_photo` — Update photo information. [write]
- `update_product_stock` — Update product stock incrementally or absolutely; the upstream default is incremental. [write]
- `update_quick_return_stock` — Update a product's quick-return stock. [write]
- `update_supply_stock` — Update SKU stock for a supply product. [write]
- `update_video` — Update a video-center video's title and description. [write]
- `update_waybill` — Update an electronic waybill. [write]
- `upload_customization_image` — Upload a customization-service image by passing the base64-encoded image URL to 1688. [write]
- `upload_photo` — Upload a photo of at most 2 MB from a public URL. Supported formats: jpg, jpeg, gif, bmp and png; PNG transparency is not preserved by 1688. [write]
- `upload_shipping_voucher` — Upload a shipping voucher from a public file URL. [write]
- `upload_video` — Upload a video of at most 50 MB to the video center using a public file URL. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change 1688 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — 1688 is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/1688
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- 1688 homepage: https://www.1688.com/
- API documentation: https://open.1688.com/doc/apiAuth.htm
