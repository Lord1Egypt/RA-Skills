---
name: postking-social
description: Generate, approve, and schedule social posts on PostKing across LinkedIn, X, Instagram, Threads, and Facebook — plus content weeks and repurposing.
license: MIT-0
compatibility: "Works with any MCP-compatible client connected to postking-mcp (local stdio or hosted at https://mcp.postking.app/mcp); the pking CLI is an optional fast path when a shell is available."
metadata:
  icon: https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-social.svg
  category: marketing
---

# PostKing Social

Handles the social-post lifecycle on PostKing: generating AI drafts or saving manual content, approving/scheduling them, running the recurring Smart Week cadence or a one-off bulk fill, repurposing existing content into new posts, connecting/disconnecting social accounts, attaching visuals, managing the brand's asset library, and configuring per-platform social media rules. Requires an active brand — use the `postking` skill's brand-pick flow first if one isn't set.

## When to Use

Use this skill when the user wants to draft, approve, schedule, or reschedule a social post; paste/save finished copy without AI generation; bulk-fill a date range with posts; set up or run a weekly/recurring posting cadence; turn a URL, blog article, or piece of text into platform posts; connect or disconnect a social account; attach or change a post's image/card/quote/carousel; upload, tag, or search the brand's asset library; edit a platform's content/tone rules; or browse trending posts for hook inspiration, extract them into reusable templates, or reuse a saved template.

## When NOT to Use

- Blog articles (writing, publishing, WordPress/Medium/Substack) → `postking-blog`.
- Landing pages or side pages → `postking-landing-pages`.
- Multi-channel campaign briefs and strategy (Storylines) → `postking-storylines`.
- Subreddit-specific matching or native Reddit rewrites → `postking-reddit`.
- Managing saved voice profiles themselves, or a standalone de-slop/AI-detection pass → `postking-brand-voice`.
- No active brand yet, or first-time social account connection → `postking-getting-started`.

## Minimal tool subset

- `list_brands`, `set_active_brand` — brand context.
- `check_social_accounts`, `generate_connect_link`, `disconnect_social_account` — confirm/connect/disconnect platforms before posting.
- `generate_post`, `create_post`, `approve_post`, `schedule_post`, `reschedule_post`, `cancel_post`, `delete_post`, `get_post`, `list_posts`, `get_calendar` — the core post lifecycle.
- `generate_bulk_posts` — one-off AI fill across a date range (not the recurring cadence below).
- `get_weekly_schedule`, `set_weekly_schedule`, `enable_weekly_schedule`, `disable_weekly_schedule`, `delete_weekly_schedule`, `run_weekly_schedule_day` — recurring cadence (Smart Week).
- `repurpose_content` — turn a URL/text/blog/post into new social drafts.
- `generate_post_visual_options`, `pick_post_visual`, `regenerate_post_visual`, `clear_post_visual`, `generate_post_carousel` — visuals.
- `search_stock_images`, `search_web_images`, `suggest_assets_for_post` — visual discovery, feeding into the picks above.
- `list_assets`, `view_asset`, `tag_asset`, `list_asset_tags`, `delete_asset`, `import_asset_from_url`, `import_assets_csv`, `upload_asset` (+ chunked `upload_asset_begin`/`upload_asset_chunk`/`upload_asset_finish`/`upload_asset_abort`) — brand asset library housekeeping.
- `get_social_media_rules`, `set_social_media_rules` — per-platform content/tone rules.
- `trends_list` — trending-post hooks.
- `template_list`, `template_create`, `template_update`, `template_delete`, `template_extract`, `template_pick` — reusable post templates (extract from a trend, or hand-author, then reuse).

## Procedure

### Connect, verify, and disconnect social accounts

1. `check_social_accounts({ brandId? })` — list connected/disconnected platforms before posting; run this first in any new session.
2. `generate_connect_link({ brandId?, platform? })` — get a browser URL for OAuth; share it with the user to complete the connection. Omit `platform` for a generic connect link covering all supported platforms.
3. `disconnect_social_account({ accountId, brandId? })` — remove a connected account by its account ID (from `check_social_accounts`). This does not delete past posts.

