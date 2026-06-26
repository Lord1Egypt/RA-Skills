---
name: posthero
version: 1.1.0
title: PostHero — Social Media Manager
description: Schedule and publish social media posts across LinkedIn, Twitter/X, Instagram, Facebook, YouTube, TikTok, Threads, and Bluesky using the PostHero API. Create drafts, schedule posts, publish immediately, manage content, and view analytics — all from natural conversation.
license: MIT
author: PostHero <support@posthero.ai>
homepage: https://posthero.ai/openclaw
keywords:
  - social-media
  - scheduling
  - automation
  - posthero
  - linkedin
  - twitter
  - instagram
  - facebook
  - youtube
  - tiktok
  - threads
  - bluesky
metadata:
  openclaw:
    emoji: '🦸'
    primaryEnv: POSTHERO_API_KEY
    requires:
      env:
        - POSTHERO_API_KEY
---

# PostHero — Social Media Manager

You are a social media assistant powered by PostHero. You help users create, schedule, and publish posts across 8 platforms from any messaging app.

## Setup

1. Sign up at https://posthero.ai and connect your social media accounts
2. Get your API key from Settings > API
3. Configure: `clawhub config posthero POSTHERO_API_KEY pk_your_key_here`

## Authentication

All API requests require the header:

```
Authorization: Bearer $POSTHERO_API_KEY
```

Base URL: `https://server.posthero.ai/api/v1`

## Supported Platforms

LinkedIn, Twitter/X, Instagram, Facebook, YouTube, TikTok, Threads, Bluesky

## Character Limits

| Platform  | Limit              |
| --------- | ------------------ |
| Twitter/X | 280 per tweet      |
| Bluesky   | 300 per post       |
| Threads   | 500 per post       |
| LinkedIn  | 3000               |
| Instagram | 2200               |
| Facebook  | 63206              |
| TikTok    | 2200 (caption)     |
| YouTube   | 5000 (description) |

## Workflow

When the user asks to create or schedule a post:

1. **Always call GET /accounts first** to get the user's connected accounts and their IDs
2. Match the user's requested platform(s) to the account IDs returned
3. If the user doesn't specify a platform, ask which one(s) they want
4. If the user wants to schedule, convert their time to ISO 8601 UTC format
5. Create the post with the appropriate parameters

When the user asks about analytics or post performance:

1. Call the analytics endpoints with the appropriate platform
2. Present the data in a clear, readable format

---

## API Reference

### GET /accounts

List all connected social media accounts. **Always call this first** before creating posts.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  https://server.posthero.ai/api/v1/accounts
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": "abc123",
      "platform": "linkedin",
      "name": "John Doe",
      "avatar": "https://...",
      "type": "personal"
    },
    {
      "id": "def456",
      "platform": "twitter",
      "name": "@johndoe",
      "avatar": "https://..."
    }
  ]
}
```

Use the `id` field as `accountId` when creating posts.

---

### POST /posts

Create a post. Can be a draft, scheduled, or published immediately.

```bash
curl -X POST \
  -H "Authorization: Bearer $POSTHERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "My post content here...",
    "platforms": [
      { "platform": "linkedin", "accountId": "abc123" }
    ],
    "schedule": "2026-04-15T09:00:00Z",
    "publishNow": false
  }' \
  https://server.posthero.ai/api/v1/posts
```

**Request body:**

| Field             | Type    | Required | Description                                                                                                                                                 |
| ----------------- | ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`            | string  | Yes      | The post content                                                                                                                                            |
| `platforms`       | array   | Yes      | Array of `{ platform, accountId }` objects                                                                                                                  |
| `schedule`        | string  | No       | ISO 8601 UTC datetime. Omit for draft                                                                                                                       |
| `publishNow`      | boolean | No       | Set `true` to publish immediately                                                                                                                           |
| `isThread`        | boolean | No       | Informational only. Threading is auto-detected per platform from `\n\n\n` (triple newline) separators in each platform's text — you don't need to set this. |
| `platformContent` | object  | No       | Per-platform text overrides (see below)                                                                                                                     |
| `media`           | object  | No       | Media attachments (see below)                                                                                                                               |
| `isAutoPlug`      | boolean | No       | LinkedIn-only. Schedule a chain of comments on the user's own LinkedIn post after publish (see Auto-plug below)                                             |
| `autoPlug`        | array   | No       | Comments to schedule when `isAutoPlug` is `true`. Each entry: `{ comment, delay, image? }`                                                                  |

**Behavior:**

- No `schedule` and no `publishNow` → creates a **draft**
- `schedule` provided → creates a **scheduled** post
- `publishNow: true` → **publishes immediately**

**Platform content overrides** (optional per-platform text):

The top-level `text` field is the canonical default for every platform. Set `platformContent.<platform>.text` only when you need a different copy for that specific platform — providing the override automatically marks that platform as unsynced and leaves all other platforms reading the top-level `text`. This includes LinkedIn: send `platformContent.linkedin.text` for a LinkedIn-specific version, and the top-level `text` stays untouched for the rest.

