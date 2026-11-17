# Markaestro MCP tools

Every tool returns JSON text. Failures come back as an error result whose
first line is `CODE (HTTP status): message`, followed by per-channel issues
and a hint. Ids are opaque strings; copy them exactly.

## Discovery

**`get_channel_rules`** `{}` → `{ rules, keyMode: "live" | "test", baseUrl }`

**`list_products`** `{}` → `{ products: [{ id, name, channels: [...] }], count }`
One entry for a single-brand connection; every brand in the workspace for an
all-brands connection, which then passes `productId` to `create_post`,
`create_posts`, `list_posts`, `create_evergreen_queue`, and (to report on one
brand rather than the workspace) `get_analytics` and `list_post_analytics`.

**`list_destinations`** `{ productId }` →
`{ destinations: [{ id, channel, provider, label, deliveryMode, ... }], count }`
Needed only when one channel has several accounts (two Facebook Pages, say).

## Posts

**`list_posts`** `{ status?, limit? (1-100), cursor? }` → `{ posts: [...], nextCursor }`
Statuses: `draft`, `scheduled`, `publishing`, `published`,
`platform_action_required`, `failed`, `partial_failed`.

**`get_post`** `{ postId }` → `{ post }`
A post carries `status`, `caption`, `targets[]`, `mediaAssetIds`,
`scheduledAt`, `publishedAt`, `externalUrl`, `publishResults[]`, `nextAction`.

**`create_post`**
```json
{
  "caption": "Launch day.",
  "targets": [
    { "channel": "linkedin" },
    { "channel": "instagram", "deliveryMode": "direct_publish",
      "settings": { "__type": "instagram", "postType": "feed" } }
  ],
  "mediaAssetIds": ["ast_123"],
  "scheduledAt": "2026-09-10T14:00:00Z"
}
```
→ `{ post, note }`. Without `scheduledAt` the post is a draft. For one channel
use `channel` (plus optional `destinationId`, `deliveryMode`, `settings`)
instead of `targets`. Never send both.

**`create_posts`** `{ posts: [ ...up to 25 create_post bodies ] }` →
`{ results: [{ ok, post } | { ok: false, error }], created, total }`

**`publish_post`** `{ postId }` → `{ run: { id, status, ... } }`
Publishes now. Poll `get_job_run` with `run.id`.

**`update_post`** `{ postId, caption?, mediaAssetIds?, settings?, scheduledAt? }` → `{ post }`
Edits a draft or scheduled post; omitted fields keep their value.
`mediaAssetIds` replaces the media. `settings` carries one channel's settings
with `__type` naming that channel. `scheduledAt` only reschedules a post that
is already scheduled. Errors: `VALIDATION_POST_NOT_EDITABLE` (published,
publishing, or failed), `VALIDATION_POST_NOT_SCHEDULED` (scheduledAt on a
draft), `VALIDATION_SETTINGS_CHANNEL_NOT_TARGETED`, plus any channel rule the
new caption or media breaks.

**`mark_post_posted`** `{ postId, externalUrl? }` → `{ post: { id, status: "published", externalId, externalUrl } }`
Only for a post in `platform_action_required`, after the user confirms they
posted it. Needs `posts.publish`.

**`delete_post`** `{ postId }` → `{ deleted: true, id, ... }`
Removes a draft, or cancels a scheduled, failed, or waiting-to-be-posted post.
A published post is refused: taking posts down stays with the user in
Markaestro.

**`bulk_posts`**
`{ ids: [...], action: "reschedule", scheduledAt }` or
`{ ids, action: "status", status: "draft" | "scheduled" }`
→ `{ succeeded: [ids], failed: [{ id, error }] }`

## Media

