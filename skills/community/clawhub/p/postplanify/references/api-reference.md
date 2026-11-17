# PostPlanify API reference

Base URL: `https://api.postplanify.com/api/v1`
Auth: `Authorization: Bearer $POSTPLANIFY_API_KEY` on every request.
All timestamps are UTC, ISO 8601. The machine-readable spec is at https://postplanify.com/openapi.yaml.

## Responses

Success:

```json
{ "ok": true, "data": { } }
```

List endpoints that paginate add:

```json
{ "pagination": { "page": 1, "limit": 20, "total": 48, "has_more": true } }
```

Error:

```json
{ "ok": false, "error": { "code": "VALIDATION_ERROR", "message": "youtubeParams.title is required for YouTube posts" } }
```

| Status | Code | Meaning | What to do |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Bad or missing field; the message names it | Fix the field or ask the user |
| 401 | `UNAUTHORIZED` | Missing, invalid or expired key | Ask the user to check `POSTPLANIFY_API_KEY` |
| 403 | `SUBSCRIPTION_INACTIVE` | The account has no plan with API access (Premium or higher) | Stop and tell the user |
| 403 | `FORBIDDEN` | Workspace needs a subscription, plan post limit reached, or the user's role does not allow the action | Stop and tell the user |
| 404 | `NOT_FOUND` | Does not exist, or the key cannot access it | Re-check the id |
| 400 | `INVALID_MEDIA_URL` | `/media/from-url` could not download the file, or its type is not allowed | Check the URL is public and the file type |
| 413 | `FILE_TOO_LARGE` | Media file larger than 100 MB | Use a smaller file |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests, or too many posts for one account in a window | See SKILL.md safety rule 7 |
| 500 | `INTERNAL_ERROR` | Server error | Retry once later; report if it persists |

Rate limit headers `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset` come with every response.

## Account

### `GET /me`

Returns the user the key belongs to: `id`, `email`, `fullName`. Use it to check the key.

## Workspaces

### `GET /workspaces`

All workspaces the user can access. Each item: `id`, `name`, `websiteUrl`, `logoUrl`, `domain`, `socialAccounts[]` (`id`, `platform`, `accountName`, `accountUrl`, `profilePictureUrl`, `customLabel`).

### `GET /workspaces/{id}`

One workspace with its social accounts.

## Social accounts

Platforms: `FACEBOOK`, `INSTAGRAM`, `X`, `LINKEDIN`, `TIKTOK`, `YOUTUBE`, `THREADS`, `BLUESKY`, `PINTEREST`, `GOOGLE_BUSINESS`.

### `GET /social-accounts`

Every connected account across all workspaces, each with `id`, `workspaceId`, `platform`, `accountName`, `accountUrl`, `profilePictureUrl`, `customLabel`.

### `GET /social-accounts/{id}`

One account.

### `GET /social-accounts/{id}/pinterest-boards`

Pinterest accounts only (other platforms return `400`). Returns `[{ "id": "715376267631025391", "name": "Recipes" }]`. Use `id` as `pinterestParams.boardId`.

## Posts

Statuses: `SCHEDULED`, `RESCHEDULED`, `PUBLISHED`, `CANCELLED`. Drafts are not available through the API.

Post object fields: `id`, `workspaceId`, `caption`, `status`, `platform`, `socialPlatformPostId` (native id once published), `isStory`, `shortenLinks`, `utmCampaign`, `scheduledAt`, `publishedAt`, `createdAt`, `updatedAt`, `socialAccount`, `medias[]` (`id`, `name`, `url`, `type`, `size`, `width`, `height`, `duration`, `coverImageUrl`), `logs[]` (`type`: `SUCCESS` | `ERROR` | `WARNING` | `INFO`, `message`, `createdAt`), `platformParams`, `label` (`name`, `color` or `null`), `metrics`.

`metrics` (or `null` when no analytics have been collected, which is not zero): `views`, `likes`, `comments`, `shares`, `engagementRate`, `platformMetrics` (platform extras such as X bookmarks or Instagram saves), `measuredAt` (date of the snapshot, refreshed daily).

### `GET /posts`

Query parameters:

| Name | Required | Notes |
|---|---|---|
| `workspaceId` | yes | |
| `status` | no | One of the statuses above |
| `socialAccountId` | no | |
| `platform` | no | |
| `from`, `to` | no | ISO 8601; matches posts scheduled or published in the range (`to` is exclusive) |
| `includeMetrics` | no | `true` attaches `metrics` to each post |
| `page` | no | Default 1 |
| `limit` | no | Default 20, max 100 |

### `POST /posts`

Create and schedule a post for one social account. Returns `201` with the post.

| Field | Required | Notes |
|---|---|---|
| `workspaceId` | yes | |
| `socialAccountId` | yes | Must belong to `workspaceId` |
| `scheduledAt` | yes | UTC, in the future |
| `caption` | no* | *A post needs a caption, media, or both |
| `mediaIds` | no | Ids from `/media/upload`, `/media/from-url` or `GET /media`. Library media must belong to the same workspace |
| `isStory` | no | Instagram and Facebook only, exactly 1 media |
| `youtubeParams`, `tiktokParams`, `pinterestParams`, `googleBusinessParams` | per platform | Only for the matching platform, see `platform-configs.md` |
| `xCommunityId`, `xTaggedUsers` | no | X only |
| `shortenLinks` | no | Shorten links with the workspace's Bitly at publish time |
| `utmCampaign` | no | Used with `shortenLinks`, max 100 chars |

