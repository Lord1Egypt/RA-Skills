---
name: markaestro
description: Schedule, publish, and review social posts through Markaestro (Facebook, Instagram, TikTok, Threads, Pinterest, LinkedIn, X, YouTube), read brand and per-post analytics, and manage Intelligent Evergreen queues using its MCP server or public API. Use when a task mentions Markaestro, posting or scheduling to a connected social account, uploading media for a post, checking whether a post published or how it performed, reporting on social performance, deciding what or when to post next, batch-scheduling or editing scheduled content, refreshing analytics, finding the best time to post, writing in a brand's voice, or managing proven recurring content.
---

# Working with Markaestro

Markaestro is a social publishing workspace. Agents reach it through the
Markaestro MCP server (preferred) or the public API at `/api/public/v1`.
The hosted MCP server signs the user in through the browser (OAuth) and
receives a key scoped at consent to one brand or to every brand in the
workspace; the REST API takes that same kind of key as a bearer token.

Tool-by-tool inputs and example outputs are in
[references/tools.md](references/tools.md). Delivery modes, post statuses,
and platform settings are in [references/settings.md](references/settings.md).
Read those when you need an exact field name.

## Before anything else

1. Confirm the MCP server is connected: a `list_products` tool should be
   available. If it is not, the fix depends on the client you are running
   in. Never ask the user for an API key when the client can open a browser;
   the sign-in hands the client a key scoped to the brands the user picks.
   - Installed but not signed in (a 401 or "needs authentication" state):
     Claude Code: run `/mcp`, pick `markaestro`, finish the sign-in.
     Cursor: Cursor Settings, Tools & MCP, click Markaestro (Needs login).
     ChatGPT: reconnect the Markaestro app in Apps & Connectors.
     Grok Build: the next tool call reopens the sign-in; grok.com: reconnect
     the connector. OpenClaw: `openclaw mcp login markaestro`, then
     `openclaw mcp reload`. Hermes: `/reload-mcp`, then call a tool.
   - Not installed at all: send the user to
     `https://markaestro.com/developers/agents?client=<claude-code|claude|cursor|chatgpt|grok|grok-bot|openclaw|hermes>`,
     which opens that client's steps. For Claude Code the whole setup is
     `claude plugin marketplace add markaestro/markaestro-agents` then
     `claude plugin install markaestro@markaestro`; any client can also add
     the server URL `https://markaestro.com/api/public/v1/mcp` directly.
   - Headless or CI only (no browser), and Grok Bot: a workspace API key from
     Settings, API is passed as a header instead:
     `claude mcp add --transport http markaestro https://markaestro.com/api/public/v1/mcp --header "Authorization: Bearer mk_..."`,
     or the local package: `claude mcp add markaestro -e MARKAESTRO_API_KEY=mk_... -- npx -y @markaestro/mcp`.
     `https://markaestro.com/developers/agents?client=headless` has the same
     header for other clients' config files.
2. Call `get_channel_rules` once per session. It returns the per-channel
   rules and `keyMode`. If `keyMode` is `test`, say so when reporting
   results: test keys never reach a real platform.
3. Call `list_products`. The brands in the answer are the ones this
   connection can act on: one for a single-brand connection, every brand
   in the workspace for an all-brands one.
   - Several brands: pass `productId` to `create_post`, `create_posts`,
     `list_posts`, and `create_evergreen_queue`, and to `get_analytics` or
     `list_post_analytics` to report on one brand (without it they cover
     the whole workspace). Confirm the brand with the user when the
     request does not name one.
   - One brand: every call uses it; `productId` can be left out.
   - The user names a brand that is not listed: they reconnect from their
     client (Claude Code: `/mcp`, sign out, sign in) and pick that brand,
     or All brands, at consent.

## The posting model

- `create_post` **saves a draft** unless `scheduledAt` is set. A draft never
  reaches a platform on its own.
