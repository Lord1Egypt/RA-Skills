# TikTok Product Module Rules

## 1. Module Scope

Use this module for TikTok Shop product discovery, category resolution, product detail, reviews, trends, rankings, and product-related creators/videos/livestreams.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Category and product discovery
3. Realtime product lookup
4. Product reviews and buyer evidence
5. Product trend and relationship attribution

## 2. Category and product discovery

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/category-primary-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/category-secondary-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/category-tertiary-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-list-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-ranking-analytics.md`
- Purpose: Find products through category, filters, rankings, or Analytics/EchoTik commerce metrics.

### Best Suited For

- winning-product research
- category sourcing
- product ranking/growth scans
- GMV/sales-based product discovery

### Routing Rules

- Resolve category levels progressively before category-sensitive product calls.
- Use product list Analytics for filtered discovery and product ranking Analytics for leaderboard-style questions.
- Analytics endpoints represent EchoTik analytics data, not realtime public-state lookup.

## 3. Realtime product lookup

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-detail.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-detail-app.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-id.md`
- Purpose: Retrieve current product state or resolve products from search/share links.

### Best Suited For

- current product detail
- SKU/layout/current marketplace state
- product share link resolution
- keyword product lookup

### Routing Rules

- Use realtime search when the user asks for current products by keyword.
- Resolve product ID from share link before detail calls.
- Use app detail when layout/SKU/seller/logistics/recommendation fields are the target.

## 4. Product reviews and buyer evidence

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-reviews.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-reviews-analytics.md`
- Purpose: Retrieve realtime or Analytics/EchoTik review evidence.

### Best Suited For

- buyer feedback checks
- review distribution analysis
- product risk review
- comment/review sampling

### Routing Rules

- Ask or infer whether the user needs current reviews or Analytics/EchoTik aggregated history.
- Do not mix realtime review samples with Analytics review aggregates without labeling the source.

## 5. Product trend and relationship attribution

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-detail-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-trends-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-creators-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-videos-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-livestreams-analytics.md`
- Purpose: Explain product performance through historical trends and traffic sources.

### Best Suited For

- product performance reports
- creator/video/live attribution
- sales and GMV trend explanation
- commerce funnel evidence

### Routing Rules

- Use product detail Analytics for rich product baseline.
- Use trends when the user asks about movement over time.
- Use related creators/videos/livestreams only when attribution or traffic-source evidence is needed.

## 6. Common Workflows

- Winning product: category resolution -> product list/ranking Analytics -> selected product detail/trends.
- Current product lookup: product search or product ID resolver -> product detail/app detail -> reviews if requested.
- Product report: detail Analytics -> trends -> reviews -> related creators/videos/livestreams.