### Generate, approve, and schedule a post

1. `generate_post({ platform, variations?, theme, voice?, brandId?, language? })` — ALWAYS pass `theme` with the specific topic/angle/tone the user wants; omitting it produces a random brand theme. This call polls until generation completes and already saves the result to a single `postId` (variation 1 is the primary, saved content — all variations live under that one `postId`, never call it again to "get the others"). `language` (`en`/`es`/`pt-BR`/`de`/`fr`/`cs`) overrides the brand's `contentLanguage` for this one call — omit it to use the brand default.
2. Show the variation(s) to the user; ask which one (if more than one) and what time.
3. `approve_post({ postId, scheduledAt, timezone? })` — `scheduledAt` is a future ISO 8601 datetime. This is the free-tier choke point. There is **no `variation` param on this MCP tool** — via MCP you always approve the post's current saved content (variation 1). Picking a different generated variation to schedule is a CLI-only affordance (`pking posts approve <id> --variation N`).
4. `get_calendar({ days })` — confirm it appears in the upcoming schedule.

### Save manual content instead of generating

Use `create_post` — not `generate_post` — whenever the user hands you finished copy (pasted text, content drafted elsewhere) and wants it saved as-is, with no AI drafting and no credit cost.

1. `check_social_accounts({ brandId? })` — confirm the target platform(s) are connected.
2. `create_post({ platforms, content, scheduledAt?, brandId? })` — `platforms` is an array (`x`/`linkedin`/`instagram`/`threads`/`facebook`), so one call can save the same `content` to multiple platforms at once, unlike `generate_post`'s single-`platform` param. Pass `scheduledAt` (future ISO 8601 UTC) to schedule immediately on save; omit it to save as an unscheduled draft (`postType: "queue"`) and approve later. Returns one post per platform, each with its own `id` and `editInVisualEditor` link.
3. If saved as a draft, `approve_post({ postId, scheduledAt, timezone? })` per post when ready to schedule.
4. `get_calendar({})` — confirm.

### Bulk-generate posts across a date range

