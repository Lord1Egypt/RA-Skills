---
name: makepost-com-app-growth
version: 2.3.0
title: Social Media Toolkit (via makepost.com)
description: Manage your social media across 9 platforms — draft captions, hashtags & post ideas, generate AI images, schedule, publish, set recurring autopilot schedules, and trigger webhooks — all through conversation.
license: MIT
author: William Engbjerg
homepage: https://makepost.com/openclaw
keywords: social-media, scheduling, publishing, content, drafts, automation, ai-captions, image-generation, hashtags, webhooks, recurring-scheduling, autopilot, n8n, zapier
metadata:
  openclaw:
    requires:
      env:
        - MAKEPOST_API_KEY
      bins:
        - npx
    primaryEnv: MAKEPOST_API_KEY
---

# Social Media Toolkit (via makepost.com)

MakePost is a social media scheduling platform built to be driven by AI agents. Draft captions, hashtags, and post ideas, generate AI images, schedule, and publish videos, image carousels, and posts to 9 platforms — TikTok, Instagram, YouTube, Facebook, X, LinkedIn, Threads, Pinterest, and Bluesky — from one place or straight from your AI agent. Set recurring autopilot schedules that auto-publish a queue, and fire signed webhooks into n8n, Zapier, Make, or your own service.

## Setup

