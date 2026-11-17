# TikTok Live Module Rules

## 1. Module Scope

Use this module for TikTok live stream search/detail and Analytics/EchoTik live relationships for creators, products, and shops.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Realtime live search and detail
3. Influencer live history
4. Product and shop live attribution

## 2. Realtime live search and detail

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/live-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/live-detail.md`
- Purpose: Find live sessions and retrieve current live room details.

### Best Suited For

- active/recent live lookup
- live room detail
- host/product context during live
- fresh live commerce checks

### Routing Rules

- Use live search for keyword-based live discovery.
- Use live detail when room_id or live target is known.
- Realtime live detail is freshness-sensitive; missing data may mean the room is no longer live or not available.

## 3. Influencer live history

- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/livestreams-analytics.md`
- Purpose: Retrieve historical livestream records for a creator from Analytics/EchoTik data.

### Best Suited For

- creator live history
- live GMV/viewer analysis
- creator live-commerce evaluation

### Routing Rules

- Use after creator identity is known.
- Label results as Analytics/EchoTik historical data.
- Enrich creator baseline through influencer detail if needed.

## 4. Product and shop live attribution

- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/product-livestreams-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/shop/shop-livestreams-analytics.md`
- Purpose: Trace live sessions associated with products or shops.

### Best Suited For

- product live traffic source analysis
- shop livestream performance review
- live commerce attribution

### Routing Rules

- Use product livestreams after product ID is known.
- Use shop livestreams after seller/shop ID is known.
- Enrich selected live rooms or related products/shops only when the user needs detail.

## 5. Common Workflows

- Live lookup: live search -> live detail.
- Creator live report: influencer detail -> influencer livestreams Analytics.
- Product/shop live attribution: product/shop detail -> livestreams Analytics -> selected live detail if current.
