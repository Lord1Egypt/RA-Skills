# PostFast API Reference

Base URL: `https://api.postfa.st`
Auth: `pf-api-key` header with workspace API key.

Rate limits are counted per endpoint, per API key. Each endpoint below lists its own limits; see [Rate Limits](#rate-limits) at the end for the defaults, the headers and the 429 response.

Unknown body fields and unknown query parameters are ignored, not rejected. A misspelled name returns no error and has no effect.

## Endpoints

### GET /social-media/my-social-accounts

List all connected social media accounts. Rate limit: 1,260/hour, 12,600/day.

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
    "inboxCapable": true,
    "followerCount": "102",
    "followerCountUpdatedAt": "2026-06-13T00:00:00.000Z"
  }
]
```

Platform values: `TIKTOK`, `INSTAGRAM`, `FACEBOOK`, `X`, `YOUTUBE`, `LINKEDIN`, `THREADS`, `BLUESKY`, `PINTEREST`, `TELEGRAM`, `GOOGLE_BUSINESS_PROFILE`

**Connection status** (on every account):
- `connectionStatus` (enum, always present): `CONNECTED` = healthy; `DISABLED` = paused, needs a reconnect in the PostFast app, won't publish.
- `disabledReason` (enum, nullable): `null` when `CONNECTED`; when `DISABLED`, one of `TOKEN_REVOKED`, `ACCOUNT_SUSPENDED`, `PERMISSION_REVOKED`, `MANUAL`.
- While an account is `DISABLED`, posts already scheduled to it are held, not deleted: they resume on reconnect, or are marked `FAILED` if their scheduled time passes while it is still disabled. Scheduling a NEW post to it returns `400 socialMediaDisconnected` (see `POST /social-posts`); saving a draft is still allowed.

**Other fields:**
- `inboxCapable` (boolean): `true` when comments on this account's posts reach the Social Inbox (TikTok, Instagram, Facebook Page and Threads connections). Facebook and Threads accounts connected before the inbox launched need one reconnect first.
- `followerCount` (string, nullable) / `followerCountUpdatedAt` (ISO 8601, nullable): the latest daily follower or subscriber count, refreshed once a day around 04:00 UTC. Instagram, Facebook Pages, YouTube (approximate; hidden-subscriber channels return null), Threads, Pinterest, Bluesky, Telegram (the PostFast bot must stay in the chat), LinkedIn organization Pages and TikTok. Not available on X or Google Business Profile.

**Recent posts imported on connect:** when a Facebook Page, Instagram, Threads or TikTok account is connected or reconnected, PostFast imports the posts published on it in the last 60 days (including posts not created through PostFast), so they appear in `GET /social-posts` and in analytics. The import runs in the background and skips posts that are already there. Metrics fill in shortly after (TikTok can take 24-48h); imported TikTok posts have no stored thumbnail.

### GET /social-media/:id/pinterest-boards

Get Pinterest boards for a connected account. Rate limit: 330/hour, 3,300/day.

**Response:**
```json
[{ "id": "internal-uuid", "boardId": "1234567890123456789", "name": "My Recipes", "description": "", "imageUrl": "https://..." }]
```

Use `boardId` (not `id`) as `pinterestBoardId`. Boards created after the account was connected don't sync on their own: the user clicks Sync Boards in the dashboard.

### GET /social-media/:id/youtube-playlists

Get YouTube playlists for a connected account. Rate limit: 330/hour, 3,300/day.

**Response:**
```json
[{ "id": "internal-uuid", "playlistId": "PLrAXtmErZgOe...", "title": "My Tutorials", "description": "", "thumbnailUrl": "https://..." }]
```

Use `playlistId` (not `id`) as `youtubePlaylistId`.

### GET /social-media/:id/gbp-locations

Get Google Business Profile locations for a connected account. Rate limit: 330/hour, 3,300/day.

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

Use the `locationId` value as `gbpLocationId` in the controls object when creating GBP posts. A location that is missing appears after Sync Locations in the dashboard.

### GET /social-media/:id/follower-history

Daily follower/subscriber snapshots for a connected account, plus the current count and net change over the range. Rate limit: 720/hour, 7,200/day.

**Query params:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `from` | ISO 8601 | no | Range start. Defaults to 90 days ago |
| `to` | ISO 8601 | no | Range end. Defaults to now. Range capped at 365 days |

**Response:**
```json
{
  "socialMediaId": "account-uuid",
  "series": [
    { "capturedAt": "2026-05-01T00:00:00.000Z", "followerCount": "102" },
    { "capturedAt": "2026-05-02T00:00:00.000Z", "followerCount": "104" }
  ],
  "currentFollowerCount": "106",
  "delta": "4",
  "trackingStartedAt": "2026-04-20T00:00:00.000Z"
}
```

- All counts are strings (bigint). `series` is oldest-first. `delta` is the signed net change across the range (`"-123"` for a drop, `"57"` for growth, no leading `+`). `series` and `delta` cover the requested range; `currentFollowerCount` and `trackingStartedAt` cover the account's whole history.
- Tracking is **forward-only**: snapshots start at `trackingStartedAt` (when PostFast began recording the account); there is no backfill before that. `currentFollowerCount`, `delta`, and `trackingStartedAt` may be absent until the first snapshot lands.
- An id that isn't in your workspace returns `200` with an empty `series`; a non-UUID returns `400`.
- **Coverage:** Facebook Pages, Instagram, YouTube, Pinterest, Threads, Bluesky, Telegram, LinkedIn company pages, TikTok. **Not available:** X, Google Business Profile, personal accounts.

### GET /social-media/search-places

Search real-world places (restaurants, venues, hotels, landmarks) to geotag Facebook and Instagram posts. Rate limit: 110/hour.

**Query params:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string | yes | Search text, min 2 characters (e.g. `q=eiffel tower`). Returns up to 100 matching places (Facebook's per-call maximum) |

Only Facebook Pages that carry address data are returned (you cannot get a non-place Page back), so narrow queries return fewer, more relevant results. Results are cached 7 days server-side.

**Request:**
```bash
curl -G "https://api.postfa.st/social-media/search-places" \
  --data-urlencode "q=national palace of culture" \
  -H "pf-api-key: $POSTFAST_API_KEY"
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

