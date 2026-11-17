# TikTok Video Module Rules

## 1. Module Scope

Use this module for TikTok video search, video detail, Analytics video lists/rankings, comments, replies, comment keywords, captions, download URLs, cover images, and product attribution.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Video discovery and ranking
3. Video detail and trend
4. Comments, replies, keywords, and captions
5. Video assets and product links

## 2. Video discovery and ranking

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-list-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-ranking-analytics.md`
- Purpose: Find videos through realtime keyword search or Analytics/EchoTik filters/rankings.

### Best Suited For

- video examples by keyword
- commerce/AI/ad video discovery
- top video rankings
- filtered video research

### Routing Rules

- Use realtime video search for current public keyword lookup.
- Use video list/ranking Analytics for historical metrics, commerce, AI, ad, or ranking analysis.
- Shortlist before expensive detail/comment enrichment.

## 3. Video detail and trend

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-detail.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-detail-analytics.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-trends.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-trends-analytics.md`
- Purpose: Retrieve current or Analytics video detail and interaction trends.

### Best Suited For

- video performance reports
- current video state
- 14-day interaction trend
- longer historical trend snapshots

### Routing Rules

- Ask realtime versus Analytics/EchoTik when detail mode is ambiguous.
- Prefer realtime interaction trends for recent 14-day movement.
- Use Analytics trends for historical snapshots and commerce/performance context.

## 4. Comments, replies, keywords, and captions

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-comments.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-comment-replies.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-comment-keywords.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-captions.md`
- Purpose: Analyze audience reaction and video text/script content.

### Best Suited For

- comment theme analysis
- reply thread expansion
- comment keyword insight
- caption/script extraction

### Routing Rules

- Use comment keywords before full comment pulling when the user wants themes.
- Use comments before replies; replies require a known comment ID.
- Use captions when the user asks what the video says or needs script analysis.

## 5. Video assets and product links

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-download-url.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/covers-batch-download.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-products-analytics.md`
- Purpose: Retrieve video download/cover assets or products attached to videos.

### Best Suited For

- download URL lookup
- bulk cover archiving
- video-to-product attribution

### Routing Rules

- Use download URL only when media asset retrieval is requested.
- Use covers batch download for bulk cover processing.
- Use video products Analytics when commerce attribution is needed.

## 6. Common Workflows

- Video report: detail mode choice -> video detail -> trend -> comments/keywords/captions/products as needed.
- Video discovery: video search/list/ranking -> selected detail -> comments/trend.
- Comment analysis: video detail -> comment keywords -> comments -> selected replies.
