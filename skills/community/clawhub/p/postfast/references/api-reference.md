# PostFast API Reference

Base URL: `https://api.postfa.st`
Auth: `pf-api-key` header with workspace API key.

## Endpoints

### GET /social-media/my-social-accounts

List all connected social media accounts.

**Response:**
```json
[
  {
    "id": "6a87b56e-ba73-4696-a415-3d524f1a92f8",
    "platform": "FACEBOOK",
    "platformUsername": "johndoe",
    "displayName": "John's Page",
    "connectionStatus": "CONNECTED",
    "disabledReason": null,
    "followerCount": "102",
    "followerCountUpdatedAt": "2026-06-13T00:00:00.000Z"
  }
]
```

Platform values: `TIKTOK`, `INSTAGRAM`, `FACEBOOK`, `X`, `YOUTUBE`, `LINKEDIN`, `THREADS`, `BLUESKY`, `PINTEREST`, `TELEGRAM`, `GOOGLE_BUSINESS_PROFILE`

**Connection status** (on every account):
- `connectionStatus` (enum, always present) — `CONNECTED` = healthy; `DISABLED` = paused, needs reconnect, won't publish.
- `disabledReason` (enum, nullable) — `null` when `CONNECTED`; when `DISABLED`, one of `TOKEN_REVOKED`, `ACCOUNT_SUSPENDED`, `PERMISSION_REVOKED`, `MANUAL`. Only `TOKEN_REVOKED` and `ACCOUNT_SUSPENDED` are emitted today; the other two are reserved so the enum stays forward-stable.
- `followerCount` (string, nullable) / `followerCountUpdatedAt` (ISO 8601, nullable) — latest daily follower or subscriber count for the account, populated once PostFast has fetched it.

Pre-check `connectionStatus` before scheduling — posting to a `DISABLED` account returns `400 socialMediaDisconnected` (see `POST /social-posts`).

### GET /social-media/:id/pinterest-boards

Get Pinterest boards for a connected account.

**Response:**
```json
[{ "boardId": "1234567890123456789", "name": "My Recipes" }]
```

### GET /social-media/:id/youtube-playlists

Get YouTube playlists for a connected account.

**Response:**
```json
[{ "playlistId": "PLrAXtmErZgOe...", "title": "My Tutorials" }]
```

### GET /social-media/:id/gbp-locations

Get Google Business Profile locations for a connected account.

**Response:**
```json
[
  {
    "id": "a1b2c3d4-...",
    "locationId": "accounts/109049740544589765860/locations/4875357571247123933",
    "title": "PostFast HQ",
    "address": "123 Main St, Sofia, Bulgaria",
    "mapsUri": "https://maps.google.com/?cid=..."
  }
]
```

Use the `locationId` value as `gbpLocationId` in the controls object when creating GBP posts.

### GET /social-media/search-places

Search real-world places (restaurants, venues, hotels, landmarks) to geotag Facebook and Instagram posts. Rate limit: 90 requests/hour.