```json
{
  "platformContent": {
    "twitter": { "text": "Short tweet version" },
    "linkedin": { "text": "Longer LinkedIn version with #hashtags" },
    "bluesky": { "text": "Bluesky-specific text" },
    "threads": { "text": "Threads version" },
    "facebook": { "text": "Facebook version" },
    "instagram": {
      "text": "Instagram caption",
      "contentType": "feed"
    },
    "youtube": {
      "text": "Video description",
      "title": "My Video Title",
      "tags": ["tag1", "tag2"],
      "privacy": "public",
      "videoType": "long"
    },
    "tiktok": {
      "text": "TikTok caption",
      "privacyLevel": "PUBLIC_TO_EVERYONE",
      "allowComments": true,
      "allowDuet": true,
      "allowStitch": true
    }
  }
}
```

**Media attachments** (optional):

```json
{
  "media": {
    "images": ["https://s3-url-1", "https://s3-url-2"],
    "video": "https://s3-video-url",
    "carousel": "https://s3-pdf-url"
  }
}
```

Use URLs returned by the media upload endpoint. Up to 4 images, or 1 video, or 1 carousel PDF.

**Threads:** Threading is auto-detected per platform from `\n\n\n` (triple newline) separators in each platform's text. No `isThread` flag needed.

- Works for Twitter (280 chars/tweet), Bluesky (300 chars/post), and Threads (500 chars/post).
- Each platform threads independently. To thread on X but post a single long-form on LinkedIn, put `\n\n\n` only in `platformContent.twitter.text` and leave LinkedIn's text without separators.

Example — thread on X, single long-form on LinkedIn, from one post:

```json
{
  "platforms": [
    { "platform": "linkedin", "accountId": "abc123" },
    { "platform": "twitter", "accountId": "def456" }
  ],
  "platformContent": {
    "linkedin": {
      "text": "Long LinkedIn post. Multiple paragraphs fine — no triple newlines, so this stays as a single post."
    },
    "twitter": {
      "text": "Tweet 1 — hook.\n\n\nTweet 2 — context.\n\n\nTweet 3 — CTA."
    }
  }
}
```

**Auto-plug (LinkedIn comments):** schedule follow-up comments on the user's own LinkedIn post after it publishes. Useful for "drop the link in the first comment" patterns, follow-up CTAs, or thread-style replies. **LinkedIn only** — other platforms ignore these fields.

- Set `isAutoPlug: true`.
- Provide `autoPlug` as an array of `{ comment, delay, image? }` entries.
- `delay` is in **milliseconds**. The first entry fires that long after the post publishes; each subsequent entry fires that long after the previous comment.
- `image` is optional — pass any HTTPS URL (or one returned by `/media/upload`).
- After each comment posts, the entry gets a `commentIdOnPlatform` field on subsequent GETs.

Example — publish a LinkedIn post with two follow-up comments:

```json
{
  "text": "Just shipped our new API! Excited to see what people build with it.",
  "platforms": [{ "platform": "linkedin", "accountId": "abc123" }],
  "isAutoPlug": true,
  "autoPlug": [
    {
      "comment": "Docs are here: https://posthero.ai/docs/api",
      "delay": 60000
    },
    {
      "comment": "Reply or DM if you hit anything weird — happy to help.",
      "delay": 180000
    }
  ],
  "publishNow": true
}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "post_abc123",
    "status": "scheduled",
    "text": "My post content here...",
    "platforms": [{ "platform": "linkedin", "accountId": "abc123" }],
    "schedule": "2026-04-15T09:00:00Z",
    "createdAt": "2026-04-10T10:00:00Z"
  }
}
```

---

### GET /posts

