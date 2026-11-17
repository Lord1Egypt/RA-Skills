---
name: mellow-hub
description: Publish or schedule posts to Instagram, TikTok, YouTube, X, LinkedIn, Threads, Bluesky, Pinterest and Facebook through Mellow Hub (remote MCP server or REST API) — use whenever asked to publish to social networks, cross-post, schedule posts, or check a post against a network's rules via Mellow Hub.
metadata:
  version: "1.0.0"
  homepage: https://www.mellow.world/hub/docs
  mcp: https://www.mellow.world/mcp
---

# Mellow Hub — publishing through an agent

Mellow Hub publishes one post to many social networks and checks every
network's own rules before anything goes out. You reach it two ways, and both
resolve to the same functions:

- **MCP** (preferred): `https://www.mellow.world/mcp` — Streamable HTTP, OAuth
  2.1 with dynamic client registration and PKCE, or an owner-issued API key as
  the bearer. 21 tools, 4 guide resources, 3 prompts.
- **REST**: `https://www.mellow.world/api/hub/v1` — `Authorization: Bearer
  mk_live_…` (an API key the owner creates at `https://www.mellow.world/hub/agents`).

Full reference: https://www.mellow.world/hub/docs (the same text as
`https://www.mellow.world/hub/llms.txt` and the MCP resource `mellow://guide/start`).

## 1. Connect

### MCP with OAuth (Claude Code, Claude.ai, ChatGPT, Cursor, Hermes, OpenClaw…)

Claude Code:

```sh
claude mcp add --transport http mellow https://www.mellow.world/mcp
```

Then authenticate when the client asks; the server answers the first request
with a 401 that points to `/.well-known/oauth-protected-resource`, and a
client that supports OAuth discovery completes registration, PKCE and the
consent screen by itself. The **person** approves on the consent screen: which
channels, which scopes, review or autopilot, a daily ceiling (1–1000, default
50) and an expiry (1–30 days, default 7). Only `channels:read` and
`posts:read` are pre-checked and the default mode is **review**, so if you
need to publish, ask the person to tick `posts:write`, `posts:publish`,
`media:write` and choose autopilot.

Generic `mcp.json` (Cursor, Codex, OpenClaw and other clients that read this
shape):

```json
{
  "mcpServers": {
    "mellow": {
      "type": "http",
      "url": "https://www.mellow.world/mcp"
    }
  }
}
```

If the client cannot do OAuth, an API key works as the bearer on the same
endpoint (never paste it into chat; read it from the environment):

```json
{
  "mcpServers": {
    "mellow": {
      "type": "http",
      "url": "https://www.mellow.world/mcp",
      "headers": { "Authorization": "Bearer ${MELLOW_HUB_KEY}" }
    }
  }
}
```

Hermes: `hermes mcp add --url https://www.mellow.world/mcp --auth oauth mellow`
then `hermes mcp login mellow`.

### REST with an API key

The owner creates a key at `/hub/agents` (`POST /api/hub/v1/keys` takes
`name`, `scopes`, `mode`, `channelScope`, `dailyPostLimit` — default 50 —
and `expiresInDays`). Default key scopes are `channels:read media:write
posts:read posts:write posts:publish metrics:read`; `channels:connect` and
`ai:generate` must be added on purpose. Keys start with `mk_live_` and are
bound to one profile — a profile header cannot switch them.

```sh
curl --fail-with-body https://www.mellow.world/api/hub/v1/whoami \
  -H "Authorization: Bearer $MELLOW_HUB_KEY"
```

## 2. The required call order

Always in this order. Each step's answer changes what the next may do.

| Step | MCP tool | REST | What to read |
| --- | --- | --- | --- |
| 1 | `whoami` | `GET /whoami` | `mode` (`autopilot` publishes; `review` only prepares), `scopes`, `channels` the credential may touch, `postsRemainingToday`, `subscription.active` and `subscription.upgradeUrl`. If `active` is false, say so to the person before doing anything else: publishing will be refused, everything else works. |
| 2 | `list_channels` | `GET /channels` | Channel ids starting `spc_`; these are what you name in `channels`. Pass `refresh: true` only after a person just connected something. |
| 3 | `register_media` **or** `request_upload_url` | `POST /media` (JSON `url`, or multipart `file` ≤ 4 MB), `POST /media/upload-url` | For a public https URL: `register_media` does a HEAD check and returns `kind`/`contentType`; nothing is copied, the network fetches the URL at publish time — the URL must still resolve then. For bytes you hold, or any video: `request_upload_url` → PUT the bytes to `uploadUrl` with their `Content-Type`, then use `mediaUrl`. The inline upload accepts JPEG, PNG, WebP, GIF, HEIC, MP4, MOV, WebM; the signed-URL path hands bytes to the provider as-is. Provider storage is temporary (purged within a day if unused). |
| 4 | `validate_post` | `POST /validate` | Free, publishes nothing, returns **every** problem at once: `{ ok, issues[], notes[] }`. Fix all `issues`, re-validate, and only then continue. `ok: true` can come with `notes` worth reading (options for a network not in the post, an unpositioned tag). |
| 5 | `create_post` | `POST /posts` with `Idempotency-Key` header (or `idempotencyKey` in the body) | Publishes now, or schedules with `scheduledAt`. Under review mode it prepares the post (`pending_review`) and stops. Never call without validating first. |
| 6 | `get_post` | `GET /posts/{id}` | Read `targets`, not just `status`. Each channel succeeds or fails on its own; `partial` means some published. A successful create is not proof every network published. |

