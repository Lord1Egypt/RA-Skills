# Data Shape and Source Type Guide

Use globally-generic source types (avoid local retailer naming in the schema):

- `official_store`
- `marketplace`
- `electronics_retailer`
- `general_retailer`
- `other`

## Offer CSV schema

Required columns:

- `product` — exact model/variant name (e.g., `iPhone 16 Pro 256GB`)
- `country` — market code (e.g., `US`, `JP`, `DE`)
- `currency` — ISO-4217 (e.g., `USD`, `JPY`, `EUR`)
- `source_type` — one of generic categories above
- `source_name` — human-readable source label
- `price` — numeric local price

Optional:

- `url` — product URL for verification

## Discovery backends

`discover` supports:

- `brave` (`BRAVE_API_KEY`)
- `tavily` (`TAVILY_API_KEY`)
- `all` (Brave first, Tavily fallback)

Tip: use `all` as default strategy; it keeps Brave as primary while preserving Tavily resilience.

## Guardrails for fair comparison

1. Compare the **same variant** (storage/color/spec bundle).
2. Keep price basis consistent (incl/excl VAT, shipping, coupons).
3. Separate new/refurb/used listings.
4. Check marketplace seller quality and warranty policy.
5. Keep timestamp of capture for each row.

## Why USD normalization

USD is a neutral comparison anchor for multi-market products.
The script converts local prices with latest FX rates and reports:

- ranked offers
- delta vs best offer
- overall spread (%)
