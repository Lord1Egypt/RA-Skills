---
name: PostThatLater
description: Schedule and manage social media posts across multiple social platforms. Query analytics, manage your queue, and publish immediately — all via natural language. Call GET /api/v1/platforms for the list of platforms active on this instance.
homepage: https://postthatlater.com
emoji: 📅
requires:
  env:
    - PTL_API_KEY
primaryEnv: PTL_API_KEY
---

# PostThatLater Skill

Schedule and manage social media posts from Claude Code or any AI assistant.

## Setup

### 1. Create an account

Sign up at https://postthatlater.com — a subscription is required to use the API.

### 2. Generate an API key

In PostThatLater: **Account Settings → API Keys → Create new key**

Copy the `sk_ptl_...` key — it's shown only once.

### 3. Set the environment variable

```bash
export PTL_API_KEY=sk_ptl_your_key_here
```

Add to `~/.zshrc` or `~/.bashrc` to persist across sessions.

### 4. Verify

```bash
curl https://postthatlater.com/api/v1/accounts \
  -H "Authorization: Bearer $PTL_API_KEY"
```

You should see your connected social media accounts.

---

## Base URL

```
https://postthatlater.com
```

All API requests require:
```
Authorization: Bearer $PTL_API_KEY
Content-Type: application/json   (for POST/PATCH)
```

---

## Critical Tips for Agents

1. **Call `GET /api/v1/accounts` first** — you need numeric account IDs to schedule posts. Never guess them.
2. **Ask for timezone once per session** — all `scheduled_at` values must be ISO 8601 UTC (e.g. `2026-03-10T09:00:00Z`). Convert from the user's local time.
3. **Confirm before `publish_now`** — publishing is immediate and irreversible. Always confirm with the user before calling the publish-now endpoint.
4. **Use `Idempotency-Key` on every POST/PATCH** — generate a UUID per request to prevent duplicate posts on retry. Example: `Idempotency-Key: $(uuidgen | tr '[:upper:]' '[:lower:]')`.
5. **Check platform limits** — always call `GET /api/v1/platforms` to get the live list of available platforms and their limits. Never hardcode a platform list or assume a platform is available.
6. **Cross-posting** — pass multiple IDs in `account_ids` to post the same content everywhere at once. The API creates one post record per account and links them via `group_id`.
7. **All times are UTC in responses** — convert to the user's timezone when displaying scheduled times.
8. **Posting with an image** — first `POST /api/v1/images` with the image URL to get a filename, then pass that filename in the `images` array of `POST /api/v1/posts`. Use `GET /api/v1/images` to list already-stored images that can be reused without re-uploading.

---

## Accounts

### List all connected accounts

```bash
curl https://postthatlater.com/api/v1/accounts \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Response:
```json
{
  "data": [
    {
      "id": 12,
      "platform": "bluesky",
      "handle": "you.bsky.social",
      "display_name": "you.bsky.social",
      "status": "connected",
      "created_at": "2026-01-10T08:30:00.000Z",
      "updated_at": "2026-01-10T08:30:00.000Z"
    }
  ],
  "meta": { "request_id": "..." }
}
```

`status` is `"connected"` (healthy) or `"error"` (needs reconnecting in dashboard).

### Get a single account

```bash
curl https://postthatlater.com/api/v1/accounts/12 \
  -H "Authorization: Bearer $PTL_API_KEY"
```

---

## Posts

### List posts

```bash
curl "https://postthatlater.com/api/v1/posts?status=pending&limit=10&offset=0" \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Query parameters:
- `status` — `pending`, `posted`, or `failed` (omit for all)
- `platform` — e.g. `bluesky`, `mastodon`, `linkedin`
- `limit` — max results (default: 20, max: 100)
- `offset` — skip N results for pagination (default: 0)

