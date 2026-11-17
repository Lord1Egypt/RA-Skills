---
name: kreatix
description: Schedule videos and text posts to Instagram, TikTok, YouTube, Facebook, X, LinkedIn and Pinterest with Kreatix, move or cancel them, and read views and follower stats.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📅"
    homepage: https://kreatix.cc/ai-agents/
    requires:
      env:
        - KREATIX_API_KEY
      bins:
        - curl
    primaryEnv: KREATIX_API_KEY
    envVars:
      - name: KREATIX_API_KEY
        required: true
        description: Kreatix agent key, starts with kx_live_. Create it at https://kreatix.cc/settings/agent
---

# Kreatix

Kreatix is a social media scheduler for people who run many pages. One video can go to every connected page at once, each with its own platform settings. This skill talks to the Kreatix MCP server over HTTPS (JSON-RPC 2.0, stateless streamable HTTP, no session to open).

## Setup

1. Sign in at https://kreatix.cc and connect your pages.
2. Create an agent key in Settings > AI agent (https://kreatix.cc/settings/agent) and put it in `KREATIX_API_KEY`.
3. A key can be revoked there at any time. After that it gets 401.

## How to call

Every action is one POST. Pass the tool's name and arguments:

```bash
curl -s https://api.kreatix.cc/mcp \
  -H "Authorization: Bearer $KREATIX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_channels","arguments":{}}}'
```

`"method":"tools/list"` returns every tool with its full input schema. Read it once if unsure about a field.

## Tools

| Tool | What it does | Main arguments |
|---|---|---|
| `list_channels` | The connected pages: id, platform, name, followers, groups. `can_post` is false for pages that are only shown. | `platform` (optional) |
| `list_groups` | Page groups, for example one brand's Instagram, TikTok and YouTube. | none |
| `schedule_post` | Plans a post on channels or a whole group, at a time or now. | `publish_at` (required), `channel_ids` or `group_id`, `caption`, `media_url`, `cover_url`, `tiktok_privacy`, `tiktok_music_confirmed`, `youtube_title`, `youtube_privacy` |
| `list_posts` | Posts with status: `upcoming` (default), `recent`, `published`, `failed`. | `status`, `channel_id`, `limit` (max 100) |
| `reschedule_post` | Moves a waiting post to another time or to now. | `post_id`, `publish_at` |
| `cancel_post` | Deletes a waiting post so it never goes out. | `post_id` |
| `get_stats` | Views, likes, comments and follower change for a period, with the period before, the best channels and the top posts. | `period`: `today`, `yesterday`, `7d` (default), `30d`, `90d` |

## Rules for the agent

- Before `schedule_post`, `reschedule_post` or `cancel_post`, show the user the channels, the caption and the time, and wait for a yes.
- Times are ISO 8601 with a UTC offset, for example `2026-11-03T18:00:00+03:00`, or the word `now`. Never send a bare `18:00`.
- `media_url` is a video already in Kreatix (a `media_url` from `list_posts`) or a public YouTube, TikTok, Instagram or Facebook post link, which Kreatix imports first. Leave it out for a text post (Facebook, LinkedIn and X only).
- TikTok channels need `tiktok_privacy` and `tiktok_music_confirmed`. Both come from the user. There is no default, so ask.
- A Pinterest video needs `cover_url` (for example a `thumbnail_url` from `list_posts`).
- One key schedules a limited number of posts an hour, with each channel counted as one post. Do not loop. Spread big batches over time instead of sending everything `now`.
- `can_post: false` pages cannot be posted to. Say so instead of retrying.
- On a 401, the key is missing or revoked. Ask the user for a new one from Settings > AI agent.

## Examples

Plan one video to a whole group tomorrow at 18:00 Istanbul time:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"schedule_post","arguments":{
  "group_id": 12,
  "media_url": "https://www.tiktok.com/@brand/video/7430000000000000000",
  "caption": "Three ways to style one linen shirt. Which one is yours?",
  "publish_at": "2026-11-11T18:00:00+03:00",
  "tiktok_privacy": "PUBLIC_TO_EVERYONE",
  "tiktok_music_confirmed": true
}}}
```

How did last week go:

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_stats","arguments":{"period":"7d"}}}
```