- `id` (string, required): numeric Facebook Page ID with location data. Use it as `facebookPlaceId` on Facebook and as `instagramLocationId` on Instagram. Resolve a place once, geotag it on either network.
- `name` (string, required): place name.
- `link` (string, optional): the place's Facebook Page URL. Nullable; useful as a "view on Facebook" link so the user can confirm the right place.
- `city`, `country`, `street`, `zip`, `pictureUrl` (all optional): present only when the Page exposes them.

Set the matching geotag via the `controls` object on `POST /social-posts` (see `facebookPlaceId` / `instagramLocationId` below).

### GET /social-media/:id/tiktok-sounds

TikTok's trending, pre-cleared Commercial Music Library sounds for a connected TikTok account, ranked by the genre, country and time window you choose. Rate limit: 110/hour.

**Query params:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `genre` | string | all genres | Raw TikTok genre value, e.g. `POP`, `HIP_HOP/RAP`, `R&B/SOUL`, `K-POP`. URL-encode `/` and `&` (`HIP_HOP%2FRAP`) |
| `countryCode` | string | `US` | Two-letter uppercase country code |
| `dateRange` | string | `7DAY` | `1DAY`, `7DAY`, `30DAY` or `90DAY` |

**Response:** up to 100 sounds, already ordered by trending rank (no pagination):
```json
[
  {
    "musicSoundId": "7xxxxxxxxxxxxxxxxxx",
    "name": "Track name",
    "artist": "Artist",
    "duration": 30,
    "thumbnailUrl": "https://...",
    "previewUrl": "https://...",
    "rankPosition": 1,
    "genres": ["POP"],
    "commercialMusicId": "...",
    "fullDurationClipId": "...",
    "trendingClipId": "..."
  }
]
```

- Use `musicSoundId` as `controls.tiktokMusicSoundId` on a TikTok photo carousel or video (plus `tiktokMusicSoundName` as a display label). `duration` is the seconds of the exact clip; `previewUrl` plays exactly what gets attached.
- The list rotates roughly daily and each filter combination is cached about 6 hours: fetch fresh ids per session instead of reusing stored ones.
- Errors: `400 tiktokSounds.invalidGenre`, `400 tiktokSounds.invalidCountryCode`, `400 tiktokSounds.invalidDateRange`; `404 tiktokSounds.socialMediaNotFound` when the id isn't a TikTok account in this workspace; `400 tiktokMusic.requiresBusinessApi` for an account connected long ago, until it is reconnected once. A valid country with no TikTok chart returns `200 []`.