**`upload_media`** `{ source, fileName?, contentType? }` → `{ asset: { id, type, url, width, height, ... } }`
`source` is a public http(s) URL or a `data:` URL; the local
`@markaestro/mcp` package also takes a file path (the hosted server refuses
one, because it cannot read the caller's disk). The type is inferred from the
extension when `contentType` is omitted.

**`list_media`** `{ type?: "image" | "video", limit?, cursor? }` → `{ assets: [...], nextCursor }`

**`get_media`** `{ assetId }` → `{ asset }` with `processingState` and `refCount`.

## Intelligent Evergreen

**`preview_evergreen_queue`** `{ sourcePostId }` → eligibility evidence and a recommended cadence. Read-only.

**`create_evergreen_queue`** `{ sourcePostId, name, variants, channels?, intervalDays?, timeZone?, localHour?, localMinute?, scheduleMode?, reviewPolicy?, expiresAt? }` → a draft queue.

**`get_evergreen_queue`**, **`list_evergreen_queues`**, and
**`list_evergreen_runs`** read policy and occurrence history.

**`get_evergreen_analytics`** returns source metrics, queue-lifetime metrics,
tracked clicks, conversions, and recent run outcomes. Unavailable provider
metrics remain `null`.

**`update_evergreen_queue`** requires the current `version`, preventing a stale
client from overwriting someone else's edit.

**`activate_evergreen_queue`** schedules future occurrences. Confirm with the
user first. It needs the user's caption confirmation, recorded with
`contentConfirmed: true` on create or update; without it the call answers
`EVERGREEN_CONTENT_REVIEW_REQUIRED`. **`pause_evergreen_queue`** unschedules the pending occurrence,
and **`resume_evergreen_queue`** computes a fresh next run. Archiving a queue
is permanent and stays with the user in Markaestro.

## Analytics (needs the `analytics.read` scope)

**`get_analytics`** `{ days?, since?, until?, channel?, source?, tz? }` → `{ analytics: { window, totals, daily, priorDaily, dailyActivity, breakdown, followerTrend, channels, leaderboard, heatmap, contentTypes, insights, coverage } }`
`window.maxDays` is the plan cap (`-1` unlimited); `totals.prior` is the
period before the window; `heatmap.engagements[weekday][hour]` uses `tz`
(minutes east of UTC, default 0, Monday is 0). `insights[].sampleSize` says
how many posts each finding rests on. The account as a whole is counted:
`source` is `markaestro` or `native` to narrow to one half, and
`coverage.bySource` reports both counts.

**`list_post_analytics`** `{ days?, since?, until?, channel?, source?, sort?, limit? }` → `{ window, sort, posts: [{ id, content, channels, publishedAt, externalUrl, contentType, source, views, reach, likes, comments, shares, saves, clicks, engagements, erByReach, erByViews }], count, truncated }`
`source` on a row is `markaestro` (went out through Markaestro) or `native`
(published directly on the platform, discovered from the connected account).
`sort` is `published_at` (default), `views`, `reach`, `engagements`, or
`engagement_rate`, descending, missing values last. `limit` defaults to 100
(max 500); `truncated` is true when more matched. `content` is the first 160
characters; use `get_post` for the whole caption.

**`get_post_analytics_history`** `{ postId }` → `{ post: { id, content, publishedAt, channels, externalUrl, source, metricsStatus, nextPollAt, latest }, stages: [{ stageKey, capturedAt, hoursAfterPublish, views, reach, engagements, likes, comments, shares, saves, viewsDelta, engagementsDelta, byChannel }] }`
Stages are oldest first (`1h`, `6h`, `24h`, ... `90d`, then `latest`); a
native post starts with `discovered`. Any id from the leaderboard or the
list works, whichever source it came from.
`NOT_FOUND` for a post outside this brand, a draft, or a sandbox post.

**`refresh_analytics`** `{ days?, channel?, productId? }` → `{ refresh: { updated, remaining, followersUpdated, errorCount, firstError, refreshedAt, ... } }`
Pulls live metrics from the platforms now. Limited to 4 calls a minute; when
`remaining` is above zero, call again to continue the window.

**`suggest_post_times`** `{ productId? }` → `{ bestTimes: { productId, objective, timing, readiness: { datedPosts, objectiveMeasured }, computedAt } }`
The brand's best posting windows, learned from its own history. `timing` is
null until there is enough history. Needs a plan with Intelligence.

## Brands

**`get_brand_profile`** `{ productId }` → `{ profile: { productId, name, description, url, categories, brandVoice, brandIdentity } }`
Read-only. Use the voice when writing captions.

**`get_tiktok_posting_options`** `{ productId? }` → `{ creatorInfo: { privacyLevelOptions, commentDisabled, duetDisabled, stitchDisabled, maxVideoPostDurationSec, creatorUsername, sandbox } }`
Read right before a TikTok Direct Post and use one of `privacyLevelOptions`.
Test keys get `sandbox: true`. Needs `posts.publish`.

## Publish runs

**`get_job_run`** `{ runId }` → `{ run: { status: queued | running | succeeded | failed, message, details } }`

**`list_job_runs`** `{ status?, resourceId? (a post id), limit?, cursor? }` → `{ runs: [...], nextCursor }`
