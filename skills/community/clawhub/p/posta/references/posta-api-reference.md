# Posta API Reference

Base URL: `https://api.getposta.app/v1`

All authenticated endpoints require: `Authorization: Bearer <access_token>`

---

## Authentication

### POST `/auth/login`
Login and get access token.

**Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response 200:**
```json
{
  "access_token": "jwt...",
  "refresh_token": "string",
  "user": {
    "id": "uuid",
    "email": "string",
    "name": "string"
  }
}
```

### POST `/auth/refresh`
Refresh an expired access token.

**Body:** `{ "refresh_token": "string" }`

**Response 200:** `{ "access_token": "jwt..." }`

### GET `/auth/me`
**Auth required.** Get current user info.

**Response 200:** `{ "id", "email", "name", "createdAt" }`

---

## Social Accounts

### GET `/social-accounts`
**Auth required.** List all connected social accounts.

**Response 200:**
```json
[
  {
    "id": "string",
    "platform": "instagram|tiktok|facebook|x|linkedin|youtube|pinterest|threads|bluesky",
    "username": "string",
    "displayName": "string",
    "profileImageUrl": "string|null",
    "isActive": true,
    "connectionError": "string|null",
    "tokenExpiresAt": "ISO8601|null",
    "connectedAt": "ISO8601",
    "lastUsedAt": "ISO8601|null"
  }
]
```

### GET `/social-accounts/:accountId/boards`
**Auth required.** Get Pinterest boards for an account.

**Response 200:** Array of `{ id, name, description, imageUrl }`

---

## Media

### POST `/media/create-upload-url`
**Auth required + active plan.** Create a signed upload URL for direct upload to cloud storage.

**Body:**
```json
{
  "name": "filename.jpg",
  "mime_type": "image/jpeg",
  "size_bytes": 1048576
}
```

Limits: Images max 20MB, Videos max 500MB, Audio max 50MB.

Allowed mime types: `image/jpeg`, `image/png`, `image/webp`, `image/gif`, `video/mp4`, `video/quicktime`, `video/webm`, `audio/mpeg` (mp3), `audio/wav`, `audio/mp4` (m4a), `audio/webm`

**Response 201:**
```json
{
  "media_id": "uuid",
  "upload_url": "https://storage.googleapis.com/...",
  "resumable_url": "string|null",
  "storage_path": "string",
  "expires_at": "ISO8601"
}
```

### PUT `{upload_url}`
Upload binary file directly to the signed URL (not through Posta API).

**Headers:** `Content-Type: <mime_type>`
**Body:** Raw binary file data

### POST `/media/:id/confirm-upload`
**Auth required + active plan.** Confirm upload completed — triggers server-side processing (thumbnails, variants).

**Response 202:**
```json
{
  "message": "Upload confirmed, processing started",
  "media": {
    "id": "uuid",
    "name": "string",
    "type": "image|video",
    "mime_type": "string",
    "size_bytes": 1048576,
    "width": 1024,
    "height": 1024,
    "duration": null,
    "processing_status": "processing",
    "thumbnail_url": "string|null",
    "original_url": "string|null",
    "variants": [],
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
}
```

### GET `/media`
**Auth required.** List user's media. Supports pagination and filtering.

**Query params:**
- `limit` (1-100, default 20)
- `offset` (default 0)
- `type`: `image` | `video` | `audio`
- `status`: `pending` | `processing` | `completed` | `failed`
- `sort`: `newest` | `oldest` (default `newest`)

**Response 200:** `{ items: Media[], total, limit, offset }`

### GET `/media/by-ids`
**Auth required.** Batch fetch media by id. Useful when reconciling a known set of ids (e.g. the media attached to a post) without paging through the full library.

**Query params:**
- `ids`: comma-separated UUIDs (1-50, deduplicated server-side)

**Response 200:**
```json
{
  "items": [Media, ...],
  "missing_ids": ["uuid", ...]
}
```
`items` is returned in the order ids were requested (after dedup); `missing_ids` lists ids not found or not owned by the user.

### GET `/media/:id`
**Auth required.** Get single media item with full details including variants.

### DELETE `/media/:id`
**Auth required.** Soft-delete a media item. **Response 204.**

### POST `/media/generate-carousel-pdf`
**Auth required.** Generate a PDF carousel from multiple images (one image per page).

**Body:** `{ "media_ids": ["uuid", ...], "title": "optional string" }`

**Response 201:** `{ "media_id", "thumbnail_url", "original_url", "page_count" }`

### POST `/media/generate-text-carousel-pdf`
**Auth required. Professional plan only** (other plans get `403 PLAN_LIMIT_EXCEEDED`).
Generate a PDF carousel where each page is slide text (title + body)
composited over a background image — e.g. AI-generated backgrounds → a LinkedIn document post.

**Body:** `{ "slides": [ { "media_id": "uuid", "title": "string", "body": "string" }, ... ], "title": "optional string", "logo_media_id": "optional uuid" }`
- 2–20 slides; each slide needs a `title` or `body`. `media_id` is an uploaded **image** you own (the background).
- `logo_media_id` (optional): an uploaded **image** you own, rendered in the bottom-right corner of every slide.

**Response 201:** `{ "media_id", "thumbnail_url", "original_url", "page_count" }` — `media_id` is a `document` (PDF) media item to attach to a post.

---

## Posts

### POST `/posts`
**Auth required + active plan.** Create a new post.

