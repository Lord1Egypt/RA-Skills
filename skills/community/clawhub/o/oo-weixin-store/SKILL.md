---
name: oo-weixin-store
description: "WeChat Store (channels.weixin.qq.com). Use this skill for ANY WeChat Store request — reading, creating, updating, and deleting data. Whenever a task involves WeChat Store, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WeChat Store"
  author: "OOMOL"
  version: "1.0.4"
  services: ["weixin_store"]
  icon: "https://static.oomol.com/logo/third-party/weixin_store.svg"
---

# WeChat Store

Operate **WeChat Store** through your OOMOL-connected account. This skill calls the `weixin_store` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WeChat Store. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "weixin_store" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "weixin_store" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `accept_aftersale` — Accept a buyer's after-sale request. Accepting a return needs a merchant address id from list_addresses; acceptType chooses between accepting the return (1) and accepting the refund (2), and is chosen automatically when omitted. [write]
- `add_product` — Create a product. All image fields must be WeChat-hosted URLs from upload_image. By default the product is saved as a draft; pass listing 1 to submit it for review and list it directly. Nested objects and arrays keep their WeChat snake_case fields as documented per field. [write]
- `apply_category` — Apply for permission to sell in a leaf category using the new category tree and certificate groups. Returns an audit id; check the audit and effective permission before publishing products. [write]
- `delete_product` — Permanently delete a product by product_id. A product under review cannot be deleted. This cannot be undone. [destructive]
- `delisting_product` — Take a listed product off the shelf. [write]
- `get_address` — Get one merchant address by address_id, including its contact, region, and send/recv flags. Accepting an after-sale return needs one of these address ids.
- `get_aftersale_complaint` — Read an after-sale dispute by its complaint id, including state and evidence history. This does not submit evidence, accept a refund or resolve the dispute.
- `get_aftersale_order` — Get one after-sale order by its id, including its status, type, products, and refund details.
- `get_category` — Get the publishing rules of one leaf category: required product and sale attributes, brand restrictions, deposit, and qualifications.
- `get_category_application` — Get the status and any rejection reason of a category application by audit id.
- `get_category_product_rule` — Get the category's product attribute, sale attribute, qualification, price, and other publishing rules for the chosen release mode.
- `get_compass_product_data` — Read historical Compass product click and transaction data. T+1 only: date must be yesterday or earlier in Asia/Shanghai. Monetary values and counts retain upstream string units.
- `get_compass_shop_overview` — Read daily shop-wide product clicks, transactions and refunds. T+1 historical data only; no same-day traffic inference. Counts and monetary values retain upstream strings, with money in fen.
- `get_freight_template` — Get one freight template by template_id, including its valuation type, shipping method, sender address, and freight rules. Freight templates bind to products through expressInfo on add_product.
- `get_funds_balance` — Read the store's available and pending-settlement balances. Does not withdraw funds or change the settlement account. Amounts retain the upstream units.
- `get_funds_flow` — Read one funds flow, including income/expense, fees and related order/after-sale ids. Preserve the upstream amount units; an unavailable flow is an error, not a zero balance.
- `get_league_plan` — Read an existing alliance plan's activation, eligibility and commission. The returned item.type uses legacy values 1/2/3; do not reuse it as request type 100/300.
- `get_league_promoter` — Read a known alliance talent's profile, sales metrics and blacklist status. Supply exactly one talent identifier, not a nickname.
- `get_merchant_ticket` — Read one merchant complaint ticket, including its deadline and merchant/platform response history.
- `get_order` — Get one order by order_id, including its products, payment, price, and delivery details. Buyer address fields are masked.
- `get_product` — Get one product by product_id. Products keep a draft and an online copy; dataType selects which.
- `get_product_audit_strategy` — Read store-wide product listing policy switches. This is not a historical delisting-reason log and does not change any policy.
- `get_product_h5_url` — Get a shareable H5 purchase link for an on-sale, self-operated store product. Optional linked WeCom company and member ids attribute orders to that company. Only WeChat Store accounts support this API.
- `get_product_qr_code` — Get a QR-code image URL for an on-sale self-operated product, optionally as standard or gift artwork. Optional bound WeCom ids attribute resulting orders. This does not publish the image.
- `get_product_restricted_info` — Read restricted sales scenes for 1 to 50 products, including alliance and talent-window restrictions. This does not change product status. Merchant quota: 100 calls per minute.
- `get_product_tag_link` — Get the WeChat sharing token for an on-sale self-operated product, with optional bound WeCom attribution. The returned token only opens inside WeChat; it is not an ordinary HTTPS link.
- `get_shop_info` — Get the basic information of the connected WeChat Store: name, avatar, subject type, and status.
- `invite_league_promoter` — Invite one known talent to cooperate with the shop. This sends an external invitation: obtain approval for the exact recipient first. Supply promoterId or the deprecated finderId, never infer promoterId from talent_appid. Do not retry blindly after a timeout; WeChat rejects duplicate invitations within 24 hours and already-cooperating talents. [write]
- `list_addresses` — List the merchant address ids of the store. After-sale returns need one of these address ids when accepting a return.
- `list_aftersale_orders` — List the after-sale order ids of the store, paginated by cursor. At least one time range pair is required, as Unix timestamps in seconds spanning at most 24 hours.
- `list_aftersale_reasons` — Read the current after-sale reason codes and labels instead of guessing their meanings.
- `list_aftersale_reject_reasons` — Read current rejection reasons, applicable after-sale scenes and need_proof. If a chosen reason requires proof, upload images with upload_aftersale_image and pass mediaFiles to reject_aftersale.
- `list_categories` — Get the full category tree of the store, including the qualifications each category requires. Use the leaf cat_id values from cats_v2 for add_product and get_category.
- `list_category_permissions` — List the store's category permissions. Filter to status 1 to find categories currently allowed for sale.
- `list_delivery_companies` — List the delivery companies the store can ship with, including each company's delivery_id.
- `list_freight_templates` — List the freight template ids of the store.
- `list_funds_flows` — List funds-flow ids for reconciliation; inspect each with get_funds_flow. Daily flows become available after 16:00 the following day. Continue while has_more using the returned next_key, incrementing page and keeping pageSize unchanged. nextKey is required when page * pageSize >= 10000.
- `list_league_products` — List existing alliance products and eligibility status. Pagination is bounded by pageSize multiplied by pageIndex <= 5000; no undocumented cursor is sent.
- `list_league_promoter_products` — Read a known cooperating talent's current window products or products sold in the last 30 days. This does not discover new talents or add products to a window.
- `list_league_promoters` — List the connected merchant's alliance talents. This is not a platform-wide talent search; follow continue_flag to paginate.
- `list_merchant_tickets` — List merchant complaint tickets and response deadlines. WeChat currently exposes shipping-reminder tickets (class 9) only; this is not a general platform-notification inbox. Paginate with start/limit and total; omitted state includes all states.
- `list_order_settlements` — Read order settlement, refund and fee breakdowns, in fen. Uses stable page-context pagination by default: pass the returned page_ctx until it is empty. Set usePageContext false to use offsets. Expected settlement is not actual profit or received cash.
- `list_orders` — List the order ids of the store, paginated by cursor. At least one time range is required, as a pair of Unix timestamps in seconds spanning at most 7 days.
- `list_product_promotion_plans` — List an existing product's alliance promotion plan identifiers before inspecting or changing a specific plan. Filtered audience type 200 is supported by this list only, not get_league_plan or update_league_plan.
- `list_product_promotion_talents` — Read talents related to one existing product promotion plan and their promotion relationship status. This is not platform-wide discovery and does not prove that a product is in a talent's window.
- `list_products` — List the product ids of the store, paginated by cursor.
- `list_valid_brands` — List the brand qualifications currently in effect for the store, paginated by cursor. Use a returned brand_id when adding a product in a brand-restricted category.
- `listing_product` — Submit a product for review and list it once approved. [write]
- `precheck_product_category` — Check whether the store may publish in a leaf category, including category permission, deposit, freight insurance, and store restrictions. Omit catId for store-wide checks only.
- `reject_aftersale` — Reject a buyer's after-sale request using a current reason from list_aftersale_reject_reasons. Check reject_scene and need_proof; when proof is required, supply mediaFiles with complete C2C URLs (upload_aftersale_image for images). [write]
- `send_delivery` — Ship an order, in one or more packages. Each package either ships by express with a waybill (deliverType 1, needs waybillId and deliveryId from list_delivery_companies, or OTHER when the company is not listed) or delivers virtual goods without logistics (deliverType 3, only for orders whose products use the phone-number delivery method). [write]
- `send_exchange_delivery` — Record shipment of a replacement in an exchange after receiving the buyer's return. Requires an actual carrier and waybill. Do not submit shipments for multiple after-sales of the same order within one minute. [write]
- `update_delivery_info` — Correct express-package logistics using old/new package identities (change_infos), including split shipments where supported. WeChat permits at most three corrections before order completion and rejects virtual-goods corrections. Confirm the actual shipment before changing its carrier or waybill. [write]
- `update_league_plan` — Change one existing alliance promotion plan: edit commission and activate (1), delist (2), or activate (4). Obtain approval for the exact plan and change first; activation or commission changes can incur commission spending. Read the plan before and after; no automatic fallback, audience changes, new plan creation or deletion is provided. [write]
- `update_order_merchant_notes` — Replace the merchant note of one order, optionally with a tag color. [write]
- `update_product` — Replace a product's editable data. This is a full overwrite: every field of add_product applies, SKUs that carry an existing sku_id are updated, SKUs without one are added, and previously existing SKUs missing from the list are deleted. [write]
- `update_product_stock` — Update the stock of a product's SKUs. This does not consume the product review quota. [write]
- `upload_aftersale_image` — Upload a JPEG, PNG, BMP or GIF transit file up to 10 MB as after-sale evidence (scene 170). Returns a C2C image URL for reject_aftersale mediaFiles. Keep the complete URL including query parameters; ordinary product-image URLs cannot substitute for this upload. [write]
- `upload_image` — Ask WeChat to fetch and host a public image URL for use in product image fields. At most 10 MB per image. [write]
- `upload_qualification_image` — Upload a qualification image (up to 2 MB) and return the file_id required for category and brand applications. Product images from upload_image cannot be used here. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WeChat Store state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WeChat Store is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/weixin_store
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WeChat Store homepage: https://channels.weixin.qq.com/shop
- API documentation: https://developers.weixin.qq.com/doc/store/API/basics/getaccesstoken.html
