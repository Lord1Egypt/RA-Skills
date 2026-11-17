---
name: podbenchmark
description: Compare print-on-demand (POD) supplier prices for one product, size, color and destination. Use when a seller asks which POD supplier is cheapest (Printify, Printful, Gelato, Prodigi, Apliiq, Artelo, CustomCat, Fourthwall, Inkthreadable or merchOne), what a blank costs delivered, how long delivery takes, how much they keep per sale on Etsy or Shopify, or which supplier fits their shop.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://podbenchmark.com
    emoji: "👕"
---

<!-- Published by POD Benchmark. Source: skills/podbenchmark/SKILL.md in the POD Benchmark repository. -->

# POD Benchmark

[POD Benchmark](https://podbenchmark.com) compares the same print-on-demand product across supplier offers for one configuration and destination: product cost, shipping, delivered total, estimated delivery, and what the seller keeps per sale.

Suppliers: Printify, Printful, Gelato, Prodigi, Apliiq, Artelo, CustomCat, Fourthwall, Inkthreadable, merchOne. Destinations: US, GB, DE, CA, AU. Currencies: USD, EUR, GBP, CAD, AUD. Prices are supplier quotes, checked on the date in the answer and before sales tax.

Free and read-only: **no API key, no signup, no account.**

## Connect

MCP, preferred: `https://podbenchmark.com/api/mcp` (Streamable HTTP, no auth header).

HTTP API: `POST https://podbenchmark.com/api/v1/tools/<tool>` with the tool's input as the JSON body. `GET https://podbenchmark.com/api/v1/tools` lists every tool with input and output JSON Schemas.

CLI, when a shell is easier: `npx podbenchmark <command>`.

```bash
curl -s https://podbenchmark.com/api/v1/tools/compare_product \
  -H 'content-type: application/json' \
  -d '{"canonicalProductId":"bella-canvas-3001","destination":"US","currency":"USD","choices":{"size":"m","color":"black"}}'
```

## Flow: search, then options, then compare

1. `search_products` finds the product: `{"query":"bella canvas 3001","destination":"US"}`. Keep a `canonicalProductId`.
2. `get_product_options` for that product, destination and currency lists sizes, colors and the opening option.
3. `compare_product` takes the product, `destination`, `currency` and either `choices` by field (`{"size":"m","color":"black"}`) or an exact `optionKey` from step 2.

Never guess a size or color. Take values from `get_product_options`; a rejected value returns `invalid_option` naming the valid ones.

## Seller context: pass only what the seller said

- `yourSupplier`: the supplier they use today. It is pinned first and every other row shows the difference per sale.
- `sellingPrice`, or `targetMargin` in percent, with `salesChannel` (`etsy`, `shopify`, `woocommerce`, `tiktok-shop`) and `shopLocation`: what they keep per sale after delivered cost and platform fees, or the price to charge for a margin.
- A price or margin without `salesChannel` or `shopLocation` returns the fields to ask for. Do not estimate platform fees yourself.
- `resolve_supplier_link`: a pasted Printify, Printful, Gelato and other supplier product link becomes the product and selected color.

## Tools

| Tool | Answers |
| --- | --- |
| `search_products` | Products by words, category, brand, supplier, audience, specs or weight, with starting delivered prices |
| `list_categories` | Categories with product counts and starting prices |
| `get_product` | Curated specs, fabric, fit, print methods, FAQs, similar products |
| `get_product_options` | The product's configuration fields, values and opening option |
| `compare_product` | Delivered comparison for one configuration, with profit when the seller's context is given |
| `resolve_supplier_link` | The product and color behind a supplier product link |
| `list_suppliers` | The suppliers POD Benchmark compares |
| `get_supplier` | Plans, monthly fees, branding, who handles checkout, where it prints |
| `get_supplier_prices` | Where a supplier is cheapest overall, by category, or against one rival |
| `supplier_guide` | Suppliers that fit a product type, shop and platform, with dated reasons |

## Reading results

- `null` or "—" is unknown, never 0. A missing price is not free and not the cheapest.
- Delivered total is product + shipping. Duty and sales tax are separate. Give duty as established (including zero), one labelled estimate, or unverified; do not narrate min–max ranges. Profit may deduct known or estimated duty, so keep its qualification. Estimated or unverified duty, and conditional design or setup prices, never support a best-profit or gap claim.
- Printify is a marketplace, so a row can say "via" a print provider. Paid plan prices appear only when `pricingTier` asks for them; the default is standard pricing.
- Report what the answer contains and no more. When you answer the seller, link the comparison at `product.url`.
- Errors are `{"ok":false,"error":{"code","message","retryable"}}`. The endpoint allows 120 requests a minute per client; `rate_limited` carries `Retry-After`.
