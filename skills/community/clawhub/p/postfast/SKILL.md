---
name: postfast
description: Schedule and manage social media posts across TikTok, Instagram, Facebook, X (Twitter), YouTube, LinkedIn, Threads, Bluesky, Pinterest, Telegram, and Google Business Profile using the PostFast API. Use when the user wants to schedule social media posts, manage social media content, upload media for social posting, list connected social accounts, check scheduled posts (filtered by account, platform, status or date), delete posts one at a time or up to 100 per call, cross-post content to multiple platforms, manage Google Business Profile posts, geotag posts with real-world places, pick trending pre-cleared TikTok sounds for photo and carousel posts, read or reply to the comments on their posts (social inbox on TikTok, Instagram, Facebook, Threads), triage or moderate comment conversations, generate a connect link so an agency client or their own app's user can connect accounts without a PostFast account, or automate their social media workflow. PostFast is a SaaS tool, no self-hosting required.
homepage: https://postfa.st
version: 1.19.0
metadata: {"openclaw":{"emoji":"⚡","primaryEnv":"POSTFAST_API_KEY","requires":{"env":["POSTFAST_API_KEY"]}},"hermes":{"tags":["social-media","scheduling","marketing","automation"],"category":"productivity"}}
---

# PostFast

Schedule social media posts across 11 platforms from one API. SaaS, no self-hosting needed.

## Setup

1. Sign up at https://app.postfa.st/register (7-day free trial, no credit card)
2. Go to Workspace Settings → generate an API key
3. Set the environment variable:
   ```bash
   export POSTFAST_API_KEY="your-api-key"
   ```

Base URL: `https://api.postfa.st`
Auth header: `pf-api-key: $POSTFAST_API_KEY`

**Important:** The header name is `pf-api-key` (not `Authorization: Bearer` or `x-api-key`). Regenerating your key in settings permanently invalidates the previous one. See [Troubleshooting](#troubleshooting) if you get 403 errors.

## Core Workflow

### 1. List connected accounts

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-media/my-social-accounts
```

Returns array of `{ id, platform, platformUsername, displayName, connectionStatus, disabledReason, inboxCapable, followerCount?, followerCountUpdatedAt? }`. Save the `id` (the `socialMediaId` required for every post).

- `connectionStatus` (always present): `CONNECTED` (healthy) or `DISABLED` (paused; the account needs reconnecting and won't publish until the user does).
- `disabledReason`: `null` unless `DISABLED`, then one of `TOKEN_REVOKED`, `ACCOUNT_SUSPENDED`, `PERMISSION_REVOKED`, `MANUAL`.
- `inboxCapable`: `true` when comments on this account's posts reach the [Social Inbox](#social-inbox-comments).
- `followerCount` (string, or null) / `followerCountUpdatedAt`: the latest daily follower or subscriber count, refreshed once a day around 04:00 UTC. Not available on X or Google Business Profile.

Check `connectionStatus` before scheduling: a `DISABLED` account rejects new scheduled posts (drafts still work). Posts already scheduled to it are held, not deleted: they resume once the user reconnects, or are marked `FAILED` if their time passes while the account is still disabled.

**Recent posts are imported on connect.** When a Facebook Page, Instagram, Threads or TikTok account is connected or reconnected, PostFast imports the posts published on it in the last 60 days (including posts not made with PostFast), so they show up in `GET /social-posts` and in analytics. Metrics fill in shortly after (TikTok can take 24-48h).

The account list changes rarely: read it once per task and reuse it, don't poll it in a loop (see [Rate Limits](#rate-limits)).

Platform values: `TIKTOK`, `INSTAGRAM`, `FACEBOOK`, `X`, `YOUTUBE`, `LINKEDIN`, `THREADS`, `BLUESKY`, `PINTEREST`, `TELEGRAM`, `GOOGLE_BUSINESS_PROFILE`

### 2. Schedule a text post (no media)

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "content": "Your post text here",
      "mediaItems": [],
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "socialMediaId": "ACCOUNT_ID_HERE"
    }],
    "controls": {}
  }'
```

Returns `{ "postIds": ["uuid-1"] }`.

### 3. Schedule a post with media (3-step flow)

**Step A.** Get signed upload URLs:
```bash
curl -X POST https://api.postfa.st/file/get-signed-upload-urls \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "contentType": "image/png", "count": 1 }'
```
Returns `[{ "key": "image/uuid.png", "signedUrl": "https://..." }]`.

**Step B.** Upload file to S3:
```bash
curl -X PUT "SIGNED_URL_HERE" \
  -H "Content-Type: image/png" \
  --data-binary @/path/to/file.png
```

**Step C.** Create post with media key:
```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "content": "Post with image!",
      "mediaItems": [{ "key": "image/uuid.png", "type": "IMAGE", "sortOrder": 0 }],
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "socialMediaId": "ACCOUNT_ID_HERE"
    }],
    "controls": {}
  }'
```

For video: use `contentType: "video/mp4"`, `type: "VIDEO"`, key prefix `video/`. A LinkedIn document (Pattern 7) or a YouTube caption file (Pattern 5c) gets a `file/` key that goes in `controls`, never in `mediaItems`.

### 4. List and filter posts

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" "https://api.postfa.st/social-posts?page=0&limit=20"
```

Returns `{ "data": [...], "totalCount": 25, "pageInfo": { "page": 1, "hasNextPage": true, "perPage": 20 } }`.

**Query parameters** (all optional; filters are AND-ed together):
- `page` (int, default 0): 0-based page index. Response shows 1-based display page in `pageInfo.page`
- `limit` (int, 1-50, default 20): items per page
- `socialMediaIds` (string): comma-separated account UUIDs (max 100); returns only these accounts' posts
- `ids` (string): comma-separated post UUIDs (max 100), to fetch known posts
- `platforms` (string): comma-separated, e.g. `FACEBOOK,INSTAGRAM,X`
- `statuses` (string): comma-separated, any of `DRAFT`, `SCHEDULED`, `PUBLISHED`, `FAILED`
- `from` / `to` (ISO 8601 UTC): date range filter on `scheduledAt`

Example, one account's scheduled posts in June: `GET /social-posts?socialMediaIds=ACCOUNT_ID&statuses=SCHEDULED&from=2026-06-01T00:00:00Z&to=2026-06-30T23:59:59Z&limit=50`

- `ids` and `socialMediaIds` only match this workspace: an id from another workspace matches nothing (`200`, no posts).
- To skip a filter, leave the parameter out. An empty value (`ids=`), a trailing comma, a non-UUID or more than 100 entries returns `400`.
- **Unknown query parameters are ignored, not rejected.** The singular `socialMediaId` is not a filter and returns every account's posts: the parameter is `socialMediaIds`.
- Results are ordered by `scheduledAt`, then `id`, so paging through a list that isn't changing is stable.
- When nothing matches, `data` is `[]` and `totalCount` is `null`, not `0`.

Each post carries `id`, `socialMediaId`, `content`, `status`, `approvalStatus`, `scheduledAt`, `publishedAt`, `failedAt`, `platformPostId`, `mediaItems`, `lastError`, `firstComment`, `firstCommentError`, `groupId`, and `controls` with the stored `threadsTopicTag`, `instagramPublishType`, `facebookContentType`, `tiktokIsDraft` and `youtubePrivacy` (posts created over the API carry every platform's defaults, so read only the field for the post's own platform). There is no `platform` field on a post: map `socialMediaId` to the account list. The list also includes posts imported when an account was connected (see section 1).

### 5. Delete posts

Deletion is immediate and cannot be undone. Unless the user gave you the exact post IDs, list the candidates first and show what you are about to remove (ID, account, scheduled time, first words of the content; for a bulk delete, the count plus a sample) and wait for a yes.

**What deleting does:** it removes the post, its schedule and its analytics from PostFast, in any status. PostFast never calls the social platform, so a post that is already `PUBLISHED` stays live on the network, and a `SCHEDULED` post that hasn't gone out yet will not publish. Say so when the user asks to delete something that has already been published.

**One post:**

```bash
curl -X DELETE -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-posts/POST_ID
```

Returns `{ "deleted": true }`. An id that doesn't exist or belongs to another workspace returns `200` with `{ "deleted": false }`, never a `404`; a non-UUID returns `400`.

**Up to 100 posts in one call:**

```bash
curl -X POST https://api.postfa.st/social-posts/bulk-delete \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ids": ["POST_ID_1", "POST_ID_2"] }'
```

Returns `200` (not 201) with `{ "deletedIds": [...], "notFoundIds": [...] }`. `notFoundIds` holds ids that don't exist or belong to another workspace; a repeated id is reported once, and repeating the same call is harmless. `ids` takes 1-100 UUIDs: `[]` returns `400` "At least one id is required", more than 100 returns `400` "ids cannot exceed 100 entries", a non-UUID returns `400` "Each id must be a valid UUID". One call counts as one request against this endpoint's own limit, separate from `DELETE /social-posts/:id`.

**Delete everything that matches a filter** (for example every scheduled post on one account, after the user confirmed): don't advance `page` while deleting, because later posts shift onto pages you have already read and get skipped. Instead repeat: read `GET /social-posts?socialMediaIds=ACCOUNT_ID&statuses=SCHEDULED&page=0&limit=50`, send the returned ids to `POST /social-posts/bulk-delete`, and stop when `data` comes back empty. Stop on any error too; after a `429`, wait `Retry-After` seconds, then run the loop again.

### 6. Cross-post to multiple platforms

Include multiple entries in the `posts` array, each with a different `socialMediaId`. Each entry has its own `content`, `scheduledAt` and `mediaItems` (the same uploaded keys can be reused across entries), but **one `controls` object applies to every post in the request**: there are no per-post controls. Posts that need different settings (a different Threads topic, Instagram publish type or geotag) go in separate requests.

### 7. Generate a connect link (for clients)

Let clients connect their social accounts to your workspace without creating a PostFast account:

```bash
curl -X POST https://api.postfa.st/social-media/connect-link \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "expiryDays": 7,
    "platforms": ["INSTAGRAM"],
    "redirectUrl": "https://yourapp.com/onboarding/social-connected",
    "externalId": "tenant-42",
    "sendEmail": true,
    "email": "client@example.com"
  }'
