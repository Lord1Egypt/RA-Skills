# TikTok Seller And Shop Module Rules

## 1. Module Scope

Use this module for TikTok Shop seller/shop discovery, shop detail, shop products, trends, rankings, and shop-related creators/videos/livestreams.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Seller discovery and ranking
3. Shop detail and trend
4. Shop product inventory
5. Shop traffic sources

## 2. Seller discovery and ranking

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-list-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-ranking-analytics.md`
- Purpose: Find shops/sellers by filters, category, GMV, product count, rankings, or commerce performance.

### Best Suited For

- seller discovery
- shop benchmarking
- top seller/ranking requests
- local/cross-border style shop research when documented

### Routing Rules

- Use shop list Analytics for filtered seller discovery.
- Use shop ranking Analytics for leaderboard-style seller questions.
- Label these as Analytics/EchoTik data in the final answer.

## 3. Shop detail and trend

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-detail-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-trends-analytics.md`
- Purpose: Retrieve seller baseline and historical performance movement.

### Best Suited For

- seller profile reports
- shop GMV/sales trend checks
- shop performance benchmarking

### Routing Rules

- Use shop detail Analytics when a seller/shop is known.
- Use shop trends when the user asks how the shop changed over time.
- If detail is empty, treat it as Analytics coverage gap, not proof the shop does not exist.

## 4. Shop product inventory

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-products.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-products-analytics.md`
- Purpose: Retrieve current or Analytics/EchoTik shop product lists.

### Best Suited For

- current catalog checks
- historical product performance by shop
- shop assortment review

### Routing Rules

- Use realtime shop products for current catalog state.
- Use shop products Analytics for performance-enriched inventory.
- If the user says product list without freshness preference, ask current versus Analytics/EchoTik.

## 5. Shop traffic sources

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-creators-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-videos-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-livestreams-analytics.md`
- Purpose: Trace creators, videos, and live sessions associated with a shop.

### Best Suited For

- shop attribution reports
- creator partner analysis
- video/live traffic source review

### Routing Rules

- Use only after the shop is identified.
- Enrich selected creators/videos/live rooms through influencer, video, or live modules when needed.

## 6. Common Workflows

- Seller discovery: shop list/ranking Analytics -> shop detail/trends.
- Catalog review: shop detail -> realtime or Analytics shop products.
- Shop report: shop detail -> trends -> products -> creators/videos/livestreams as approved.