**Query params:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string | yes | Search text, min 2 characters (e.g. `q=eiffel tower`). Returns up to 100 matching places (Facebook's per-call maximum) |

Only Facebook Pages that carry address data are returned (you cannot get a non-place Page back), so narrow queries return fewer, more relevant results. Results are cached 7 days server-side.

**Request:**
```bash
curl -G "https://api.postfa.st/social-media/search-places" \
  --data-urlencode "q=national palace of culture" \
  -H "pf-api-key: YOUR_API_KEY"
```

**Response:**
```json
[
  {
    "id": "1559011447688271",
    "name": "Национален дворец на културата - НДК",
    "link": "https://www.facebook.com/1559011447688271",
    "city": "Sofia",
    "country": "Bulgaria",
    "street": "пл. България №1",
    "zip": "1463",
    "pictureUrl": "https://graph.facebook.com/1559011447688271/picture?type=small"
  }
]
```

- `id` (string, required) — numeric Facebook Page ID with location data. Use it as `facebookPlaceId` on Facebook and as `instagramLocationId` on Instagram. Resolve a place once, geotag it on either network.
- `name` (string, required) — place name.
- `link` (string, optional) — the place's Facebook Page URL. Nullable; useful as a "view on Facebook" link so the user can confirm the right place.
- `city`, `country`, `street`, `zip`, `pictureUrl` (all optional) — present only when the Page exposes them.

Set the matching geotag via the `controls` object on `POST /social-posts` (see `facebookPlaceId` / `instagramLocationId` below).

### POST /file/get-signed-upload-urls

Get pre-signed S3 URLs for media upload.

**Request:**
```json
{ "contentType": "image/png", "count": 1 }
```

Supported content types: `image/png`, `image/jpeg`, `image/jpg`, `image/gif`, `image/webp`, `video/mp4`, `video/quicktime`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/vnd.openxmlformats-officedocument.presentationml.presentation`

**Response:**
```json
[{ "key": "image/a1b2c3d4-e5f6-7890-1234-567890abcdef.png", "signedUrl": "https://s3..." }]
```

Then PUT the raw file to `signedUrl` with matching `Content-Type` header.

### GET /social-posts

List and filter posts. Supports pagination, platform/status filtering, and date ranges.

**Query params:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | 0-based page index |
| `limit` | int | 20 | Items per page (max 50) |
| `platforms` | string | — | Comma-separated: `FACEBOOK,INSTAGRAM,X,TIKTOK,LINKEDIN,YOUTUBE,BLUESKY,THREADS,PINTEREST,TELEGRAM,GOOGLE_BUSINESS_PROFILE` |
| `statuses` | string | — | Comma-separated: `DRAFT,SCHEDULED,PUBLISHED,FAILED` |
| `from` | ISO 8601 | — | Start date filter (inclusive, on `scheduledAt`) |
| `to` | ISO 8601 | — | End date filter (inclusive, on `scheduledAt`) |

Sorting is fixed to `scheduledAt` ascending. Platform and status values are case-insensitive.

**Response:**
```json
{
  "data": [
    {
      "id": "post-uuid",
      "content": "Post text",
      "status": "DRAFT | SCHEDULED | PUBLISHED | FAILED",
      "approvalStatus": "PENDING_APPROVAL | IN_PROGRESS | APPROVED | REJECTED | NEEDS_WORK",
      "socialMediaId": "account-uuid",
      "mediaItems": [{ "key": "image/...", "type": "IMAGE", "url": "https://...", "sortOrder": 0, "coverImageKey": "image/... | null", "coverTimestamp": "5000 | null", "coverImageUrl": "https://... | null", "coverImageUpdatedUrl": "https://... | null" }],
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "publishedAt": "2026-06-15T10:00:05.000Z | null",
      "failedAt": "... | null",
      "platformPostId": "string | null",
      "groupId": "uuid | null",
      "lastError": { "message": "User-friendly error", "code": "platform-code" },
      "firstComment": "string | null",
      "firstCommentError": "string | null"
    }
  ],
  "totalCount": 25,
  "pageInfo": { "page": 1, "hasNextPage": true, "perPage": 20 }
}
```

`lastError` (nullable, `{ message, code }`) is set on failed and missed posts. Beyond platform-specific error codes, two `code` values flag missed posts:
- `MISSED_DISCONNECTED` — the post came due while its account was `DISABLED`, so it didn't publish. Reconnect the account, then retry the post.
- `MISSED_NOT_PUBLISHED` — the post passed its scheduled time plus a 2-hour grace window without publishing.

Rate limit: 200 requests/hour.

### POST /social-posts

Create/schedule one or more posts. Up to 15 posts per request. Rate limit: 350/day.

**Request:**
```json
{
  "posts": [
    {
      "content": "Post text with #hashtags",
      "mediaItems": [
        {
          "key": "image/uuid.png",
          "type": "IMAGE",
          "sortOrder": 0
        }
      ],
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "socialMediaId": "account-uuid",
      "firstComment": "Check out our link: https://example.com"
    }
  ],
  "status": "SCHEDULED",
  "approvalStatus": "APPROVED",
  "controls": {
    "tiktokPrivacy": "PUBLIC",
    "instagramPublishType": "REEL"
  }
}
```

**Post fields:**
- `content` (string, required): Post text/caption
- `mediaItems` (array): Media attachments. Each has `key` (from upload), `type` (`IMAGE`/`VIDEO`), `sortOrder` (int)
- `scheduledAt` (string): ISO 8601 UTC, must be in the future. Optional for draft posts
- `socialMediaId` (string, required): Target account ID from `/my-social-accounts`
- `firstComment` (string, optional): Auto-posted ~10s after publish. Supported: X, Instagram, Facebook, YouTube, Threads. NOT supported: TikTok, Pinterest, Bluesky, LinkedIn

**Top-level fields:**
- `status` (string): `DRAFT` or `SCHEDULED` (default: `SCHEDULED`). Drafts don't need `scheduledAt`
- `approvalStatus` (string): `APPROVED` or `PENDING_APPROVAL` (default: `APPROVED`)
- `controls` (object): Platform-specific settings. See platform-controls.md for all options

**mediaItems extra fields:**
- `coverImageKey` (string, optional): S3 key of a custom cover/thumbnail image for video posts. Upload the image first via `POST /file/get-signed-upload-urls`, then include the key here. Supported on: Instagram Reels (JPEG only, max 8MB), Facebook Reels (any format, max 10MB), Pinterest video (JPEG/PNG). NOT supported on TikTok or YouTube (use `coverTimestamp` for TikTok, `youtubeThumbnailKey` in controls for YouTube)
- `coverTimestamp` (string, optional): Milliseconds into the video to extract a frame as cover (e.g., `"5000"` = 5 seconds). Acts as fallback when `coverImageKey` is also provided. Supported on: Instagram Reels, TikTok, Pinterest video. NOT supported on Facebook Reels or YouTube

**Cover image priority:** 1) `coverImageKey` if provided, 2) `coverTimestamp` as fallback, 3) platform auto-selects if neither is set

**Controls extra notes:**
- `youtubeThumbnailKey` (string): S3 key for custom YouTube thumbnail (from upload flow). JPEG/PNG recommended, max 2MB, 1280x720 (16:9). Requires phone-verified channel. If thumbnail upload fails, video still publishes without it
- `facebookPlaceId` / `instagramLocationId` (string): geotag the post with a place ID from `GET /social-media/search-places`. Same numeric ID for both. `facebookPlaceId` is Facebook feed posts only (text/photo/carousel, not Reels/Stories/video); `instagramLocationId` is a single image/video/reel/story (not carousels)
- `facebookPlaceName` / `instagramLocationName` (string): optional display-only label for the place. Stored for your dashboard; never sent to Meta
- `facebookTargetCountries` (string[]): restrict a Facebook feed post to up to 25 ISO 3166-1 alpha-2 country codes (case-insensitive). Audience gating, so the post is hidden from everyone else and from logged-out users. Can combine with `facebookPlaceId`
- `tiktokTitle` (string): TikTok photo-carousel title, max 90 chars. When set, `content` becomes the description

**Cross-posting**: Add multiple objects to the `posts` array, each with different `socialMediaId`. The `controls` object applies to all posts in the batch.

**Platform posting limits:** X (Twitter) allows max 5 posts per account per day via API. Google Business Profile allows max 5 posts per account per day.

**Response:**
```json
{ "postIds": ["uuid-1", "uuid-2"] }
```

One ID per entry in the `posts` array.

**Error — scheduling to a disconnected account (`400`):**
```json
{
  "statusCode": 400,
  "message": "socialMediaDisconnected",
  "error": "BAD_REQUEST",
  "description": "This INSTAGRAM account is disconnected. Reconnect it before scheduling posts."
}
```
Fires only when scheduling (`status: SCHEDULED` or `scheduledAt` set). **Drafts to a disconnected account are still allowed.** `message` is the stable machine key — branch on it; show `description` to the user. Best practice: check `connectionStatus` from `GET /social-media/my-social-accounts` first so it fails before the request.

**Geo controls validation errors (`400`):** the `message` field carries a stable code.

| Situation | `message` code |
|---|---|
| Geo field sent for the wrong platform | `facebookPlaceId.notSupported` / `instagramLocationId.notSupported` / `facebookTargetCountries.notSupported` |
| Geotag on a Facebook Reel or Story | `facebookPlaceId.contentType.notSupported` |
| Geotag on a Facebook video post | `facebookPlaceId.video.notSupported` |
| Geotag on an Instagram carousel | `instagramLocationId.carousel.notSupported` |
| Country limit on a Facebook Reel or Story | `facebookTargetCountries.contentType.notSupported` |
| More than 25 countries | `facebookTargetCountries.tooMany` |
| Non-numeric place/location ID | `facebookPlaceId.invalidId` / `instagramLocationId.invalidId` |

### POST /social-media/connect-link

Generate a secure link for clients to connect their social accounts to your workspace — no PostFast account required. Rate limit: 50/hour.

**Request:**
```json
{
  "expiryDays": 7,
  "sendEmail": true,
  "email": "client@example.com"
}
```

- `expiryDays` (int, optional): 1-30, default 7
- `sendEmail` (bool, optional): Send link via email, default false
- `email` (string): Required when `sendEmail` is true

**Response:**
```json
{ "connectUrl": "https://app.postfa.st/connect?token=eyJhbGci..." }
```

Share the `connectUrl` with the client. The token is a JWT — do not truncate it.

### DELETE /social-posts/:id

Delete a scheduled post by ID.

**Response:**
```json
{ "deleted": true }
```

## Error Responses

| Code | Meaning |
|------|---------|
| `400` | Bad request — missing fields, invalid data, scheduledAt in the past |
| `400` `socialMediaDisconnected` | Scheduling to a disconnected account — reconnect it first (drafts are allowed) |
| `401` | Invalid or missing API key |
| `403` | Forbidden — insufficient permissions |
| `404` | Resource not found |
| `429` | Rate limit exceeded — check `Retry-After-*` header |

## Rate Limits

Per API key (workspace):
- 60 requests/minute
- 150 requests/5 minutes
- 300 requests/hour
- 2,000 requests/day

Response headers: `X-RateLimit-Limit-*`, `X-RateLimit-Remaining-*`, `X-RateLimit-Reset-*`, `Retry-After-*`
