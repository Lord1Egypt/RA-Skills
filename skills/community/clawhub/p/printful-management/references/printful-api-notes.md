# Printful API notes

## Base request shape

- Base URL: `https://api.printful.com`
- Auth: `Authorization: Bearer <token>`
- Optional store context header: `X-PF-Store-ID: <store_id>`
- Optional localisation header: `X-PF-Language: en_US`
- Content type for writes: `application/json`
- Common response shape:
  - `code`: mirrors HTTP status
  - `result`: payload
  - optional `paging`
  - optional `error`

## Auth and store context

For account management in this workspace, prefer a private token supplied by the user.

Recommended shell setup:

```powershell
$env:PRINTFUL_API_KEY = 'pf_xxx'
```

Avoid saving raw tokens to skill files.

Important distinction from older examples:

- newer Printful docs use the **`X-PF-Store-ID` header** for store context
- account-level private tokens can access multiple stores
- store-level tokens may already be bound to a single store

## Two sync-product families

This is the most important practical gotcha.

### 1. Ecommerce-platform sync endpoints

Use these for connected platforms like **Etsy**:

- `GET /sync/products`
- `GET /sync/products/{id}`
- `DELETE /sync/products/{id}`
- `GET /sync/variants/{id}`
- `PUT /sync/variants/{id}`
- `DELETE /sync/variants/{id}`

In the helper script, these map to commands like:

```powershell
python scripts/printful_api.py detect-store-mode --store-id 12345
python scripts/printful_api.py products-auto --store-id 12345
python scripts/printful_api.py sync-products --store-id 12345
python scripts/printful_api.py sync-product --store-id 12345 --product-id 67890
python scripts/printful_api.py update-sync-variant --store-id 12345 --variant-id 999 --body-file variant.json
```

### 2. Manual/API store endpoints

Use these for Manual Order / API platform stores:

- `GET /store/products`
- `GET /store/products/{id}`
- `POST /store/products`
- `PUT /store/products/{id}`
- `DELETE /store/products/{id}`
- `GET /store/variants/{id}`
- `POST /store/variants`
- `PUT /store/variants/{id}`
- `DELETE /store/variants/{id}`

In the helper script, these map to commands like:

```powershell
python scripts/printful_api.py manual-products --store-id 12345
python scripts/printful_api.py create-manual-product --store-id 12345 --body-file product.json
```

If one family throws a "this endpoint applies only to Manual Order / API platform" style error, switch to the other family.

## General rate limit

The Printful docs state a general limit of **120 API calls per minute**. Some intensive endpoints may allow less. Avoid tight per-item loops when bulk endpoints exist.

## Major endpoint families

### Stores

- `GET /stores`
- `GET /stores/{id}`

Use first when you need store IDs.

### Orders

- `GET /orders`
- `GET /orders/{id}`
- `POST /orders`
- `PUT /orders/{id}`
- `DELETE /orders/{id}`
- `POST /orders/{id}/confirm`
- `POST /orders/estimate-costs`

### Catalog

- `GET /products`
- `GET /products/{id}`
- `GET /products/variant/{id}`
- `GET /products/{id}/sizes`
- `GET /categories`
- `GET /categories/{id}`

Use catalog endpoints to discover Printful product and variant options before creating store products.

### Product templates

- `GET /product-templates`
- `GET /product-templates/{id}`
- `DELETE /product-templates/{id}`

### Files and artwork helpers

- `POST /files`
- `GET /files/{id}`
- thread color suggestion endpoint

### Shipping, tax, and country codes

- shipping rates endpoint
- country list endpoint
- tax country list endpoint
- tax calculation endpoint

### Webhooks

- `GET /webhooks`
- `POST /webhooks`
- `DELETE /webhooks`

Useful when building automations that react to orders, stock updates, or product sync events.

### Mockups

- create mockup task
- get task result
- get variant printfiles
- get layout templates

### Warehouse, reports, approvals

- warehouse product list/detail
- statistics reports
- approval sheet list and actions

## Safe workflow reminders

1. Start with reads.
2. Confirm IDs before writes.
3. For live changes, tell the user exactly what will change.
4. Prefer one larger request over many tiny requests when the API supports it.
5. Keep raw response dumps small unless the user asks for full JSON.
6. Never bundle real private tokens into the skill package.

## Practical interpretation hints

- `stores` tell you which store IDs exist.
- `sync products` are the user's managed store products.
- `catalog products` are Printful's underlying printable products, not necessarily listed in the user's store.
- A seller asking for "items for sale" usually wants **sync products**, not catalog products.
- For Etsy-connected stores, `sync-products` is usually the right first stop.

## ClawHub publication hygiene

Before publishing:

- make sure no private token, order data dump, or local credential file is inside the skill folder
- keep instructions generic and reusable
- ensure scripts work without machine-specific absolute paths
- package the skill and validate it again