Sending params for the wrong platform (for example `youtubeParams` on an Instagram post) returns `400`.

Possible `403`: the workspace has no active subscription, or the plan's post limit is reached (the message says which).
Possible `429`: more than 6 posts in an hour or 100 in a day for that social account.

### `GET /posts/{id}`

One post, always including `metrics`, `logs` and `platformParams`.

### `PATCH /posts/{id}`

Edit a `SCHEDULED` or `RESCHEDULED` post. Send only the fields to change: `caption`, `scheduledAt` (future), the matching platform params, `xCommunityId`, `xTaggedUsers`, `shortenLinks`, `utmCampaign`. Changing `scheduledAt` reschedules it. Returns the updated post.

### `POST /posts/{id}/cancel`

Stop a `SCHEDULED` or `RESCHEDULED` post from publishing. The post stays, with status `CANCELLED`. Returns the post.

### `DELETE /posts/{id}`

Permanently delete a post. Cannot be undone. Returns `{ "id": "..." }`.

## Media

Allowed: JPEG, PNG, GIF, WebP, MP4, MOV, PDF (LinkedIn documents). Max 100 MB.
Media object: `id`, `name`, `url`, `type` (MIME), `size`, `createdAt`, `source` (`upload` or `library`, on `GET /media`).

### `POST /media/from-url`

JSON body `{ "url": "https://...", "filename": "optional.jpg" }`. The server downloads the file (redirects followed). Returns `201` with the media object. `400` if the URL is invalid, unreachable or the type is not allowed; `413` if over 100 MB.

### `POST /media/upload`

`multipart/form-data` with a `file` field:

```bash
curl -s -X POST https://api.postplanify.com/api/v1/media/upload \
  -H "Authorization: Bearer $POSTPLANIFY_API_KEY" \
  -F "file=@photo.jpg"
```

### `GET /media`

| Name | Notes |
|---|---|
| `workspaceId` | Include this workspace's dashboard media library. Without it, only API uploads are returned |
| `type` | `image` or `video` (library items) |
| `page`, `pageSize` | Library paging, default 50, max 100 |

### `DELETE /media/{id}`

Delete an uploaded file. Returns `204`. Posts already published are not affected.

## Analytics

Analytics sync periodically, so figures can lag by up to a day.

### `GET /analytics/{workspaceId}/overview`

Last 7 days for the whole workspace:

- `accounts[]`: `id`, `platform`, `accountName`, `customLabel`, `analyticsLastSyncAt`, `currentFollowers`, `followersChange`, `followersChangePct`, `views`, `engagement`, `avgEngagementRate`, `postCount`
- `topPosts[]`: top 10 by views, with `platform`, `text`, `postUrl`, `thumbnailUrl`, `views`, `likes`, `comments`, `shares`, `engagementRate`, `label`
- `dailyViews[]`: `date`, `views`, `engagement`
- `followerSnapshots[]`

### `GET /analytics/{workspaceId}/{socialAccountId}`

Account and post metrics for one account. The shape depends on the platform. Common: `meta.lastUpdated`; post items have `engagementRatePct`, `totalInteractions` and `internalLabel`; account objects have follower and following counts.

### `GET /analytics/{workspaceId}/{socialAccountId}/trends`

`days` query parameter, 1 to 365, default 30. Returns:

- `accountSnapshots[]`: `date`, `followersCount`, `followingCount`
- `dailyMetrics[]`: `date`, `totalViews`, `totalLikes`, `totalComments`, `totalShares`, `totalEngagement`, `weightedEngagementRate`
- `account.platform`

## Comments

Available for Instagram, Facebook, LinkedIn and Google Business (reviews). Synced in the background, so results reflect the last sync.

Comment object: `id` (platform-native; LinkedIn ids are URNs), `workspaceId`, `parentCommentId`, `text`, `username` (LinkedIn shows `"LinkedIn User"` for others), `timestamp`, `likeCount`, `replyCount`, `isHidden`, `isRead`, `brandReplied`, `rating` (1 to 5, Google reviews only), `socialAccount`, `post` (`permalink`, `caption`, `mediaUrl`, ...).

### `GET /comments`

| Name | Required | Notes |
|---|---|---|
| `workspaceId` | yes | |
| `socialAccountId` | no | |
| `platform` | no | `INSTAGRAM`, `FACEBOOK`, `LINKEDIN` or `GOOGLE_BUSINESS` |
| `unreadOnly` | no | `true` for unread only |
| `page` | no | Default 1 |
| `limit` | no | Default 20, max 50 |

Top-level comments only, newest first.

### `GET /comments/{platformCommentId}/replies`

Replies to one comment, oldest first. URL-encode LinkedIn URNs: `urn:li:comment:(activity:12345,67890)` becomes `urn%3Ali%3Acomment%3A%28activity%3A12345%2C67890%29`.

### `POST /comments/{platformCommentId}/reply`

Body `{ "message": "Thanks!" }`. Posts publicly on the platform immediately. Returns `201` with the new reply's `id` and `parentCommentId`.

Max length: Instagram 2,200, Facebook 8,000, LinkedIn 1,250, Google Business 4,096 characters. Replying to a hidden comment returns `400`.