Response:
```json
{
  "data": [
    {
      "id": 101,
      "text": "Hello from the API!",
      "scheduled_at": "2026-03-15T09:00:00.000Z",
      "status": "pending",
      "platform": "bluesky",
      "account_id": 12,
      "images": [],
      "platform_post_id": null,
      "platform_post_url": null,
      "error_message": null,
      "retry_count": 0,
      "likes": 0,
      "comments": 0,
      "shares": 0,
      "group_id": null,
      "created_at": "2026-03-01T12:00:00.000Z",
      "updated_at": null
    }
  ],
  "meta": { "request_id": "...", "total": 5, "limit": 10, "offset": 0 }
}
```

### Create a post (schedule)

```bash
curl -X POST https://postthatlater.com/api/v1/posts \
  -H "Authorization: Bearer $PTL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen | tr '[:upper:]' '[:lower:]')" \
  -d '{
    "text": "Hello from the PostThatLater API!",
    "scheduled_at": "2026-03-15T09:00:00.000Z",
    "account_ids": [12, 15]
  }'
```

Body parameters:
- `text` *(required)* — post content; must not exceed platform char limit
- `scheduled_at` *(required)* — ISO 8601 UTC datetime; must be in the future
- `account_ids` *(required)* — array of account IDs (at least one)
- `images` — optional array of image filenames

Returns HTTP `201` with the first created post. All posts share a `group_id`.

### Get a single post

```bash
curl https://postthatlater.com/api/v1/posts/101 \
  -H "Authorization: Bearer $PTL_API_KEY"
```

### Update a post

Only works on `pending` posts. Returns `409 conflict` if already published or failed.

```bash
curl -X PATCH https://postthatlater.com/api/v1/posts/101 \
  -H "Authorization: Bearer $PTL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen | tr '[:upper:]' '[:lower:]')" \
  -d '{
    "text": "Updated content for the post",
    "scheduled_at": "2026-03-16T10:00:00.000Z"
  }'
```

### Delete a post

Cannot delete `posted` posts (returns `409`). Failed posts can be deleted.

```bash
curl -X DELETE https://postthatlater.com/api/v1/posts/101 \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Response:
```json
{ "data": { "deleted": true, "id": 101 }, "meta": { "request_id": "..." } }
```

### Publish immediately

Bypasses the scheduler. Post must be `pending` or `failed`. **Irreversible — confirm with user first.**

```bash
curl -X POST https://postthatlater.com/api/v1/posts/101/publish-now \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Response:
```json
{
  "data": {
    "id": 101,
    "status": "posted",
    "platform_post_url": "https://bsky.app/profile/you.bsky.social/post/...",
    ...
  },
  "meta": { "request_id": "..." }
}
```

---

## Images

Post with images by first ingesting the image from a URL, then passing the returned filename when creating a post.

### Ingest an image from a URL

Downloads, processes (EXIF rotation, compression, format conversion), and stores the image server-side. Returns a `filename` to use in posts.

```bash
curl -X POST https://postthatlater.com/api/v1/images \
  -H "Authorization: Bearer $PTL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/photo.jpg"}'
```

Response:
```json
{
  "data": { "filename": "1741036800000-123456789.jpeg" },
  "meta": { "request_id": "..." }
}
```

Pass the filename in the `images` array of `POST /api/v1/posts`. Check `GET /api/v1/platforms` for the `max_images` limit per platform.

### List stored images

Returns all images referenced by your posts with file metadata and which post IDs use each image. Use this to reuse an already-uploaded image without re-ingesting.

```bash
curl https://postthatlater.com/api/v1/images \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Response:
```json
{
  "data": [
    {
      "filename": "1741036800000-123456789.jpeg",
      "url": "/uploads/1741036800000-123456789.jpeg",
      "size": 284672,
      "created_at": "2026-03-01T09:00:00.000Z",
      "referenced_by_post_ids": [101, 104]
    }
  ],
  "meta": { "request_id": "...", "total": 1 }
}
```

---

## Analytics

### Overall posting health summary

```bash
curl "https://postthatlater.com/api/v1/analytics/summary?period=30d" \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Query parameters: `period` — `7d`, `30d`, `90d`, or `all` (default: `30d`)