### POST /file/get-signed-upload-urls

Get pre-signed S3 URLs for media upload. Rate limit: 180/minute, 420/day.

**Request:**
```json
{ "contentType": "image/png", "count": 1 }
```

Accepted content types: `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `video/mp4`, `video/webm`, `video/mov`, `video/quicktime`, `application/pdf`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/vnd.ms-powerpoint`, `application/vnd.openxmlformats-officedocument.presentationml.presentation`, `application/x-subrip` (.srt), `text/vtt` (.vtt). Anything else (including `image/jpg`, use `image/jpeg`) returns `400`.

Size caps: 250MB per video (Bluesky 100MB, Telegram 50MB), 10MB per image, 60MB per document, 10MB per caption file (SRT/VTT).

**Response:**
```json
[{ "key": "image/a1b2c3d4-e5f6-7890-1234-567890abcdef.png", "signedUrl": "https://s3..." }]
```

Then PUT the raw file to `signedUrl` with a `Content-Type` header that matches the requested `contentType`. Images get `image/` keys, videos `video/`, documents and caption files `file/` (for example `file/uuid.srt`).

### GET /social-posts

List and filter posts. Supports pagination, account/post/platform/status filtering, and date ranges. Rate limit: 720/hour, 7,200/day.

**Query params:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | 0-based page index |
| `limit` | int | 20 | Items per page (1-50) |
| `socialMediaIds` | string | | Comma-separated account UUIDs, max 100: only these accounts' posts |
| `ids` | string | | Comma-separated post UUIDs, max 100 |
| `platforms` | string | | Comma-separated: `FACEBOOK,INSTAGRAM,X,TIKTOK,LINKEDIN,YOUTUBE,BLUESKY,THREADS,PINTEREST,TELEGRAM,GOOGLE_BUSINESS_PROFILE` |
| `statuses` | string | | Comma-separated: `DRAFT,SCHEDULED,PUBLISHED,FAILED` |
| `from` | ISO 8601 | | Start date filter (inclusive, on `scheduledAt`) |
| `to` | ISO 8601 | | End date filter (inclusive, on `scheduledAt`) |

- All filters are AND-ed. `ids` and `socialMediaIds` are workspace-scoped, so ids from another workspace match nothing (`200`, no posts).
- To skip a filter, leave the parameter out: an empty value (`ids=`), a trailing comma, a non-UUID or more than 100 entries returns `400` (e.g. "Each socialMediaId must be a valid UUID").
- Unknown query parameters are ignored: the singular `socialMediaId` is not a filter and returns every account's posts.
- Results are ordered by `scheduledAt`, then `id`. Platform and status values are case-insensitive.
- Pages are offset-based: deleting while you walk the pages shifts later posts onto pages you have already read. To delete everything matching a filter, re-read `page=0` until it comes back empty (see `POST /social-posts/bulk-delete`).
- When nothing matches, `data` is `[]` and `totalCount` is `null`, not `0`.

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
      "firstCommentError": "string | null",
      "controls": {
        "threadsTopicTag": null,
        "instagramPublishType": "TIMELINE",
        "facebookContentType": "POST",
        "tiktokIsDraft": false,
        "youtubePrivacy": "PUBLIC"
      }
    }
  ],
  "totalCount": 25,
  "pageInfo": { "page": 1, "hasNextPage": true, "perPage": 20 }
}
```

- A post has no `platform` field: map `socialMediaId` to `GET /social-media/my-social-accounts`.
- `controls` holds the stored settings that decide a post's format, visibility or topic. Posts created over the API carry every platform's defaults, so read only the field for the post's own platform.
- The list includes posts imported from the platform when an account was connected.

`lastError` (nullable, `{ message, code }`) is set on failed and missed posts. Beyond platform-specific error codes, two `code` values flag missed posts:
- `MISSED_DISCONNECTED`: the post came due while its account was `DISABLED`, so it didn't publish. Reconnect the account, then retry the post.
- `MISSED_NOT_PUBLISHED`: the post passed its scheduled time plus a 2-hour grace window without publishing.

### POST /social-posts

Create/schedule one or more posts. Up to 15 posts per request. Rate limit: 180/minute, 420/day.

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
    "tiktokAllowComments": true,
    "instagramPublishType": "REEL"
  }
}
```