Use `generate_bulk_posts` for a one-off fill of many posts over a date range — this is distinct from the recurring Smart Week cadence below (no `dayConfigs`, doesn't repeat).

1. `check_social_accounts({ brandId? })` — confirm the platform is connected.
2. `generate_bulk_posts({ platform, days, frequency?, postsPerDay?, times?, voice?, language?, brandId? })` — `days` (1–90) is how many days to fill; `frequency` is `daily` | `every_other` | `every_third` | `weekdays` (default `daily`); `postsPerDay` (1–5, default 1); `times` is a comma-separated string of posting times, e.g. `"09:00,14:00"` (default `"09:00"`). Runs in the background and returns `{ operationId, totalQueued, pollUrl }`.
3. `get_job({ pollUrl, wait: true })` — poll until `state` is `completed`/`partially_failed`/`failed`; do not call `generate_bulk_posts` again while it's pending.
4. `list_posts({ status: "created" })` or `get_calendar({ days })` to review the generated drafts, then `approve_post` each one that's ready.

### Plan a content week (Smart Week)

1. `get_weekly_schedule({ brandId? })` — view the current cadence, if any.
2. `set_weekly_schedule({ enabled?, leadTimeDays?, timezone?, voiceProfileId?, dayConfigs, brandId? })` where `dayConfigs` is an array of `{ dayOfWeek (0=Sun…6=Sat), mediums: [{ medium, postsPerDay }] }`. There are **no `monday`/`tuesday`/… params** and the flag is `enabled`, not `enable` — those are CLI-only sugar.
3. `enable_weekly_schedule({ brandId? })` / `disable_weekly_schedule({ brandId? })` — toggle an already-created schedule on/off without resending `dayConfigs`. `disable_weekly_schedule` pauses (config is kept); use `delete_weekly_schedule({ confirm: true, brandId? })` instead to remove the schedule entirely.
4. `run_weekly_schedule_day({ date, brandId? })` — `date` is `YYYY-MM-DD`. This is the Smart Week engine; call it per day, or leave the schedule `enabled` to run automatically.
5. `list_posts({ status: "created" })` → `get_post({ postId })` to review each draft.
6. `approve_post({ postId, scheduledAt, timezone? })` per draft.
7. `get_calendar({ days: 7 })` — verify the final week.

### Repurpose a URL, blog, or text into multi-platform posts

1. `check_social_accounts({ brandId? })` — confirm which platforms are connected.
2. `repurpose_content({ brandId, sourceType: "url", sourceUrl, targetType: "social", targetPlatforms: ["linkedin", "x"] })` — PostKing crawls the URL internally; do not fetch it yourself.
   - Text input: `sourceType: "text", sourceContent: "<text>"`.
   - From an existing blog: `sourceType: "blog", sourceBlogId: <articleId>`.
   - From an existing post: `sourceType: "social_post", sourcePostId: <postId>`.
   - Optional: `angle`, `variations`, `voiceProfileIds` (single ID applies to all platforms, or `["x:id1","linkedin:id2"]` per platform).
3. `get_post({ postId })` per generated post — inspect before scheduling.
4. `approve_post({ postId, scheduledAt })` — free-tier choke point.
5. `get_calendar({})` — confirm.

### Pick a visual for a post

1. `generate_post_visual_options({ postId, platform })` — always run this first. Relay the numbered options to the user, especially the recommended one — the returned params ARE the spec, no need to render anything yourself.
2. If none of the prepared options fit, widen the search before picking:
   - `suggest_assets_for_post({ context, limit?, brandId? })` — AI-matched picks from the brand's own asset library for the post's content/topic (`context`). Try this first — it surfaces on-brand assets already in the library.
   - `search_stock_images({ query, platform?, detail?, brandId? })` — licensed stock photo/video libraries; pass `platform` (e.g. `"linkedin"`) to bias dimensions.
   - `search_web_images({ query, maxResults?, gl?, hl?, openLicensedOnly?, brandId?, detail? })` — broader Google Images search across the whole web (not just stock libraries). `openLicensedOnly` is a best-effort filter, not a legal guarantee — still verify usage rights before publishing.
   - A `search_stock_images`/`search_web_images` result isn't directly usable by `pick_post_visual` — first `import_asset_from_url({ url, name?, tags?, assetType?, brandId? })` to add it to the library (pass `assetType: "google-image"` for web-search results, to record provenance), then reference the returned `assetId` in `pick_post_visual`.
3. `pick_post_visual({ postId, platform, style?, variant?, assetId?, slot?, kind? })` — pass the chosen option's fields verbatim from step 1's response, or the imported asset's `assetId`. There is **no numeric `pick` param on the MCP tool** (that's CLI-only sugar); you must supply one of `style`, `assetId`, or `slot`, or the tool errors. Pass `kind: "quote"` (or `"card"`/`"photo"`/etc.) when the chosen option is a quote/card template style — omitting `kind` defaults to `"card"` and rejects quote styles.
4. "Show me more" → `regenerate_post_visual({ postId, platform, loadExternal: true })` pulls additional stock results, then re-run `generate_post_visual_options`.
5. `clear_post_visual({ postId, platform })` to remove a pick. For carousels: set cards first (`set_post_cards`/`edit_post_card`), then `generate_post_carousel({ postId })`.

### Manage the asset library

