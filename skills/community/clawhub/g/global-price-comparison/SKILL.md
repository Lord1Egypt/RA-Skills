---
name: global-price-comparison
description: Discover and compare the same product across multiple countries and source types (official stores, marketplaces, retailers) using Brave and/or Tavily web search, then normalize all offers to USD for ranking and spread analysis. Use when users ask for global product price comparison, cross-country official price checks, or cheapest-market analysis.
---

# Global Price Comparison

Use this skill to run a **global same-product price scan** and output a **USD-normalized comparison**.

## Quick start

```bash
# 1) Create a starter CSV template
python scripts/global_price_compare.py template --out /tmp/offers.csv

# 2) (Optional) discover candidate links by country/source type
# Uses Brave and Tavily when available (BRAVE_API_KEY / TAVILY_API_KEY)
python scripts/global_price_compare.py discover \
  --product "iPhone 16 Pro 256GB" \
  --countries US,JP,DE,UK \
  --source-types official_store,marketplace,electronics_retailer \
  --engine all \
  --out /tmp/discover.json

# 3) Fill /tmp/offers.csv with verified offers, then compare
python scripts/global_price_compare.py compare \
  --input /tmp/offers.csv \
  --format markdown
```

## Workflow

1. Define exact product variant (model/storage/spec).
2. Run `discover` to get candidate URLs by market and source type.
3. Add verified offers to CSV (`product,country,currency,source_type,source_name,price,url`).
4. Run `compare` to normalize all prices to USD and rank best/worst.
5. Share markdown/JSON/CSV output.

## Commands

### Template

```bash
python scripts/global_price_compare.py template --out /tmp/offers.csv
```

### Discover candidate links

```bash
python scripts/global_price_compare.py discover \
  --product "PlayStation 5 Slim" \
  --countries US,JP,DE \
  --source-types official_store,marketplace,electronics_retailer \
  --engine all \
  --count 3 \
  --format markdown
```

Notes:
- `discover` supports `--engine brave|tavily|all` (default `all`).
- For `all`, it uses **Brave first** and only falls back to Tavily when Brave fails or returns no results.
- Set one or both keys as needed: `BRAVE_API_KEY`, `TAVILY_API_KEY`.
- Source types are intentionally generic (not local-store specific).

### Compare offers in USD

```bash
python scripts/global_price_compare.py compare \
  --input /tmp/offers.csv \
  --format markdown \
  --out /tmp/comparison.csv
```

Outputs include:
- ranked offers by USD price
- delta vs best offer
- spread in USD and %

## Defaults

Default country set:
- `US, UK, JP, DE, FR, CA, AU, SG, HK, TW`

Default source types:
- `official_store`
- `marketplace`
- `electronics_retailer`
- `general_retailer`

## Data/quality guardrails

Before finalizing recommendations:
- confirm same model/variant
- confirm tax/shipping basis consistency
- separate new vs refurbished/used
- keep URL + timestamp evidence

Detailed schema + guardrails:
- `references/data-shape-and-source-types.md`

## Resources

- Script: `scripts/global_price_compare.py`
- Reference: `references/data-shape-and-source-types.md`