```

Returns `{ "connectUrl": "https://app.postfa.st/connect?token=..." }`. Share the URL so they can connect accounts directly. The token is a long JWT: pass the full URL on as returned, never truncate it. Rate limit: 60/hour.

Every field is optional (`expiryDays` is 1-30, default 7):

- `platforms` restricts which of the 11 the link offers. Omit it to offer all of them, and never send an empty array (rejected). The scope is baked into the link's token and enforced server-side, so a scoped link cannot connect any other platform.
- `redirectUrl` makes the connect page offer a `Return to <your host>` button once connecting finishes, carrying `status` (`success` or `error`), plus `platform` and `accountId` on success or `message` on error, plus your `externalId`. `accountId` is the same id `my-social-accounts` returns (for Facebook, the first Page the user picked), so it is the completion signal: there is no webhook and no need to poll and diff. After the Facebook or LinkedIn page step the return URL also carries `accountIds`, every account connected, comma-separated. Bluesky and Telegram connect inside the page and don't offer the button. https only (`http` is accepted on `localhost` / `127.0.0.1` / `[::1]`), max 2000 chars, no credentials in the URL.
- `externalId` is your own reference (a tenant or user id), echoed back unchanged on that return URL. Max 128 chars, `A-Za-z0-9-._~:@` only.
- `sendEmail` + `email` email the link to the client. Delivery is best effort: a failed send still returns the link.

The same fields exist as `generate_connect_link` MCP tool arguments in `postfast-mcp` ≥ 0.6.0.

### 8. Create a draft post

**Two unrelated concepts share the word "draft". Don't mix them up:**

| What you want | How |
|---------------|-----|
| **PostFast draft** (any platform): saved in PostFast, not scheduled, user finalizes from the dashboard | Set `status: "DRAFT"` and **omit** `scheduledAt`. Works for every platform. |
| **TikTok app draft**: pushes the post to the TikTok app's draft inbox so the user finishes editing on their phone | Set `controls.tiktokIsDraft: true`. TikTok-only. This is **not** a PostFast draft state: it still needs `scheduledAt`. |

**⚠️ Common mistake: `status` placement.** `status` is a **top-level** field, sibling of `posts` and `controls`. It is **not** a per-post field. If you put it inside the post object, the API silently ignores it, defaults to `SCHEDULED`, and rejects the request with `"All posts must have scheduledAt when status is not present, as default is SCHEDULED"`.

```jsonc
// ❌ Wrong: status nested inside the post
{ "posts": [{ "content": "...", "status": "DRAFT", "socialMediaId": "..." }] }

// ✅ Right: status at top level
{ "posts": [{ "content": "...", "socialMediaId": "..." }], "status": "DRAFT", "controls": {} }
```

Per-post fields: `content`, `mediaItems`, `socialMediaId`, `scheduledAt` (optional for drafts), `firstComment`.
Top-level fields: `status` (`SCHEDULED` default, or `DRAFT`), `approvalStatus` (`APPROVED` default; `PENDING_APPROVAL` holds the post for review in PostFast instead of publishing it), `controls`.

Unknown fields are ignored, not rejected, wherever they sit. A misspelled or misplaced field returns no error; the setting just doesn't apply, so check field names against this skill when something doesn't take effect.

**PostFast draft (recommended for "save now, schedule later"):**

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{ "content": "Draft idea...", "mediaItems": [], "socialMediaId": "ACCOUNT_ID" }],
    "status": "DRAFT",
    "controls": {}
  }'
```

See [examples/draft-post.json](examples/draft-post.json) for the platform-agnostic pattern, or [examples/tiktok-app-draft.json](examples/tiktok-app-draft.json) for the TikTok-app-inbox case.

### 9. Get post analytics

Fetch published posts with their performance metrics:

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" \
  "https://api.postfa.st/social-posts/analytics?startDate=2026-03-01T00:00:00.000Z&endDate=2026-03-31T23:59:59.999Z&platforms=TIKTOK,INSTAGRAM"
```

**Query parameters:**
- `startDate` (ISO 8601, required): start of date range
- `endDate` (ISO 8601, required): end of date range
- `platforms` (string, optional): comma-separated filter
- `socialMediaIds` (string, optional): comma-separated account UUIDs

Returns `{ "data": [{ id, content, socialMediaId, platformPostId, publishedAt, latestMetric }] }`. Only `PUBLISHED` posts that have a `platformPostId` appear. There is no pagination, so keep date ranges reasonable. Rate limit: 1,260/hour, 12,600/day.

`latestMetric` fields: `impressions`, `reach`, `likes`, `comments`, `shares`, `totalInteractions`, `fetchedAt`, `extras`. The count fields are strings (bigint). `latestMetric` is null if metrics haven't been fetched yet.

**Video watch-time** (video posts only): `latestMetric` also carries `avgWatchTimeSeconds` and `totalWatchTimeSeconds` (seconds, rounded to 2 decimals) on Facebook, Instagram Reels, YouTube, Pinterest, LinkedIn company pages, and TikTok, plus `videoViews` where the platform reports views separately from impressions (not on Instagram, YouTube, or TikTok). Unlike the counts, these are plain JSON numbers. TikTok additionally exposes `total_time_watched`, `average_time_watched`, `full_video_watched_rate` (completion rate), and `favorites` in `extras`. These are averages and totals, not a per-second retention curve (no platform exposes that). Fields are omitted when there is no data, and always on Threads, X, and personal accounts. Numbers lag 24-48h, and reach keeps building over the first week or so.

**Instagram engagement rates**: Instagram posts also carry `saveRate` on `latestMetric` (saves ÷ reach as a percentage, rounded to 2 decimals; feed posts, Reels, and carousels). Instagram Reels additionally carry `reelsSkipRate` (percentage of viewers who skipped the reel in the first 3 seconds, rounded to 2 decimals; may be absent on low-view reels or until metrics refresh).

**Supported platforms for analytics:** Facebook, Instagram, Threads, LinkedIn, TikTok, YouTube, Pinterest. LinkedIn personal accounts are excluded. YouTube returns views, likes, comments, and total interactions (no reach or shares).

**Pinterest specifics** (requires a Pinterest business account):

Canonical fields:
- `impressions`, `likes` (reactions: heart/applaud/idea/etc.), `comments`: **lifetime** totals from Pinterest's pin endpoint.
- `shares`: **90-day rolling save count**. This is the only canonical field that isn't lifetime; Pinterest's v5 API does not expose lifetime save totals.
- `totalInteractions`: sum of pin clicks + outbound clicks + saves + reactions + comments. Mostly lifetime, but the saves portion is 90-day, so treat it as a "best available" interaction total rather than strictly lifetime.
- `reach`: always null (Pinterest doesn't return it).

`extras` (lifetime):
- `pin_clicks`: opens of the pin's close-up view
- `outbound_clicks`: clicks to the destination URL
- `engagement`, `engagement_rate`, `pin_click_rate`, `outbound_click_rate`: Pinterest's lifetime analytics fields, passed through when present

`extras` (90-day rolling):
- `impressions_90d`, `pin_clicks_90d`, `outbound_clicks_90d`: same metrics as their lifetime counterparts but for the last 90 days
- `save_rate`: saves ÷ impressions over the 90-day window

`extras` for video pins (when present):
- `video_mrc_views`, `video_avg_watch_time`, `video_v50_watch_time`, `video_10s_views`, `video_start`, `quartile_95_percent_view`

Refresh cadence: every 6 hours for pins under 14 days old, once a day for pins 14–60 days old. You can also trigger a manual refresh from the dashboard.

### 10. Get follower history

Daily follower/subscriber snapshots for a connected account:

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" \
  "https://api.postfa.st/social-media/ACCOUNT_ID/follower-history?from=2026-05-01T00:00:00.000Z&to=2026-05-31T23:59:59.999Z"
```