**Post fields:**
- `content` (string, required): Post text/caption
- `mediaItems` (array): Media attachments. Each has `key` (from upload), `type` (`IMAGE`/`VIDEO`, must match the file), `sortOrder` (int)
- `scheduledAt` (string): ISO 8601 UTC, must be in the future. Required unless the request is a `DRAFT`
- `socialMediaId` (string, required): Target account ID from `/my-social-accounts`
- `firstComment` (string, optional): Auto-posted ~10s after publish (up to 3 attempts). Supported: X, Instagram, Facebook, YouTube, Threads, and TikTok (TikTok: max 1,200 chars, comments must be enabled on the post; an account that can't post comments returns `firstComment.tiktok.notSupported`). NOT supported: Pinterest, Bluesky, LinkedIn, Google Business Profile (validation error)

**Top-level fields:**
- `status` (string): `DRAFT` or `SCHEDULED` (default: `SCHEDULED`). Drafts don't need `scheduledAt`
- `approvalStatus` (string): `APPROVED` or `PENDING_APPROVAL` (default: `APPROVED`). `PENDING_APPROVAL` holds the post for review in PostFast
- `controls` (object): Platform-specific settings, shared by every post in the request (there are no per-post controls). See platform-controls.md for all options

**mediaItems extra fields:**
- `coverImageKey` (string, optional): S3 key of a custom cover/thumbnail image for video posts. Upload the image first via `POST /file/get-signed-upload-urls`, then include the key here. Supported on: Instagram Reels (JPEG only, max 8MB), Facebook Reels (any format, max 10MB), Pinterest video (JPEG/PNG). NOT supported on TikTok or YouTube (use `coverTimestamp` for TikTok, `youtubeThumbnailKey` in controls for YouTube)
- `coverTimestamp` (string, optional): Milliseconds into the video to extract a frame as cover (e.g., `"5000"` = 5 seconds). Acts as fallback when `coverImageKey` is also provided. Supported on: Instagram Reels, TikTok, Pinterest video. NOT supported on Facebook Reels or YouTube

**Cover image priority:** 1) `coverImageKey` if provided, 2) `coverTimestamp` as fallback, 3) platform auto-selects if neither is set

**Controls extra notes:**
- `youtubeThumbnailKey` (string): S3 key for custom YouTube thumbnail (from upload flow). JPEG/PNG recommended, max 2MB, 1280x720 (16:9). Requires phone-verified channel. If thumbnail upload fails, video still publishes without it
- `youtubeLanguage` (string): the video's language as a BCP-47 code (`en`, `en-GB`, `es`, `es-419`, `fr`, `pt-BR`); sets YouTube's video language and title/description language. PostFast normalizes the code (`pt-br` becomes `pt-BR`). Creation-only
- `youtubeCaptionKey` (string): an uploaded .srt or .vtt file (`file/uuid.srt` or `.vtt`, from `contentType` `application/x-subrip` or `text/vtt`), added as a caption track in `youtubeLanguage` right after the video uploads. Needs `youtubeLanguage`; one track per video; timed SRT/WebVTT in plain UTF-8, max 10MB, checked at creation. If the captions can't be added at publish, the video publishes without them. Creation-only
- `facebookPlaceId` / `instagramLocationId` (string): geotag the post with a place ID from `GET /social-media/search-places`. Same numeric ID for both. `facebookPlaceId` is Facebook feed posts only (text/photo/carousel, not Reels/Stories/video); `instagramLocationId` is a single image/video/reel/story (not carousels)
- `facebookPlaceName` / `instagramLocationName` (string): optional display-only label for the place. Stored for your dashboard; never sent to Meta
- `facebookTargetCountries` (string[]): restrict a Facebook feed post to up to 25 ISO 3166-1 alpha-2 country codes (case-insensitive). Audience gating, so the post is hidden from everyone else and from logged-out users. Can combine with `facebookPlaceId`
- `tiktokTitle` (string): TikTok photo-carousel title, max 90 chars. When set, `content` becomes the description
- `tiktokMusicSoundId` (string, max 128) / `tiktokMusicSoundName` (string, max 256, display-only): a licensed track from `GET /social-media/:id/tiktok-sounds`, added by TikTok at publish, on a photo carousel or a video (on a video the track and the original sound each play at 50%). Mutually exclusive with `tiktokAutoAddMusic: true`, which is photo-only. Not applied to TikTok app drafts
- `threadsTopicTag` (string): the post's topic on Threads, 1-50 chars, no `.` or `&`. If the text also has a #hashtag, the topic wins and the hashtag stays plain text
- `tiktokIsAigc` / `instagramIsAiGenerated` / `youtubeContainsSyntheticMedia` (boolean, default false): AI disclosure labels, each ignored by the other platforms. Creation-only: there is no update route, and Instagram's label can't be removed after publishing