Optional afterwards: `preview_post` (how it will read per network; needs a
valid post), `list_posts` (find a post after a timeout), `reschedule_post`,
`cancel_post` (needs `confirm: true`), `get_metrics` (needs `metrics:read`),
`list_platforms` (needs no scope).

## 3. Idempotency keys — non-negotiable

- `create_post` refuses a request without `idempotencyKey`: 8–120 characters
  from `A-Z a-z 0-9 _ . : -`.
- Derive it from the task, not at random: `week-38-tue-morning`,
  `blog-142-linkedin`, `client-acme-launch-2026-09-25`.
- A timeout is not a refusal. Retry the **same** request with the **same**
  key: Mellow returns the original post instead of a second publication.
- Reusing a key for **different** content is refused with
  `idempotency_key_reused` (409). Do not generate a new key to get past it —
  compare with what you sent before.
- Recovering a `partial` post uses a **new** key and names **only the failed
  channels**.

## 4. The post

```json
{
  "caption": "The long version, written for LinkedIn…",
  "media": ["https://cdn.example.com/clip.mp4"],
  "channels": ["spc_linkedin", "spc_bluesky", "spc_x", "spc_youtube"],
  "scheduledAt": "2026-09-25T10:00:00Z",
  "options": {
    "youtube": { "title": "Why we rebuilt the editor", "privacyStatus": "public" }
  },
  "perChannel": {
    "spc_bluesky": { "caption": "The short version." },
    "spc_x": { "caption": "The short version." }
  },
  "idempotencyKey": "editor-rebuild-2026-09-25"
}
```

- `caption` — one text for the post (up to 63,206 characters overall; each
  network has its own limit, checked per channel).
- `media` — ordered list, up to 35 items; each a public https URL or
  `{ url, thumbnailUrl?, thumbnailTimestampMs?, tags? }`. `tags` mark accounts
  on the picture (Instagram and Facebook only, max 20) — not collaborators.
- `channels` — 1 to 25 `spc_…` ids, no duplicates.
- `scheduledAt` — ISO 8601 with a timezone, in the future; omit to publish now.
- `options` — per-network settings keyed by platform id; applies to every
  channel of that network.
- `perChannel` — overrides for one channel (caption, media, that network's
  options); wins over `options`. This is how Bluesky gets 300 characters while
  LinkedIn keeps 3,000.