Returns:
```json
{
  "socialMediaId": "account-uuid",
  "series": [{ "capturedAt": "2026-05-01T00:00:00.000Z", "followerCount": "102" }],
  "currentFollowerCount": "106",
  "delta": "4",
  "trackingStartedAt": "2026-04-20T00:00:00.000Z"
}
```

- `from` / `to` (ISO 8601, optional): default last 90 days, range capped at 365 days.
- All counts are strings (bigint). `series` is oldest-first. `delta` is the signed net change across the range (`"-123"` for a drop, `"57"` for growth, no leading `+`). `series` and `delta` cover the requested range; `currentFollowerCount` and `trackingStartedAt` cover the account's whole history.
- Tracking is **forward-only**: snapshots begin at `trackingStartedAt` (when PostFast started recording the account), with no backfill before then. `currentFollowerCount`, `delta`, and `trackingStartedAt` may be absent until the first snapshot lands.
- An id that isn't in your workspace returns `200` with an empty `series`; a non-UUID returns `400`.
- **Coverage**: Facebook Pages, Instagram, YouTube (approximate; channels that hide their subscriber count return null), Pinterest, Threads, Bluesky, Telegram (the PostFast bot must stay in the chat), LinkedIn company pages, TikTok. **Not available**: X, Google Business Profile, personal accounts.

## Common Patterns

### Pattern 1: Cross-platform campaign

Post the same content to LinkedIn, X, and Threads at the same time:

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [
      { "content": "Big announcement!", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "LINKEDIN_ID" },
      { "content": "Big announcement!", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "X_ID" },
      { "content": "Big announcement!", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "THREADS_ID" }
    ],
    "controls": {}
  }'
```

See [examples/cross-platform-post.json](examples/cross-platform-post.json) for a complete example.

### Pattern 2: Instagram Reel with upload

1. Get signed URL with `contentType: "video/mp4"`
2. PUT video to signed URL
3. Create post with `instagramPublishType: "REEL"`

Optional: add a custom cover image by uploading a JPEG (max 8MB) via the same 3-step flow, then set `coverImageKey` in the media item. You can also set `coverTimestamp` (milliseconds) as a fallback frame.

See [examples/instagram-reel.json](examples/instagram-reel.json) for the basic request, or [examples/instagram-reel-cover.json](examples/instagram-reel-cover.json) for a Reel with a custom cover image.

### Pattern 3: TikTok video with interaction settings

Upload video, then post with interaction controls:

```bash
# controls object:
{
  "tiktokAllowComments": true,
  "tiktokAllowDuet": false,
  "tiktokAllowStitch": false,
  "tiktokBrandContent": true
}
```

**`tiktokPrivacy` is deprecated. Don't set it.** TikTok videos publish at the account's default privacy (no per-post control) and photos default to public. For a private post, save it as a TikTok app draft (`tiktokIsDraft: true`) and set visibility on the phone.

**Sound:** `tiktokMusicSoundId` (a `musicSoundId` from the tiktok-sounds helper) attaches a licensed trending track to a photo carousel **or** a video; on a video the track and the video's original sound each play at 50% volume (no volume or trim controls). `tiktokAutoAddMusic: true` lets TikTok pick a track, photo posts only. The two are mutually exclusive (both set returns `tiktokMusic.conflictAutoAddMusic`). With neither set, a photo post publishes silent and a video keeps its own audio. Music controls are not applied to TikTok app drafts (`tiktokIsDraft: true`).

**TikTok Business account:** `firstComment`, follower history, and analytics watch-time all require a TikTok Business account. New connections and reconnects upgrade to Business automatically.

See [examples/tiktok-video.json](examples/tiktok-video.json).

### Pattern 4: Pinterest pin (board required)

Always fetch boards first, then post:

```bash
# Step 1: Get boards
curl -s -H "pf-api-key: $POSTFAST_API_KEY" \
  https://api.postfa.st/social-media/PINTEREST_ACCOUNT_ID/pinterest-boards

# Step 2: Post with board ID
# controls: { "pinterestBoardId": "BOARD_ID", "pinterestLink": "https://yoursite.com" }
```

See [examples/pinterest-pin.json](examples/pinterest-pin.json).

### Pattern 5: YouTube Short with tags and playlist

Upload video, then post with YouTube controls:

```bash
# controls object:
{
  "youtubeIsShort": true,
  "youtubeTitle": "Quick Tip: Batch Your Content",
  "youtubePrivacy": "PUBLIC",
  "youtubePlaylistId": "PLxxxxxx",
  "youtubeTags": ["tips", "productivity", "social media"],
  "youtubeMadeForKids": false
}
```

See [examples/youtube-short.json](examples/youtube-short.json).

### Pattern 5b: YouTube video with custom thumbnail

Upload both video and thumbnail image, then reference the thumbnail key in controls:

```bash
# 1. Upload thumbnail image (separate from video upload)
curl -X POST https://api.postfa.st/file/get-signed-upload-urls \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "contentType": "image/jpeg", "count": 1 }'
# PUT thumbnail to signed URL

# 2. Upload video (same 3-step flow as always)

# 3. Create post with thumbnail key in controls:
{
  "youtubeIsShort": false,
  "youtubeTitle": "Full Tutorial: Social Media Strategy",
  "youtubePrivacy": "PUBLIC",
  "youtubeThumbnailKey": "image/abc123.jpg",
  "youtubeTags": ["tutorial", "social media"],
  "youtubeMadeForKids": false
}
```

Thumbnail specs: JPEG/PNG recommended, max 2MB, 1280x720 (16:9), min width 640px. Requires phone-verified YouTube channel. If thumbnail upload fails, the video still publishes without the custom thumbnail.

See [examples/youtube-video-thumbnail.json](examples/youtube-video-thumbnail.json).

### Pattern 5c: YouTube video with language and captions

Set the video's language and add your own caption track:

1. Upload the caption file: get a signed URL with `contentType: "application/x-subrip"` (.srt) or `contentType: "text/vtt"` (.vtt) and `count: 1`, then PUT the file. The key looks like `file/uuid.srt`.
2. Upload the video (same 3-step flow as always).
3. Create the post with the video in `mediaItems` and the caption key in `controls`:

```bash
# controls object:
{
  "youtubeIsShort": false,
  "youtubeTitle": "Full Tutorial: Social Media Strategy",
  "youtubePrivacy": "PUBLIC",
  "youtubeLanguage": "en",
  "youtubeCaptionKey": "file/abc123.srt"
}
```

- `youtubeLanguage` is a BCP-47 code (`en`, `en-GB`, `es`, `es-419`, `fr`, `pt-BR`). It sets both YouTube's "Video language" and its "Title and description language". PostFast normalizes the code before sending it (`pt-br` becomes `pt-BR`); an unknown code returns `400 youtubeLanguage.invalid`.
- `youtubeCaptionKey` needs `youtubeLanguage` (otherwise `400 youtubeCaptionKey.languageRequired`). The track is added in that language right after the video uploads, and viewers see it named by its language. YouTube's automatic captions stay available separately. One caption track per video.
- The file must be timed SRT or WebVTT in plain UTF-8, at most 10MB. PostFast checks it when the post is created (`400 media.invalidMedia` if it's missing, empty, over 10MB, or not timed SRT/WebVTT in plain UTF-8). If the captions still can't be added when the video publishes, the video publishes without them.
- Both controls apply to every post in the request and are set at creation only. Videos in different languages, each with its own caption file, go in separate requests.

See [examples/youtube-video-captions.json](examples/youtube-video-captions.json).

### Pattern 6: Google Business Profile post

Always fetch locations first, then post with GBP-specific controls:

```bash
# Step 1: Get locations
curl -s -H "pf-api-key: $POSTFAST_API_KEY" \
  https://api.postfa.st/social-media/GBP_ACCOUNT_ID/gbp-locations