1. `list_assets({ type?, tags?, search?, limit?, detail?, brandId? })` — browse the library; `type` is `IMAGE`/`DOCUMENT`/`VIDEO`/`LINK`/`LOTTIE`. `view_asset({ assetId, detail?, brandId? })` for one asset's full detail.
2. Add assets:
   - `import_asset_from_url({ url, name?, tags?, assetType?, brandId? })` — one public URL (e.g. a `search_web_images`/`search_stock_images` result).
   - `import_assets_csv({ urls, detail?, brandId? })` — batch-import up to 50 public URLs in one call.
   - `upload_asset({ filePath?, fileBase64?, fileName?, mimeType?, name?, description?, tags?, brandId? })` — upload a local file or inline base64; provide exactly one of `filePath`/`fileBase64`. **Prefer `filePath`** for local files — the server reads and base64-encodes it server-side, which avoids the truncation risk below.
   - Chunked upload (`upload_asset_begin` → `upload_asset_chunk` ×N → `upload_asset_finish`, or `upload_asset_abort` to cancel) — use this instead of `upload_asset`'s `fileBase64` **only** for large files sent over the remote/HTTP transport with no local file path available (e.g. a generated or fetched file the agent holds only as base64): a single large base64 string can get truncated crossing the LLM→tool_call boundary on that transport. `upload_asset_begin` returns `uploadId` + a recommended chunk size (~16000 chars); send chunks in order starting at index 0 with no gaps; `upload_asset_finish` verifies size/sha256 (if provided at `_begin`) before saving. Uploads expire after 10 minutes of inactivity.
3. `tag_asset({ assetId, addTags?, removeTags?, brandId? })` — add/remove tags (at least one required). `list_asset_tags({ brandId? })` — see every tag in use across the library.
4. `delete_asset({ assetId, confirm: true, brandId? })` — soft-delete; `confirm: true` is required.

### Manage per-platform social media rules

These are the same content/structure/engagement/visual-strategy rules editable in dashboard Settings → Social media rules — they steer `generate_post`'s tone and structure, not a specific post.

1. `get_social_media_rules({ platform?, brandId? })` — `platform` is `linkedin`/`x/twitter`/`facebook`/`instagram`/`threads`/`general`; omit to return all 6. Always call this before `set_social_media_rules` so you only change fields the user actually asked to change.
2. `set_social_media_rules({ platform, rules, replace?, brandId? })` — `platform` (singular, required) is the one platform being updated. `rules` accepts nested groups (`content`, `structure`, `engagement`, `visualStrategy`, each with free-text sub-fields like `postLength`, `hook`, `hashtags`) plus flat arrays (`secrets`, `guidelines`, `contentTypes`, `avoid`, `principles`). By default this **merges** provided fields into the existing ruleset — arrays you provide replace the old array, everything else is preserved. Pass `replace: true` to overwrite the entire platform ruleset instead.

### Trends as hooks, and turning one into a reusable template

`trends_list` is account/niche-scoped (no `brandId`, works before any brand is picked); every `template_*` tool below is brand-scoped.

1. `trends_list({ niche?, platform?, days?, limit?, sort? })` — niches: `ai-saas`, `marketing`, `web3` (default `ai-saas`); platform currently only `x`. The crawler runs every 3 days; default window is 3 days. Each result includes a hook/template/pattern/virality-reason deconstruction. Feed a result's text into `generate_post`'s `theme` or `repurpose_content`'s `angle` for quick hook inspiration, or turn it into a saved, reusable template with the steps below.
2. To turn a trending (or any pasted) post into a template: `template_extract({ postText, save?, brandId? })` — AI deconstructs the post text into a reusable template (title/body-with-placeholders/example/category/pattern). Synchronous, no polling. Pass `save: true` to persist it directly in the same call (skip step 3); omit `save` to just preview the extraction and decide first.
3. To persist an extraction that wasn't auto-saved, or to hand-author templates directly: `template_create({ title, body, example?, category?, pattern?, platforms?, isFavorite?, brandId? })` for one template, or pass the bulk `templates: [...]` array instead (bulk takes precedence if both are given).
4. To reuse an existing saved template instead of extracting a new one: `template_list({ category?, detail?, brandId? })` (ordered favorite-first, then most-used) to fetch candidates — use `detail: "full"` since `template_pick` needs each candidate's `id`/`title`/`body`/`category` — then `template_pick({ count, theme, templates, brandId? })` to have AI re-rank and return the best-fitting `templateIds`. **`template_pick` does not read the library itself** — it only scores the `templates` array you pass in, so `template_list` must run first.
5. `template_update({ templateId, title?, body?, example?, category?, pattern?, platforms?, isFavorite?, brandId? })` / `template_delete({ templateId, brandId? })` (irreversible) — template housekeeping.
6. To turn a chosen template into an actual post: fill its `body` placeholders (e.g. `[HOOK] … [CTA]`) for the topic at hand, then `create_post` (finished copy, no AI) or `generate_post` (let AI draft from `theme`) as in the sections above.

