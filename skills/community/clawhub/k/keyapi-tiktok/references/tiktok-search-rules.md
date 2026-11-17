# TikTok Search Module Rules

## 1. Module Scope

Use this module for keyword, image, URL, and resolver-style TikTok searches before routing to product, seller, creator, video, live, hashtag, or music workflows.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Realtime keyword search by entity
3. Product image search and pagination
4. Identifier and link resolution
5. Analytics search fallback

## 2. Realtime keyword search by entity

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/live-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/hashtag-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/music-search.md`
- Purpose: Find current public entities from a keyword.

### Best Suited For

- current product lookup
- creator lookup by handle/keyword
- video examples by keyword
- active/recent live search
- hashtag or music seed resolution

### Routing Rules

- Use the dedicated realtime search endpoint for the target entity when the user asks to search.
- Preserve returned IDs for downstream detail, comments, trend, or related-entity calls.
- Do not use Analytics search when the user clearly asks for latest/current public results.

## 3. Product image search and pagination

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-photo-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-photo-search-page.md`
- Purpose: Search TikTok Shop products from an image and paginate additional visual matches.

### Best Suited For

- find similar products from an image
- visual product sourcing
- image-driven product discovery

### Routing Rules

- Use initial photo search first; it does not paginate directly.
- Preserve image_uri and box_detection from the initial response for page requests.
- Prefer scripts/keyapi-api.mjs with --image-file instead of inline base64 JSON.

## 4. Identifier and link resolution

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-id.md`
- Purpose: Resolve canonical product identifiers before detail workflows.

### Best Suited For

- product share-link handling
- preparing detail/report calls

### Routing Rules

- Use product ID extraction when the user gives a product share link.
- Do not guess IDs from URLs or display text.

## 5. Analytics search fallback

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/search-analytics.md`
- Purpose: Search across Analytics/EchoTik products, shops, and influencers when the task needs enriched commerce metrics.

### Best Suited For

- cross-entity commerce discovery
- broad Analytics/EchoTik search
- fallback when entity-specific Analytics list is not enough

### Routing Rules

- Use this when the user asks for Analytics/EchoTik search-box style behavior or cross-entity discovery.
- For precise product, seller, or influencer research, prefer the dedicated list/ranking endpoints first.
- Enrich selected results through the relevant detail module.

## 6. Common Workflows

- Keyword search: dedicated realtime search -> selected detail module.
- Image search: product photo search -> photo search page -> product detail/list enrichment.
- Share link: product ID resolver -> product detail/trend/related entities.
- Cross-entity Analytics search: search analytics -> product/seller/influencer module enrichment.