# Step 2: Create a standard post with CTA
# controls: { "gbpLocationId": "accounts/.../locations/...", "gbpTopicType": "STANDARD", "gbpCallToActionType": "LEARN_MORE", "gbpCallToActionUrl": "https://yoursite.com" }
```

Three post types: `STANDARD` (updates), `EVENT` (time-bound), `OFFER` (deals with coupons). EVENT and OFFER require `gbpEventTitle`, `gbpEventStartDate`, `gbpEventEndDate`.

See [examples/gbp-standard.json](examples/gbp-standard.json), [examples/gbp-event.json](examples/gbp-event.json), and [examples/gbp-offer.json](examples/gbp-offer.json).

### Pattern 7: LinkedIn document post

Documents (PDF, PPTX, DOCX) display as swipeable carousels on LinkedIn.

1. Get signed URL with `contentType: "application/pdf"`
2. PUT the file to signed URL
3. Create post using `linkedinAttachmentKey` instead of `mediaItems`

```bash
# controls: { "linkedinAttachmentKey": "file/uuid.pdf", "linkedinAttachmentTitle": "Q1 Marketing Playbook" }
# Note: mediaItems should be [] when using linkedinAttachmentKey
```

See [examples/linkedin-document.json](examples/linkedin-document.json).

### Pattern 8: First comment (auto-posted after publish)

Add a `firstComment` to any post. It's auto-posted ~10 seconds after the main post goes live (up to 3 retries):

```json
{
  "posts": [{ "content": "Main post text", "firstComment": "Link: https://postfa.st", "mediaItems": [], "scheduledAt": "...", "socialMediaId": "X_ID" }],
  "controls": {}
}
```

Supported on: X, Instagram, Facebook, YouTube, Threads, and TikTok. NOT supported on: Pinterest, Bluesky, LinkedIn, Google Business Profile (a validation error). **TikTok caveat:** max 1,200 chars, comments must be enabled on the post, and a TikTok account that can't post comments is rejected with `firstComment.tiktok.notSupported`. On X, a link in the first comment counts toward the monthly X link-post allowance (see [Rate Limits](#rate-limits)).

See [examples/x-first-comment.json](examples/x-first-comment.json).

### Pattern 9: X (Twitter) retweet

Schedule a retweet (content and media are ignored):

```json
{
  "posts": [{ "content": "", "scheduledAt": "...", "socialMediaId": "X_ID" }],
  "controls": { "xRetweetUrl": "https://x.com/username/status/1234567890" }
}
```

See [examples/x-retweet.json](examples/x-retweet.json).

### Pattern 10: Batch scheduling (a week of posts)

Schedule multiple posts at different times in a single API call (up to 15 posts per request; the endpoint allows 180 requests per minute and 420 per day). Before a large batch, check the per-account daily posting limits and the plan's queue ceiling in [Rate Limits](#rate-limits).

See [examples/batch-scheduling.json](examples/batch-scheduling.json).

### Pattern 11: Geotag a post with a place (Facebook / Instagram)

Tag a post with a real-world location in two steps: resolve the place, then attach its `id` in `controls`.

**Step 1. Resolve the place** (returns up to 100 address-carrying Facebook Pages, cached 7 days):

```bash
curl -sG "https://api.postfa.st/social-media/search-places" \
  --data-urlencode "q=national palace of culture" \
  -H "pf-api-key: $POSTFAST_API_KEY"
