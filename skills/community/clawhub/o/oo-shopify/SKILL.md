---
name: oo-shopify
description: "Shopify (shopify.com). Use this skill for ANY Shopify request — reading, creating, updating, and deleting data. Whenever a task involves Shopify, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Shopify"
  author: "OOMOL"
  version: "1.0.7"
  services: ["shopify"]
  icon: "https://static.oomol.com/logo/third-party/shopify.svg"
---

# Shopify

Operate **Shopify** through your OOMOL-connected account. This skill calls the `shopify` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Shopify. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "shopify" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "shopify" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_collection_products` — Add products to a manual collection. Requires write_products. [write]
- `add_tags` — Add tags to a supported resource. Requires the write scope for that resource. [write]
- `adjust_inventory_quantities` — Apply incremental Shopify inventory quantity changes with required idempotency and explicit compare-and-swap values. [write]
- `cancel_bulk_operation` — Request cancellation of a bulk operation; poll its status until cancellation completes. [destructive]
- `cancel_order` — Cancel an order, optionally refunding payments, restocking, and notifying the customer. Requires write_orders and order cancellation permission. [destructive]
- `close_order` — Archive an order. Requires write_orders. [destructive]
- `complete_draft_order` — Complete a draft order, creating an order and recording the selected payment state. Requires write_draft_orders. [write]
- `count_articles` — Count Shopify REST articles in a blog with optional filters.
- `count_blogs` — Count Shopify REST blogs in the connected shop.
- `count_pages` — Count Shopify REST pages with optional filters.
- `create_article` — Create a blog article. Requires write_content or write_online_store_pages. [write]
- `create_blog` — Create a blog. Requires write_content or write_online_store_pages. [write]
- `create_collection` — Create a manual or automated collection. Supply collection or the legacy input argument. Requires write_products; unavailable on Starter and Retail plans. [write]
- `create_customer` — Create a customer with contact details and addresses. Requires write_customers and applicable protected customer data access. [write]
- `create_customer_address` — Add a customer address. Requires write_customers. [write]
- `create_draft_order` — Create a draft order with line items, customer details, discounts, and shipping. Requires write_draft_orders. [write]
- `create_files` — Create files from externally hosted URLs. Poll each returned file ID for processing completion. Requires write_files. [write]
- `create_fulfillment` — Create a Shopify fulfillment for one or more fulfillment orders with optional tracking and customer notification. [write]
- `create_metaobject` — Create a metaobject for an existing definition. Requires write_metaobjects. [write]
- `create_page` — Create an online store page. Requires write_content or write_online_store_pages. [write]
- `create_product` — Create one Shopify product with typed product attributes and optional media sources. [write]
- `create_product_variants` — Create product variants with option values, inventory, prices, and media. Requires write_products. [write]
- `create_refund` — Refund order line items, shipping, and transactions. Reuse the same idempotencyKey when retrying the same refund. Requires write_orders. [write]
- `delete_article` — Delete a blog article. Requires write_content or write_online_store_pages. [destructive]
- `delete_blog` — Delete a blog and its articles. Requires write_content or write_online_store_pages. [destructive]
- `delete_collection` — Delete a collection without deleting its products. Requires write_products. [destructive]
- `delete_customer` — Delete a customer when Shopify's business rules permit it. Requires write_customers. [destructive]
- `delete_customer_address` — Delete a customer address. Requires write_customers. [destructive]
- `delete_draft_order` — Delete a draft order. Requires write_draft_orders. [destructive]
- `delete_files` — Delete files from the shop. Requires write_files. [destructive]
- `delete_metafields` — Delete metafields identified by owner, namespace, and key. Requires write access to their owners. [destructive]
- `delete_metaobject` — Delete a metaobject. Requires write_metaobjects. [destructive]
- `delete_page` — Delete an online store page. Requires write_content or write_online_store_pages. [destructive]
- `delete_product` — Delete a product. Requires write_products and product deletion permission. [destructive]
- `delete_product_variants` — Delete product variants. Requires write_products. [destructive]
- `download_bulk_result` — Download a completed or partial Shopify bulk JSONL result and upload it to connector transit storage.
- `duplicate_product` — Duplicate a product, optionally including images and translations. Requires write_products. [write]
- `execute_graphql` — Execute a JSON-friendly Shopify Admin GraphQL query or mutation against the connected shop. [write]
- `get_article` — Retrieve one Shopify REST article by blog ID and article ID.
- `get_blog` — Retrieve one Shopify REST blog by numeric ID.
- `get_bulk_operation` — Retrieve one Shopify bulk operation by ID for progress polling and result URL discovery.
- `get_collection` — Retrieve one Shopify collection by GraphQL global ID.
- `get_customer` — Retrieve one Shopify customer by GraphQL global ID.
- `get_draft_order` — Get a draft order and its invoice URL. Requires read_draft_orders.
- `get_file` — Get a file's processing state, errors, and available download URL. Requires read_files.
- `get_fulfillment_order` — Retrieve one Shopify fulfillment order with independently paginated line items.
- `get_inventory_item` — Retrieve one Shopify inventory item by GraphQL global ID.
- `get_inventory_quantities` — Retrieve selected inventory quantity states for one Shopify inventory item at one location.
- `get_job` — Check whether a Shopify background job has completed.
- `get_location` — Retrieve one Shopify location by GraphQL global ID.
- `get_metaobject` — Get a metaobject and its fields. Requires read_metaobjects.
- `get_order` — Retrieve one Shopify order by GraphQL global ID.
- `get_order_cancel_result` — Poll an order cancellation and return its success or failure status and errors. Requires read_orders and order cancellation permission.
- `get_page` — Retrieve one Shopify REST page by numeric ID.
- `get_product` — Retrieve one Shopify product by GraphQL global ID.
- `get_product_operation` — Poll a product deletion or duplication operation. Requires read_products.
- `get_shop` — Retrieve basic shop information for the connected Shopify Admin token.
- `list_article_authors` — List Shopify REST article authors across the connected shop.
- `list_article_tags` — List Shopify REST article tags across all articles in the connected shop.
- `list_articles` — List Shopify REST articles in a blog with optional filters and pagination.
- `list_blog_article_tags` — List Shopify REST article tags for one blog.
- `list_blogs` — List Shopify REST blogs with optional handle filtering and pagination.
- `list_bulk_operations` — Search bulk operations and their result URLs.
- `list_collections` — List Shopify collections with optional search query and cursor pagination.
- `list_customers` — List Shopify customers with optional search query and cursor pagination.
- `list_draft_orders` — Search draft orders with cursor pagination. Requires read_draft_orders.
- `list_files` — Search files and their processing states. Requires read_files.
- `list_inventory_items` — List Shopify inventory items with optional search query and cursor pagination.
- `list_locations` — List Shopify inventory locations with optional filters and cursor pagination.
- `list_metaobjects` — Search metaobjects of a definition type. Requires read_metaobjects.
- `list_order_fulfillment_orders` — List fulfillment orders and fulfillable line items for one Shopify order.
- `list_orders` — List Shopify orders with optional search query and cursor pagination.
- `list_pages` — List Shopify REST pages with optional filters and pagination.
- `list_product_variants` — List Shopify product variants with optional search query and cursor pagination.
- `list_products` — List Shopify products with optional search query and cursor pagination.
- `list_publications` — List publications available to the app. Requires read_publications.
- `mark_order_paid` — Record payment for an order; this does not charge a payment method. Requires write_orders. [write]
- `open_order` — Reopen an archived order. Requires write_orders. [write]
- `publish_resource` — Publish a resource to publications. Requires write_publications. [write]
- `remove_collection_products` — Remove products from a manual collection and return a background job. Requires write_products. [write]
- `remove_tags` — Remove tags from a supported resource. Requires the write scope for that resource. [write]
- `send_draft_order_invoice` — Send the draft order invoice email. Requires write_draft_orders. [write]
- `send_order_invoice` — Send an invoice email for an order. Requires write_orders. [write]
- `set_default_customer_address` — Select the customer's default address. Requires write_customers. [write]
- `set_inventory_quantities` — Set absolute Shopify inventory quantities with required idempotency and explicit compare-and-swap values. [write]
- `set_metafields` — Set metafields atomically, optionally using compareDigest for optimistic concurrency. Requires write access to the owning resources. [write]
- `submit_bulk_query` — Submit a Shopify Admin GraphQL bulk query and return an operation ID for asynchronous polling. [write]
- `unpublish_resource` — Unpublish a resource from publications. Requires write_publications. [destructive]
- `update_article` — Update a blog article. Requires write_content or write_online_store_pages. [write]
- `update_blog` — Update a blog. Requires write_content or write_online_store_pages. [write]
- `update_collection` — Update a collection and its rules. Supply collection or the legacy input argument. Requires write_products. [write]
- `update_customer` — Update a customer identified by input.id. Requires write_customers. [write]
- `update_customer_address` — Update a customer address. Requires write_customers. [write]
- `update_draft_order` — Update a draft order. Requires write_draft_orders. [write]
- `update_metaobject` — Update a metaobject. Requires write_metaobjects. [write]
- `update_page` — Update an online store page. Requires write_content or write_online_store_pages. [write]
- `update_product` — Update one Shopify product by GraphQL global ID with typed attributes and optional new media. [write]
- `update_product_variants` — Update product variants. When allowPartialUpdates is true, return successful variants together with errors. Requires write_products. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Shopify state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Shopify is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential, API key, OAuth2) at:

  ```text
  https://console.oomol.com/connections/shopify
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Shopify homepage: https://www.shopify.com
- API documentation: https://shopify.dev/docs/api/admin-rest