**Cross-posting**: Add multiple objects to the `posts` array, each with different `socialMediaId`. The `controls` object applies to all posts in the batch, so posts that need different settings go in separate requests.

**Posting limits** (PostFast Fair Usage Policy, per social account per day, tracked across every workspace the account is in, reset at midnight UTC): Instagram 35, Facebook 25, LinkedIn 35, TikTok 15, YouTube 10, Pinterest 15, Bluesky 70, Threads 65, Telegram 25, Google Business Profile 5, X 6 (9 on Pro and Enterprise). X also has a plan-based daily pool shared by the organization and a monthly allowance of posts containing a link. Plans also cap how many posts can sit in the queue at once and how many drafts can be stored: Starter 150 / 50, Creator 1,500 / 600, Growth 3,000 / 2,000, Pro 50,000 / 50,000, Enterprise 80,000 / 80,000. Source of truth: https://postfa.st/fair-usage

**Response:**
```json
{ "postIds": ["uuid-1", "uuid-2"] }
```

One ID per entry in the `posts` array.

**Error: scheduling to a disconnected account (`400`):**
```json
{
  "statusCode": 400,
  "message": "socialMediaDisconnected",
  "error": "BAD_REQUEST",
  "description": "This INSTAGRAM account is disconnected. Reconnect it before scheduling posts."
}
```
Fires only when scheduling (`status: SCHEDULED` or `scheduledAt` set). **Drafts to a disconnected account are still allowed.** `message` is the stable machine key, so branch on it and show `description` to the user. Best practice: check `connectionStatus` from `GET /social-media/my-social-accounts` first so it fails before the request.

**Other validation codes (`400`, in `message`):**

| Situation | `message` code |
|---|---|
| Both `tiktokMusicSoundId` and `tiktokAutoAddMusic: true` | `tiktokMusic.conflictAutoAddMusic` |
| Invalid Threads topic | `threadsTopicTag.invalid` |
| First comment on a TikTok account that can't post comments | `firstComment.tiktok.notSupported` |
| Geo field sent for the wrong platform | `facebookPlaceId.notSupported` / `instagramLocationId.notSupported` / `facebookTargetCountries.notSupported` |
| Geotag on a Facebook Reel or Story | `facebookPlaceId.contentType.notSupported` |
| Geotag on a Facebook video post | `facebookPlaceId.video.notSupported` |
| Geotag on an Instagram carousel | `instagramLocationId.carousel.notSupported` |
| Country limit on a Facebook Reel or Story | `facebookTargetCountries.contentType.notSupported` |
| More than 25 countries | `facebookTargetCountries.tooMany` |
| Non-numeric place/location ID | `facebookPlaceId.invalidId` / `instagramLocationId.invalidId` |
| Caption file missing, empty, over 10MB, or not timed SRT/WebVTT in plain UTF-8 | `media.invalidMedia` |
| `youtubeCaptionKey` that isn't a `file/uuid.srt` or `.vtt` upload (checked on every platform) | `youtubeCaptionKey.invalid` |
| YouTube post with a caption key but no `youtubeLanguage` | `youtubeCaptionKey.languageRequired` |
| Unknown `youtubeLanguage` code on a YouTube post | `youtubeLanguage.invalid` |

### DELETE /social-posts/:id

Delete one post, in any status. Rate limit: 200/hour.

**Response:**
```json
{ "deleted": true }
```

- An id that doesn't exist or belongs to another workspace returns `200` with `{ "deleted": false }`, never a `404`. A non-UUID returns `400`.
- It removes the post, its schedule and its analytics from PostFast, and its media files once nothing else in PostFast uses them. PostFast never calls the social platform: a post that is already published stays live there, and a scheduled post that hasn't published yet will not publish.

### POST /social-posts/bulk-delete

Delete up to 100 posts in one request. Rate limit: 200/hour (its own budget, separate from `DELETE /social-posts/:id`); one call counts as one request.