# → [{ "id": "1559011447688271", "name": "...", "link": "https://www.facebook.com/1559011447688271", "city": "Sofia", "country": "Bulgaria", "zip": "1463", "pictureUrl": "https://graph.facebook.com/.../picture?type=small" }]
```

`q` needs at least 2 characters. The returned `id` is a Facebook Page ID that carries location data, and it works on both networks.

**Step 2. Attach the `id`** in the `controls` object (same value either way):

- Facebook feed post: `"facebookPlaceId": "1559011447688271"`
- Instagram single-media post: `"instagramLocationId": "1559011447688271"`

Optionally add `facebookPlaceName` / `instagramLocationName` for a readable label. Those are display-only: PostFast stores them for your dashboard and never sends them to Meta.

**Where a geotag is allowed:**

- `facebookPlaceId`: Facebook feed posts only (text, photo, carousel). Not Reels, Stories, or video.
- `instagramLocationId`: a single image, video, reel, or story. Not carousels (2 or more media items).

**Limit a Facebook feed post to specific countries** (optional, combine with a geotag):

```jsonc
"controls": { "facebookPlaceId": "1559011447688271", "facebookTargetCountries": ["BG", "DE", "AT"] }
```

`facebookTargetCountries` takes up to 25 ISO 3166-1 alpha-2 codes and is hard audience gating, not a hint: only logged-in users in those countries can see the post, so total reach drops. Feed posts only.

**Batch geotagged posts by platform.** `controls` apply to every post in the `posts[]` array and each geo field is validated per platform, so send Facebook posts in one request and Instagram posts in another. That keeps a Facebook-only field from landing on an Instagram post and vice versa.

See [examples/facebook-geotag.json](examples/facebook-geotag.json) and [examples/instagram-geotag.json](examples/instagram-geotag.json).

### Pattern 12: Threads post with a topic

`controls.threadsTopicTag` sets the post's topic on Threads: one topic per post, 1-50 characters, no `.` or `&` (an invalid topic returns `400 threadsTopicTag.invalid`). It shows as the post's topic in Threads; if the text also contains a #hashtag, the topic you set wins and the hashtag stays plain text. Only Threads posts use it, and like every key in `controls` it applies to every post in the request, so Threads posts that need different topics go in separate requests.

```json
{
  "posts": [{ "content": "Five things we learned shipping our API", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "THREADS_ID" }],
  "controls": { "threadsTopicTag": "Startups" }
}
```

See [examples/threads-topic.json](examples/threads-topic.json).

### Pattern 13: AI disclosure labels

Three optional booleans (default `false`), each ignored by every platform other than its own:

- `tiktokIsAigc`: TikTok's AI-generated content label
- `instagramIsAiGenerated`: Instagram's "AI info" label on images, videos, reels, stories and carousels (it labels the whole post, not single slides)
- `youtubeContainsSyntheticMedia`: YouTube's altered or synthetic content disclosure (sent only when `true`)

They are set at creation only: there is no route to update a post, and on Instagram the label cannot be removed after publishing. Since `controls` is shared by the whole request, a flag set on a mixed batch applies to every post in it.

See [examples/tiktok-aigc-video.json](examples/tiktok-aigc-video.json).

## Platform-Specific Controls

Pass these in the `controls` object. See [references/platform-controls.md](references/platform-controls.md) for full details.

| Platform | Key Controls |
|---|---|
| **TikTok** | `tiktokTitle` (photo carousels, max 90), `tiktokAllowComments`, `tiktokAllowDuet`, `tiktokAllowStitch`, `tiktokIsDraft`, `tiktokIsAigc`, `tiktokBrandOrganic`, `tiktokBrandContent`, `tiktokAutoAddMusic`, `tiktokMusicSoundId` (trending Commercial Music Library sound from the tiktok-sounds helper below, max 128 chars; photo carousels AND videos on Business-API connections; on a video it plays at 50% over the original sound at 50%; mutually exclusive with `tiktokAutoAddMusic`, sending both is rejected; not applied when `tiktokIsDraft` is true), `tiktokMusicSoundName` (display-only label for the chosen sound, max 256 chars, never sent to TikTok; set it whenever the id is set). `tiktokAutoAddMusic` is photo posts only. `tiktokPrivacy` is **deprecated** (no-op) |
| **Instagram** | `instagramPublishType` (TIMELINE/STORY/REEL), `instagramPostToGrid`, `instagramCollaborators`, `instagramTrialReelStrategy`, `instagramLocationId`, `instagramLocationName`, `instagramIsAiGenerated` |
| **Facebook** | `facebookContentType` (POST/REEL/STORY), `facebookReelsCollaborators`, `facebookPlaceId`, `facebookPlaceName`, `facebookTargetCountries` |
| **YouTube** | `youtubeIsShort`, `youtubeTitle`, `youtubePrivacy`, `youtubePlaylistId`, `youtubeTags`, `youtubeMadeForKids`, `youtubeCategoryId`, `youtubeThumbnailKey`, `youtubeContainsSyntheticMedia`, `youtubeLanguage` (BCP-47 code), `youtubeCaptionKey` (an uploaded .srt or .vtt file; needs `youtubeLanguage`) |
| **LinkedIn** | `linkedinAttachmentKey`, `linkedinAttachmentTitle` (for document posts) |
| **X (Twitter)** | `xRetweetUrl` (retweet) |
| **Pinterest** | `pinterestBoardId` (required), `pinterestLink` |
| **Google Business Profile** | `gbpLocationId` (required), `gbpTopicType`, `gbpCallToActionType`, `gbpCallToActionUrl`, `gbpEventTitle`, `gbpEventStartDate`, `gbpEventEndDate`, `gbpOfferCouponCode`, `gbpOfferRedeemUrl`, `gbpOfferTerms` |
| **Threads** | `threadsTopicTag` (one topic per post, 1-50 chars, no `.` or `&`) |
| **Bluesky** | No platform-specific controls. Text + up to 10 images or 1 video |
| **Telegram** | No platform-specific controls. Text + images/video/mixed media |

## Helper Endpoints

- **Pinterest boards**: `GET /social-media/{id}/pinterest-boards` → returns `[{ id, boardId, name, description, imageUrl }]`. Use `boardId` (not `id`) as `pinterestBoardId`. Boards created after connecting don't sync on their own: the user clicks Sync Boards in the dashboard
- **YouTube playlists**: `GET /social-media/{id}/youtube-playlists` → returns `[{ id, playlistId, title, description, thumbnailUrl }]`. Use `playlistId` (not `id`) as `youtubePlaylistId`
- **GBP locations**: `GET /social-media/{id}/gbp-locations` → returns `[{ id, locationId, title, address, mapsUri }]`. Use `locationId` as `gbpLocationId` in controls. A missing location appears after Sync Locations in the dashboard
- **Follower history**: `GET /social-media/{id}/follower-history?from=&to=` → daily snapshots `{ series: [{ capturedAt, followerCount }], currentFollowerCount, delta, trackingStartedAt }`. Forward-only, default 90d, max 365d. Covers every platform except X and personal Facebook
- **Place search (geotag)**: `GET /social-media/search-places?q=<text>` → returns `[{ id, name, link?, city?, country?, street?, zip?, pictureUrl? }]`. The `id` is a Facebook Page ID that works as BOTH `facebookPlaceId` (Facebook) and `instagramLocationId` (Instagram); `link` is the place's Facebook Page URL. `q` needs min 2 chars, returns up to 100 address-carrying Pages, cached 7 days. Rate limit: 110/hour
- **Connect link**: `POST /social-media/connect-link` → returns `{ connectUrl }`. Let clients connect accounts without a PostFast account. Params: `expiryDays` (1-30, default 7), `platforms` (string[], restricts which platforms the link offers; omit for all 11, empty array rejected, enforced server-side), `redirectUrl` (https except `http` on localhost, max 2000 chars; the connect page then offers a return button carrying `status`, `platform`, `accountId`, `externalId`, plus `accountIds` after the Facebook/LinkedIn page step), `externalId` (your own reference, max 128 chars, `A-Za-z0-9-._~:@`), `sendEmail` (bool, best effort), `email` (required if sendEmail=true). Rate limit: 60/hour
- **TikTok trending sounds**: `GET /social-media/{id}/tiktok-sounds?genre=&countryCode=&dateRange=` → up to 100 trending pre-cleared Commercial Music Library tracks, already ordered by trending rank: `[{ musicSoundId, name, artist, duration, thumbnailUrl, previewUrl, rankPosition, genres, commercialMusicId, fullDurationClipId, trendingClipId }]` (`duration` is the seconds of the exact clip, `previewUrl` plays exactly what gets attached). No pagination: narrow with the params and filter the rest yourself. TikTok **Business-API connections only**: an account connected long ago returns `400 tiktokMusic.requiresBusinessApi` until it is reconnected once. `genre` takes raw TikTok values like `POP`, `HIP_HOP/RAP`, `R&B/SOUL`, `K-POP`, default all genres (URL-encode the `/` and `&`, e.g. `HIP_HOP%2FRAP`); `countryCode` = 2-letter uppercase, default US; `dateRange` = `1DAY | 7DAY | 30DAY | 90DAY`, default 7DAY. Bad values return `400` `tiktokSounds.invalidGenre` / `tiktokSounds.invalidCountryCode` / `tiktokSounds.invalidDateRange`; a valid country with no TikTok chart returns `200 []`; an id that isn't a TikTok account in this workspace returns `404 tiktokSounds.socialMediaNotFound`. The list rotates roughly daily (each filter combination is cached ~6h), so fetch fresh instead of reusing old ids. Use a result's `musicSoundId` as `tiktokMusicSoundId` in the post's controls (plus `tiktokMusicSoundName` for the label). Rate limit: 110/hour

## Social Inbox (Comments)

Read and answer the comments on your connected accounts' posts (TikTok Business connections, Instagram, Facebook Pages, and Threads) through the same API. Comments arrive within seconds of being posted, from the moment an account is connected onward (no history backfill). Comments only: the single DM-shaped action is the official Instagram private reply below. Included on every PostFast plan.

**Conversations** group comments per post and carry `status` (`OPEN` | `SNOOZED` | `CLOSED`), `unreadCount`, `assignedToUserId`, and a **server-computed reply capability**: `canReply`, `maxReplyLength`, `maxPrivateReplyLengthBytes` (1000 on Instagram, null elsewhere), `windowState`, `disabledReason`. Always derive whether and how long you can reply from those fields, never from hardcoded platform rules (for context, today's public reply caps are TikTok 1,200, Instagram 2,200, Facebook 8,000 and Threads 500 characters, but `maxReplyLength` is the authoritative value). Each conversation also includes `postPreview` with the post's `caption`, `thumbnailUrl`, and, when available, its public `permalink` (every field individually optional; use the permalink to link the user straight to the post on the platform; currently null on Instagram). **Items** are the individual comments and replies, with `direction` (`INBOUND` | `OUTBOUND`), `state` (`VISIBLE` | `HIDDEN` | `DELETED`), author info, `deliveryStatus` on your outbound replies (`PENDING` | `SENT` | `FAILED`), and on Instagram comments `canPrivateReply`. `authoredByUserId` is null on replies sent with an API key (keys belong to the workspace, not a user).

Lists use the same envelope as posts (`{ data, totalCount, pageInfo }`, `page` 0-based). GETs return `200`, every POST returns `201`, and a conversation id outside your workspace returns `200` with a `null` body, not a `404`.

- **List conversations**: `GET /social-inbox/conversations?page=0&limit=20` (newest activity first): optional filters `platforms`, `socialMediaIds`, `statuses` (comma-separated), `unreadOnly`, `assignedToUserId`
- **One conversation**: `GET /social-inbox/conversations/{id}`
- **List items**: `GET /social-inbox/conversations/{conversationId}/items?page=0&limit=20&order=ASC` (`DESC` for newest first)
- **Unread total**: `GET /social-inbox/unread-count` → `{ "unreadCount": 7 }`
- **Reply**: `POST /social-inbox/items/{itemId}/reply` with `{ "text": "...", "idempotencyKey": "optional-unique-key" }`. The path takes the comment ITEM id, not the conversation id; respect the conversation's `canReply` and `maxReplyLength`. Retrying with the same `idempotencyKey` never double-sends. A second reply while one is still in flight returns `inbox.replyInProgress`
- **Duplicate guard**: sending the same reply text repeatedly across a workspace (case- and spacing-insensitive, rolling 24 hours, short courtesy replies exempt) returns `inbox.repetitiveReply`. Treat it as an instruction to rephrase, not a transient failure to retry. Replies are also rate-limited, so batch triage at a human pace
- **Instagram private reply**: `POST /social-inbox/items/{itemId}/private-reply` with `{ "text": "...", "idempotencyKey": "optional" }`: Instagram only, once per comment (`inbox.privateReplyAlreadySent`), within 7 days of the comment (`inbox.privateReplyWindowExpired`), up to 1,000 BYTES (emoji and non-Latin text count multiple); check the item's `canPrivateReply` first. Arrives as a DM and may land in the recipient's Message Requests folder
- **Hide / unhide / delete**: `POST /social-inbox/items/{itemId}/state` with `{ "action": "HIDE" | "UNHIDE" | "DELETE" }`: acts on the platform itself; hide and unhide work on all four platforms; `DELETE` is irreversible and not supported on Threads (`inbox.deleteNotSupported`)
- **Mark read**: `POST /social-inbox/conversations/{conversationId}/read` (PostFast state only, nothing changes on the platform)
- **Set status**: `POST /social-inbox/conversations/{conversationId}/status` with `{ "status": "OPEN" | "SNOOZED" | "CLOSED" }` (PostFast state only)
- **Assign**: `POST /social-inbox/conversations/{conversationId}/assign` with `{ "assigneeUserId": "..." }`; send `{}` to unassign; a non-member returns `inbox.assigneeNotMember`

Errors come back as `{ "statusCode": <number>, "message": "<code>" }`, where `message` is usually a stable `inbox.*` code (`inbox.conversationNotFound`, `inbox.itemNotFound`, `inbox.replyTooLong`, `inbox.replyNotSupported`, `inbox.rateLimited`, and the ones above). Branch on the code, not on the wording.

`list_accounts` marks which accounts feed the inbox via `inboxCapable`. Facebook accounts connected before 2026-07-28 and Threads accounts connected before 2026-08-04 need one reconnect in the PostFast dashboard before comments flow. Replies you send appear exactly once, with no duplicate when the platform reports the reply back. The same operations are exposed as MCP tools (`list_inbox_conversations`, `get_inbox_conversation`, `list_inbox_items`, `get_inbox_unread_count`, `reply_to_inbox_item`, `send_inbox_private_reply`, `set_inbox_item_state`, `mark_inbox_conversation_read`, `set_inbox_conversation_status`, `assign_inbox_conversation`) in `postfast-mcp` ≥0.3.0.

## Rate Limits

API limits are counted **per endpoint, per workspace API key**: calls to one endpoint never use another endpoint's budget. Every endpoint has four windows (1 minute, 5 minutes, 1 hour, 24 hours), and exceeding any of them returns `429`.

**Default** (every endpoint, for each window it doesn't set itself): 72/minute, 180/5 minutes, 360/hour, 2,400/day.

**Endpoints that set their own windows:**

| Endpoint | Own limits |
|---|---|
| `POST /social-posts` (up to 15 posts per call) | 180/minute, 420/day |
| `GET /social-posts` | 720/hour, 7,200/day |
| `DELETE /social-posts/:id` | 200/hour |
| `POST /social-posts/bulk-delete` (up to 100 ids per call) | 200/hour |
| `GET /social-posts/analytics` | 1,260/hour, 12,600/day |
| `POST /file/get-signed-upload-urls` | 180/minute, 420/day |
| `GET /social-media/my-social-accounts` | 1,260/hour, 12,600/day |
| `GET /social-media/:id/follower-history` | 720/hour, 7,200/day |
| `GET /social-media/:id/pinterest-boards`, `/youtube-playlists`, `/gbp-locations` | 330/hour, 3,300/day |
| `GET /social-media/search-places` | 110/hour |
| `GET /social-media/:id/tiktok-sounds` | 110/hour |
| `POST /social-media/connect-link` | 60/hour |
| Social Inbox reads (`GET /social-inbox/...`) and mark-read | 1,080/hour, 10,800/day |
| `POST /social-inbox/items/:id/reply` | 180/minute, 420/day |
| `POST /social-inbox/items/:id/private-reply` | 120/minute, 360/day |
| `POST /social-inbox/items/:id/state` | 240/hour |
| `POST /social-inbox/conversations/:id/status` and `/assign` | 720/hour, 7,200/day |

For example, `DELETE /social-posts/:id` sets 200/hour, so it allows 72/minute, 180/5 minutes, 200/hour and 2,400/day.

**How the windows behave:** a window starts at the endpoint's first call, not on a clock boundary (the 24-hour window is not a midnight reset). Once a window is exceeded, that endpoint stays blocked for the full length of the window, and **calls made while blocked still count toward it**, so retrying in a loop keeps it blocked.

**Headers:** every response carries one set per window, named `short` (1 minute), `medium` (5 minutes), `long` (1 hour) and `daily` (24 hours): `X-RateLimit-Limit-<window>`, `X-RateLimit-Remaining-<window>`, `X-RateLimit-Reset-<window>` (seconds until that window resets).

**429 response:** `Retry-After-<window>`, named after the window that was exceeded, plus the standard `Retry-After` with the same value in seconds (up to 60 for the minute window, up to 86,400 for the daily one). Body: `{"statusCode":429,"message":"Too many requests. Please try again later.","error":"Too Many Requests"}`.

**Staying inside the limits:** read `X-RateLimit-Remaining-<window>` before a burst; on a `429`, wait `Retry-After` seconds before calling that endpoint again (other endpoints keep working); batch up to 15 posts per create call and up to 100 ids per bulk delete; never poll the account list or the post list in a tight loop.

**Posting limits per social account** (PostFast Fair Usage Policy, separate from the API limits above): each account can publish per day Instagram 35, Facebook 25, LinkedIn 35, TikTok 15, YouTube 10, Pinterest 15, Bluesky 70, Threads 65, Telegram 25, Google Business Profile 5, X 6 (9 on Pro and Enterprise). The count is tracked per social account across every workspace it is connected to, and resets at midnight UTC.

**X (Twitter) also has organization-wide caps** that depend on the plan: a daily pool shared by every X account in the organization (8 posts/day on Starter up to 280 on Enterprise) and a monthly allowance of posts containing a link (14 on Starter up to 120 on Enterprise; a link in the text or the first comment counts, a link in both counts twice). Each plan also caps how many posts can sit in the queue and how many drafts can be stored. Per-plan tables: [references/platform-controls.md](references/platform-controls.md) (X) and [references/api-reference.md](references/api-reference.md) (queue ceilings).

These limits can change; https://postfa.st/fair-usage is the source of truth. Warn the user before a batch that would cross them.

## Media Specs Quick Reference

Upload caps for every platform: 250MB per video (Bluesky 100MB, Telegram 50MB), 10MB per image, 60MB per document, 10MB per caption file (SRT/VTT, YouTube only). No post carries more than 10 media items, on any platform.

| Platform | Images | Video | Carousel |
|---|---|---|---|
| TikTok | Carousels only | 1 video, MP4/MOV, 3s-10min | Up to 10 images (TikTok itself allows 35; PostFast takes 10) |
| Instagram | JPEG/PNG | 1 video; Reels 3-90s | Up to 10, images and videos mixed |
| Facebook | JPG/PNG | 1 per post | Up to 10 images (no mixing with video) |
| YouTube | — | 1 video; Shorts under 3min, H.264; optional SRT/VTT caption file | — |
| LinkedIn | Up to 10 | 1 video | Up to 10 images (no mixing), or 1 document (PDF/DOC/DOCX/PPT/PPTX) |
| X (Twitter) | Up to 4 | 1 video (no mixing with images) | — |
| Pinterest | 1 image, 2:3 ratio ideal | 1 video | 2-5 static images |
| Google Business Profile | 1 image (JPEG/PNG, 5MB max) | Not supported | — |
| Bluesky | Up to 10 (JPEG/PNG/GIF/WebP, 2MB each) | 1 MP4 | Up to 10 images (no mixing with video) |
| Threads | Supported | Supported | Up to 10, images and videos mixed |
| Telegram | Up to 10 | Supported | Up to 10 mixed media |

## Common Gotchas

1. **Always fetch accounts first**: `socialMediaId` is a UUID, not a platform name. Call `GET /social-media/my-social-accounts` to get valid IDs.
2. **Media MUST go through 3-step upload**: No external URLs. Always: get signed URL → PUT to S3 → use the `key` in `mediaItems`.
3. **`scheduledAt` must be in the future**: ISO 8601 UTC format. Past dates return 400.
4. **Pinterest ALWAYS requires `pinterestBoardId`**: Fetch boards first with `GET /social-media/{id}/pinterest-boards`.
5. **TikTok requires video for standard posts**: Images only work in photo carousels, up to 10 images per post (TikTok allows 35, PostFast takes 10).
6. **LinkedIn documents use `linkedinAttachmentKey`**: NOT `mediaItems`. Set `mediaItems: []` when posting documents.
7. **Content-Type on S3 PUT must match**: The `Content-Type` header in your S3 PUT must match what you requested in `get-signed-upload-urls`.
8. **Instagram Reels need video 3-90 seconds**: Outside this range returns an error.
9. **YouTube Shorts need video under 3 minutes**: H.264 codec with AAC audio recommended.
10. **X (Twitter) has a 280 character limit** (4,000 with X Premium). Longer content is silently truncated.
11. **Cross-posting shares controls**: The `controls` object applies to ALL posts in the batch and there are no per-post controls. Platform-irrelevant controls are ignored; posts that need different settings go in separate requests.
12. **X (Twitter) has plan-based limits**: 6 posts per account per day (9 on Pro and Enterprise), a shared daily pool for the whole organization, and a monthly allowance of posts with links. See [Rate Limits](#rate-limits).
13. **`firstComment` works on 6 platforms**: X, Instagram, Facebook, YouTube, Threads, and TikTok (TikTok: max 1,200 chars, comments enabled on the post; an account that can't post comments gets `firstComment.tiktok.notSupported`). Pinterest, Bluesky, LinkedIn and Google Business Profile return a validation error.
14. **Retweets ignore content/media**: When `xRetweetUrl` is set, the `content` and `mediaItems` fields are ignored.
15. **LinkedIn documents support PDF, DOC, DOCX, PPT, PPTX**: Max 60MB. Cannot mix with regular media.
16. **Pagination is 0-based**: `page=0` returns the first page. Response `pageInfo.page` shows 1-based display number. Results are ordered by `scheduledAt`, then `id`; deleting while you page skips posts, so re-read `page=0` instead (see section 5).
17. **Instagram trial reels require `instagramPublishType: "REEL"`**: Setting `instagramTrialReelStrategy` without it returns 400. Also cannot be combined with `instagramCollaborators`.
18. **YouTube custom thumbnails require phone verification**: `youtubeThumbnailKey` only works if the YouTube channel is phone-verified. If it fails, the video still publishes without the custom thumbnail.
19. **GBP ALWAYS requires `gbpLocationId`**: Fetch locations first with `GET /social-media/{id}/gbp-locations`. Use the `locationId` field (not `id`).
20. **GBP supports only 1 image**: No video, no carousels. JPEG/PNG, max 5MB.
21. **GBP EVENT/OFFER posts require dates**: `gbpEventStartDate` and `gbpEventEndDate` are required when `gbpTopicType` is `EVENT` or `OFFER`.
22. **GBP content limit is 1,500 characters**: Shorter than most platforms.
23. **GBP posts expire**: Standard posts auto-expire after 6 months. Event/Offer posts expire at their end date.
24. **`coverTimestamp` is milliseconds**: e.g., `"5000"` = 5 seconds into the video. Not seconds.
25. **`coverImageKey` platform limits**: Instagram Reels: JPEG only, max 8MB. Facebook Reels: any format, max 10MB. Pinterest video: JPEG/PNG. NOT supported on TikTok (use `coverTimestamp`) or YouTube (use `youtubeThumbnailKey`).
26. **Facebook Reels don't support `coverTimestamp`**: Only `coverImageKey` works for FB Reel covers. `coverTimestamp` is ignored.
27. **Disconnected accounts reject scheduled posts**: If an account's `connectionStatus` is `DISABLED`, scheduling to it returns `400 socialMediaDisconnected`. Drafts still work, and posts already queued are held until the user reconnects. Check `connectionStatus` from `my-social-accounts` first, and watch `lastError.code` for `MISSED_DISCONNECTED` (post was due while the account was down) or `MISSED_NOT_PUBLISHED`.
28. **Geotags need a place ID from `search-places`**: Call `GET /social-media/search-places?q=...` first; the returned `id` doubles as `facebookPlaceId` (Facebook feed posts) and `instagramLocationId` (Instagram single-media posts). Both take the same numeric ID.
29. **Geotag placement is restricted**: `facebookPlaceId` is feed-only (Reels/Stories reject it with `facebookPlaceId.contentType.notSupported`, video with `facebookPlaceId.video.notSupported`). `instagramLocationId` rejects carousels with `instagramLocationId.carousel.notSupported`. A geo field on the wrong platform returns `*.notSupported`.
30. **`facebookTargetCountries` shrinks reach**: Up to 25 ISO 3166-1 alpha-2 codes (over 25 returns `facebookTargetCountries.tooMany`). It's audience gating, not a hint: the post is hidden from anyone outside those countries and from logged-out users. Feed posts only.
31. **`facebookPlaceName` / `instagramLocationName` are display-only**: PostFast stores them for your dashboard and never sends them to Meta. Only the IDs and country codes reach the platform.
32. **Batch geotagged posts by platform**: `controls` apply to the whole batch and geo fields validate per platform, so put Facebook posts in one request and Instagram posts in another.
33. **Unknown fields and query parameters are ignored, not rejected**: A misspelled field, `status` inside a post object, or the singular `socialMediaId` on `GET /social-posts` returns no error; it simply has no effect. Use the exact names in this skill (`socialMediaIds`, plural, is the account filter).
34. **Deleting never touches the platform**: `DELETE /social-posts/:id` and `POST /social-posts/bulk-delete` remove posts from PostFast only. A published post stays live on the social network; the user removes it there.
35. **`totalCount` is `null` when nothing matches**, not `0`. Check `data.length` instead.
36. **Rate limits are per endpoint, and blocked calls count**: A `429` on one endpoint doesn't block the others. Wait `Retry-After` seconds; retrying sooner extends the block.
37. **TikTok sounds rotate and exclude each other**: `tiktokMusicSoundId` and `tiktokAutoAddMusic` can't both be set (`tiktokMusic.conflictAutoAddMusic`), `tiktokAutoAddMusic` is photo-only, and sound ids rotate daily, so fetch a fresh list per session instead of reusing stored ids.
38. **YouTube titles and descriptions can't contain `<` or `>`**: YouTube doesn't allow either character, and PostFast rejects the post before saving it. The description holds up to 5,000 characters; the title 100.
39. **Bluesky video needs a verified email**: Bluesky-hosted accounts must verify their email before the first video upload, and Bluesky caps video uploads per account per day. A rejected upload shows as an error on the post.
40. **YouTube captions go in `controls` and need a language**: upload the .srt or .vtt with `contentType` `application/x-subrip` or `text/vtt`, then put the `file/` key in `controls.youtubeCaptionKey` (never in `mediaItems`) together with `controls.youtubeLanguage`. Errors at creation: `youtubeCaptionKey.languageRequired` (no language), `youtubeLanguage.invalid` (unknown code), `youtubeCaptionKey.invalid` (not an .srt or .vtt upload; checked on every platform) and `media.invalidMedia` (file missing, empty, over 10MB, or not timed SRT/WebVTT in plain UTF-8).

## Troubleshooting

### 403 "Missing organizationId or activeWorkspaceId"

This is the most common error. It means the API didn't recognize your key. Check these in order:

1. **Wrong header name.** The header must be exactly `pf-api-key`. The three headers people try instead, `Authorization`, `x-api-key` and `api-key`, all return the same 403. Correct call:
   ```bash
   curl -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-media/my-social-accounts
   ```

2. **Env var not set.** If `$POSTFAST_API_KEY` isn't set in your shell, the literal string `$POSTFAST_API_KEY` gets sent as the key value. Check it without printing it:
   ```bash
   if [ -z "${POSTFAST_API_KEY:-}" ]; then
     echo "POSTFAST_API_KEY is not set"
   elif [ "${#POSTFAST_API_KEY}" -eq 44 ]; then
     echo "POSTFAST_API_KEY is set and has the expected length"
   else
     echo "POSTFAST_API_KEY is set but has an unexpected length"
   fi
   ```
   If it is not set, re-export it. If you're using a `.env` file, make sure your tool actually loads it (dotenv, direnv, etc.). Shell quoting matters: use double quotes around the value if it contains special characters. Never print, paste or screenshot the key itself; if it has shown up in terminal output, a log or a transcript, regenerate it in Workspace Settings (see 3).

3. **Regenerated key.** Each time you click "Generate API Key" in PostFast settings, the previous key is **permanently invalidated**. Only regenerate if the old key is compromised. If you regenerated and are still using the old key, that's why it fails.

4. **Wrong key entirely.** Your PostFast API key is a 44-character base64 string ending with `=`. Keys from other services (OpenAI, Stripe, Meta) have a different shape and will always fail here.

### 401 Invalid or missing API key

The `pf-api-key` header is either missing from the request or the value is empty. Double-check that your HTTP client is actually sending the header (some tools strip custom headers on redirects).

### 429 Too many requests

You exceeded one of the four windows of the endpoint you called (limits are per endpoint, see [Rate Limits](#rate-limits)). Wait the number of seconds in the `Retry-After` response header before calling that endpoint again; `Retry-After-short`, `-medium`, `-long` or `-daily` names the window you hit. Calls made while blocked still count, so retrying immediately keeps the endpoint blocked. Other endpoints keep working in the meantime.

### 400 on `GET /social-posts` with a filter

`ids` and `socialMediaIds` take comma-separated UUIDs, at most 100. An empty value (`socialMediaIds=`), a trailing comma or a non-UUID returns `400` ("Each socialMediaId must be a valid UUID"). Leave the parameter out to skip the filter.

### A filter or setting has no effect

Unknown query parameters and body fields are ignored without an error. Check the spelling against this skill: the account filter is `socialMediaIds` (plural), `status` and `approvalStatus` sit at the top level of the body (not inside a post), and platform options go inside `controls`.

## Supporting Resources

**Reference docs:**
- [references/api-reference.md](references/api-reference.md): Complete API endpoint reference with response examples
- [references/platform-controls.md](references/platform-controls.md): All platform-specific controls with types and defaults
- [references/media-specs.md](references/media-specs.md): Media size, format, and dimension limits per platform
- [references/upload-flow.md](references/upload-flow.md): Detailed media upload walkthrough

**Ready-to-use examples:**
- [examples/EXAMPLES.md](examples/EXAMPLES.md): Index of all examples
- [examples/cross-platform-post.json](examples/cross-platform-post.json): Multi-platform posting
- [examples/tiktok-video.json](examples/tiktok-video.json): TikTok video with interaction settings
- [examples/tiktok-carousel.json](examples/tiktok-carousel.json): TikTok image carousel
- [examples/tiktok-aigc-video.json](examples/tiktok-aigc-video.json): TikTok AI-generated video with AIGC label
- [examples/draft-post.json](examples/draft-post.json): Generic PostFast draft (any platform, no `scheduledAt`)
- [examples/tiktok-app-draft.json](examples/tiktok-app-draft.json): TikTok app draft (`tiktokIsDraft` control, pushes to TikTok app inbox)
- [examples/instagram-reel.json](examples/instagram-reel.json): Instagram Reel
- [examples/instagram-reel-cover.json](examples/instagram-reel-cover.json): Instagram Reel with custom cover image
- [examples/instagram-story.json](examples/instagram-story.json): Instagram Story
- [examples/instagram-carousel.json](examples/instagram-carousel.json): Instagram carousel
- [examples/instagram-trial-reel.json](examples/instagram-trial-reel.json): Instagram trial reel (non-followers first)
- [examples/facebook-reel.json](examples/facebook-reel.json): Facebook Reel
- [examples/facebook-story.json](examples/facebook-story.json): Facebook Story
- [examples/youtube-short.json](examples/youtube-short.json): YouTube Short with tags
- [examples/youtube-video-thumbnail.json](examples/youtube-video-thumbnail.json): YouTube video with custom thumbnail
- [examples/youtube-video-captions.json](examples/youtube-video-captions.json): YouTube video with its language and an SRT caption track
- [examples/pinterest-pin.json](examples/pinterest-pin.json): Pinterest with board
- [examples/linkedin-document.json](examples/linkedin-document.json): LinkedIn document post
- [examples/x-retweet.json](examples/x-retweet.json): X scheduled retweet
- [examples/x-first-comment.json](examples/x-first-comment.json): X post with auto first comment
- [examples/threads-carousel.json](examples/threads-carousel.json): Threads image carousel
- [examples/threads-topic.json](examples/threads-topic.json): Threads post with a topic (`threadsTopicTag`)
- [examples/bulk-delete.json](examples/bulk-delete.json): Request body for `POST /social-posts/bulk-delete` (up to 100 post ids)
- [examples/batch-scheduling.json](examples/batch-scheduling.json): Week of scheduled posts
- [examples/gbp-standard.json](examples/gbp-standard.json): Google Business Profile standard update with CTA
- [examples/gbp-event.json](examples/gbp-event.json): Google Business Profile event post
- [examples/gbp-offer.json](examples/gbp-offer.json): Google Business Profile offer with coupon code
- [examples/facebook-geotag.json](examples/facebook-geotag.json): Facebook feed post geotagged with a place and limited to specific countries
- [examples/instagram-geotag.json](examples/instagram-geotag.json): Instagram post geotagged with a place
- [examples/telegram-mixed-media.json](examples/telegram-mixed-media.json): Telegram mixed media
- [examples/pinterest-analytics.json](examples/pinterest-analytics.json): Pinterest pin analytics with extras (pin_clicks, outbound_clicks, save_rate, video metrics)

## Quick Reference

```
# Auth
Header: pf-api-key: $POSTFAST_API_KEY