**Body:**
```json
{
  "caption": "string (per-platform cap, optional if mediaIds provided)",
  "hashtags": ["string"],
  "mediaIds": ["uuid"],
  "socialAccountIds": ["string (required, min 1)"],
  "scheduledAt": "ISO8601 datetime (optional)",
  "isDraft": true,
  "processingEnabled": true,
  "platformConfigurations": {
    "tiktok": {
      "privacyLevel": "PUBLIC_TO_EVERYONE",
      "allowComment": true,
      "allowDuet": false,
      "allowStitch": false,
      "contentDisclosure": false,
      "brandContentToggle": false,
      "brandOrganicToggle": false,
      "videoTitle": "string"
    },
    "pinterest": {
      "boardId": "string",
      "link": "https://...",
      "altText": "string"
    }
  }
}
```

Note: Either `caption` or at least one `mediaIds` entry is required.

**Caption limits are enforced per target platform** (tightest constraint across `socialAccountIds` wins). The outer Zod cap is 63206 (Facebook).

| Platform  | Max caption |
|-----------|-------------|
| X/Twitter | 280         |
| Bluesky   | 300         |
| Threads   | 500         |
| Pinterest | 500         |
| Instagram | 2200        |
| TikTok    | 2200        |
| LinkedIn  | 3000        |
| YouTube   | 5000        |
| Facebook  | 63206       |

A caption that exceeds the tightest platform's limit returns `400` with the platform and limit named.

**Response 201:** Full post object

### GET `/posts`
**Auth required.** List posts with pagination and filtering.

**Query params:**
- `limit` (1-100, default 20)
- `offset` (default 0)
- `status`: `draft` | `scheduled` | `processing` | `posted` | `partially_posted` | `failed`
- `isDraft`: `true` | `false`

**Response 200:** `{ items: Post[], total, limit, offset }`

### GET `/posts/calendar`
**Auth required.** Lightweight calendar view of posts.

**Query params:**
- `start`: `YYYY-MM-DD` (required)
- `end`: `YYYY-MM-DD` (required)

**Response 200:** `{ items: Post[] }`

### GET `/posts/:postId`
**Auth required.** Get a single post with full details.

### PATCH `/posts/:postId`
**Auth required + active plan.** Update a post. All fields optional.

**Body:** Same fields as create, all optional.

### DELETE `/posts/:postId`
**Auth required.** Delete a post. **Response 204.**

### POST `/posts/:postId/schedule`
**Auth required + active plan.** Schedule a post for future publishing.

**Body:** `{ "scheduledAt": "ISO8601 datetime (required)" }`

### POST `/posts/:postId/publish`
**Auth required + active plan.** Publish a post immediately.

### POST `/posts/:postId/cancel`
**Auth required.** Cancel a scheduled post (returns to draft).

---

## Analytics

### GET `/analytics/capabilities`
**Auth required + active plan.** Get analytics capabilities for user's plan tier.

### GET `/analytics/overview`
**Auth required + active plan.** Get overview stats.

**Query params:** `period` (e.g., `7d`, `30d`, `90d`), `socialAccountIds` (comma-separated)

**Response 200:**
```json
{
  "totalPosts": 42,
  "totalImpressions": 15000,
  "totalEngagements": 1200,
  "avgEngagementRate": 8.0,
  "followerChange": 150,
  "topPlatform": "instagram",
  "periodStart": "ISO8601",
  "periodEnd": "ISO8601"
}
```

### GET `/analytics/posts`
**Auth required + starter plan.** Get analytics for all posts. Paginated, sortable.

**Query params:** `limit`, `offset`, `sortBy` (e.g., `engagements`, `impressions`), `sortOrder` (`asc`|`desc`), `socialAccountIds`

### GET `/analytics/posts/:postId`
**Auth required + starter plan.** Detailed analytics for a single post.

### GET `/analytics/best-times`
**Auth required + starter plan.** Get best posting times as a heatmap.

**Response 200:** Heatmap data by day-of-week and hour with engagement scores.

### GET `/analytics/trends`
**Auth required + active plan.** Get trend data for charts.

**Query params:** `period`, `metric` (`impressions`|`engagements`|`engagement_rate`), `socialAccountIds`

### GET `/analytics/content-types`
**Auth required + starter plan.** Content type performance breakdown.

### GET `/analytics/hashtags`
**Auth required + professional plan.** Hashtag performance analysis.

### GET `/analytics/compare`
**Auth required + professional plan.** Compare 2-4 posts side by side.

**Query params:** `postIds` (comma-separated, 2-4 IDs)

### GET `/analytics/export/csv`
**Auth required + professional plan.** Export analytics as CSV.

### GET `/analytics/export/pdf`
**Auth required + professional plan.** Export analytics as PDF.

### GET `/analytics/benchmarks`
**Auth required + professional plan.** Engagement benchmarks for your niche.

### POST `/analytics/refresh/:postResultId`
**Auth required + starter plan.** Manually refresh analytics for a single post.

### POST `/analytics/refresh-all`
**Auth required + starter plan.** Refresh all analytics (rate limited: 1 per hour).

---

## Users

### GET `/users/plan`
**Auth required.** Get current plan info, limits, and usage.

**Response 200:**
```json
{
  "plan": "trial|starter|professional",
  "limits": {
    "posts": 10,
    "socialAccounts": 3,
    "mediaStorage": "500MB"
  },
  "usage": {
    "posts": 5,
    "socialAccounts": 2,
    "mediaStorage": "120MB"
  },
  "expiresAt": "ISO8601|null"
}
```

### GET `/users/profile`
**Auth required.** Get user profile.

### PATCH `/users/profile`
**Auth required.** Update user profile.

---

## Platforms

### GET `/platforms`
**Public.** List all supported platforms with summaries.

### GET `/platforms/specifications`
**Public.** Get full platform specifications (character limits, media requirements, supported features).

### GET `/platforms/aspect-ratios`
**Public.** Get aspect ratio reference for all platforms.

### GET `/platforms/:platformId`
**Public.** Get detailed specs for a specific platform.
