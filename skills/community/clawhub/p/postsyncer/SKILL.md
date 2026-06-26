---
name: postsyncer-social-media-assistant
version: 2.2.1
title: Social Media Assistant (via postsyncer.com)
description: Manages social media through PostSyncer using REST and/or MCP. Use when scheduling, posting, or managing content across Instagram, TikTok, YouTube, X (Twitter), LinkedIn, Facebook, Threads, Bluesky, Pinterest, Telegram, Mastodon. Covers posts (including Reels/video cover images), media library (list, import URLs, delete, multipart file upload), media folders (CRUD), comments with optional `media` attachments, labels, campaigns, and analytics. Accounts must be pre-connected in the PostSyncer app.
license: MIT
author: PostSyncer <support@postsyncer.com>
homepage: https://postsyncer.com/openclaw
keywords: [social-media, postsyncer, automation, scheduling, instagram, tiktok, youtube, twitter, linkedin, api]
metadata:
  openclaw:
    requires:
      env:
        - POSTSYNCER_API_TOKEN
    primaryEnv: POSTSYNCER_API_TOKEN
---

# PostSyncer Social Media Assistant

Autonomously manage social media through [PostSyncer](https://postsyncer.com) using the REST API.

## Setup

1. Create a PostSyncer account at [app.postsyncer.com](https://app.postsyncer.com)
2. [Connect social profiles](https://app.postsyncer.com/dashboard?action=accounts) (Instagram, TikTok, YouTube, X, LinkedIn, etc.)
3. Go to [**Settings → API Integrations**](https://app.postsyncer.com/dashboard?action=settings&section=api-integrations) and create a personal access token with abilities: `workspaces`, `accounts`, `posts`, and (if you use them) `labels`, `campaigns`
4. Add to `.env`: `POSTSYNCER_API_TOKEN=your_token`

## PostSyncer MCP (optional)

[PostSyncer MCP](https://postsyncer.com/openclaw) uses the **same Bearer token** as REST. Typical tools: `list-workspaces`, `list-accounts`, post CRUD (including `content[].cover_image` for Reels/video covers), **`get-post-by-url`**, **`get-post-by-platform-post-id`**, **`analyze-twitter-post`** (fetch any public X/Twitter URL, load replies, answer a question with AI), **`list-media`**, **`get-media`**, **`upload-media-from-url`**, **`upload-media-file`** (base64, same rules as REST file upload), **`delete-media`**, **`list-folders`**, **`create-folder`**, **`get-folder`**, **`update-folder`**, **`delete-folder`**, comments, labels, campaigns, analytics.

**Raw multipart** (`POST /api/v1/media/upload/file`) is usually easier from curl/scripts; MCP uses **`upload-media-file`** with base64 for clients that only send JSON tool arguments.

## How to Make API Calls

All requests go to `https://postsyncer.com/api/v1` with the header:

```
Authorization: Bearer $POSTSYNCER_API_TOKEN
Content-Type: application/json
```

Use `web_fetch`, `curl`, or any HTTP tool available. Always read `$POSTSYNCER_API_TOKEN` from the environment.

---

## API Reference

### Discovery (Call First)

**List Workspaces** — `GET /api/v1/workspaces`

```bash
curl "https://postsyncer.com/api/v1/workspaces" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Returns workspaces with `id`, `name`, `slug`, `timezone`.

**List Accounts** — `GET /api/v1/accounts`

```bash
curl "https://postsyncer.com/api/v1/accounts" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Returns accounts with `id`, `platform`, `username`, `workspace_id`.

---

### Media library

Requires the `posts` ability. Responses include `id`, `workspace_id`, `folder_id`, and asset metadata.

**List Media** — `GET /api/v1/media`

```bash
curl -G "https://postsyncer.com/api/v1/media" \
  --data-urlencode "workspace_id=12" \
  --data-urlencode "page=1" \
  --data-urlencode "per_page=50" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Query params: `workspace_id`, `folder_id`, `root_only` (true/false), `page`, `per_page` (max 100).

**Get Media** — `GET /api/v1/media/{media_id}`

```bash
curl "https://postsyncer.com/api/v1/media/999" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Import from URLs** — `POST /api/v1/media/upload/url`

```bash
curl -X POST "https://postsyncer.com/api/v1/media/upload/url" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": 12, "urls": ["https://example.com/photo.jpg"], "folder_id": null}'
```

**Upload file (multipart)** — `POST /api/v1/media/upload/file`

Use `multipart/form-data` with fields such as `workspace_id`, `file` (and optional chunk/chunk metadata if your client uses chunked upload). Not JSON.

**Delete Media** — `DELETE /api/v1/media/{media_id}` *(confirm first)*

```bash
curl -X DELETE "https://postsyncer.com/api/v1/media/999" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

---

### Media folders

Requires the `posts` ability.

**List Folders** — `GET /api/v1/folders`

```bash
curl -G "https://postsyncer.com/api/v1/folders" \
  --data-urlencode "workspace_id=12" \
  --data-urlencode "root=1" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Query params: `workspace_id`, `parent_id`, `root` (top-level only).

**Create Folder** — `POST /api/v1/folders`

```bash
curl -X POST "https://postsyncer.com/api/v1/folders" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": 12, "name": "Campaign assets", "color": "#3b82f6", "parent_id": null}'
```

**Get Folder** — `GET /api/v1/folders/{id}`

**Update Folder** — `PUT /api/v1/folders/{id}`

```bash
curl -X PUT "https://postsyncer.com/api/v1/folders/5" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Renamed folder"}'
```

**Delete Folder** — `DELETE /api/v1/folders/{id}` *(confirm first)*

---

### Posts

**List Posts** — `GET /api/v1/posts`

```bash
curl "https://postsyncer.com/api/v1/posts?page=1&per_page=20&include_comments=false" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Query params: `page`, `per_page` (max 100), `include_comments` (true/false).

**Get Post** — `GET /api/v1/posts/{id}`

```bash
curl "https://postsyncer.com/api/v1/posts/123" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Create Post** — `POST /api/v1/posts`

```bash
curl -X POST "https://postsyncer.com/api/v1/posts" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": 12,
    "schedule_type": "schedule",
    "content": [{
      "text": "Caption #hashtags",
      "media": [42],
      "cover_image": {"thumbnail": 43}
    }],
    "accounts": [{"id": 136}, {"id": 95, "settings": {"post_type": "REELS"}}],
    "schedule_for": {"date": "2026-03-26", "time": "14:30", "timezone": "America/New_York"},
    "labels": [5],
    "repeatable": false
  }'
```

- `schedule_type`: `publish_now` | `schedule` | `draft`
- `schedule_for`: Optional scheduling object used when `schedule_type` is `schedule`. Provide `{"date": "YYYY-MM-DD", "time": "HH:MM", "timezone": "..."}` to schedule for a specific date/time, or omit/leave empty to auto-schedule to the next available time slot
- `content`: Array of thread items. Each needs `text` and/or `media`: an array of **library media IDs** (integers) and/or **HTTPS URL strings** (import or list media first when you want stable IDs). Optional `cover_image` on video posts (see below).
- `accounts`: Array of `{id, settings?}`. Platform-specific options go in `settings`

#### Video cover images (`content[].cover_image`)

For video posts, set `cover_image` on the **first** content item. Only that thread's cover is used when publishing.

| Field | Type | Description |
|-------|------|-------------|
| `thumbnail` | integer or URL | **Custom cover image upload** — workspace media library **id** (image only) or public **HTTPS URL**. |
| `video_cover_timestamp_ms` | integer | **Frame selection from the attached video** — timestamp in **milliseconds** (e.g. `2500` = 2.5s). |

#### Platform requirements

| Platform | Cover method | API field |
|----------|--------------|-----------|
| **TikTok** | Frame selection from video **only** | `video_cover_timestamp_ms` |
| **YouTube** | Custom thumbnail upload **only** | `thumbnail` |
| **Instagram** (Reels) | Custom thumbnail upload **only** | `thumbnail` |
| **Facebook** (Reels / video) | Custom thumbnail upload **only** | `thumbnail` |

**Do not mix methods across platforms in one request without understanding the table above.** TikTok does not accept custom thumbnail uploads via the API — use `video_cover_timestamp_ms`. YouTube, Instagram, and Facebook require a custom image in `thumbnail` — frame timestamps are not used.

**Example — Instagram / Facebook / YouTube (custom thumbnail):**

```json
"content": [{
  "text": "New reel!",
  "media": [1842],
  "cover_image": {"thumbnail": 1843}
}],
"accounts": [{"id": 136, "settings": {"post_type": "REELS"}}]
```

**Example — TikTok (frame from video):**

```json
"content": [{
  "text": "New TikTok!",
  "media": [1842],
  "cover_image": {"video_cover_timestamp_ms": 2500}
}]
```

Typical workflow for YouTube / Instagram / Facebook: upload the video → upload the cover image → create the post with both in `content[0]`. For TikTok: upload the video → set `video_cover_timestamp_ms` to the desired frame.

**Update Post** — `PUT /api/v1/posts/{id}`

```bash
curl -X PUT "https://postsyncer.com/api/v1/posts/123" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": [{"text": "Updated caption", "media": [42], "cover_image": {"thumbnail": 43}}], "schedule_for": {"date": "2026-03-27", "time": "10:00"}}'
```

Only posts that have not been published yet can be updated. Supports the same `content[].cover_image` shape as create.

**Delete Post** — `DELETE /api/v1/posts/{id}` *(confirm with user first)*

```bash
curl -X DELETE "https://postsyncer.com/api/v1/posts/123" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Analyze X/Twitter Post (AI)** — `POST /api/v1/posts/analyze-twitter`

Fetch any public X/Twitter status URL, load all replies, and answer a question with Claude Sonnet 4.6. The post does not need to exist in PostSyncer.

```bash
curl -X POST "https://postsyncer.com/api/v1/posts/analyze-twitter" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://x.com/user/status/1234567890", "question": "What is the overall sentiment in the replies?"}'
```

MCP equivalent: **`analyze-twitter-post`** with the same `url` and `question` fields.

---

### Comments

**List Comments** — `GET /api/v1/comments`

```bash
curl -G "https://postsyncer.com/api/v1/comments" \
  --data-urlencode "post_id=123" \
  --data-urlencode "per_page=20" \
  --data-urlencode "include_replies=true" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Query params: `post_id` (required), `per_page`, `page`, `include_replies`, `platform`.

**Get Comment** — `GET /api/v1/comments/{id}`

```bash
curl "https://postsyncer.com/api/v1/comments/456" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Create Comment / Reply** — `POST /api/v1/comments`

```bash
curl -X POST "https://postsyncer.com/api/v1/comments" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post_id": 123, "content": "Reply text", "parent_comment_id": null, "media": [42]}'
```

Optional `media`: array of **integer library IDs** and/or **HTTPS URLs** (same shape as post `content[].media`; do not use a deprecated `media_urls` field).

**Update Comment** — `PUT /api/v1/comments/{id}`

```bash
curl -X PUT "https://postsyncer.com/api/v1/comments/456" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated reply text"}'
```

**Hide Comment** — `POST /api/v1/comments/{id}/hide`

```bash
curl -X POST "https://postsyncer.com/api/v1/comments/456/hide" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Delete Comment** — `DELETE /api/v1/comments/{id}` *(confirm first)*

```bash
curl -X DELETE "https://postsyncer.com/api/v1/comments/456" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Sync Comments from Platforms** — `POST /api/v1/comments/sync`

```bash
curl -X POST "https://postsyncer.com/api/v1/comments/sync" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post_id": 123}'
```

---

### Labels

**List Labels** — `GET /api/v1/labels`

```bash
curl "https://postsyncer.com/api/v1/labels" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Get Label** — `GET /api/v1/labels/{id}`

**Create Label** — `POST /api/v1/labels`

```bash
curl -X POST "https://postsyncer.com/api/v1/labels" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Campaign 2026", "color": "#3b82f6", "workspace_id": 12}'
```

**Update Label** — `PUT /api/v1/labels/{id}`

**Delete Label** — `DELETE /api/v1/labels/{id}` *(confirm first)*

---

### Analytics

All analytics endpoints require the `posts` API ability.

**All Workspaces** — `GET /api/v1/analytics`

```bash
curl "https://postsyncer.com/api/v1/analytics" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**By Workspace** — `GET /api/v1/analytics/workspaces/{workspace_id}`

```bash
curl "https://postsyncer.com/api/v1/analytics/workspaces/12" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**By Post** — `GET /api/v1/analytics/posts/{post_id}`

```bash
curl "https://postsyncer.com/api/v1/analytics/posts/123" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**By Account** — `GET /api/v1/analytics/accounts/{account_id}`

```bash
curl "https://postsyncer.com/api/v1/analytics/accounts/136" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

**Sync Post Analytics** — `POST /api/v1/analytics/posts/{post_id}/sync`

```bash
curl -X POST "https://postsyncer.com/api/v1/analytics/posts/123/sync" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

Queues background jobs to refresh metrics. Does not return metrics directly — call GET after sync.

---

### Account Management

**Delete Account** — `DELETE /api/v1/accounts/{id}` *(destructive, confirm first)*

```bash
curl -X DELETE "https://postsyncer.com/api/v1/accounts/136" \
  -H "Authorization: Bearer $POSTSYNCER_API_TOKEN"
```

---

## Platform-Specific Settings

Pass per-platform options in `accounts[].settings` when creating/updating posts:

**Pinterest:** `{"board_id": 123456}`

**X/Twitter:**
```json
{"reply_settings": "everyone", "for_super_followers_only": false, "quote_tweet_id": null, "reply": {"in_reply_to_tweet_id": null}, "community_id": null, "share_with_followers": true}
```

**TikTok:**
```json
{"privacy_level": "PUBLIC_TO_EVERYONE", "disable_comment": false, "disable_duet": false, "disable_stitch": false, "post_mode": "DIRECT_POST"}
```
Cover: **`video_cover_timestamp_ms` only** — pick a frame from the video. Custom thumbnail upload is not supported on TikTok.

**Instagram:** `{"post_type": "REELS"}` — options: `REELS`, `STORIES`, `POST`. Cover: **`thumbnail` only** — upload a custom cover image.

**Facebook:** Cover for Reels/video: **`thumbnail` only** — upload a custom cover image (use `post_type: "REELS"` when posting as a Reel).

**YouTube:**
```json
{"video_type": "video", "title": "My Video", "privacyStatus": "public", "notifySubscribers": true}
```
Cover: **`thumbnail` only** — upload a custom video thumbnail.

**LinkedIn:** `{"visibility": "PUBLIC"}` — options: `PUBLIC`, `CONNECTIONS`, `LOGGED_IN`

**Bluesky:** `{"website_card": {"uri": "https://...", "title": "...", "description": "..."}}`

**Telegram:** `{"disable_notification": false, "protect_content": false}`

---

## Common Workflows

### Schedule a Post to Multiple Platforms

1. `GET /api/v1/workspaces` → get `workspace_id`
2. `GET /api/v1/accounts` → get `id`s for target platforms
3. Optionally `POST /api/v1/media/upload/url` (or MCP `upload-media-from-url`) → use returned `id`s in `content[].media`
4. `POST /api/v1/posts` with `schedule_type: "schedule"` and `schedule_for`

### Publish a Reel / Video with a Cover (Instagram, Facebook, YouTube)

1. Upload the video → `POST /api/v1/media/upload/file` or `POST /api/v1/media/upload/url` → note video `id`
2. Upload a cover image → note cover `id`
3. `POST /api/v1/posts` with `content[0].media` = video id, `content[0].cover_image.thumbnail` = cover id, and platform settings (e.g. `post_type: "REELS"` for Instagram/Facebook)

### Publish a TikTok with a Cover Frame

1. Upload the video → note video `id`
2. `POST /api/v1/posts` with `content[0].media` = video id and `content[0].cover_image.video_cover_timestamp_ms` = frame time in milliseconds (TikTok does not support custom thumbnail upload)

### Reply to Comments

1. `GET /api/v1/posts` → find post `id`
2. `POST /api/v1/comments/sync` with `post_id`
3. `GET /api/v1/comments?post_id=123&include_replies=true`
4. `POST /api/v1/comments` with `post_id` and optional `parent_comment_id`

### Check Performance

1. `GET /api/v1/analytics/posts/{id}` for a specific post
2. If stale: `POST /api/v1/analytics/posts/{id}/sync`, then re-fetch

### Analyze a Public X/Twitter Thread

1. `POST /api/v1/posts/analyze-twitter` (or MCP `analyze-twitter-post`) with a public status URL and a question
2. Use the returned `answer` for sentiment, objections, feature requests, or other reply themes

---

## Best Practices

- **Video covers:** Match the cover method to the platform — **TikTok:** `video_cover_timestamp_ms` only; **YouTube / Instagram / Facebook:** `thumbnail` only (upload a cover image first)
- **Always start with** `GET /workspaces` and `GET /accounts` to discover IDs; use `GET /folders` and `GET /media` when organizing or attaching library assets
- **New automations:** Use `schedule_type: "draft"` or confirm before `publish_now`
- **Destructive actions:** State what will happen, confirm before delete operations
- **Multi-network:** One post can target multiple accounts; check per-platform `status` in the response
- **Rate limits:** 60 requests/minute — don't call sync endpoints repeatedly
- **Hashtags:** Keep relevant and limited (3–5 per post)

---

## Error Handling

| Status | Meaning |
|--------|---------|
| `401` | Token missing or invalid |
| `403` | Token lacks required ability (e.g. `posts`) |
| `404` | Resource not found or no access |
| `422` | Validation error — check required fields and formats |
| `429` | Rate limited — wait before retrying |

---

## Links

- [API Documentation](https://docs.postsyncer.com/api-reference/introduction)
- [PostSyncer Dashboard](https://app.postsyncer.com)
- [API Authentication](https://docs.postsyncer.com/essentials/authentication)
