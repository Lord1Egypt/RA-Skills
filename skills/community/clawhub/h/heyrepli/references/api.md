# HeyRepli API Reference

Base URL: `https://api.heyrepli.com`
Auth: header `X-API-Key: ***` on every call. Get the key at https://app.heyrepli.com/dashboard/settings/account (Settings → Account → API Key → Copy).
Health (no auth): `GET /health`.
Errors: `{ "ok": false, "error": { "code": "...", "message": "..." } }`. Common codes: `UNAUTHORIZED` (missing key), `INVALID_API_KEY`, `BAD_REQUEST`, `BAD_TIMESTAMP`, HTTP 429 (rate limit — respect `Retry-After`).

## Surface 1: MCP endpoint

`POST /api/v1/mcp`, `Content-Type: application/json`, JSON-RPC 2.0.

```json
{ "jsonrpc": "2.0", "id": 1, "method": "tools/call",
  "params": { "name": "<tool>", "arguments": { ... } } }
```

Other methods: `initialize`, `ping`, `tools/list`, `resources/list`.

### Data / scraping tools

| Tool | Args | Notes |
|---|---|---|
| `scrape_youtube_transcript` | `videoId` (ID or full URL) | Works WITHOUT any YouTube API key (Innertube). Unique selling point. |
| `scrape_youtube_video` | `videoId` | Requires YOUTUBE_API_KEY in user's HeyRepli account. |
| `scrape_youtube_search` | `query`, `maxResults` (1-50, default 10) | Requires YOUTUBE_API_KEY. |
| `tiktok_video_insights` | `url` (video URL or ID) | Official TikTok Display API. ⚠️ Server handler implements it as `scrape_tiktok_video`; if one name errors, use the other. |
| `scrape_instagram_post` | `url` | Via Apify: caption, images, likes, comments. |
| `scrape_twitter_tweet` | `tweetId` (numeric ID or URL) | Requires TWITTER_BEARER_TOKEN configured. |
| `scrape_linkedin_posts` | `username`, `maxPosts` (1-50, default 20) | Via Apify. |
| `scrape_facebook_posts` | `pageId` (ID, username, or URL), `maxPosts` (1-50, default 20) | Via Apify. |

### AI tool

`ai_rewrite`:
- `text` (required) — content to rewrite
- `style`: `professional` | `casual` | `funny` | `story` | `promo` (default `casual`)
- `provider`: `auto` | `deepseek` | `kimi` | `grok` (default `auto`)
- `platform`: `twitter` | `linkedin` | `facebook` | `instagram` | `tiktok` (adjusts length/tone)

### Publish tools (need OAuth connected in dashboard first)

| Tool | Args | Limit |
|---|---|---|
| `publish_twitter` | `text` | 280 chars; connect at /dashboard/publish |
| `publish_linkedin` | `text` | 3000 chars |
| `publish_facebook` | `text` | — |

If the account is not OAuth-connected, the call returns an error — direct the user to the dashboard, don't retry.

### Utility

`get_usage`: no args. Returns current-month usage, quota remaining, plan limits.

## Surface 2: Open REST API (built for n8n / skills / webhooks)

| Endpoint | Params / Body | Returns |
|---|---|---|
| `GET /api/v1/open/posts` | query: `platform`, `status` (default `all`), `limit` (≤100, default 20) | Post list: id, platform, content, status, scheduled_at, published_at |
| `POST /api/v1/open/replies` | body: `platform`*, `comment_text`*, `post_id` | Creates AI draft reply (status `draft`, reviewable in dashboard) |
| `POST /api/v1/open/schedule` | body: `platform`*, `content`*, `scheduled_at`* (ISO 8601) | Schedules a post |
| `GET /api/v1/open/mentions` | query: `limit` (≤200, default 50) | Brand mentions: platform, author, text, sentiment |
| `GET /api/v1/open/analytics` | query: `period` (default `7d`) | Totals: posts, replies, mentions |

\* = required.

## Plans (subject to change — check https://heyrepli.com/pricing)

- Free: 50 AI replies + 5 rewrites + 10 scheduled posts / month
- Starter $49: 800 + 30 + 200
- Pro $99: 1,500 + 100 + 500 + 80 brand mentions
- Agency $199: 3,000 + 500 + unlimited posts + 300 mentions
