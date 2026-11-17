# Scenario Cards

Use these scenario cards to translate natural-language TikTok requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

creators, products, shops, sellers, categories, videos, comments, captions, hashtags, music, live streams, ads, keywords, trends, and market-intelligence signals

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Search, image lookup, ID resolution, and cross-entity discovery | `tiktok-search-rules.md` | /tiktok/shop/, /tiktok/content/, /tiktok/influencer/ |
| Product discovery, category resolution, detail, reviews, ranking, trend, and attribution | `tiktok-product-rules.md` | /tiktok/shop/ |
| Shop/seller discovery, detail, products, ranking, trend, and traffic sources | `tiktok-seller-rules.md` | /tiktok/shop/ |
| Creator/influencer discovery, detail, rankings, trends, content, products, live history, and graph | `tiktok-influencer-rules.md` | /tiktok/influencer/ |
| Video discovery, detail, comments, captions, trends, assets, and product links | `tiktok-video-rules.md` | /tiktok/content/ |
| Live stream lookup and live commerce attribution | `tiktok-live-rules.md` | /tiktok/content/, /tiktok/shop/, /tiktok/influencer/ |
| Ads, keyword, top product, trending hashtag, music, and video intelligence | `tiktok-intelligence-rules.md` | /tiktok/intelligence/ |

## 1. Search and resolve TikTok entities

