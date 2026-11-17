# TikTok Intelligence Module Rules

## 1. Module Scope

Use this module for TikTok ads, keyword insights, top product insights, trending hashtags, trending music, and trending videos.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Ads and creative intelligence
3. Keyword and product market intelligence
4. Trending content surfaces

## 2. Ads and creative intelligence

- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/insights-ads.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/insights-ads-detail.md`
- Purpose: Find and inspect top-performing TikTok ads.

### Best Suited For

- ad creative research
- industry ad benchmarking
- ad detail analysis

### Routing Rules

- Use insights ads for discovery.
- Use ads detail only after selecting a specific ad.
- Report creative/performance fields returned by the API without inventing missing metrics.

## 3. Keyword and product market intelligence

- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/insights-keyword.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/insights-products.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/insights-product-detail.md`
- Purpose: Understand keyword demand and top product/category signals.

### Best Suited For

- keyword opportunity analysis
- top product/category insights
- market research

### Routing Rules

- Use keyword insights for topic/product demand questions.
- Use top products insights for product category ranking.
- Use product insight detail after selecting a top product/category target.

## 4. Trending content surfaces

- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/trending-videos.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/trending-hashtags.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/trending-hashtag-detail.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/trending-music.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/intelligence/trending-music-detail.md`
- Purpose: Retrieve current trending videos, hashtags, and music signals.

### Best Suited For

- trend monitoring
- viral content research
- hashtag/music opportunity review

### Routing Rules

- Use list endpoints for discovery and detail endpoints only after selecting a target.
- Use video, search, or content modules to enrich selected trend examples.

## 5. Common Workflows

- Ad research: insights ads -> ad detail for selected items.
- Keyword/product research: keyword insights or top products -> product detail module as needed.
- Trend scan: trending videos/hashtags/music -> detail/enrichment for selected targets.
