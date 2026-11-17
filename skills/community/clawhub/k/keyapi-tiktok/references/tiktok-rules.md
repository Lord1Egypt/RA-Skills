# TikTok Rules

Use this file for TikTok platform-level routing boundaries. Use module files for scenario-specific workflows.

## Data Source Standard

- Endpoint titles containing `Analytics` and docs paths ending in `-analytics` represent EchoTik analytics data.
- Endpoints without `Analytics` are realtime/current interfaces.
- Ask a short mode question when realtime and Analytics variants both exist and the user does not specify freshness versus historical depth.

## Scenario Module Routing

- Use `tiktok-search-rules.md` for keyword search, image search, share-link/product ID resolution, and Analytics cross-entity search.
- Use `tiktok-product-rules.md` for product discovery, categories, product detail, reviews, trends, rankings, and product-related creators/videos/live sessions.
- Use `tiktok-seller-rules.md` for shop/seller discovery, detail, products, trends, rankings, and shop-related creators/videos/live sessions.
- Use `tiktok-influencer-rules.md` for creator discovery, detail, rankings, trends, videos, products, livestreams, follower graph, region, and milestones.
- Use `tiktok-video-rules.md` for video detail, video discovery, comments, captions, trends, downloads, covers, and video-product attribution.
- Use `tiktok-live-rules.md` for realtime live search/detail and Analytics live relationships for creators, products, and shops.
- Use `tiktok-intelligence-rules.md` for ads, keyword insights, top products, trending videos, hashtags, and music.
- Use `tiktok-content-rules.md` and `tiktok-shop-rules.md` only as composite routers when the user request is broad and needs disambiguation.

## Identifier Discipline

- Preserve product_id, seller/shop identifiers, creator user_id/unique_id/sec_uid, video_id, room_id, hashtag_id, music IDs, image_uri, and box_detection exactly as returned.
- Resolve identifiers through documented resolver/search endpoints before detail or related-entity calls.
- Do not infer REST paths or IDs from docs URLs, display titles, or previous 404 responses.

## Output Guidance

- State whether the workflow used realtime data, Analytics/EchoTik data, or both.
- For reports, group findings by entity baseline, performance/trend evidence, relationship attribution, and limitations.
- Keep observed API facts separate from analytical inference.
