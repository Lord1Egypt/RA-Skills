---
name: product-commerce
description: Search products, check prices and stock, create quotes, place orders — multi-tenant B2B/B2C commerce API
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["commerce","products","orders","quotes","b2b"]}
---

# Product Commerce

Search products, check prices and availability, create quotes, place orders. Multi-tenant B2B/B2C platform — heating fuel (granulas, briketes) and wood products (plywood, veneer, OSB).

## Base URL

`https://sputnikx.xyz/api`

## Search Products (free)
```bash
curl "https://sputnikx.xyz/api/feed/products.json"
```

## Get Prices (free)
```bash
curl "https://sputnikx.xyz/api/feed/prices"
```

## Check Availability (free)
```bash
curl "https://sputnikx.xyz/api/v1/agent/products/check?sku=GRAN-001"
```

## Create Quote ($0.10 x402)
```bash
curl -X POST https://sputnikx.xyz/api/v1/agent/orders/quote \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":10}]}'
```

## Place Order ($0.10 x402)
```bash
curl -X POST https://sputnikx.xyz/api/v1/agent/orders/place \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":10}],"delivery_address":"Riga, Latvia"}'
```

## MCP Tools
```
search_products — Search with filters (category, type, keyword)
get_prices — Current EUR prices with price_per_kg
check_availability — Stock across warehouse locations
create_quote — Draft quote with 21% VAT
place_order — Place order (max EUR 50,000, idempotent)
order_status — Check order by ID
```
