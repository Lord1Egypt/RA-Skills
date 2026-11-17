# TikTok Influencer Module Rules

## 1. Module Scope

Use this module for TikTok creator/influencer discovery, profile detail, Analytics/EchoTik lists/rankings, videos, products, live history, follower graph, region, milestones, and QR code.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Creator search and profile detail
3. Creator discovery, ranking, and trends
4. Creator content, products, live, and audience context
5. Follower and following graph

## 2. Creator search and profile detail

- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/detail.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/detail-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/qrcode.md`
- Purpose: Find creators and retrieve realtime or Analytics/EchoTik profile records.

### Best Suited For

- creator lookup
- profile validation
- creator report baseline
- QR code generation

### Routing Rules

- Use realtime search/detail for current public creator lookup.
- Use detail Analytics for historical/commercial creator context.
- Ask realtime versus Analytics/EchoTik when the user asks for creator detail without freshness preference.

## 3. Creator discovery, ranking, and trends

- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/list-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/ranking-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/trends-analytics.md`
- Purpose: Discover and benchmark creators through Analytics/EchoTik data.

### Best Suited For

- creator discovery
- GMV/follower/engagement ranking
- creator trend analysis
- historical benchmarking

### Routing Rules

- Use influencer list Analytics for filtered discovery.
- Use ranking Analytics for leaderboard-style questions.
- Use trends Analytics when the user asks how a creator changed over time.

## 4. Creator content, products, live, and audience context

- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/videos.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/videos-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/products-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/livestreams-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/region.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/milestones.md`
- Purpose: Retrieve creator videos, promoted products, livestream history, audience region, and growth milestones.

### Best Suited For

- creator content audit
- promoted product review
- creator live history
- audience region or milestone checks

### Routing Rules

- Use realtime videos for current video lists and Analytics videos for enriched performance.
- Use products/livestreams Analytics for commerce attribution.
- Use region/milestones only when the user asks for audience geography or growth markers.

## 5. Follower and following graph

- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/followers.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/influencer/following.md`
- Purpose: Retrieve follower or following lists for a creator.

### Best Suited For

- relationship sampling
- audience/account graph checks
- following/follower lookup

### Routing Rules

- Use only when graph lists are explicitly requested.
- Enrich selected related accounts only if the user asks for profile detail.

## 6. Common Workflows

- Creator discovery: search/list/ranking -> selected detail -> videos/products/trends.
- Creator report: detail mode choice -> trends -> videos/products/livestreams -> region/milestones if requested.
- Creator graph: detail -> followers/following -> selected enrichment.
