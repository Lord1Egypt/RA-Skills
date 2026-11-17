# Scenario Cards

Use these scenario cards to translate natural-language YouTube requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

videos, Shorts, comments, sub-comments, streams, related videos, search results, trending videos, channels, channel IDs, channel URLs, channel videos, and search suggestions

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Video detail, comments, sub-comments, streams, and related videos | `youtube-video-rules.md` | /youtube/ |
| Channel description, channel videos, channel search, and channel ID/URL conversion | `youtube-channel-rules.md` | /youtube/ |
| General search, filtered search, Shorts search, trending videos, and search suggestions | `youtube-search-trends-rules.md` | /youtube/ |

## 1. Analyze a video

- User intent: Retrieve video metadata, playback/stream options, related videos, and discussion context.
- Primary entity: video
- Ask for: video URL or ID, whether comments/sub-comments/streams/related videos are needed, and page depth.
- Default workflow: Fetch video information first; call streams only when playback format data is needed, related videos for recommendation context, and comments/sub-comments for audience discussion.
- Reference module: `youtube-video-rules.md`
- Endpoint shortlist:
  - [Get video information](https://docs.keyapi.ai/en/youtube/get_video_info.md) - Get detailed information about a YouTube video, returning the full raw data (including playerResponse and initialData).
  - [Get video streams info](https://docs.keyapi.ai/en/youtube/get_video_streams.md) - Get format information and playback URLs for all quality levels of a YouTube video. Returns both standard formats (audio+video merged) and adaptive formats (audio and video separate). Suitable for scenarios where all quality options need to be displayed.
  - [Get related videos](https://docs.keyapi.ai/en/youtube/get_related_videos.md) - Get recommended related content for a YouTube video (recommended video list). Similar to the related videos shown on the right side of the video playback page. Returns all recommended videos at once (typically 20-30 videos).
  - [Get video comments](https://docs.keyapi.ai/en/youtube/get_video_comments.md) - Get comments for a YouTube video. Supports paginated retrieval.
  - [Get video sub comments](https://docs.keyapi.ai/en/youtube/get_video_comment_replies.md) - Get replies to a YouTube video comment.

## 2. Search videos and Shorts

- User intent: Find videos or Shorts by keyword with optional filters and sorting.
- Primary entity: video / Shorts search result
- Ask for: query, upload time, duration/type/features/sort filters when needed, Shorts versus general video preference, and top N.
- Default workflow: Use the narrowest search endpoint: search video for simple video search, filtered search for advanced constraints, and Shorts search for short-form discovery.
- Reference module: `youtube-search-trends-rules.md`
- Endpoint shortlist:
  - [Search video](https://docs.keyapi.ai/en/youtube/search_video.md) - Search for videos.
  - [General search with filters](https://docs.keyapi.ai/en/youtube/get_general_search.md) - Search YouTube with advanced filters. Supports filtering by upload time, video duration, content type, features, and sort order.
  - [YouTube Shorts search](https://docs.keyapi.ai/en/youtube/get_shorts_search.md) - Dedicated search for YouTube Shorts (videos under 60 seconds), using the native YouTube API. Supports filters and sort options. The first request may return mixed content; use continuation_token for subsequent requests to get pure Shorts.
  - [Get search suggestions](https://docs.keyapi.ai/en/youtube/get_search_suggestions.md) - Get YouTube search suggestions (autocomplete). Similar to the suggestions shown when typing in the YouTube search box.

## 3. Monitor trending and query demand

- User intent: Inspect trending videos or generate search suggestions for a topic.
- Primary entity: trend / suggestion
- Ask for: region or market when documented, seed query, and result depth.
- Default workflow: Use trending videos for current market attention and search suggestions to expand query variants before deeper search.
- Reference module: `youtube-search-trends-rules.md`
- Endpoint shortlist:
  - [Get trending videos](https://docs.keyapi.ai/en/youtube/get_trending_videos.md) - Get trending videos.
  - [Get search suggestions](https://docs.keyapi.ai/en/youtube/get_search_suggestions.md) - Get YouTube search suggestions (autocomplete). Similar to the suggestions shown when typing in the YouTube search box.
  - [Search video](https://docs.keyapi.ai/en/youtube/search_video.md) - Search for videos.

## 4. Analyze channels and channel catalogs

- User intent: Retrieve channel details, convert channel identifiers, or collect channel videos.
- Primary entity: channel
- Ask for: channel URL, handle, name, or channel ID; whether videos should be collected; and page depth.
- Default workflow: Resolve channel ID/URL when needed, then fetch channel description and channel videos; use channel search endpoints for discovery.
- Reference module: `youtube-channel-rules.md`
- Endpoint shortlist:
  - [Get channel ID](https://docs.keyapi.ai/en/youtube/get_channel_id.md) - Get a channel ID from the channel name.
  - [Get channel ID from URL](https://docs.keyapi.ai/en/youtube/get_channel_id_from_url.md) - Get the channel ID (channel_id) from a YouTube channel URL. Supports multiple URL formats including @username format, /channel/ format, /c/ format, and /user/ format.
  - [Get channel URL from channel ID](https://docs.keyapi.ai/en/youtube/get_channel_url.md) - Get the channel handle (@username) from a YouTube channel ID. This is the reverse operation of get_channel_id.
  - [Get channel description](https://docs.keyapi.ai/en/youtube/get_channel_description.md) - Get detailed information about a YouTube channel, including channel description, view count, subscriber count, join date, social links, etc.
  - [Get channel videos](https://docs.keyapi.ai/en/youtube/get_channel_videos.md) - Get a list of videos from a YouTube channel. Supports paginated retrieval; use continuation_token to get more videos.
  - [Search channel](https://docs.keyapi.ai/en/youtube/search_channel.md) - Search for channels.
  - [Search channels](https://docs.keyapi.ai/en/youtube/search_channels.md) - Search YouTube channels. Returns only channel-type results (filters out videos, playlists, etc.). Supports paginated retrieval for more channels.

## 5. Build a YouTube topic or competitor report

- User intent: Compare videos/channels for a topic, creator, or market.
- Primary entity: mixed video/channel report
- Ask for: topic, target channels, region, sections, and max page budget.
- Default workflow: Confirm sections, then combine search/trending, video information, channel description/videos, comments, and related videos only where they add evidence.
- Reference module: `youtube-search-trends-rules.md`
- Endpoint shortlist:
  - [General search with filters](https://docs.keyapi.ai/en/youtube/get_general_search.md) - Search YouTube with advanced filters. Supports filtering by upload time, video duration, content type, features, and sort order.
  - [Search video](https://docs.keyapi.ai/en/youtube/search_video.md) - Search for videos.
  - [Get trending videos](https://docs.keyapi.ai/en/youtube/get_trending_videos.md) - Get trending videos.
  - [Get video information](https://docs.keyapi.ai/en/youtube/get_video_info.md) - Get detailed information about a YouTube video, returning the full raw data (including playerResponse and initialData).
  - [Get channel description](https://docs.keyapi.ai/en/youtube/get_channel_description.md) - Get detailed information about a YouTube channel, including channel description, view count, subscriber count, join date, social links, etc.
  - [Get channel videos](https://docs.keyapi.ai/en/youtube/get_channel_videos.md) - Get a list of videos from a YouTube channel. Supports paginated retrieval; use continuation_token to get more videos.
  - [Get video comments](https://docs.keyapi.ai/en/youtube/get_video_comments.md) - Get comments for a YouTube video. Supports paginated retrieval.
  - [Get related videos](https://docs.keyapi.ai/en/youtube/get_related_videos.md) - Get recommended related content for a YouTube video (recommended video list). Similar to the related videos shown on the right side of the video playback page. Returns all recommended videos at once (typically 20-30 videos).

## Docs Search Strategy

1. Map the user's natural-language request to the closest scenario and API concept, then search `llms.txt` for the platform slug plus that semantic entity/action. Do not rely on literal keyword matching when the user wording is vague, translated, or business-oriented.
2. Prefer the narrowest endpoint whose title and description match the requested workflow.
3. Resolve the selected endpoint page before any live call; never infer method or path from this file.
4. Compose multiple endpoints only when the user asks for a report, comparison, enrichment, or explanation that one endpoint cannot answer.
5. API calls are live by default. Repeating the same parameters calls the API again. Large payloads may return a stdout preview; when complete fields are needed for analysis, rerun the same documented request with `--output-file <temp-or-workspace-.tmp-keyapi-file>.json` and read the API payload from `data.data`. Use a user-facing output path only when the user asks to save or export results.

## User Input Compression

Compress parameter-heavy tasks into:

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the object being searched, analyzed, compared, ranked, or monitored
- Scope: market, country, language, category, keyword, identifier, date window, and page depth
- Sort or metric: freshness, relevance, growth, engagement, rating, sales, price, audience, or other documented metric
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report