1. Create a MakePost account at [makepost.com](https://makepost.com)
2. Connect your social accounts (TikTok, Instagram, YouTube, etc.)
3. Generate an API key from Settings
4. Store your API key:
   ```
   MAKEPOST_API_KEY=sk_live_your_key_here
   ```

## Auth

All requests use Bearer token:
```
Authorization: Bearer <MAKEPOST_API_KEY>
```

MCP endpoint: `https://makepost.com/api/mcp/`

API docs: `https://api.makepost.com`

## Available Tools

### Publishing

**list_videos** — List uploaded videos ready for posting.
- `limit` (int, default 50) — Max videos to return.
- Returns: video ID, title, duration (seconds), source ("upload" or "creatify"), linked app name.
- Only completed videos included (processing/errored excluded). Sorted newest first.

**upload_video** — Upload a video from a public URL into MakePost.
- `video_url` (string, required) — Public URL to .mp4, .mov, .webm, or .m4v. Max 500MB, max 10 minutes.
- `title` (string, required) — Video title.
- `caption` (string) — Default caption for publishing. Falls back to title if empty.
- `app_id` (string) — Project to link to. Accepts project ID or name. Auto-selects if you have one project.
- `cover_timestamp` (float) — Seconds into the video to extract as cover frame (e.g. 5.5).
- `cover_image_url` (string) — Public URL to a custom cover image (JPEG/PNG/WebP/GIF, max 10MB). Alternative to cover_timestamp. Accepts any public URL directly — no need to upload the cover image separately first.
- Returns: video_id, url, title, duration, file_size, is_short_eligible, cover_url.
- Runs content moderation automatically. Rejected content is deleted.
- For direct file uploads (not URL), use the REST API endpoint `POST /v1/media/upload-file` with multipart form data.

**list_accounts** — List connected social media accounts.
- Returns: account ID, platform, username, provider, avatar_url.
- Only active (connected) accounts returned. Disconnected accounts excluded.
- Platforms: tiktok, instagram, youtube, facebook, x, linkedin, threads, pinterest, bluesky.

**list_account_groups** — List account groups with their member accounts.
- Returns: group ID, name, account_ids, accounts (with platform and name).
- Groups are collections of accounts that can be published to together.
- Use group IDs with the group_ids parameter in publish_content.

**schedule_post** — Schedule a video to one or more social media accounts at a specific time.
- `video_id` (string, required) — Video ID from list_videos.
- `account_ids` (list of strings, required) — Account IDs from list_accounts.
- `scheduled_at` (string, required) — ISO 8601 datetime (e.g. "2026-03-22T15:00:00").
- `timezone` (string) — IANA timezone (e.g. "America/New_York"). Defaults to your account timezone.
- `caption` (string) — Post caption. Falls back to video script, then title.
- Inactive accounts in the list are silently skipped. Response times are always UTC.

**list_posts** — List your posts, optionally filtered by status.
- `status` (string) — Filter: "scheduled", "published", "failed", "pending", or "processing".
- `limit` (int, default 50) — Max posts to return (1-100).
- Status lifecycle: scheduled → pending → processing → published or failed.
- All timestamps in UTC. Sorted by scheduled_at (newest first).

**cancel_scheduled_post** — Cancel a scheduled post before it publishes.
- `post_id` (string, required) — Post ID to cancel.
- Only works on posts with status "scheduled". The post is permanently deleted.

**reschedule_scheduled_post** — Change when a scheduled post will be published.
- `post_id` (string, required) — Post ID to reschedule.
- `scheduled_at` (string, required) — New publish time in ISO 8601.
- `timezone` (string) — IANA timezone. Defaults to your account timezone.
- Only works on "scheduled" posts. New time must be at least 5 minutes in the future.

**edit_scheduled_post_caption** — Edit the caption of a scheduled post.
- `post_id` (string, required) — Post ID to edit.
- `caption` (string, required) — The new caption text.
- Only works on posts with status "scheduled".

**get_publishing_results** — Check publishing results for a post.
- `post_id` (string, required) — Post ID to check.
- Returns: status, platform_url (null while pending), stats (views, likes, comments, shares — null until synced), error_message (only for failed posts).

### Content Publishing

**publish_content** — Create and publish content (text, image, video, or carousel) to one or more accounts.
- `content_type` (string, required) — "text", "image", "video", or "carousel".
- `caption` (string, required) — Main post caption. Used for all platforms unless overridden by captions.
- `account_ids` (list of strings) — Account IDs to post to. Required unless is_draft=True.
- `media_id` (string) — Pre-uploaded media ID (from upload_image or upload_video). Required for image/video/carousel.
- `scheduled_at` (string) — ISO 8601 datetime. Omit to publish immediately.
- `timezone` (string) — IANA timezone for scheduled_at.
- `is_draft` (bool, default false) — Save as draft without publishing. Account IDs and captions are stored for later use.
- `title` (string) — Optional title (used by YouTube).
- `app_id` (string) — Project ID to associate content with (from list_apps).
- `captions` (dict) — Per-platform caption overrides, e.g. {"linkedin": "Professional version", "x": "Short version"}.
- `group_ids` (list of strings) — Account group IDs to resolve to individual accounts (from list_account_groups).
- `tiktok_is_draft` (bool, default false) — Send to TikTok as a draft instead of publishing live. The video appears in the user's TikTok drafts for editing before posting.
- Text-only posts work on X, LinkedIn, Threads, Bluesky, Facebook. TikTok, Instagram, YouTube, Pinterest require media.

**upload_image** — Upload an image from a public URL into MakePost.
- `image_url` (string, required) — Public URL to .jpg, .png, .webp, or .gif. Max 20MB.
- `title` (string) — Image title.
- `app_id` (string) — Project to link to. Auto-selects if you have one project.
- Returns: media_id, url, title. Use media_id with publish_content.
- For direct file uploads (not URL), use the REST API endpoint `POST /v1/media/upload-file` with multipart form data.

**list_drafts** — List your draft posts.
- `limit` (int, default 50) — Max drafts to return (1-100).
- Sorted newest first.
- Returns draft_account_ids (stored target accounts) and draft_captions (stored per-platform captions) if set.

**publish_draft_tool** — Publish a draft post (immediately or scheduled).
- `post_id` (string, required) — Draft post ID from list_drafts.
- `account_ids` (list of strings) — Account IDs. If omitted, uses accounts stored when the draft was created.
- `scheduled_at` (string) — ISO 8601 datetime. Omit for immediate.
- `timezone` (string) — IANA timezone.

**update_draft_tool** — Update a draft post's content, accounts, or captions.
- `post_id` (string, required) — Draft post ID.
- `caption` (string) — New main caption text.
- `content_type` (string) — New content type.
- `media_id` (string) — New media ID.
- `account_ids` (list of strings) — Updated list of account IDs for this draft.
- `captions` (dict) — Updated per-platform caption overrides, e.g. {"x": "Short", "linkedin": "Long"}.

**delete_draft_tool** — Delete a draft post permanently.
- `post_id` (string, required) — Draft post ID to delete.

### Bulk Operations

**bulk_publish_content** — Publish, schedule, or draft up to 20 content items in a single request.
- `items` (list, required) — Array of content items (max 20). Each item has the same fields as publish_content: content_type, caption, account_ids, media_id, scheduled_at, timezone, is_draft, title, app_id, captions, group_ids, tiktok_is_draft.
- Each item is processed independently — failures on individual items do not stop the batch.
- Returns a list of per-item results with success/failure status and error details for failed items.
- Rate limit: 5 requests per minute.

**bulk_upload_media** — Upload up to 20 images or videos from public URLs in a single request.
- `items` (list, required) — Array of media items (max 20). Each item has: `url` (string, required), `type` ("image" or "video", default "image"), `title` (string), `app_id` (string).
- Image URLs: .jpg, .png, .webp, or .gif. Max 20MB per image.
- Video URLs: .mp4, .mov, .webm, or .m4v. Max 500MB, max 10 minutes per video.
- Each item is processed independently — failures on individual items do not stop the batch.
- Returns a list of per-item results with media_id on success or error details on failure.
- Rate limit: 3 requests per minute.

**bulk_cancel_posts** — Cancel up to 50 scheduled posts in a single request.
- `post_ids` (list of strings, required) — Post IDs to cancel (max 50).
- Only works on posts with status "scheduled". Non-scheduled posts are skipped with an error.
- Each post is processed independently — failures on individual posts do not stop the batch.
- Returns a list of per-item results with success/failure status and error details.
- Rate limit: 10 requests per minute.

**bulk_reschedule_posts** — Reschedule up to 50 scheduled posts in a single request.
- `items` (list, required) — Array of reschedule items (max 50). Each item has: `post_id` (string, required), `scheduled_at` (string, required — ISO 8601 datetime), `timezone` (string).
- Only works on "scheduled" posts. New time must be at least 5 minutes in the future.
- Each post is processed independently — failures on individual posts do not stop the batch.
- Returns a list of per-item results with success/failure status and error details.
- Rate limit: 10 requests per minute.

### Projects

**list_apps** — List your projects.
- Returns: project ID, name, type, rating, rating_count.
- Projects are optional containers to organize content by client, brand, or campaign.
- Pass a project ID as the optional `app_id` when uploading or publishing to associate content with that project.
- Sorted newest first.

### AI Generation

**generate_caption** — Draft a post caption from a short brief.
- `brief` (string, required) — What the post is about (topic, angle, key points).
- `platform` (string) — Target platform (e.g. "tiktok", "linkedin"). Tailors length and style to the platform's norms.
- `tone` (string) — Desired tone (e.g. "casual", "professional", "playful").
- Returns: a ready-to-use caption. Counts toward your monthly AI usage.

**generate_hashtags** — Generate relevant hashtags for a topic.
- `topic` (string, required) — The subject to find hashtags for.
- `count` (int) — How many hashtags to return.
- `platform` (string) — Target platform for platform-appropriate tags.
- Returns: a list of hashtags. Counts toward your monthly AI usage.

**generate_post_ideas** — Brainstorm distinct post ideas for a theme.
- `topic` (string, required) — The theme or product to generate ideas for.
- `count` (int) — How many ideas to return.
- Returns: a list of distinct ideas, each with a hook, an angle, and a suggested caption. Counts toward your monthly AI usage.

**generate_title** — Write a short, viral hook or title.
- `topic` (string, required) — What the content is about.
- `platform` (string) — Target platform (e.g. "youtube" for a video title).
- Returns: a short hook/title. Counts toward your monthly AI usage.

**generate_image** — Generate an AI image (Google Imagen) ready to post.
- `prompt` (string, required) — Description of the image to create.
- `aspect_ratio` (string) — Image shape: "1:1" (default), "3:4", "4:3", "9:16", or "16:9".
- `app_id` (string) — Project to link the resulting media to.
- Returns: a `media_id` plus the image URL — use the media_id directly with publish_content or schedule_post. Counts toward your monthly AI usage.

**get_usage** — Check your AI usage and plan limits.
- Returns: this month's AI generation usage (captions, hashtags, ideas, titles, images) and your plan's limits.

### Platform Info

**get_platform_rules** — Get per-platform posting rules so you post correctly.
- `platform` (string) — Optional. A single platform to look up; omit to return rules for all 9.
- Returns: caption character limits, supported media types (video/image/carousel/text), and carousel min/max sizes for each platform.
- Use this before drafting captions or building carousels so content fits each platform's constraints.

### Webhooks

**list_webhooks_tool** — List your registered webhook endpoints.
- Returns: each endpoint's ID, URL, subscribed events, and the full list of available events.

**create_webhook_tool** — Register a webhook endpoint to receive signed events.
- `url` (string, required) — HTTPS endpoint MakePost will POST to.
- `events` (list of strings) — Events to subscribe to (e.g. "post.published", "post.failed"). Omit to receive all events.
- Returns: the endpoint ID and a signing `secret` — shown only once. Each delivery includes an `X-MakePost-Signature` header (HMAC-SHA256 of the body using your secret); verify it to confirm authenticity.
- Wire MakePost into n8n, Zapier, Make, or your own service.

**delete_webhook_tool** — Remove a webhook endpoint.
- `webhook_id` (string, required) — Endpoint ID to delete.

### Recurring Scheduling

Set-and-forget autopilot: create a posting plan with recurring weekday + time slots, add media to its queue, and each slot automatically publishes the next queued item.

**create_posting_plan_tool** — Create a recurring posting plan.
- `name` (string, required) — Plan name.
- `account_ids` (list of strings, required) — Accounts the plan publishes to.
- `slots` (list, required) — Recurring slots, each with a weekday and a time (e.g. Monday 09:00, Thursday 17:30).
- `timezone` (string) — IANA timezone the slots are interpreted in (e.g. "America/New_York").
- Returns: the plan ID. Each slot auto-publishes the next item from the plan's queue.

**list_posting_plans_tool** — List your recurring posting plans.
- Returns: each plan's ID, name, accounts, slots, timezone, and active/paused state.

**add_to_posting_queue** — Add uploaded media to a plan's queue.
- `plan_id` (string, required) — The posting plan.
- `media_id` (string, required) — Pre-uploaded media (from upload_image, upload_video, generate_image, or bulk_upload_media).
- `caption` (string) — Caption to use when this item publishes.
- Items publish in queue order, one per upcoming slot.

**list_posting_queue** — View the queued items for a plan.
- `plan_id` (string, required) — The posting plan.
- Returns: queued items in publish order.

**pause_posting_plan** — Pause a plan so its slots stop auto-publishing.
- `plan_id` (string, required) — The plan to pause.

**resume_posting_plan** — Resume a paused plan.
- `plan_id` (string, required) — The plan to resume.

**delete_posting_plan_tool** — Delete a posting plan.
- `plan_id` (string, required) — The plan to delete.

## Example Workflows

- "Post 'Just launched v2.0!' to all my accounts" — Creates a text post and publishes to all text-compatible platforms.
- "Upload this image and post it to Instagram and Facebook with the caption 'New feature'" — Uploads the image, then publishes to selected accounts.
- "Save a draft post about our upcoming feature for later" — Creates a draft that can be edited and published when ready. Accounts and per-platform captions are preserved.
- "Draft a post for X and LinkedIn with different captions for each" — Creates a draft with per-platform captions stored for later publishing.
- "Post to all accounts in my MakePost group" — Uses list_account_groups to find the group, then publishes with group_ids.
- "Upload https://example.com/my-video.mp4 and schedule it to all my accounts tomorrow at noon" — Downloads the video, runs moderation, and schedules across all connected platforms.
- "Post my latest video to TikTok and Instagram tomorrow at 3pm" — Finds your most recent video, picks the right accounts, and schedules it.
- "How did my last post do?" — Uses get_publishing_results to report status and engagement stats (views, likes, comments, shares).
- "Show me my drafts and publish the one about the launch to LinkedIn" — Lists drafts, then publishes the right one to the selected account.
- "List my projects and schedule this video under the Acme client" — Lists projects, then publishes with the project ID passed as app_id.

### Bulk Operations

- "Schedule a week of posts — Monday text, Tuesday image, Wednesday video, Thursday text, Friday carousel, Saturday image, Sunday video" — Uses bulk_publish_content with 7 items, each with a different scheduled_at and content_type, all in one call.
- "Upload these 10 product screenshots and then post them all to Instagram and LinkedIn" — First calls bulk_upload_media with 10 image URLs, then uses the returned media_ids in bulk_publish_content to publish all 10.
- "Cancel all my scheduled posts for next week" — Lists posts filtered by status "scheduled", identifies the ones in the target date range, then calls bulk_cancel_posts with their IDs.
- "Move all my Friday posts to Saturday at the same times" — Lists scheduled posts, filters for Friday, then calls bulk_reschedule_posts with each post shifted by one day.

### AI Generation

- "Write me a punchy TikTok caption for our new feature launch" — Uses generate_caption with the brief and platform "tiktok", then you can publish it directly.
- "Give me 10 hashtags for a fitness reel" — Uses generate_hashtags with the topic and count.
- "Brainstorm 5 post ideas about productivity, each with a hook and caption" — Uses generate_post_ideas and returns distinct angles ready to schedule.
- "Make an image of a sunset over mountains and post it to Instagram" — Uses generate_image to create the image (returns a media_id), then publish_content with that media_id.
- "How much of my AI quota have I used this month?" — Uses get_usage to report generation counts against your plan limits.

### Platform Rules

- "What's the caption limit on X vs LinkedIn?" — Uses get_platform_rules to report per-platform caption limits.
- "Build a carousel — how many images can I post on Instagram?" — Uses get_platform_rules to check carousel min/max sizes before assembling the carousel.

### Webhooks

- "Notify my n8n workflow whenever a post publishes" — Uses create_webhook_tool with the n8n URL and the "post.published" event, then returns the signing secret to configure signature verification.
- "Show me my webhook endpoints" — Uses list_webhooks_tool to list registered endpoints and the available events.

### Recurring Scheduling (Autopilot)

- "Set up a plan that posts to TikTok every Mon/Wed/Fri at 9am, then queue these 6 videos" — Uses create_posting_plan_tool with three slots, then add_to_posting_queue for each video. Each slot auto-publishes the next queued item.
- "Pause my autopilot plan while I'm on vacation" — Uses pause_posting_plan, then resume_posting_plan when you're back.
- "What's left in my posting queue?" — Uses list_posting_queue to show upcoming items in publish order.

## Tips

- **Project auto-selection**: If you have only one project, you can omit app_id from any tool — it auto-selects.
- **Flexible project lookup**: Pass a project name (case-insensitive) instead of the internal ID.
- **Timezone handling**: schedule_post and reschedule default to your account timezone if you don't specify one.
- **Caption fallbacks**: If no caption is provided, publishing uses the video's script, then its title.
- **Per-platform captions**: Use the captions dict in publish_content to write a different caption per platform.
- **Drafts**: Save content with is_draft=True, then publish or schedule it later with publish_draft_tool.
- Post to multiple platforms simultaneously by including multiple account IDs in schedule_post.

## REST API

The MCP tools above also have equivalent REST API endpoints at `https://api.makepost.com/v1/`. Full interactive docs at `https://api.makepost.com`.

**New endpoint groups:**
- AI generation: `POST /v1/ai/caption`, `POST /v1/ai/hashtags`, `POST /v1/ai/ideas`, `POST /v1/ai/title`, `POST /v1/ai/image`, and `GET /v1/ai/usage`.
- Platform rules: `GET /v1/platforms` — per-platform caption limits, supported media, and carousel sizes.
- Webhooks: `GET /v1/webhooks`, `POST /v1/webhooks`, `DELETE /v1/webhooks/{id}`, and `POST /v1/webhooks/{id}/test`. Deliveries are signed with an `X-MakePost-Signature` (HMAC-SHA256) header.
- Recurring schedules: `GET /v1/schedules`, `POST /v1/schedules`, `DELETE /v1/schedules/{id}`, `POST /v1/schedules/{id}/pause`, `POST /v1/schedules/{id}/resume`, and `POST /v1/schedules/{id}/queue`.

**Direct file upload** (REST API only — not available via MCP):
```
POST https://api.makepost.com/v1/media/upload-file
Content-Type: multipart/form-data
Authorization: Bearer <MAKEPOST_API_KEY>

file: <binary>       (required) Image or video file
type: "image"|"video"|"cover" (default "image")
title: string         (optional)
app_id: string        (optional)
```
- Images: max 20MB, JPEG/PNG/WebP/GIF
- Videos: max 500MB, MP4/MOV/WebM, max 10 minutes
- Returns same response as upload_image or upload_video

**REST API: Cover Image Upload** — Upload a cover image without creating a media record.
- `POST /v1/media/upload-file` with `type: "cover"` — returns `{"url": "...", "type": "cover"}` with no media_id.
- `POST /v1/media/upload` with `type: "cover"` — same, from a public URL.
- Use the returned URL as `cover_image_url` when uploading a video.

## Supported Platforms

TikTok, Instagram, YouTube, Facebook, X, LinkedIn, Threads, Pinterest, Bluesky
