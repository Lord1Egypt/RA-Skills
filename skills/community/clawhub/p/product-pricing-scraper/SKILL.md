---
name: product-pricing-scraper
description: Scrape and compare product prices across e-commerce sites. Use when the user needs to extract pricing data, track price changes, compare prices across retailers, or monitor competitor pricing. Supports Amazon, eBay, Walmart, and generic product pages. Outputs structured JSON/CSV with price normalization and currency conversion.
---

# Product Pricing Scraper

Scrape, normalize, and compare product prices across e-commerce sites.

## Quick Start

```
"Compare prices for [product name] across Amazon, eBay, and Walmart"
"Scrape pricing from [URL]"
"Track price changes for [product]"
```

## Workflow

1. **Identify target** — accept product name (search across sites) or specific URL(s)
2. **Scrape** — use `scripts/scrape_prices.py` for each target
3. **Normalize** — strip currency symbols, unify units, convert currencies if needed
4. **Compare** — rank by price, flag outliers, compute average/median
5. **Output** — JSON or CSV via `--format` flag

## Scraping Strategies

### Static pages (most product listings)
Use `web_fetch` + cheerio-style parsing. No browser needed.

### Dynamic pages (JS-rendered prices)
Use the `browser` tool with snapshot + act to navigate and extract.

### Anti-bot considerations
- Randomize delays (2-5s between requests)
- Rotate User-Agent strings
- Respect robots.txt — check before scraping
- Limit concurrent requests per domain

## Price Normalization

- Strip currency symbols and whitespace
- Convert per-unit pricing (e.g., "$2.99/oz" → unit price)
- Handle price ranges (take lowest)
- Flag "was/now" discounted prices — record both

## Output Schema

```json
{
  "query": "product name or url",
  "scraped_at": "ISO-8601",
  "results": [
    {
      "source": "amazon",
      "url": "https://...",
      "title": "Product Title",
      "price": 29.99,
      "currency": "USD",
      "unit_price": null,
      "original_price": 39.99,
      "in_stock": true,
      "rating": 4.5,
      "review_count": 1234
    }
  ],
  "summary": {
    "lowest": { "source": "amazon", "price": 29.99 },
    "highest": { "source": "walmart", "price": 34.99 },
    "average": 32.49,
    "median": 31.99
  }
}
```

## Scripts

- **`scripts/scrape_prices.py`** — main scraper: accepts product name or URL list, outputs structured JSON
- See **`references/selectors.md`** for site-specific CSS selectors

## Ethics & Compliance

- Respect robots.txt and rate limits
- Do not scrape behind login walls without explicit permission
- Do not collect personal data
- Check site ToS before bulk scraping