**Request:**
```json
{ "ids": ["post-uuid-1", "post-uuid-2"] }
```

**Response (`200`, not 201):**
```json
{ "deletedIds": ["post-uuid-1"], "notFoundIds": ["post-uuid-2"] }
```

- `ids` is required: 1-100 post UUIDs, each a UUID v4. `[]` returns `400` "At least one id is required", more than 100 returns `400` "ids cannot exceed 100 entries", a non-UUID returns `400` "Each id must be a valid UUID".
- `notFoundIds` holds the ids that don't exist or belong to another workspace (both get the same answer). A repeated id is reported once, and repeating a call with the same ids is harmless (they all come back in `notFoundIds`).
- Deletes the same way as `DELETE /social-posts/:id`: any status, PostFast only, published posts stay live on the platform.
- **Delete everything that matches a filter:** re-read `GET /social-posts` at `page=0` with the same filter and bulk-delete what it returns until it comes back empty. Stop on any error, including a `429`; wait `Retry-After` seconds and continue.

### GET /social-posts/analytics

Published posts with their latest performance metrics. Rate limit: 1,260/hour, 12,600/day.

**Query params:** `startDate` (required, ISO 8601), `endDate` (required, ISO 8601), `platforms` (optional, comma-separated), `socialMediaIds` (optional, comma-separated UUIDs).

**Response:** `{ "data": [{ id, content, socialMediaId, platformPostId, publishedAt, latestMetric }] }`

- Only `PUBLISHED` posts with a `platformPostId`; LinkedIn personal accounts are excluded; no pagination, so keep date ranges reasonable.
- `latestMetric` is null until metrics are fetched. Count metrics (`impressions`, `reach`, `likes`, `comments`, `shares`, `totalInteractions`) are strings (bigint); `extras` holds platform-specific metrics.
- Watch time (`avgWatchTimeSeconds`, `totalWatchTimeSeconds`, `videoViews`) and Instagram's `saveRate` / `reelsSkipRate` are plain JSON numbers. Field-by-field detail per platform: SKILL.md section 9 and `examples/pinterest-analytics.json`.

### POST /social-media/connect-link

Generate a secure link for clients to connect their social accounts to your workspace, no PostFast account required. Can be scoped to specific platforms and return the user to your own app when done. Rate limit: 60/hour.

**Request:**
```json
{
  "expiryDays": 7,
  "platforms": ["INSTAGRAM"],
  "redirectUrl": "https://yourapp.com/onboarding/social-connected",
  "externalId": "tenant-42",
  "sendEmail": true,
  "email": "client@example.com"
}
```

- `expiryDays` (int, optional): 1-30, default 7
- `platforms` (string[], optional): Restrict the link to these platforms. Omit to offer all 11; an empty array is rejected. Values are the same platform names `my-social-accounts` returns (`TIKTOK`, `INSTAGRAM`, `FACEBOOK`, `X`, `LINKEDIN`, `YOUTUBE`, `BLUESKY`, `THREADS`, `PINTEREST`, `TELEGRAM`, `GOOGLE_BUSINESS_PROFILE`). The scope is carried inside the link's token and enforced server-side, so a scoped link cannot connect any other platform
- `redirectUrl` (string, optional): Where the connect page offers to send the user when connecting finishes. https only, except `http` on `localhost` / `127.0.0.1` / `[::1]`; max 2000 chars; a URL carrying credentials is rejected
- `externalId` (string, optional): Your own reference, echoed back unchanged on the return URL. Max 128 chars, `A-Za-z0-9-._~:@` only
- `sendEmail` (bool, optional): Send link via email, default false. Delivery is best effort: a send failure still returns a link
- `email` (string): Required when `sendEmail` is true

**Response:**
```json
{ "connectUrl": "https://app.postfa.st/connect?token=eyJhbGci..." }
```

Share the `connectUrl` with the client. The token is a JWT and can be long, so do not truncate it.

**Return URL:** when `redirectUrl` is set, the connect page offers a `Return to <your host>` button carrying `status` (`success` or `error`), plus `platform` and `accountId` on success or `message` on error, plus your `externalId`. `accountId` is the same id `GET /social-media/my-social-accounts` returns (for Facebook, the first Page the user picked), so it is the completion signal: there is no webhook, and no need to poll and diff. After the Facebook or LinkedIn page step it also carries `accountIds`, every account connected, comma-separated (the chosen Pages on Facebook; the profile plus the chosen organization pages on LinkedIn). Facebook and LinkedIn offer the button after the page step; Bluesky and Telegram connect in the page and do not offer it.