- `scheduledAt` (ISO 8601, UTC) makes the post `scheduled`; the worker
  publishes it at that time. Convert the user's local time to UTC and echo the
  UTC time back to them.
- `publish_post` publishes **now**. Ask the user before calling it for anything
  public. It returns a job run; poll `get_job_run` until `succeeded` or
  `failed` and report the message.
- Facebook, Instagram, and TikTok require an explicit `deliveryMode` when
  scheduling: `direct_publish` to post through the platform API, or
  `manual_reminder` for a timed reminder the user posts by hand. Threads,
  Pinterest, LinkedIn, X, and YouTube default to `direct_publish`.
- One post, several channels: pass `targets` (one entry per channel) instead
  of `channel`. Each target can carry its own `destinationId` and
  `deliveryMode`. Platform `settings` may ride on one target only.
- A week of content: `create_posts` takes up to 25 items in one call and
  reports success or failure per item. Check every `ok` before summarizing.
- To change a draft or scheduled post, `update_post` edits its caption,
  media, one channel's `settings`, or (scheduled only) its time; omitted
  fields stay as they are. Published and failed posts cannot be edited, and
  channels are fixed once a post exists.
- Before writing captions, read `get_brand_profile {productId}` for the
  brand's voice and identity. Before picking a time, `suggest_post_times`
  gives the brand's best windows, learned from its own history (null until
  there is enough; then fall back to asking the user).
- TikTok Direct Post: call `get_tiktok_posting_options` first and use one of
  its `privacyLevelOptions` in the tiktok `settings`.

## What agents cannot do

Account settings, billing, team members, API keys, and connecting or
disconnecting social accounts are not available to agents; send the user to
Markaestro for those. Agents also cannot delete a published post or take one
down from a platform, and cannot archive an Evergreen queue: say so and
point the user to Markaestro rather than looking for another way.

## Media

- Upload first with `upload_media` (a public URL or data URL; a file path
  only with the local `@markaestro/mcp` package, since the hosted server
  cannot read your disk), then pass the returned asset id in
  `mediaAssetIds`. Uploads count against the monthly quota, so reuse an asset
  from `list_media` when the same file was uploaded before.
- Instagram, TikTok, and Pinterest require media. LinkedIn requires text.
  Video must be the only media item on LinkedIn and Pinterest. YouTube takes
  exactly one video; a vertical or square video of 3 minutes or less becomes
  a Short on YouTube's side.

## A safe scheduling flow

```
get_channel_rules
list_products                       -> productId, connected channels
list_destinations {productId}       -> only if a channel has several accounts
upload_media {source}               -> asset id (skip for text-only)
create_post {caption, targets|channel, mediaAssetIds, scheduledAt, deliveryMode}
get_post {postId}                   -> confirm status and scheduledAt
```

Report back the post id, status, channels, and the UTC schedule. Mention that
it can be edited with `update_post` or cancelled with `delete_post` until it
publishes.

## Reading the schedule

- `list_posts {status: "scheduled"}` is the queue; `published`, `failed`,
  `platform_action_required`, and `draft` cover the rest.
- `platform_action_required` means a person must finish the post: TikTok inbox
  handoff, or a manual reminder. Say what the next action is; do not treat it
  as failed. Once the user confirms they posted it, `mark_post_posted` (with
  the live link if they have it) records it as published.
- `partial_failed` means some targets published and some did not. Read
  `publishResults` on the post before retrying anything.

## Reading performance

- `get_analytics` is the brand overview for a window (`days`, or `since`
  and `until`): totals with the prior period, per-channel rollups, daily
  series, engagement breakdown, follower trend, top posts, a weekday-by-hour
  heatmap, content-type averages, and `insights` (plain-language findings,
  each with its `sampleSize`). Read it before recommending what, when, or
  where to post, and quote the sample size when you repeat an insight.