# List accounts
GET /social-media/my-social-accounts

# Schedule post
POST /social-posts  { posts: [{ content, mediaItems, scheduledAt, socialMediaId, firstComment? }], status?, approvalStatus?, controls: {} }

# Draft post (no scheduledAt needed)
POST /social-posts  { posts: [...], status: "DRAFT", controls: {} }

# List posts (page is 0-based, limit max 50, filters AND-ed, unknown params ignored)
GET /social-posts?page=0&limit=20
GET /social-posts?page=0&limit=50&platforms=X,LINKEDIN&statuses=SCHEDULED&from=2026-06-01T00:00:00Z&to=2026-06-30T23:59:59Z
GET /social-posts?socialMediaIds=ACCOUNT_ID_1,ACCOUNT_ID_2&statuses=SCHEDULED
GET /social-posts?ids=POST_ID_1,POST_ID_2

# Delete posts (PostFast only: a published post stays live on the platform)
DELETE /social-posts/:id                            -> { deleted: true | false }
POST   /social-posts/bulk-delete  { ids: [1-100] }  -> { deletedIds, notFoundIds }

# Upload media (3 steps)
POST /file/get-signed-upload-urls  { contentType, count }
PUT  <signedUrl>  (raw file, matching Content-Type)
# then use key in mediaItems