## CLI fast path

| Goal | Command |
|---|---|
| Pick active brand | `pking brand list` / `pking brand set <brandId>` |
| Generate a post | `pking posts generate --platform linkedin --variations 3 --theme "..."` |
| Approve & schedule (pick a variation) | `pking posts approve <postId> --schedule 2026-08-01T14:00:00Z --variation 2 --timezone America/New_York` |
| View calendar | `pking posts calendar --days 7` |
| Plan a content week | `pking weekly-schedule set --monday "linkedin:1,x:1" --timezone America/New_York --enable` then `pking weekly-schedule run-day --date <YYYY-MM-DD>` |
| Repurpose a URL | `pking repurpose --source-type url --source-url <url> --target-type social --target-platforms linkedin,x` |
| Visual options / pick | `pking visuals options <postId> --platform <p>` → `pking visuals pick <postId> --platform <p> --pick <N>` |
| Trends | `pking trends list --niche ai-saas --days 3 --json` |

For the full command catalog, use the `postking` skill's `references/commands.md`, or run `pking --help` / `pking <group> --help`.

## Pitfalls

- **`approve_post` has no `variation` param via MCP.** If the user wants a specific generated variation scheduled (not variation 1), that's a CLI-only affordance (`--variation N`); via MCP the only way is to work from the CLI, or use the visual editor link (`editInVisualEditor`, returned by `generate_post`/`get_post`) to edit the saved content directly.
- **`set_weekly_schedule` needs `dayConfigs`, not per-day flags.** Passing `monday`/`tuesday`/etc. or `enable` (instead of `enabled`) will fail validation.
- **`pick_post_visual` needs an explicit `style`/`assetId`/`slot`.** There is no index-based `pick` param — always call `generate_post_visual_options` first and copy its fields.
- **Omitting `theme` on `generate_post` gives a random topic.** Always pass it when the user wants specific content.
- **Visuals are never auto-attached.** `generate_post` prepares visual options but does not attach one — nothing changes until `pick_post_visual` is called.
- **`create_post` vs `generate_post`.** `create_post` saves the user's own finished content verbatim (no AI, no credits, takes `platforms` array for multi-platform in one call); `generate_post` drafts AI content for one `platform` and costs credits. Don't call `generate_post` when the user already gave you the copy to post.
- **`cancel_post` vs `delete_post`.** `cancel_post` reverts a scheduled/approved post to draft without deleting it (reversible). `delete_post` removes the post permanently regardless of status. Use `delete_post` only when the user actually wants it gone.
- **Chunked asset upload is not the default.** Use `upload_asset` with `filePath` for local files. Reach for `upload_asset_begin`/`upload_asset_chunk`/`upload_asset_finish` only when uploading from base64 content over the remote/HTTP transport with no local file path — a large single `fileBase64` string can get silently truncated crossing that boundary.
- **`INSUFFICIENT_CREDITS` / `FREE_CAP_REACHED`** — surface the error envelope's `checkoutUrl` in one line and stop; don't retry or recap.

## Verification

- `get_credits({ detail: "short" })` — confirms auth and balance.
- `check_social_accounts({})` — confirms at least one connected platform.
- `list_posts({ status: "created", limit: 1 })` — confirms the brand/posts API is reachable.