- User intent: Start from a keyword, image, share link, handle, or ambiguous input and resolve the right entity before detail calls.
- Primary entity: search target / resolver
- Ask for: keyword, image file/URL, share link, region, entity type, and whether current or Analytics/EchoTik results are needed.
- Default workflow: Use dedicated realtime search or resolver endpoints first; use Analytics cross-entity search only for enriched commerce discovery; route selected results to product, seller, creator, video, live, or intelligence modules.
- Reference module: `tiktok-search-rules.md`
- Endpoint shortlist:
  - [Product Search](https://docs.keyapi.ai/en/tiktok/shop/product-search.md) - Search TikTok Shop products in real time by keyword. Use offset for subsequent pages.
  - [Product Image Search](https://docs.keyapi.ai/en/tiktok/shop/product-photo-search.md) - Use this endpoint together with Product Image Search Page - Real-Time API. This endpoint does not accept pagination parameters. Each request returns 6 different random products in e_com_items. To retrieve more product data, record image_uri and box_detection from the photo_search object in this resp…
  - [Product Image Search Page](https://docs.keyapi.ai/en/tiktok/shop/product-photo-search-page.md) - Use this endpoint together with Product Image Search - Real-Time API. Pass image_uri and box_detection from the photo_search object returned by Product Image Search to retrieve additional paginated results.
  - [Get Product ID from Share Link](https://docs.keyapi.ai/en/tiktok/shop/product-id.md) - Extract the TikTok Shop product ID from a product share link or URL.
  - [Search Influencers](https://docs.keyapi.ai/en/tiktok/influencer/search.md) - Search TikTok influencers by keyword. Returns a list of matching creator profiles with follower counts, engagement rates, and basic metrics.
  - [Search Videos](https://docs.keyapi.ai/en/tiktok/content/video-search.md) - Search TikTok videos by keyword, returning a list of matching videos with view counts, engagement metrics, and creator info.
  - [Search Live Streams](https://docs.keyapi.ai/en/tiktok/content/live-search.md) - Search for active or recent TikTok live streams by keyword, returning matching streams with viewer counts and host information.
  - [Search Hashtags](https://docs.keyapi.ai/en/tiktok/content/hashtag-search.md) - Search TikTok hashtags by keyword, returning matching tags with video counts and usage statistics.
  - [Search Music](https://docs.keyapi.ai/en/tiktok/content/music-search.md) - Search TikTok music tracks by keyword, returning matching audio with usage counts and associated video data.
  - [General Search (Analytics)](https://docs.keyapi.ai/en/tiktok/content/search-analytics.md) - Perform a general search across TikTok Shop using the analytics dataset, returning products, shops, and influencers matching the query with rich performance metrics.

## 2. Find and analyze products

- User intent: Discover winning products, inspect current product detail, review buyer feedback, or explain product performance.
- Primary entity: product / category / review / attribution
- Ask for: keyword, product ID/share link, category, image, region, ranking metric, and report sections.
- Default workflow: Resolve category/product first, then use realtime detail for current state or Analytics/EchoTik endpoints for ranking, trend, reviews, and traffic-source attribution.
- Reference module: `tiktok-product-rules.md`
- Endpoint shortlist:
  - [Primary Categories (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/category-primary-analytics.md) - Retrieve the list of top-level product categories available in TikTok Shop.
  - [Secondary Categories (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/category-secondary-analytics.md) - Retrieve secondary product categories under a given primary category in TikTok Shop.
  - [Tertiary Categories (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/category-tertiary-analytics.md) - Retrieve third-level product subcategories under a given secondary category in TikTok Shop.
  - [Product List (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-list-analytics.md) - Search and filter TikTok Shop products using analytics data with rich metrics including sales volume, GMV, review counts, and historical trend data.
  - [Product Ranking (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-ranking-analytics.md) - Retrieve ranked lists of TikTok Shop products by sales volume, GMV, or other metrics, computed from large-scale analytics data.
  - [Get Product Detail](https://docs.keyapi.ai/en/tiktok/shop/product-detail.md) - Retrieve real-time product details from TikTok Shop, including title, price, inventory, ratings, and seller information.
  - [Product Detail (App)](https://docs.keyapi.ai/en/tiktok/shop/product-detail-app.md) - Retrieve real-time TikTok Shop product details from the new app endpoint, including product layout, SKU, seller, logistics, review, and recommendation data.
  - [Product Detail (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-detail-analytics.md) - Retrieve comprehensive analytics data for one or more TikTok Shop products, including historical sales trends, associated creator data, and detailed performance metrics.
  - [Get Product Reviews](https://docs.keyapi.ai/en/tiktok/shop/product-reviews.md) - Retrieve customer reviews for a TikTok Shop product, including ratings, review text, and buyer information.
  - [Product Reviews (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-reviews-analytics.md) - Retrieve aggregated customer reviews for a TikTok Shop product from the analytics dataset, with historical review data and rating distributions.
  - [Product Trends (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-trends-analytics.md) - Retrieve historical trend snapshots for a TikTok Shop product, showing sales volume curves, GMV changes, and view trends over time.
  - [Product Creators (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-creators-analytics.md) - Retrieve the list of TikTok creators who have promoted a specific product, with performance metrics including views, sales, and GMV generated per creator.
  - [Product Videos (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-videos-analytics.md) - Retrieve the list of TikTok videos associated with a product, including view counts, engagement metrics, and conversion data.
  - [Product Livestreams (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-livestreams-analytics.md) - Retrieve the list of TikTok livestreams in which a specific product was promoted, including viewer counts and GMV data.

## 3. Evaluate shops and sellers

- User intent: Find, benchmark, or report on TikTok Shop sellers and their product inventory or traffic sources.
- Primary entity: shop / seller
- Ask for: seller/shop identifier, market/category, ranking metric, product section, trend section, and traffic-source sections.
- Default workflow: Use shop list/ranking Analytics for discovery, shop detail/trends for baseline and movement, realtime or Analytics products for inventory, and related creators/videos/live for attribution.
- Reference module: `tiktok-seller-rules.md`
- Endpoint shortlist:
  - [Shop List (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-list-analytics.md) - Search and filter TikTok Shop sellers using analytics data, with metrics including GMV, product count, and historical sales performance.
  - [Shop Ranking (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-ranking-analytics.md) - Retrieve ranked lists of TikTok Shop sellers by GMV, product count, or other metrics, computed from large-scale analytics data.
  - [Shop Detail (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-detail-analytics.md) - Retrieve comprehensive analytics data for a TikTok Shop seller, including historical GMV, product portfolio, associated creators, and performance trends.
  - [Shop Trends (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-trends-analytics.md) - Retrieve historical trend snapshots for a TikTok Shop, showing GMV growth, product count changes, and sales volume over time.
  - [Get Shop Products](https://docs.keyapi.ai/en/tiktok/shop/shop-products.md) - Retrieve the real-time product listing for a TikTok Shop seller, including current inventory, prices, and product status.
  - [Shop Products (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-products-analytics.md) - Retrieve the analytics-enriched product list for a TikTok Shop seller, with historical sales data and performance metrics for each product.
  - [Shop Creators (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-creators-analytics.md) - Retrieve the list of TikTok creators affiliated with a shop, including their contribution to GMV, video count, and commission data.
  - [Shop Videos (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-videos-analytics.md) - Retrieve the list of TikTok videos promoting products from a specific shop, with view counts, engagement data, and sales conversion metrics.
  - [Shop Livestreams (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-livestreams-analytics.md) - Retrieve historical livestream records for a TikTok Shop, including viewer counts, GMV generated, and product sales data from each session.

## 4. Find and benchmark creators

- User intent: Find creators for a niche/product/category or evaluate creator commerce performance.
- Primary entity: creator / influencer
- Ask for: keyword, handle/user ID, market, category/product context, mode preference, and desired sections.
- Default workflow: Use realtime search/detail for current lookup; use Analytics list/ranking/trends for discovery and benchmarking; enrich with videos, products, live history, region, milestones, or graph only when useful.
- Reference module: `tiktok-influencer-rules.md`
- Endpoint shortlist:
  - [Search Influencers](https://docs.keyapi.ai/en/tiktok/influencer/search.md) - Search TikTok influencers by keyword. Returns a list of matching creator profiles with follower counts, engagement rates, and basic metrics.
  - [Get Influencer Detail](https://docs.keyapi.ai/en/tiktok/influencer/detail.md) - Retrieve real-time profile information for a TikTok influencer by unique ID, including follower count, bio, video count, and engagement data.
  - [Influencer Detail (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/detail-analytics.md) - Retrieve comprehensive analytics data for one or more TikTok influencers, including historical follower growth, video performance metrics, product promotion data, and audience insights computed from extensive historical records.
  - [Influencer List (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/list-analytics.md) - Search and filter TikTok influencers using analytics data with rich multi-dimensional metrics including follower trends, engagement rates, sales performance, and historical data computed from a large-scale dataset.
  - [Influencer Ranking (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/ranking-analytics.md) - Retrieve ranked lists of TikTok influencers sorted by metrics such as follower count, GMV, and engagement rate, computed from large-scale analytics data.
  - [Influencer Trends (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/trends-analytics.md) - Retrieve historical trend snapshots for a TikTok influencer, showing follower growth curves, view trends, and engagement rate changes over time.
  - [Get Influencer Videos](https://docs.keyapi.ai/en/tiktok/influencer/videos.md) - Retrieve the latest video list for a TikTok influencer, including view counts, likes, comments, and shares for each video.
  - [Influencer Videos (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/videos-analytics.md) - Retrieve an analytics-enriched video list for a TikTok influencer, with historical performance metrics, product associations, and engagement trend data.
  - [Influencer Products (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/products-analytics.md) - Retrieve the list of products promoted by a TikTok influencer, with historical sales data, commission rates, and product performance metrics.
  - [Influencer Livestreams (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/livestreams-analytics.md) - Retrieve historical livestream records for a TikTok influencer, including viewer counts, GMV, and product sales data from past live sessions.
  - [Get Influencer Region](https://docs.keyapi.ai/en/tiktok/influencer/region.md) - Retrieve regional data for a TikTok influencer, including audience geographic distribution across countries and regions.
  - [Get Influencer Milestones](https://docs.keyapi.ai/en/tiktok/influencer/milestones.md) - Retrieve milestone and achievement data for a TikTok influencer, showing historical growth markers and key follower milestones.
  - [Get Influencer Followers](https://docs.keyapi.ai/en/tiktok/influencer/followers.md) - Retrieve the follower list for a TikTok influencer, with basic profile information for each follower.
  - [Get Influencer Following](https://docs.keyapi.ai/en/tiktok/influencer/following.md) - Retrieve the list of accounts a TikTok influencer is following, with basic profile information for each account.

## 5. Analyze videos and discussion

- User intent: Search videos, explain performance, inspect comments/captions, retrieve assets, or trace products attached to videos.
- Primary entity: video / comments / captions / assets
- Ask for: video URL/ID, keyword, mode preference, and whether comments, captions, trends, downloads, covers, or products are needed.
- Default workflow: Use video search/list/ranking for discovery, detail/trend endpoints for performance, comment keyword/comments/replies for audience reaction, captions for script, and video products for commerce attribution.
- Reference module: `tiktok-video-rules.md`
- Endpoint shortlist:
  - [Search Videos](https://docs.keyapi.ai/en/tiktok/content/video-search.md) - Search TikTok videos by keyword, returning a list of matching videos with view counts, engagement metrics, and creator info.
  - [Video List (Analytics)](https://docs.keyapi.ai/en/tiktok/content/video-list-analytics.md) - Search and filter TikTok videos using analytics data, with rich metrics including historical view counts, engagement rates, and product association data.
  - [Video Ranking (Analytics)](https://docs.keyapi.ai/en/tiktok/content/video-ranking-analytics.md) - Retrieve ranked lists of TikTok videos by views, engagement, or sales metrics, computed from large-scale analytics data.
  - [Get Video Detail](https://docs.keyapi.ai/en/tiktok/content/video-detail.md) - Retrieve real-time details for a TikTok video, including view count, likes, comments, shares, and full video metadata.
  - [Video Detail (Analytics)](https://docs.keyapi.ai/en/tiktok/content/video-detail-analytics.md) - Retrieve comprehensive analytics data for one or more TikTok videos, including historical performance metrics, associated products, and engagement trend data.
  - [Video Interaction Trends](https://docs.keyapi.ai/en/tiktok/content/video-trends.md) - Retrieve interaction trend data for a TikTok video over the past 14 days, showing daily changes in views, likes, and comments.
  - [Video Trends (Analytics)](https://docs.keyapi.ai/en/tiktok/content/video-trends-analytics.md) - Retrieve historical trend snapshots for a TikTok video, showing view count growth, like trends, and engagement rate changes over time.
  - [Get Video Comments](https://docs.keyapi.ai/en/tiktok/content/video-comments.md) - Retrieve the comment list for a TikTok video, including comment text, author info, and like counts.
  - [Get Video Comment Replies](https://docs.keyapi.ai/en/tiktok/content/video-comment-replies.md) - Retrieve reply threads for a specific comment on a TikTok video.
  - [Video Comment Keywords](https://docs.keyapi.ai/en/tiktok/content/video-comment-keywords.md) - Analyze the comment section of a TikTok video to extract frequently mentioned keywords and surface audience sentiment signals.
  - [Get Video Captions](https://docs.keyapi.ai/en/tiktok/content/video-captions.md) - Extract text content and subtitles from a TikTok video, useful for content analysis and transcription.
  - [Get Video Download URL](https://docs.keyapi.ai/en/tiktok/content/video-download-url.md) - Retrieve the download URL for a TikTok video, returning a watermark-free link where available.
  - [Batch Download Cover Images](https://docs.keyapi.ai/en/tiktok/content/covers-batch-download.md) - Download cover images for multiple TikTok videos in a single request, useful for bulk content processing and archiving.
  - [Video Products (Analytics)](https://docs.keyapi.ai/en/tiktok/content/video-products-analytics.md) - Retrieve the list of products featured in a TikTok video, with sales data and conversion metrics computed from analytics records.

## 6. Analyze live commerce

- User intent: Find live sessions, inspect current live detail, or evaluate creator/product/shop live history.
- Primary entity: live stream / live attribution
- Ask for: live keyword or room_id, creator/product/shop identifier, and whether current live state or Analytics/EchoTik history is needed.
- Default workflow: Use realtime live search/detail for current live lookup; use influencer/product/shop livestream Analytics for historical live-commerce attribution.
- Reference module: `tiktok-live-rules.md`
- Endpoint shortlist:
  - [Search Live Streams](https://docs.keyapi.ai/en/tiktok/content/live-search.md) - Search for active or recent TikTok live streams by keyword, returning matching streams with viewer counts and host information.
  - [Get Live Stream Detail](https://docs.keyapi.ai/en/tiktok/content/live-detail.md) - Retrieve real-time details for a TikTok live stream, including viewer count, host info, and products being promoted.
  - [Influencer Livestreams (Analytics)](https://docs.keyapi.ai/en/tiktok/influencer/livestreams-analytics.md) - Retrieve historical livestream records for a TikTok influencer, including viewer counts, GMV, and product sales data from past live sessions.
  - [Product Livestreams (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/product-livestreams-analytics.md) - Retrieve the list of TikTok livestreams in which a specific product was promoted, including viewer counts and GMV data.
  - [Shop Livestreams (Analytics)](https://docs.keyapi.ai/en/tiktok/shop/shop-livestreams-analytics.md) - Retrieve historical livestream records for a TikTok Shop, including viewer counts, GMV generated, and product sales data from each session.

## 7. Run market intelligence and trend research

- User intent: Understand ads, keywords, top products, trending videos, hashtags, or music in a market.
- Primary entity: ad / keyword / top product / trend
- Ask for: market, category or keyword, ranking metric, time window when documented, and top N.
- Default workflow: Use the narrowest intelligence endpoint for the target surface, then enrich selected ads/products/videos/hashtags/music through detail modules only when needed.
- Reference module: `tiktok-intelligence-rules.md`
- Endpoint shortlist:
  - [Top Ads Insights](https://docs.keyapi.ai/en/tiktok/intelligence/insights-ads.md) - Retrieve insights on top-performing TikTok ads, including ad creative types, engagement rates, and industry distribution.
  - [Top Ad Insights Detail](https://docs.keyapi.ai/en/tiktok/intelligence/insights-ads-detail.md) - Retrieve detailed insights for a specific top-performing TikTok ad, including creative analysis and performance metrics.
  - [Keyword Insights](https://docs.keyapi.ai/en/tiktok/intelligence/insights-keyword.md) - Retrieve market insights for a keyword on TikTok, including related products, creator activity, and consumer interest trends.
  - [Top Products Insights](https://docs.keyapi.ai/en/tiktok/intelligence/insights-products.md) - Retrieve insights on top-performing TikTok Shop products within a category, including sales rankings and growth metrics.
  - [Top Product Insights Detail](https://docs.keyapi.ai/en/tiktok/intelligence/insights-product-detail.md) - Retrieve detailed insights for a specific top-performing TikTok Shop product category, including trending items and sales data.
  - [Trending Videos](https://docs.keyapi.ai/en/tiktok/intelligence/trending-videos.md) - Retrieve the current list of trending videos on TikTok, with view counts, engagement metrics, and creator information.
  - [Trending Hashtags](https://docs.keyapi.ai/en/tiktok/intelligence/trending-hashtags.md) - Retrieve the current list of trending hashtags on TikTok, with video counts and growth metrics.
  - [Trending Hashtag Detail](https://docs.keyapi.ai/en/tiktok/intelligence/trending-hashtag-detail.md) - Retrieve detailed data for a trending TikTok hashtag, including video count, view trends, and top associated content.
  - [Trending Music](https://docs.keyapi.ai/en/tiktok/intelligence/trending-music.md) - Retrieve the current list of trending music tracks on TikTok, with usage counts and popularity metrics.
  - [Trending Music Detail](https://docs.keyapi.ai/en/tiktok/intelligence/trending-music-detail.md) - Retrieve detailed data for a trending TikTok music track, including usage count, associated video examples, and popularity timeline.

## Docs Search Strategy

1. Map the user's natural-language request to the closest scenario and API concept, then search `llms.txt` for the platform slug plus that semantic entity/action. Do not rely on literal keyword matching when the user wording is vague, translated, or business-oriented.
2. Prefer the narrowest endpoint whose title and description match the requested workflow.
3. Resolve the selected endpoint page before any live call; never infer method or path from this file.
4. Compose multiple endpoints only when the user asks for a report, comparison, enrichment, or explanation that one endpoint cannot answer.
5. API calls are live by default. Repeating the same parameters calls the API again. Large payloads may return a stdout preview; when complete fields are needed for analysis, rerun the same documented request with `--output-file <temp-or-workspace-.tmp-keyapi-file>.json` and read the API payload from `data.data`. Use a user-facing output path only when the user asks to save or export results.

## User Input Compression

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the object being searched, analyzed, compared, ranked, or monitored
- Scope: market, country, language, category, keyword, identifier, date window, and page depth
- Sort or metric: freshness, relevance, growth, engagement, rating, sales, price, audience, or other documented metric
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report

## TikTok Data Source Choice

- Endpoint titles containing `Analytics`, and docs paths ending in `-analytics`, represent EchoTik analytics data. Use them for historical, ranking, commerce-performance, and enriched analysis.
- Endpoints without `Analytics` are realtime/current interfaces. Use them for current detail, current search, comments, live status, downloads, image search, and other freshness-sensitive tasks.
- When both modes exist and the user does not specify freshness versus historical depth, ask a short mode question before execution.