- `draft: true` — keep it in Mellow, send nothing (free of the monthly
  allowance; still counts toward the credential's daily ceiling).

Platform ids: `instagram`, `tiktok`, `tiktok_business`, `youtube`, `x`,
`linkedin`, `threads`, `bluesky`, `pinterest`, `facebook`.

## 5. Per-network rules (from Mellow's platform registry)

| Network | Caption | Title | Media | Placement | Options worth knowing |
| --- | --- | --- | --- | --- | --- |
| Instagram | ≤ 2,200, optional | — | 1–10, image or video; stories exactly 1; reels 1 video | `timeline`, `reels`, `stories` | `placement`, `collaborators` (≤ 3), `shareToFeed`, `location`, `trialReelType` (`manual`/`performance`), `audioName`. Professional (Business/Creator) account only. |
| TikTok | ≤ 2,200, optional | ≤ 90, optional (headline on photo posts) | 1 video **or** up to 35 images; never mixed | — | `title`, `privacyStatus` (`public`/`private`), `allowComment`, `allowDuet`, `allowStitch`, `discloseYourBrand`, `discloseBrandedContent`, `isAiGenerated`, `isDraft`, `autoAddMusic` |
| TikTok Business | ≤ 2,200, optional | ≤ 90, optional | 1 video or up to 35 images | — | Same as TikTok; a second TikTok connection mode, not a tenth network |
| YouTube | ≤ 5,000, optional (becomes the description) | ≤ 100, **required** | exactly 1 video (landscape allowed; square/vertical ≤ 3 min may become Shorts — there is no Shorts switch) | — | `title` (required), `description`, `tags` (≤ 30), `categoryId`, `defaultLanguage`, `privacyStatus` (`public`/`private`/`unlisted`), `embeddable`, `license`, `publicStatsViewable`, `publishAt`, `madeForKids`, `containsSyntheticMedia`, `recordingDate` |
| X | ≤ 280, optional (standard tier; Mellow cannot see premium) | — | 0–4 images or 1 video; text alone is fine | — | `poll` (2–4 options, 5–10,080 minutes), `communityId`, `quoteTweetId`, `replySettings` |
| LinkedIn | ≤ 3,000, **required** | — | 0–20 images or 1 video | — | `resharePostId`. Company page needs admin rights; personal profile needs Mellow's own LinkedIn app |
| Threads | ≤ 500, optional | — | 0–20; text alone is fine | `timeline`, `reels` | `placement` |
| Bluesky | ≤ 300 **graphemes**, **required** | — | 0–4 images or 1 video | — | none. Connected with handle + app password, not OAuth |
| Pinterest | ≤ 500, optional (pin description) | ≤ 100, optional | exactly 1 image or video | — | `title`, `boardIds` (≤ 10; optional — the provider pins to the first board if none is named), `link` |
| Facebook | ≤ 63,206, optional | — | 0–10; stories exactly 1; reels 1 video | `timeline`, `reels`, `stories` | `placement`, `location`, `collaborators` (≤ 10), `setCaptionForEachImage`. Pages only, never personal timelines |

Video thumbnails: `thumbnailUrl` on the media item where the network accepts
one (Instagram, TikTok Business, YouTube, Facebook). Mellow does not download
media, so duration, resolution and aspect ratio are the network's own
judgement — passing `validate_post` does not settle them.

## 6. Errors and what to do

Every error carries `code`, a sentence and `retryable`. If `retryable` is
false, the same request will fail the same way; change the request or stop.

| Code | Where | What to do |
| --- | --- | --- |
| `subscription_required` (402) | `create_post` unless `draft` | Stop. Relay the message and the upgrade URL from `whoami` (`https://www.mellow.world/hub/pricing`) to the person. Connecting, drafting, validating and previewing keep working. |
| `monthly_limit_reached` (402) | `create_post` | The plan's publications for this month are spent (a post counts once per destination). Publish to fewer networks, wait for the month, or the person changes plan. Never split the post to sneak under the limit without asking. |
| `daily_limit_reached` (429) | `create_post` | This credential's rolling-24-hour ceiling is used up (drafts and cancelled posts count too). Stop and tell the person; only the owner can raise it. |
| `invalid_request` with `issues[]` (400) — the audit journal calls this `validation_failed` | `create_post` | You skipped or ignored `validate_post`. Fix every listed issue (each names the channel and field), validate again, then create. |
| `insufficient_scope` (403) | any tool | The credential lacks that permission. Ask the owner to grant it when creating the key or approving the connection; do not retry. |
| `channel_not_connected` (400) / `channel_out_of_scope` (403) | validation and posts | Call `list_channels`; use only the channels the credential was given. Reading or changing a stored post requires access to every destination in it. |
| `idempotency_key_reused` (409) | `create_post` | You sent different content under an old key. Use a new key — after checking you are not duplicating. |
| `confirmation_required` (400) | `cancel_post` | Set `confirm: true` — only after the person asked for the cancellation. |
| `already_published` (409) | `cancel_post` | Nothing can unpublish through an API; a person deletes it in the network. |
| `not_movable` (409) | `reschedule_post` | Only scheduled posts move; drafts and published posts do not. |
| `schedule_in_past` | validation | Omit `scheduledAt` to publish now, or give a future time. |
| `caption_too_long`, `caption_required`, `title_required`, `title_too_long`, `media_required`, `media_too_many`, `media_kind_unsupported`, `media_kinds_mixed`, `placement_unsupported`, `story_media_count`, `reel_media_count`, `reel_needs_video`, `option_required` | `validate_post` issues | Fix the named field for the named channel — usually with `perChannel` for one channel or `options.<platform>` for a network. |
| `media_url_invalid` / `media_url_unreachable` | `register_media` | Media must be a public https URL the network can fetch. |
| `provider_error` (retryable flag), `provider_result_failed`, `result_never_confirmed` | after sending | Read `retryable`; for a failed target read its `errorMessage`; if never confirmed, check the account before republishing. |
| `workspace_mismatch` (403) | any | A machine credential cannot switch profiles; use the credential made for the profile you need. |

## 7. The human stays in the loop

- **Connecting an account is not yours to do.** `connect_channel` returns a
  URL and a sentence saying who has to open it; Bluesky additionally needs a
  handle and an app password typed by the person. Pass both on and wait; then
  `list_channels` with `refresh: true`. The link lives ten minutes.
- **Review mode means "prepare and stop".** `whoami.mode === "review"` →
  `create_post` yields `pending_review`; tell the person it is waiting for
  approval in Mellow. Approval is refused to any non-person actor
  (`approval_requires_person`).
- **Studio credits are money.** `studio_generate` spends AI credits (outline 2,
  cover/illustration 10) and needs the explicit `ai:generate` scope. Quote
  first with `studio_quote`, then ask before spending unless the person already
  delegated that expense. Buying credits or changing a plan is never done by
  an agent.
- **Publishing is public and cannot be undone.** Say so before an immediate
  `create_post` when the person did not explicitly ask to publish now.

## 8. Safety rules

1. Never publish under a mode the person did not choose: read `whoami` and
   act within `mode`, `scopes` and `channels`. Do not ask for a broader key
   to work around a refusal.
2. Respect the daily ceiling: check `postsRemainingToday` before a batch;
   if a plan needs more posts than remain, tell the person instead of
   spreading them over credentials or keys.
3. Validate every post, every time, before `create_post`. Never send a
   `partial` post again in full.
4. One stable idempotency key per post; the same key on retry; a new key only
   for genuinely new content.
5. Never echo, log or store an API key, an OAuth token or a signed
   `uploadUrl`. Refer to keys as `$MELLOW_HUB_KEY`.
6. Do not fabricate results: a `create_post` response is not a publication.
   Report `targets[].status` and the public `url` from `get_post`.
7. Everything you do is journaled for the owner (`hub_audit_events`) and
   visible at `/hub/agents`; act as if the journal will be read.

## 9. REST quick reference

Base `https://www.mellow.world/api/hub/v1`, header `Authorization: Bearer
$MELLOW_HUB_KEY`, JSON bodies, camelCase.

| Method and path | Scope | Notes |
| --- | --- | --- |
| `GET /whoami` | `channels:read` | Same payload as the MCP tool |
| `GET /channels` | `channels:read` | `?refresh=true` re-reads from the provider |
| `POST /channels` | `channels:connect` | Returns the URL a person opens |
| `DELETE /channels/{id}` | `channels:connect` | Disconnect |
| `POST /media` | `media:write` | JSON `{ "url" }` = the `register_media` HEAD check; multipart `file` part ≤ 4 MB = inline upload in one hop |
| `POST /media/upload-url` | `media:write` | Signed PUT target for large files and video |
| `POST /validate` | `posts:read` | `{ ok, issues, notes }`; HTTP 200 even when `ok: false` |
| `GET /posts` | `posts:read` | `?status=…&limit=…` |
| `POST /posts` | `posts:write`, `posts:publish` | `Idempotency-Key` header or `idempotencyKey` body; 201 on create **and** on idempotent replay |
| `GET /posts/{id}` | `posts:read` | Per-target results |
| `PATCH /posts/{id}` | `posts:write` | Reschedule (`scheduledAt`) |
| `DELETE /posts/{id}` | `posts:write` | Cancel |
| `POST /posts/{id}/approve` | `posts:publish`, **signed-in person only** | Agents receive `approval_requires_person` |
| `GET /metrics` | `metrics:read` | `?channelId=…&limit=…` |
| `GET /platforms`, `GET /pricing` | none | Public JSON |

Validate then create, with the public example from
https://www.mellow.world/hub/guides/schedule-posts-api (edit
`post.example.json` first — the `spc_…` ids and the media URL are placeholders):

```sh
curl --fail-with-body https://www.mellow.world/api/hub/v1/validate \
  -H "Authorization: Bearer $MELLOW_HUB_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @post.json

curl --fail-with-body https://www.mellow.world/api/hub/v1/posts \
  -H "Authorization: Bearer $MELLOW_HUB_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: studio-process-video-slot-001" \
  --data-binary @post.json
```

A dependency-free input checker that lists channels and validates a file
without creating anything: `https://www.mellow.world/hub/examples/mellow-hub-check.mjs`
(`node mellow-hub-check.mjs --channels`, `node mellow-hub-check.mjs post.json`;
Node 22+).

## 10. Creative Studio (optional)

`studio_list` → `studio_quote(kind)` → ask → `studio_generate(request,
maxCredits, idempotencyKey)` → poll `studio_job` → `studio_project` /
`studio_save` (free edits, current `revision` required) → `studio_export`
(free JPEGs). Use exported carousel URLs as `media` in `validate_post` /
`create_post`; attach a cover as `thumbnailUrl` on the video item, keeping the
video. Formats 4:5, 1:1, 9:16, 16:9. Export never publishes.