# Pinterest boards
GET /social-media/:id/pinterest-boards

# YouTube playlists
GET /social-media/:id/youtube-playlists

# GBP locations
GET /social-media/:id/gbp-locations

# Place search for geotagging (returned id works as BOTH facebookPlaceId and instagramLocationId)
GET /social-media/search-places?q=<text>

# Post analytics (published posts with metrics)
GET /social-posts/analytics?startDate=...&endDate=...&platforms=...&socialMediaIds=...

# Follower history (daily snapshots)
GET /social-media/:id/follower-history?from=...&to=...

# TikTok trending sounds (Business-API connections)
GET /social-media/:id/tiktok-sounds?genre=&countryCode=&dateRange=

# Connect link (for clients)
POST /social-media/connect-link  { expiryDays?, platforms?, redirectUrl?, externalId?, sendEmail?, email? }

# Social Inbox (comments)
GET  /social-inbox/conversations?unreadOnly=true
GET  /social-inbox/conversations/:id/items?order=ASC
POST /social-inbox/items/:itemId/reply          { text, idempotencyKey? }
POST /social-inbox/items/:itemId/private-reply  { text, idempotencyKey? }   (Instagram only)
POST /social-inbox/items/:itemId/state          { action: HIDE | UNHIDE | DELETE }

