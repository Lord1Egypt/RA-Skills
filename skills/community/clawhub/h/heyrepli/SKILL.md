---
name: heyrepli
description: "Scrape social media, generate AI replies, and publish/schedule posts via the HeyRepli API. Use when the user asks to get a YouTube transcript, fetch TikTok/Instagram/X(Twitter)/LinkedIn/Facebook post data, rewrite or draft social content, publish or schedule a post, track brand mentions, or check HeyRepli usage/quota."
homepage: https://heyrepli.com
license: MIT
---

# HeyRepli

HeyRepli is an AI social concierge API: data scraping for 7 platforms, AI rewrite/draft, publishing, brand-mention tracking, and analytics. All through one API key.

## Setup

1. Get an API key: log in at https://app.heyrepli.com → Settings → Account (https://app.heyrepli.com/dashboard/settings/account) → copy your API key
2. Export it (never hardcode in files or output):

```bash
export HEYREPLI_API_KEY="***"
```

Every call sends it as header `X-API-Key`. Free tier: 50 AI replies + 5 rewrites + 10 scheduled posts per month.

## Two API surfaces

- **MCP endpoint** (13 tools, JSON-RPC): `POST https://api.heyrepli.com/api/v1/mcp`
- **Open REST API** (5 endpoints): `https://api.heyrepli.com/api/v1/open/*`

Prefer the helper script; it handles both and prints JSON.

## Workflow

Use `scripts/heyrepli.py` (Python 3.8+, stdlib only):

```bash
# List all MCP tools
python scripts/heyrepli.py list-tools

# Call any MCP tool (scraping, AI rewrite, publish)
python scripts/heyrepli.py call scrape_youtube_transcript --args '{"videoId":"dQw4w9WgXcQ"}'
python scripts/heyrepli.py call ai_rewrite --args '{"text":"just shipped a new feature lol","style":"professional","provider":"auto"}'

# Open REST endpoints
python scripts/heyrepli.py rest posts --params platform=twitter
python scripts/heyrepli.py rest replies --body '{"platform":"twitter","comment_text":"nice product!"}'
python scripts/heyrepli.py rest schedule --body '{"platform":"twitter","content":"hello","scheduled_at":"2026-09-28T09:00:00Z"}'
python scripts/heyrepli.py rest mentions
python scripts/heyrepli.py rest analytics --params period=7d
python scripts/heyrepli.py usage
```

Full tool list, arguments, and endpoint parameters: read `references/api.md`.

## Caveats

- TikTok tool name mismatch on the server: tools/list declares `tiktok_video_insights` but the handler implements `scrape_tiktok_video`. If one name errors, try the other.
- `publish_twitter/linkedin/facebook` require the user to have completed OAuth for that platform in the HeyRepli dashboard first; otherwise the call fails with an OAuth error — tell the user to connect the account, do not retry blindly.
- `scrape_youtube_transcript` works without any YouTube API key (Innertube). `scrape_youtube_video` and `scrape_youtube_search` require a YOUTUBE_API_KEY configured in the user's HeyRepli account.
- Rate limits are per plan; on HTTP 429 respect `Retry-After`, never loop.
- Errors return `{ "ok": false, "error": { "code", "message" } }` — surface `message` to the user verbatim.
- API status check: `GET https://api.heyrepli.com/health` (no auth).
