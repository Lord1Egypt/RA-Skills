# TikTok Content Composite Rules

## 1. Module Scope

Use this file only as a content-level router. For detailed execution rules, load the specific search, video, live, or intelligence module that matches the request.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Route search-style content requests
3. Route video analysis requests

## 2. Route search-style content requests

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/hashtag-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/music-search.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/live-search.md`
- Purpose: Route content search requests to the dedicated search module.

### Best Suited For

- video keyword search
- hashtag/music seed resolution
- live search

### Routing Rules

- Load tiktok-search-rules.md for search behavior and pagination.
- Do not execute from this composite file alone; resolve the endpoint docs through the target module.

## 3. Route video analysis requests

- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-detail.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-comments.md`
- Documentation: `https://docs.keyapi.ai/en/tiktok/content/video-captions.md`
- Purpose: Route video detail, comments, captions, trends, and assets to the video module.

### Best Suited For

- video report
- comment analysis
- caption extraction
- download/cover lookup

### Routing Rules

- Load tiktok-video-rules.md for video workflows.
- Use tiktok-live-rules.md instead when the target is a live room.

## 4. Common Workflows

- Content request: identify whether it is search, video, live, hashtag/music, or market trend -> load the specific module.