**Connect link validation errors (`400`):** the `message` field carries a stable code.

| Situation | `message` code |
|---|---|
| `redirectUrl` is not https (and not loopback `http`) | `connectLink.redirectUrlNotHttps` |
| `redirectUrl` is otherwise unusable, e.g. it carries credentials | `connectLink.redirectUrlInvalid` |
| `externalId` uses characters outside `A-Za-z0-9-._~:@` | `connectLink.externalIdInvalid` |

Enum and length violations fail class-validator first, so those come back as a `message` **array** instead of a code: `"platforms should not be empty"`, `"each value in platforms must be one of the following values: ..."`, `"externalId must be shorter than or equal to 128 characters"`, `"redirectUrl must be shorter than or equal to 2000 characters"`.

### Social Inbox

Comments on your own published posts (TikTok, Instagram, Facebook Pages, Threads). Full behaviour, object fields and error codes: SKILL.md "Social Inbox (Comments)". GETs return `200`, every POST returns `201`.

| Route | Body | Rate limit |
|---|---|---|
| `GET /social-inbox/conversations` | query: `page`, `limit`, `platforms`, `socialMediaIds`, `statuses`, `unreadOnly`, `assignedToUserId` | 1,080/hour, 10,800/day |
| `GET /social-inbox/conversations/:id` | | 1,080/hour, 10,800/day |
| `GET /social-inbox/conversations/:id/items` | query: `page`, `limit`, `order` (`ASC` default, `DESC`) | 1,080/hour, 10,800/day |
| `GET /social-inbox/unread-count` | | 1,080/hour, 10,800/day |
| `POST /social-inbox/items/:id/reply` | `{ text, idempotencyKey? }` | 180/minute, 420/day |
| `POST /social-inbox/items/:id/private-reply` (Instagram) | `{ text, idempotencyKey? }`, text max 1,000 bytes | 120/minute, 360/day |
| `POST /social-inbox/items/:id/state` | `{ action: HIDE \| UNHIDE \| DELETE }` | 240/hour |
| `POST /social-inbox/conversations/:id/read` | | 1,080/hour, 10,800/day |
| `POST /social-inbox/conversations/:id/status` | `{ status: OPEN \| SNOOZED \| CLOSED }` | 720/hour, 7,200/day |
| `POST /social-inbox/conversations/:id/assign` | `{ assigneeUserId? }` (send `{}` to unassign) | 720/hour, 7,200/day |

## Error Responses

| Code | Meaning |
|------|---------|
| `400` | Bad request: missing fields, invalid data, scheduledAt in the past, a malformed filter |
| `400` `socialMediaDisconnected` | Scheduling to a disconnected account: reconnect it first (drafts are allowed) |
| `401` | Invalid or missing API key |
| `403` | Forbidden: the key is valid but lacks permission for the action |
| `404` | Resource not found, e.g. `tiktokSounds.socialMediaNotFound`. Deleting a post never returns 404 (`{ "deleted": false }` instead) |
| `429` | Rate limit exceeded for that endpoint: wait `Retry-After` seconds |
| `500` | Unexpected server error |

## Rate Limits

Counted per endpoint, per workspace API key: calls to one endpoint never use another endpoint's budget. Each endpoint has four windows; the limits listed above override the default for those windows only.

**Default (per endpoint):** 72/minute, 180/5 minutes, 360/hour, 2,400/day.

**Windows:** a window starts at the endpoint's first call, not on a clock boundary. Once a window is exceeded, the endpoint stays blocked for the full length of that window, and calls made while blocked still count toward it.

**Headers** on every response, one set per window (`short` = 1 minute, `medium` = 5 minutes, `long` = 1 hour, `daily` = 24 hours): `X-RateLimit-Limit-<window>`, `X-RateLimit-Remaining-<window>`, `X-RateLimit-Reset-<window>` (seconds until that window resets).

**429 response:** `Retry-After` (seconds) and `Retry-After-<window>` for the window that was exceeded (up to 60 for the minute window, up to 86,400 for the daily one). Body:
```json
{ "statusCode": 429, "message": "Too many requests. Please try again later.", "error": "Too Many Requests" }
```
