---
name: keyapi-tiktok-content-analysis
description: Analyze TikTok content at scale — extract insights from videos, hashtags, music tracks, and live streams including engagement trends, comment sentiment, caption transcription, and commerce attribution data.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"📊"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-tiktok-content-analysis

> Analyze TikTok content at scale — extract insights from videos, hashtags, music, and live streams to inform content strategy, trend discovery, and audience engagement research.

This skill provides comprehensive content intelligence on TikTok using the KeyAPI MCP service. It enables deep analysis of video performance, comment sentiment, caption extraction, hashtag reach, music popularity, and live-stream activity — all backed by real-time data and historical analytics datasets.

Use this skill when you need to:
- Analyze the performance trajectory of specific TikTok videos or content creators
- Research hashtag reach and trending topics for content positioning
- Extract video captions and analyze comment sentiment for audience insights
- Identify high-performing music tracks for content creation
- Monitor live-stream activity and audience engagement patterns
- Build content performance benchmarks for editorial or marketing strategy

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **KEYAPI_TOKEN** | A valid API token from [keyapi.ai](https://keyapi.ai/). If you don't have one, register at the site to obtain your free token. Set it as an environment variable: `export KEYAPI_TOKEN=your_token_here` |
| **Node.js** | v18 or higher |
| **Dependencies** | Run `npm install` in the skill directory to install `@modelcontextprotocol/sdk` |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## MCP Server Configuration

All tool calls in this skill target the KeyAPI MCP server:

```
Server URL : https://mcp.keyapi.ai
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

### Video Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search videos by keyword | `search_videos` | Discovery, keyword-content association |
| Real-time video details (views, likes, comments, metadata) | `get_video_detail` | Snapshot of a specific video |
| Extract captions/transcripts from a video | `get_video_captions` | Content analysis, transcription, SEO |
| Read video comments | `get_video_comments` | Audience sentiment, community feedback |
| Read replies to a specific comment | `get_video_comment_replies` | Deep conversation thread analysis |
| Extract top keywords from a video's comments | `video_comment_keywords` | Audience interest signals, semantic analysis |
| View 14-day engagement trend (views, likes, comments) | `video_interaction_trends` | Virality decay analysis, momentum tracking |
| Get downloadable video URL (no watermark where available) | `get_video_download_url` | Content archiving, offline analysis — param: `url` (the video's share URL) |
| Search and filter videos with analytics data | `video_list_analytics` | Data-driven video discovery, benchmarking |
| Comprehensive analytics for one or more videos | `video_detail_analytics` | Historical performance, product associations |
| Historical trend snapshots (views, likes, ER over time) | `video_trends_analytics` | Long-term performance analysis |
| Products featured in a video and their sales data | `video_products_analytics` | Commerce attribution |
| Ranked video list by views, engagement, or sales | `video_ranking_analytics` | Top-N content, competitive benchmarking |
| Batch download video cover images | `batch_download_cover_images` | Bulk cover image archiving and processing |

### Hashtag Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Get videos under a specific hashtag | `get_hashtag_videos` | Hashtag content exploration — requires `hashtag_id` (not name); resolve via `search_hashtags` first |
| Search hashtags by keyword | `search_hashtags` | Hashtag discovery, volume assessment |

### Music Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search music tracks by keyword | `search_music` | Sound discovery for content creation |

### Live Stream Nodes

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Get live stream details (viewers, host, products) | `get_live_stream_detail` | Real-time live commerce monitoring — requires both `room_id` and `user_id` |
| Search active or recent live streams by keyword | `search_live_streams` | Live stream discovery, competitive monitoring |

### Cross-Domain Search

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Search across products, shops, and creators simultaneously | `general_search_analytics` | Broad cross-domain discovery from a single keyword |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify the Content Analysis Objective and Select Nodes

Clarify the user's goal and map it to one or more nodes. Common research patterns:

- **Video performance analysis**: Start with `get_video_detail`, deepen with `video_detail_analytics` + `video_trends_analytics`.
- **Comment and sentiment analysis**: Use `get_video_comments` + `video_comment_keywords`.
- **Hashtag research**: Use `search_hashtags` to find relevant tags, then `get_hashtag_videos` for content within the tag.
- **Music trend research**: Use `search_music` to find tracks, cross-reference with `trending_music` (see keyapi-tiktok-intelligence skill).
- **Live stream monitoring**: Use `search_live_streams` to find active streams, then `get_live_stream_detail` with both `room_id` and `user_id` for specifics.
- **Commerce content analysis**: Use `video_products_analytics` to correlate video content with product sales data.
- **Cross-domain keyword research**: Use `general_search_analytics` for a unified view across products, shops, and creators.

Multiple nodes can be selected for cross-dimensional analysis — for example, analyzing a video's engagement trend while simultaneously extracting its comment keywords to understand what drove viewer interest.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and valid values:

```bash
node scripts/run.js --schema <tool_name>

# Examples
node scripts/run.js --schema video_list_analytics
node scripts/run.js --schema video_comment_keywords
```

### Step 3 — Call APIs and Cache Results Locally

Execute the required tool calls and persist all responses to the local cache.

**Calling a tool (using `scripts/run.js`):**

```bash
# Single call — result is cached automatically
node scripts/run.js --tool <tool_name> --params '<json_args>' --pretty

# Fetch all pages at once (auto-pagination)
node scripts/run.js --tool <tool_name> --params '<json_args>' --all-pages

# Force a fresh call, skip cache
node scripts/run.js --tool <tool_name> --params '<json_args>' --no-cache
```

**Example — get video details:**

```bash
node scripts/run.js --tool get_video_detail \
  --params '{"video_id":"7xxxxxxxxxxxxxxxxx"}' --pretty
```

**Example — extract comment keywords:**

```bash
node scripts/run.js --tool video_comment_keywords \
  --params '{"video_id":"7xxxxxxxxxxxxxxxxx"}' --pretty
```

**Pagination for analytics endpoints:**

All `*_analytics` endpoints use `page_num` (1-indexed) and `page_size` (max 10). `run.js` injects these automatically if not specified.

```
--page-num 1  --page-size 10   → first page (default)
--all-pages                    → all pages merged into one result
```

**Cache directory structure:**

```
.keyapi-cache/
├── videos/
│   └── {video_id}/
│       ├── detail.json               # get_video_detail / video_detail_analytics
│       ├── captions.json             # get_video_captions
│       ├── comments.json             # get_video_comments
│       ├── comment_keywords.json     # video_comment_keywords
│       ├── interaction_trends.json   # video_interaction_trends
│       ├── trends_analytics.json     # video_trends_analytics
│       ├── products.json             # video_products_analytics
│       └── download_url.json         # get_video_download_url
├── hashtags/
│   └── {hashtag_id}/
│       └── videos.json               # get_hashtag_videos
├── live_streams/
│   └── {room_id}/
│       └── detail.json               # get_live_stream_detail
├── searches/
│   ├── videos/
│   │   └── {md5_of_query_params}.json    # search_videos, video_list_analytics
│   ├── hashtags/
│   │   └── {keyword}.json                # search_hashtags
│   ├── music/
│   │   └── {keyword}.json                # search_music
│   ├── live_streams/
│   │   └── {keyword}.json                # search_live_streams
│   └── general/
│       └── {md5_of_query_params}.json    # general_search_analytics
├── rankings/
│   └── videos_{params_hash}.json         # video_ranking_analytics
└── images/
    └── covers/
        └── {converted_filename}           # batch_download_cover_images output
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given entity and node. If a valid cache file exists, load from disk and skip the API call.

**Cover image processing (mandatory):**

> **⚠️ Cover image conversion is required for all analytics responses.**
>
> After every API call that returns content with images, scan all image URLs in the response. If any URL's host matches `echosell-images.tos-ap-southeast-1.volces.com`, collect **all such URLs** and issue a single `batch_download_cover_images` call. Replace the original URLs in your working dataset with the converted URLs returned. Save converted images to `.keyapi-cache/images/covers/`.

**Example — batch cover image conversion (`run.js` does this automatically):**

```bash
node scripts/run.js --tool batch_download_cover_images \
  --params '{
    "cover_urls": "https://echosell-images.tos-ap-southeast-1.volces.com/img/abc.jpg,https://echosell-images.tos-ap-southeast-1.volces.com/img/def.jpg"
  }' --pretty
```

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured content intelligence report tailored to the analysis type:

**For video analysis:**
1. **Video Overview** — Title, creator, publish date, view count, likes, comments, shares.
2. **Engagement Deep-Dive** — 14-day interaction trend, engagement rate vs. category benchmarks, virality signals.
3. **Audience Insights** — Top comment themes, keyword frequency, positive/negative sentiment signals.
4. **Content-Commerce Link** — Products featured, sales generated, conversion indicators.
5. **Strategic Takeaways** — What made this content perform (hook analysis, format, timing, hashtag leverage).

**For hashtag/topic analysis:**
1. **Hashtag Profile** — Total video count, view volume, growth trend.
2. **Top Content** — Highest-performing videos within the hashtag, common formats.
3. **Creator Patterns** — Who is driving the conversation, creator tier distribution.
4. **Opportunity Assessment** — Saturation level, engagement quality, best entry timing.

**For music analysis:**
1. **Track Overview** — Title, artist, total usage count.
2. **Usage Trends** — Growth in video adoption over time.
3. **Content Fit** — Types of content using this track, associated hashtags and themes.

**For live stream analysis:**
1. **Stream Profile** — Host, viewer count, products featured, duration.
2. **Commerce Performance** — GMV generated, conversion signals.
3. **Engagement Quality** — Peak concurrent viewers, comment activity.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Pagination** | All `*_analytics` endpoints use `page_num` (starts at `1`) and `page_size`. Never use page `0`. |
| **Cover images** | **Always** batch-convert all image URLs from `echosell-images.tos-ap-southeast-1.volces.com` via `batch_download_cover_images`. This applies to all analytics endpoint responses. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request once after a brief pause before reporting the error. |
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. |
| **Batch efficiency** | When processing multiple videos, collect all cover image URLs across all responses and issue a single `batch_download_cover_images` call rather than calling it per-item. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; check video_id format and parameter values |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — video or stream may have been deleted | Verify the ID is correct; the content may no longer be available on TikTok |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry once after 2–3 seconds; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