Response:
```json
{
  "data": {
    "period": "30d",
    "total_posts": 45,
    "by_status": {
      "posted": 40,
      "pending": 3,
      "failed": 2
    },
    "success_rate": 95.2,
    "total_likes": 312,
    "total_comments": 48,
    "total_shares": 91,
    "total_engagement": 451
  },
  "meta": { "request_id": "..." }
}
```

### Top posts by engagement

```bash
curl "https://postthatlater.com/api/v1/analytics/top-posts?period=30d&limit=5" \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Query parameters:
- `period` — `7d`, `30d`, or `all` (default: `30d`)
- `limit` — number of posts (default: 5, max: 20)

### Per-post metrics

```bash
curl https://postthatlater.com/api/v1/posts/101/metrics \
  -H "Authorization: Bearer $PTL_API_KEY"
```

Response:
```json
{
  "data": {
    "post_id": 101,
    "platform": "bluesky",
    "likes": 42,
    "comments": 8,
    "shares": 15,
    "engagement": 65,
    "published_at": "2026-03-01T09:00:00.000Z"
  },
  "meta": { "request_id": "..." }
}
```

### Breakdown by platform

```bash
curl "https://postthatlater.com/api/v1/analytics/by-platform?period=30d" \
  -H "Authorization: Bearer $PTL_API_KEY"
```

### Timeline (daily post counts)

```bash
curl "https://postthatlater.com/api/v1/analytics/timeline?period=7d" \
  -H "Authorization: Bearer $PTL_API_KEY"
```

---

## Platform Capabilities

**Public endpoint — no authentication required.**

Returns character limits and capabilities for all currently available platforms.
New platforms may be added over time, so always fetch this list rather than
hardcoding platform names or limits.

```bash
curl https://postthatlater.com/api/v1/platforms
```

Response fields per platform:
- `name` — slug used in API calls (e.g. `bluesky`)
- `display_name` — human-readable name
- `char_limit` — maximum post length in characters
- `max_images` — maximum images per post
- `supports_video` — whether video uploads are accepted
- `notes` — platform-specific connection or usage notes
```

---

## Error Handling

All errors follow:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed.",
    "details": [
      { "field": "text", "message": "Text exceeds Bluesky character limit (300 chars)." },
      { "field": "scheduled_at", "message": "scheduled_at must be a future datetime." }
    ]
  }
}
```

| Code | HTTP | Meaning |
|------|------|---------|
| `invalid_api_key` | 401 | Missing, malformed, or revoked Bearer token |
| `subscription_required` | 402 | No active subscription |
| `not_found` | 404 | Resource doesn't exist or belongs to another user |
| `conflict` | 409 | Action not allowed in current state (e.g. editing a published post) |
| `validation_error` | 400 | Request body failed validation — check `details` array for field-level errors |
| `rate_limited` | 429 | 60 req/min per key — check `Retry-After` header |
| `internal_error` | 500 | Unexpected server error |

---

## Example Session

```
User: Schedule a post about our summer sale on Bluesky and Mastodon for tomorrow at 10am EST

Agent workflow:
1. GET /api/v1/accounts       → find Bluesky (id: 12) and Mastodon (id: 15)
2. GET /api/v1/platforms      → confirm char limits (300 / 500)
3. Convert 10am EST → 15:00 UTC (March 5 → 2026-03-05T15:00:00Z)
4. Confirm with user: "Ready to schedule 'Summer sale...' to Bluesky + Mastodon for Mar 5 at 10am EST?"
5. POST /api/v1/posts with account_ids: [12, 15] and Idempotency-Key header
6. Report back: "Scheduled! Post #101 and #102 will go out March 5 at 10am EST."
```
