---
name: HashCats Amazon Intelligence
description: x402 pay-per-call API for Amazon product search, filtering, ranking, detailed extraction, and one-shot "best products" recommendations. No API keys required — agents pay in USDC automatically.
homepage: https://api.hashcats.io
version: 0.1.0
tags: [amazon, shopping, product-intelligence, x402, ecommerce, scraping, agent-tool]
emoji: "🛒"
requires:
  env: []   # None required — fully x402-native
---

# HashCats Amazon Intelligence Skill

## Overview
This skill teaches OpenClaw agents how to use the **HashCats API**[](https://api.hashcats.io) — a fast, structured Amazon product intelligence service.

It is **x402-native**: agents detect the 402 response, pay a tiny USDC amount instantly via their wallet, and continue. No keys, no subscriptions.

## Core Capabilities
- **Natural language search** — POST /search (e.g. "noise cancelling headphones under 200")
- **Filter** — POST /filter on a list of products (stock, price, rating, shipping, relevance, etc.)
- **Rank** — POST /rank by relevance, lowest_price, fastest_shipping, best_reviews, or best_value
- **Product details** — POST /product-details (single URL or up to 10 URLs) with full structured data (reviews, pricing, offers, warranty, etc.)
- **One-shot best products** — POST /best (search + filter + rank in one call with your priorities)

All endpoints return clean, structured JSON perfect for agent reasoning.

## Recommended Usage Patterns (what agents should say/do)
- For quick recommendations: Use `/best` with a query and priorities (max_price, min_rating, min_review_count, ship_within_days).
- For composable workflows: `/search` → `/filter` → `/rank` → optionally `/product-details` on top results.
- For deep research: Pull details from specific product URLs.

Example agent flows:
- "Find the best noise cancelling headphones under $200 that ship fast and have good reviews using HashCats"
- "Get full details on https://www.amazon.com/dp/B0GLNV4LJ9"
- "Search Amazon for wireless earbuds, filter in-stock non-sponsored ones with at least 4.5 stars, then rank by best_value"

## Setup & Prerequisites
1. Make sure the official x402 skill is installed (it handles automatic payment on 402 responses).
2. No extra configuration needed — the skill discovers the base URL and x402 flow automatically.

## Pricing (what agents will pay)
- /search, /filter, /rank: ~$0.003 each
- /product-details: ~$0.010
- /best (one-shot): ~$0.020

Prices are micropayments in USDC on Base Sepolia (or mainnet when enabled).

## Documentation
- Live docs: https://api.hashcats.io/docs
- OpenAPI: https://api.hashcats.io/openapi.json
- Base URL: https://api.hashcats.io

## Tips for Best Results
- Start with `/best` for most shopping/recommendation tasks.
- Use `/product-details` when you need histograms, warranty info, offer details, or multi-URL extraction.
- Combine with other shopping or reasoning skills for full agent workflows.

Agents using this skill get reliable, structured Amazon data without scraping headaches or rate-limit drama.