- `list_post_analytics` is one row per post with its latest metrics,
  including posts published directly on the platform (`source: "native"`)
  that the connected account was scanned for. `sort: "engagements"` or
  `"views"` finds what worked; `get_post` has the full caption and media
  for a Markaestro row, and `externalUrl` opens a native one. Pass
  `source` to compare the two halves of the account.
- Numbers look stale, or the user just posted: `refresh_analytics` pulls
  live metrics from the platforms now. It is limited to a few calls a
  minute; when `remaining` is above zero, a second call continues the window.
- To take a published post down, the user does it in Markaestro or in the
  platform's own app; agents cannot. `delete_post` only removes drafts and
  posts that have not reached a platform.
- `get_post_analytics_history` shows how one post earned its numbers (the
  1h to 90d snapshots with growth between them) and whether polling is still
  `active`. A post under 24 hours old is not yet comparable to older ones.
- `coverage.bySource` in `get_analytics` says how many analyzed posts were
  Markaestro posts and how many were native. A native post discovered
  today has a `discovered` snapshot only; its history fills in from there.
- The window is clamped to the plan's history; `window.maxDays` in the
  answer says the cap (`-1` is unlimited). If the user asks for more than
  the plan keeps, say so rather than presenting the clamped window as the
  full one.
- `null` means the platform does not report that metric (TikTok and Threads
  never report reach). Never read it as zero, and use
  `engagementRateByViews` where reach is missing.
- These tools need the `analytics.read` scope. A 403 here means the key
  predates the scope: the user creates a new key, or reconnects the agent.

## Intelligent Evergreen

- Call `preview_evergreen_queue` with a published post id first. It returns
  measured eligibility and a recommended cadence without writing anything.
- `create_evergreen_queue` creates a draft policy. It does not schedule posts.
- Ask the user to confirm the cadence, channels, variants, and review policy
  before calling `activate_evergreen_queue`. Show every caption variant and,
  once the user confirms they are accurate, pass `contentConfirmed: true` on
  `create_evergreen_queue` or `update_evergreen_queue`. Activation and resuming
  answer `EVERGREEN_CONTENT_REVIEW_REQUIRED` until that confirmation exists.
- `review_each_run` creates a draft occurrence for each run. It never
  auto-publishes. `approve_future_runs` creates ordinary scheduled posts.
- Pause stops the queue and unschedules its pending occurrence; resume
  restarts it. Archiving is permanent and stays with the user in Markaestro. Use `list_evergreen_runs` to report evaluation outcomes and
  `get_evergreen_analytics` for lifetime metrics and attributed conversions.

## Errors

Every failure carries a stable `code`. The common ones:

| Code | Meaning | What to do |
| --- | --- | --- |
| `UNAUTHENTICATED` | Key missing, revoked, expired, or wrong mode | Ask the user for a valid key |
| `FORBIDDEN` | Key lacks the scope | Ask for a key with the needed scope |
| `VALIDATION_ERROR` with `issues[]` | One or more targets invalid | Fix each listed channel and retry |
| `VALIDATION_SCHEDULED_DELIVERY_MODE_REQUIRED` | Scheduled Meta or TikTok post without `deliveryMode` | Add `deliveryMode` |
| `VALIDATION_POST_IS_PUBLISHING` | Post mid-publish | Wait, then retry |
| `RATE_LIMITED`, `RATE_LIMITED_CHANNEL` | Too many calls or channel ceiling | Wait for `Retry-After`; the server already retried once |
| `QUOTA_EXCEEDED_*` | Plan limit reached | Tell the user which limit |
| `NOT_FOUND` on a post | Not this brand's post | Check the id and the key's brand |

Never invent a post id, an asset id, or a destination id. Read them from the
tools.

## Without the MCP server

The same operations exist as REST calls with
`Authorization: Bearer mk_...` against `https://markaestro.com/api/public/v1`.
The OpenAPI description is served at `/api/public/v1/openapi.json`. Send an
`Idempotency-Key` header on every mutation.