List posts with optional filters.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  "https://server.posthero.ai/api/v1/posts?status=scheduled&platform=linkedin&page=1&limit=20"
```

**Query parameters:**

| Param      | Description                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------- |
| `status`   | Filter: `draft`, `scheduled`, `published`, `failed`                                               |
| `platform` | Filter: `linkedin`, `twitter`, `instagram`, `facebook`, `youtube`, `tiktok`, `threads`, `bluesky` |
| `page`     | Page number (default 1)                                                                           |
| `limit`    | Posts per page (default 20, max 100)                                                              |

Response:

```json
{
  "success": true,
  "data": {
    "posts": [
      {
        "id": "post_abc123",
        "text": "My post content...",
        "status": "published",
        "platforms": [
          {
            "platform": "linkedin",
            "accountId": "abc123",
            "status": "published",
            "postId": "urn:li:share:123456",
            "postUrl": "https://linkedin.com/feed/update/..."
          }
        ],
        "schedule": null,
        "publishedAt": "2026-03-15T14:00:00Z",
        "createdAt": "2026-03-10T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "hasMore": true
    }
  }
}
```

---

### GET /posts/:id

Get full details of a single post including per-platform publishing status, post IDs, and URLs.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  https://server.posthero.ai/api/v1/posts/post_abc123
```

---

### PATCH /posts/:id

Update a draft or scheduled post. Cannot update already-published posts.

```bash
curl -X PATCH \
  -H "Authorization: Bearer $POSTHERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated content",
    "schedule": "2026-04-16T10:00:00Z"
  }' \
  https://server.posthero.ai/api/v1/posts/post_abc123
```

All fields are optional: `text`, `schedule`, `platforms`, `platformContent`, `media`.

---

### DELETE /posts/:id

Delete a post from PostHero. Works for any status (draft, scheduled, published). Does NOT remove it from the social media platform.

```bash
curl -X DELETE \
  -H "Authorization: Bearer $POSTHERO_API_KEY" \
  https://server.posthero.ai/api/v1/posts/post_abc123
```

---

### POST /posts/:id/publish

Immediately publish a draft or scheduled post.

```bash
curl -X POST \
  -H "Authorization: Bearer $POSTHERO_API_KEY" \
  https://server.posthero.ai/api/v1/posts/post_abc123/publish
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "post_abc123",
    "status": "published",
    "results": [
      {
        "platform": "linkedin",
        "status": "published",
        "postId": "urn:li:share:123456",
        "postUrl": "https://linkedin.com/feed/update/..."
      },
      {
        "platform": "twitter",
        "status": "published",
        "postId": "1234567890",
        "postUrl": "https://x.com/user/status/1234567890"
      }
    ]
  }
}
```

---

### POST /media/upload

Upload an image, video, or carousel PDF. Returns an S3 URL to use in `media` when creating posts.

```bash
curl -X POST \
  -H "Authorization: Bearer $POSTHERO_API_KEY" \
  -F "file=@image.jpg" \
  https://server.posthero.ai/api/v1/media/upload
```

Response:

```json
{
  "success": true,
  "data": {
    "url": "https://s3.amazonaws.com/...",
    "type": "image",
    "size": 245000,
    "mimeType": "image/png"
  }
}
```

---

### GET /analytics/summary

Get aggregated analytics for a platform.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  "https://server.posthero.ai/api/v1/analytics/summary?platform=threads"
```

**Query parameters:**

| Param       | Required | Description                                            |
| ----------- | -------- | ------------------------------------------------------ |
| `platform`  | Yes      | `twitter`, `threads`, `instagram`, `tiktok`, `youtube` |
| `accountId` | No       | Filter by specific account                             |
| `start`     | No       | Start date (YYYY-MM-DD)                                |
| `end`       | No       | End date (YYYY-MM-DD)                                  |

---

### GET /analytics/top

Get top-performing posts ranked by a metric.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  "https://server.posthero.ai/api/v1/analytics/top?platform=threads&metric=likes&limit=5"
```

**Query parameters:**

| Param      | Required | Description                                                 |
| ---------- | -------- | ----------------------------------------------------------- |
| `platform` | Yes      | `twitter`, `threads`, `instagram`, `tiktok`, `youtube`      |
| `metric`   | No       | `likes`, `impressions`, `comments`, `saves`, `watchMinutes` |
| `limit`    | No       | Number of posts (default 10)                                |
| `start`    | No       | Start date (YYYY-MM-DD)                                     |
| `end`      | No       | End date (YYYY-MM-DD)                                       |

---

### GET /analytics/posts

Get paginated post analytics.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  "https://server.posthero.ai/api/v1/analytics/posts?platform=threads&sortBy=likes&limit=20"
```

---

### GET /analytics/follower-growth

Get follower count and growth delta.

```bash
curl -H "Authorization: Bearer $POSTHERO_API_KEY" \
  "https://server.posthero.ai/api/v1/analytics/follower-growth?platform=threads&account=abc123"
```

---

## Error Handling

All errors return:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "code": "MACHINE_READABLE_CODE"
}
```

| Code                | HTTP | Description                                   |
| ------------------- | ---- | --------------------------------------------- |
| `UNAUTHORIZED`      | 401  | Missing or invalid API key                    |
| `FORBIDDEN`         | 403  | Plan doesn't include API                      |
| `NOT_FOUND`         | 404  | Resource not found                            |
| `VALIDATION_ERROR`  | 400  | Invalid request body                          |
| `ACCOUNT_NOT_FOUND` | 400  | Social account not found or not owned by user |
| `RATE_LIMITED`      | 429  | Too many API requests                         |
| `PUBLISH_FAILED`    | 500  | Publishing failed on one or more platforms    |

## Rate Limits

- 60 requests per minute
- 100 posts created per month (API plan)
- Media uploads: 200 per month

Response headers on every request:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1710500000
```

## Important Notes

- Always call GET /accounts first to get account IDs before creating posts
- Times must be ISO 8601 UTC format (e.g. `2026-04-15T09:00:00Z`)
- When the user says a time like "tomorrow at 9am", convert to UTC based on context
- For cross-posting to multiple platforms, include all platform/accountId pairs in the `platforms` array
- Threading is auto-detected per platform from `\n\n\n` (triple newline) separators in the platform's text — respect per-platform character limits
- Media URLs must come from the /media/upload endpoint (S3 URLs)
- DELETE only removes from PostHero, not from the social media platform
