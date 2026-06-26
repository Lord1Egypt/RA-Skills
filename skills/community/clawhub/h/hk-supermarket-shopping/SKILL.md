---
id: hk-supermarket-shopping
name: HK Supermarket Shopping
description: Real-time price comparison for Hong Kong supermarkets using the Consumer Council's daily pricewatch. For any product query, returns the cheapest supermarket, price, and how many you could buy with $100. The skill auto-detects query language (English or Chinese) and responds in the same language. No authentication required; data downloads automatically on first use.
version: 1.2.3
author: Steven Ho
license: MIT
tags:
  - shopping
  - hong-kong
  - price-comparison
  - consumer
  - multilingual
source: https://github.com/StevenHo1394/openclaw/tree/main/skills/hk-supermarket-shopping

tools:
  - name: price_lookup
    description: Query Hong Kong supermarket prices. Accepts product names, brands, or categories in English or Chinese. Returns a concise plain-text answer with the cheapest option and budget quantity.
    parameters:
      type: object
      properties:
        query:
          type: string
          description: Product name, brand, or category to search. Max 200 characters. Examples: "Coke Zero", "milk", "雞蛋", "橄欖油", "frozen shrimp"
          maxLength: 200
      required: [query]
    returns:
      type: string
      description: Plain-text, single-line answer. Example: "Overall cheapest: PARKNSHOP - Coca-Cola Zero Sugar 500ml ($9.50). With $100 you can buy 10 items (remaining $5.00)."
    example:
      input: "Coke Zero"
      output: "Overall cheapest: PARKNSHOP - Coca-Cola Zero Sugar 500ml ($9.50). With $100 you can buy 10 items (remaining $5.00)."

requirements:
  - command: python3
    description: Python 3.8+ runtime (standard library only; no external binaries required)

capabilities:
  offline_after_initial: true
  auto_refresh: daily
  multilingual: true
  secure: true

example_queries:
  - price lookup: "How much is milk?"
  - brand search: "Coke Zero price"
  - Chinese: "雞蛋", "橄欖油"
  - category: "frozen seafood", "olive oil"

dependencies: []
conflicts: []
priority: 100
enabled: true

---

# HK Supermarket Shopping (v1.2.3)

Real-time price lookup for Hong Kong supermarkets using the Consumer Council's daily pricewatch. The `price_lookup` tool searches for products and returns the cheapest option, price, and how many you can buy with $100. Language (English/Chinese) is auto-detected from your query.

## Quick Reference

| Query | Expected Result |
|-------|-----------------|
| `"Coke Zero"` | `Overall cheapest: PARKNSHOP - Coca-Cola Zero Sugar 500ml ($9.50). With $100 you can buy 10 items (remaining $5.00).` |
| `"milk"` | Similar format with cheapest supermarket and price |
| `"雞蛋"` | Response in Chinese: `整體最平：...` |

## Setup

1. Install the skill by copying the folder to OpenClaw's skills/ directory.
2. No configuration required.
3. The skill downloads the latest pricewatch CSV on first use and stores it in `data/`.
4. Data is automatically housekept; only today's file is kept (older than 1 day removed).
5. All downloads use SSL verification; no insecure proxies.

## Technical Details

- **Data Source**: Consumer Council pricewatch (English CSV) – updated daily.
- **Retention**: 1 day (auto housekeeping).
- **Offline Support**: Works after initial download.
- **Multilingual**: Auto-detects query language and responds accordingly.
- **Security**: Input length limited to 200 characters, SSL-verified downloads, no command injection vulnerabilities, no external binary dependencies.
- **Runtime**: Pure Python – uses `urllib` from standard library (no `curl` or other external tools).