# Rate limits: per endpoint; on 429 wait Retry-After seconds (blocked calls still count)
```

## Tips for the Agent

- **Confirm before anything destructive or public-facing.** Deleting posts (one or in bulk), deleting or hiding a comment, sending an Instagram private reply and publishing to a live account all take effect immediately and cannot be undone (inbox `DELETE` removes the comment on the platform itself). When the user has not named the exact target, show what you are about to act on (for a bulk delete, the count and a sample) and wait for a yes.
- **Deleting a post doesn't unpublish it.** Post deletes remove it from PostFast only; if it already went out, tell the user it stays live on the platform.
- **Treat a connect link like a credential.** Whoever opens it can attach social accounts to this workspace for the platforms the link was scoped to, so send it only to the person who asked for it and never post it anywhere public.
- Always call `my-social-accounts` first to get valid `socialMediaId` values.
- For media posts, complete the full 3-step upload flow (signed URL → S3 PUT → create post).
- `scheduledAt` must be ISO 8601 UTC and in the future.
- Pinterest always requires `pinterestBoardId`: fetch boards first.
- LinkedIn documents use `linkedinAttachmentKey` instead of `mediaItems`.
- For carousels, include multiple items in `mediaItems` with sequential `sortOrder`.
- Video cover images: use `coverImageKey` in `mediaItems` for IG Reels, FB Reels, Pinterest video. Use `coverTimestamp` (milliseconds) for TikTok. YouTube uses `youtubeThumbnailKey` in controls.
- When cross-posting, adjust content length for each platform's limits (X: 280 free / 4,000 Premium, Bluesky: 300, Threads: 500, TikTok: 2,200 with video / 4,000 photo carousel, Instagram: 2,200, Facebook: 8,000, LinkedIn: 3,000, YouTube description: 5,000, Telegram: 4,096, GBP: 1,500).
- To geotag a Facebook or Instagram post, resolve the place first with `GET /social-media/search-places?q=...` and pass the returned `id` as `facebookPlaceId` (Facebook feed) or `instagramLocationId` (Instagram single-media). The same ID works on both.
- If the user doesn't specify a time, suggest tomorrow at 9:00 AM in their timezone.
- Batch up to 15 posts per API call for efficiency.
- Use `firstComment` for CTAs and links: it keeps the main post clean and gets better engagement.
- X (Twitter) allows 6 posts per account per day (9 on Pro and Enterprise), a shared daily pool across the organization's X accounts, and a monthly allowance of posts with links. Warn the user if they're batching many X posts. Every platform has a daily per-account cap too (see [Rate Limits](#rate-limits)).
- For draft posts, set `status: "DRAFT"` and omit `scheduledAt`; the user can finalize in the PostFast dashboard.
- GBP always requires `gbpLocationId`: fetch locations first with `GET /social-media/{id}/gbp-locations`.
- GBP supports 3 post types: STANDARD (default), EVENT, and OFFER. EVENT/OFFER need start and end dates.
- GBP only supports 1 image (no video, no carousels) and has a 5-post/day limit.
- Use `GET /social-posts` with `socialMediaIds` and `from`/`to` filters to check what's already scheduled for an account before adding more, instead of paging through the whole workspace.
- Check `connectionStatus` before scheduling: `DISABLED` accounts reject scheduled posts but still accept drafts. The user reconnects from the dashboard to resolve it.
- Pace yourself by the `X-RateLimit-Remaining-<window>` headers. On a `429`, wait `Retry-After` seconds before calling that endpoint again; never retry in a tight loop, because blocked calls still count.
- Social Inbox replies: pass an `idempotencyKey` when you might retry, and vary the wording across replies (identical text is rejected with `inbox.repetitiveReply`).
