---
name: printful-management
description: Manage a Printful account through the Printful REST API using a private API token. Use when the user wants to inspect or manage Printful stores, connected-store sync products, manual/API-store products, variants, orders, product templates, file library items, shipping rates, webhooks, mockups, warehouse products, tax endpoints, approval sheets, reports, or exports; when building a local Printful integration; or when converting seller requests like "list my Printful items", "show my stores", "export my products to CSV", "update this synced variant", "create a mockup task", or "configure Printful webhooks" into safe API calls.
---

# Printful Management

Use this skill to work with a user's Printful account via API token instead of brittle browser login.

## Quick start

1. Get a Printful private token from the user.
2. Prefer storing it in the current shell as `PRINTFUL_API_KEY` instead of hardcoding it into files.
3. Use `scripts/printful_api.py` for live calls.
4. Start with safe read calls:
   - `stores`
   - `sync-products` for connected-platform stores like Etsy
   - `manual-products` for Manual Order / API stores
   - `orders`
5. Before write operations, summarize the exact mutation and wait for confirmation unless the user already clearly asked for the change.

## Core workflow

### 1. Identify the seller task

Classify the request into one of these buckets:

- **Stores**: inspect stores, get store IDs
- **Connected-store products**: list sync products or variants for Etsy and similar platform-connected stores
- **Manual/API-store products**: create or manage products for Manual Order / API stores
- **Orders**: list orders, inspect one order, create draft orders, confirm fulfillment
- **Catalog**: inspect Printful catalog products, variants, categories, and size guides before creating store products
- **Files / mockups**: upload artwork, inspect file library, generate mockups
- **Webhooks**: inspect or configure webhook delivery
- **Shipping / tax**: quote shipping, inspect tax-country support, calculate tax rates
- **Reporting / warehouse / approvals**: pull stats, warehouse product data, or approval sheet actions

If the request is vague, ask one short clarifying question.

### 2. Start read-only

Prefer these discovery calls first:

```powershell
python scripts/printful_api.py stores
python scripts/printful_api.py sync-products --store-id <id>
python scripts/printful_api.py orders --store-id <id>
```

If `sync-products` fails with a Manual/API-store style error, switch to:

```powershell
python scripts/printful_api.py manual-products --store-id <id>
```

These usually reveal the IDs needed for later write calls.

### 3. Handle auth safely

Prefer ephemeral auth in the shell:

```powershell
$env:PRINTFUL_API_KEY = 'pf_xxx'
```

The helper script also accepts `--api-key`, but environment variables are better because they reduce accidental logging and file leakage.

### 4. Use the helper script

`scripts/printful_api.py` wraps a broad set of Printful endpoints and also supports arbitrary API requests.

Common reads:

```powershell
python scripts/printful_api.py scopes
python scripts/printful_api.py stores
python scripts/printful_api.py store --store-id 12345
python scripts/printful_api.py sync-products --store-id 12345 --limit 100
python scripts/printful_api.py sync-product --store-id 12345 --product-id 67890
python scripts/printful_api.py manual-products --store-id 12345 --limit 100
python scripts/printful_api.py orders --store-id 12345 --limit 50
python scripts/printful_api.py order --store-id 12345 --order-id 111
python scripts/printful_api.py catalog-products --limit 20
python scripts/printful_api.py catalog-product --product-id 71
python scripts/printful_api.py catalog-variant --variant-id 4011
python scripts/printful_api.py categories
python scripts/printful_api.py templates --store-id 12345
python scripts/printful_api.py webhooks --store-id 12345
python scripts/printful_api.py statistics --store-id 12345
python scripts/printful_api.py export-products --store-id 12345 --format markdown --output-file report.md
python scripts/printful_api.py export-products --store-id 12345 --format csv --output-file products.csv
```

Common writes:

```powershell
python scripts/printful_api.py create-manual-product --store-id 12345 --body-file product.json
python scripts/printful_api.py update-sync-variant --store-id 12345 --variant-id 999 --body-file variant.json
python scripts/printful_api.py create-order --store-id 12345 --body-file order.json
python scripts/printful_api.py confirm-order --store-id 12345 --order-id 111
python scripts/printful_api.py add-file --store-id 12345 --body-file file.json
python scripts/printful_api.py set-webhooks --store-id 12345 --body-file webhook.json
python scripts/printful_api.py create-mockup-task --store-id 12345 --body-file mockup.json
```

Raw requests:

```powershell
python scripts/printful_api.py raw GET /stores
python scripts/printful_api.py raw GET /sync/products?limit=10 --store-id 12345
python scripts/printful_api.py raw POST /webhooks --store-id 12345 --body-file webhook.json
```

Notes:
- The script uses the modern `X-PF-Store-ID` header for store context.
- Responses are pretty-printed JSON.
- `--output file.json` also saves the response to disk.
- `export-products` can generate markdown, CSV, or JSON summaries for store products.
- Non-2xx responses return a non-zero exit code.

## Mutation rules

For create/update/delete operations:

1. Confirm the target store, product, variant, order, or template ID.
2. Show the exact endpoint family and payload in plain language.
3. Mention that the change affects live Printful data.
4. Prefer draft or test-safe operations first when available.
5. Respect rate limits; Printful docs indicate a general limit of 120 API calls per minute.

## Common endpoint map

Use this quick map before reaching for raw mode:

- **Stores**
  - `GET /stores`
  - `GET /stores/{id}`
- **Connected-platform sync products**
  - `GET /sync/products`
  - `GET /sync/products/{id}`
  - `GET /sync/variants/{id}`
  - `PUT /sync/variants/{id}`
  - `DELETE /sync/variants/{id}`
- **Manual/API-store products**
  - `GET /store/products`
  - `GET /store/products/{id}`
  - `POST /store/products`
  - `PUT /store/products/{id}`
  - `DELETE /store/products/{id}`
  - `GET /store/variants/{id}`
  - `POST /store/variants`
  - `PUT /store/variants/{id}`
  - `DELETE /store/variants/{id}`
- **Orders**
  - `GET /orders`
  - `GET /orders/{id}`
  - `POST /orders`
  - `PUT /orders/{id}`
  - `DELETE /orders/{id}`
  - `POST /orders/{id}/confirm`
  - `POST /orders/estimate-costs`
- **Catalog**
  - `GET /products`
  - `GET /products/{id}`
  - `GET /products/variant/{id}`
  - `GET /products/{id}/sizes`
  - `GET /categories`
  - `GET /categories/{id}`
- **Product templates**
  - `GET /product-templates`
  - `GET /product-templates/{id}`
  - `DELETE /product-templates/{id}`
- **Webhooks**
  - `GET /webhooks`
  - `POST /webhooks`
  - `DELETE /webhooks`
- **Mockups**
  - create task
  - get task result
  - get printfiles
  - get layout templates
- **Reports / warehouse / approvals**
  - statistics
  - warehouse product list/detail
  - approval sheet list/actions

If exact payload fields matter, read `references/printful-api-notes.md`, `references/request-examples.md`, and, if needed, the official docs page the user supplied.

## Response style

When reporting account data back to the user:

- Summarize first.
- Then list IDs, names, statuses, and counts.
- Do not dump giant raw JSON unless the user asked for it.
- If products are "for sale", distinguish between catalog products and the user’s synced store products.
- Call out whether the store is likely a connected-platform store or a Manual/API store if that changes which endpoint family applies.

## Publication hygiene

If the user wants the skill published to ClawHub:

1. Ensure no secrets or local dumps live inside the skill folder.
2. Validate and package the skill.
3. Use the `clawhub` CLI to publish the **skill folder**, not random extra workspace files.
4. Do not publish until the user explicitly wants the live publish action.

## Local reference

Read `references/printful-api-notes.md` when you need a compact refresher on auth, endpoint-family selection, rate limits, and publication hygiene. Read `references/request-examples.md` when you need starter JSON bodies for common writes.
