---
name: powerpost
description: Generate social media content and publish to all major platforms from one command.
version: 0.4.0
metadata:
  openclaw:
    requires:
      env:
        - POWERPOST_API_KEY
        - POWERPOST_WORKSPACE_ID
      bins:
        - curl
    primaryEnv: POWERPOST_API_KEY
    emoji: "⚡"
    homepage: https://powerpost.ai
---

# PowerPost Skill

PowerPost writes social media captions, generates images and videos, manages your content calendar, and publishes to Instagram, TikTok, X/Twitter, YouTube, Facebook, and LinkedIn through a single API.

## Setup

The user needs two credentials:

- `POWERPOST_API_KEY` — their API key (starts with `pp_live_sk_`). They can create one at https://powerpost.ai/settings/api
- `POWERPOST_WORKSPACE_ID` — their workspace ID. Found at https://powerpost.ai/settings/workspaces

There are two ways to configure these in OpenClaw. The API key can go in the Skills UI (the "API key" field) or via config. The workspace ID has to be set via config since the UI only has one field per skill:

```bash
openclaw config set skills.entries.powerpost.apiKey "pp_live_sk_YOUR_KEY"
openclaw config set skills.entries.powerpost.env.POWERPOST_WORKSPACE_ID "YOUR_WORKSPACE_ID"
```

Each API key is assigned a set of scopes that control what it can do. There are presets in the dashboard:

- **Full access** — every scope, including `posts:publish`.
- **Draft only** — everything except `posts:publish`. Good when a human should review before anything goes live.
- **Read only** — only the `:read` scopes. Can't generate, upload, or publish.

You can also pick scopes individually. See the [scope reference](#api-key-scopes) below — a 403 from any endpoint means the key is missing the scope that endpoint needs.

New accounts start with 50 free credits. Pricing details at https://powerpost.ai/pricing

## First run

Before running any PowerPost command, make sure both credentials are set. If either is missing, walk the user through setup:

1. If `POWERPOST_API_KEY` is not set:
   - Ask if they have a PowerPost account. If not, they can sign up at https://powerpost.ai/login
   - Point them to https://powerpost.ai/settings/api to create an API key.
   - They can paste it into the "API key" field on the Skills page in the OpenClaw UI, or run: `openclaw config set skills.entries.powerpost.apiKey "pp_live_sk_..."`

2. If `POWERPOST_WORKSPACE_ID` is not set:
   - Point them to https://powerpost.ai/settings/workspaces to find it.
   - They need to run: `openclaw config set skills.entries.powerpost.env.POWERPOST_WORKSPACE_ID "their-workspace-id"` — there's no UI field for this one, it has to be set via config.

3. Once both are set, verify by calling `GET /account/credits`. If it returns a balance, you're good. If it returns 401, the API key is wrong.

Don't run any other PowerPost commands until both credentials are confirmed working.

## Base URL

All requests go to:

```
https://powerpost.ai/api/v1
```

## Authentication Headers

Every request needs `x-api-key` (or `Authorization: Bearer <key>`). All content endpoints also need `X-Workspace-Id`. The only exception is `GET /account/credits` which only needs `x-api-key`.

```
x-api-key: $POWERPOST_API_KEY
X-Workspace-Id: $POWERPOST_WORKSPACE_ID
```

## API Key Scopes

Each endpoint requires a specific scope on the API key. If the key doesn't have the scope, the request returns 403. The "Required scope" line under each endpoint below tells you which one applies.

| Scope               | What it lets you do                                  |
|---------------------|------------------------------------------------------|
| `account:read`      | Read the credit balance.                             |
| `content:read`      | List and fetch caption generations.                  |
| `content:generate`  | Start new caption generations. Spends credits.       |
| `images:read`       | List and fetch image generations.                    |
| `images:generate`   | Start new image generations. Spends credits.         |
| `videos:read`       | List and fetch video generations.                    |
| `videos:generate`   | Start new video generations. Spends credits.         |
| `media:write`       | Upload images and videos.                            |
| `posts:read`        | Fetch posts and their items.                         |
| `posts:write`       | Create draft posts.                                  |
| `posts:publish`     | Publish, schedule, and cancel posts. Spends credits. |
| `calendar:read`     | List and fetch calendar entries.                     |
| `calendar:write`    | Create, update, and delete calendar entries.         |
| `analytics:read`    | Read per-item performance metrics.                   |

If the user gets a 403, tell them which scope is missing and that they can adjust it at https://powerpost.ai/settings/api

## Core Workflow

The standard PowerPost flow is:

1. **Check credits** to make sure the user has enough balance.
2. **Generate content** from text, images, or video (async — returns a generation ID).
3. **Poll for results** every 2-3 seconds until status is `completed` or `failed`.
4. **Optionally generate images or videos** from the captions or a text prompt (also async — poll for results).
5. **Create a post** combining the generated captions and images into a draft.
6. **Show the draft** to the user for review before publishing.
7. **Publish** the post immediately, or **schedule** it for later. Scheduled posts can be canceled before they fire.

After publishing, you can also fetch per-item **analytics** to see how it performed (views, likes, comments).

Always check credits before generating content. Always show the user what will be published and get confirmation before calling publish or schedule.

---

## Endpoints

### 1. Check Credits

Use this to check how many credits the user has before starting any generation.

```bash
curl https://powerpost.ai/api/v1/account/credits \
  -H "x-api-key: $POWERPOST_API_KEY"
```

Note: This endpoint does NOT need the `X-Workspace-Id` header.

Response:

```json
{
  "balance": 47
}
```

Tell the user their current balance. If balance is low, warn them before they start a generation.

**Required scope:** `account:read`

### Credit Costs

Credit costs vary by action:
- **Caption generation:** depends on research mode, input type, number of source URLs, and video length.
- **Image generation:** depends on model and quantity.
- **Video generation:** depends on model, duration, and whether audio is enabled.
- **Publishing:** depends on platform. Premium platforms like X cost more.

For caption, image, and video generation, the exact cost comes back in the response as `credits_used` along with `remaining_credits`. Publishing is different — items are charged in the background as each one goes out, so the publish response itself does not include a cost. To see what publishing cost, fetch the credit balance after it completes.

Always check credits before starting a generation so the user knows the cost upfront. Credits are only charged for successful operations. Failed generations, failed publish attempts, and failed URL scrapes are refunded.

---

### 2. Upload Media

Use this when the user wants to generate content from images or video, or when they want to attach media to a post.

```bash
curl -X POST https://powerpost.ai/api/v1/media/upload \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -F "file=@/path/to/file" \
  -F "type=image"
```

The `type` field must be `image` or `video`.

Supported formats:
- Images: JPEG, PNG, WebP (max 10 MB)
- Videos: MP4, MOV, WebM (max 500 MB)

Response:

```json
{
  "media_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "image",
  "file_name": "photo.jpg",
  "file_size": 245000,
  "mime_type": "image/jpeg",
  "created_at": "2026-01-10T18:30:00Z"
}
```

Save the `media_id` from the response. You will need it for content generation (`media_ids` field) or for creating posts (`media_ids` in post items).

Tell the user the upload was successful and show the file name and size.

**Required scope:** `media:write`

---

### 3. Generate Content

Use this when the user wants to create social media captions.

There are three input modes, determined by which fields you provide:
- **Text only:** Send `prompt` (required, 3-2000 chars).
- **Image input:** Send `media_ids` with image IDs (+ optional `prompt` for context).
- **Video input:** Send `media_ids` with a video ID (+ optional `prompt` for context).

You must provide either `prompt` or `media_ids` (or both).

```bash
curl -X POST https://powerpost.ai/api/v1/content/generate \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "We just shipped dark mode across all our apps",
    "post_types": ["instagram-reel", "tiktok-video", "x-post"],
    "research_mode": "regular"
  }'
```

**Required fields:**
- `post_types` (string array) — At least one post type. See the post types table below.
- `research_mode` (string) — `"regular"` or `"deep"`. Use regular for quick tasks, deep for important posts.

**Optional fields:**
- `writing_style_id` (string) — A custom writing style ID created in the dashboard.
- `cta_text` (string, max 100 chars) — A custom call-to-action.
- `source_urls` (string array, max 10) — URLs to scrape for research context. Must be HTTPS. Private/internal URLs are filtered out for security. Each URL adds to the generation cost.

**Post types:**

| Platform  | Post Types                                            |
|-----------|-------------------------------------------------------|
| Instagram | `instagram-feed`, `instagram-reel`, `instagram-story` |
| TikTok    | `tiktok-video`, `tiktok-photos`                       |
| YouTube   | `youtube-video`, `youtube-short`                      |
| X         | `x-post`                                              |
| Facebook  | `facebook-post`, `facebook-reel`, `facebook-story`    |
| LinkedIn  | `linkedin-post`                                       |

Multiple post types from the same platform produce one shared caption for that platform. The post type declares publishing intent.

Response:

```json
{
  "generation_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "credits_used": 10,
  "remaining_credits": 90,
  "status_url": "/api/v1/content/generations/550e8400-e29b-41d4-a716-446655440000"
}
```

Tell the user the generation has started, how many credits it cost, and that you are waiting for it to complete. Then immediately start polling.

**Required scope:** `content:generate`

---

### 4. Get Generation Status (Polling)

After starting a generation, poll this endpoint every 2-3 seconds until `status` is `completed` or `failed`. Do not poll more than 60 times (about 2 minutes).

```bash
curl https://powerpost.ai/api/v1/content/generations/GENERATION_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**While processing:**

```json
{
  "generation_id": "550e8400-...",
  "status": "processing",
  "prompt": "We just shipped dark mode",
  "platforms": ["tiktok", "instagram"],
  "research_mode": "regular",
  "credits_used": 10,
  "created_at": "2026-01-10T18:30:00Z"
}
```

If status is still `processing` or `pending`, wait 3 seconds and poll again.

**When completed:**

```json
{
  "generation_id": "550e8400-...",
  "status": "completed",
  "prompt": "We just shipped dark mode",
  "platforms": ["tiktok", "instagram"],
  "research_mode": "regular",
  "credits_used": 10,
  "created_at": "2026-01-10T18:30:00Z",
  "outputs": {
    "tiktok": "Dark mode activated! POV: your eyes at 2am finally getting some relief... #darkmode #tech",
    "instagram": "Dark mode is here!\n\nYour late-night scrolling just got easier on the eyes... #DarkMode #ProductUpdate"
  }
}
```

The `outputs` object is keyed by platform name (not post type). Each value is a string, EXCEPT YouTube which has a `title` and `description`:

```json
"youtube": {
  "title": "We Just Shipped Dark Mode",
  "description": "Dark mode is finally here across all our apps... #darkmode"
}
```

When completed, display all generated captions to the user, clearly labeled by platform.

**When failed:**

The response includes an `error` object with `code` and `message`. Credits are refunded on failure. Tell the user the generation failed and show the error message.

**Required scope:** `content:read`

---

### 5. List Generations

Use this when the user wants to see their recent generations or search for a past generation.

```bash
curl "https://powerpost.ai/api/v1/content/generations?status=completed&limit=10" \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

Query parameters (all optional):
- `status` — Filter by: `pending`, `processing`, `completed`, `failed`
- `limit` — Results per page, 1-100 (default 20)
- `cursor` — Pagination cursor from `next_cursor` in a previous response

Response:

```json
{
  "data": [
    {
      "generation_id": "550e8400-...",
      "status": "completed",
      "prompt": "We just shipped dark mode",
      "platforms": ["tiktok", "instagram"],
      "research_mode": "regular",
      "credits_used": 10,
      "created_at": "2026-01-10T18:30:00Z"
    }
  ],
  "next_cursor": "gen_cursor_abc123",
  "has_more": true
}
```

The list endpoint does NOT include `outputs`. To get the full content of a specific generation, use the get generation endpoint with its ID.

Show the user a summary table of their generations. If they want to see the content of a specific one, fetch it with the get endpoint.

**Required scope:** `content:read`

---

### 6. Generate Images

Use this when the user wants to create AI-generated images. There are three input modes:

**Text mode:** Describe the image in `prompt`.
**Reference mode:** Provide `prompt` + `style_images` (media IDs of uploaded reference images, max 4).
**Post mode:** Provide `generation_id` to create images matching an existing caption generation (+optional `prompt` for extra direction and `source_post_type` to pick which platform caption to use).

```bash
curl -X POST https://powerpost.ai/api/v1/images/generate \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Minimalist workspace with laptop and coffee, warm morning light",
    "size": "square",
    "quantity": 2,
    "model": "nano-banana-2"
  }'
```

**Fields:**
- `prompt` (string, max 2000 chars) — Required for text and reference modes. Optional for post mode.
- `size` (string) — `square` (1:1), `feed` (4:5), `portrait` (9:16), `landscape` (16:9). Default: `square`.
- `quantity` (number, 1-4) — How many images to generate. Default: 1.
- `model` (string) — `nano-banana-2` (default, fast generation, great text), `flux2-flex` (best for multi-reference and fine control), `ideogram-3` (best text rendering and logos), `gpt-image-2` (most photorealistic, best detail).
- `enhance_prompt` (boolean) — Let AI optimize the prompt. Default: false.
- `style_images` (string array) — Media IDs of reference images (max 4). For reference mode.
- `generation_id` (string) — Caption generation ID. For post mode.
- `source_post_type` (string) — Which platform's caption to use as source. For post mode only.

**Model and size compatibility:**
- `flux2-flex`: square, feed, portrait, landscape
- `ideogram-3`: square, feed, portrait, landscape
- `gpt-image-2`: square, portrait, landscape (NO feed). Portrait is 1024×1536 and landscape is 1536×1024.
- `nano-banana-2`: square, feed, portrait, landscape

If the user requests a model/size combo that is not supported, warn them and suggest an alternative.

Response:

```json
{
  "image_generation_id": "7a8b9c0d-e1f2-3456-abcd-ef7890123456",
  "status": "processing",
  "credits_used": 10,
  "remaining_credits": 36,
  "status_url": "/api/v1/images/generations/7a8b9c0d-e1f2-3456-abcd-ef7890123456"
}
```

Tell the user that image generation has started and begin polling.

**Required scope:** `images:generate`

---

### 7. Get Image Generation Status (Polling)

Poll this endpoint every 2-3 seconds until status is `completed` or `failed`.

```bash
curl https://powerpost.ai/api/v1/images/generations/IMAGE_GENERATION_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**When completed:**

```json
{
  "image_generation_id": "7a8b9c0d-...",
  "status": "completed",
  "prompt": "Minimalist workspace with laptop and coffee",
  "size": "square",
  "quantity": 2,
  "created_at": "2026-01-10T18:30:00Z",
  "images": [
    {
      "media_id": "img-001-abcd-efgh",
      "url": "https://powerpost.ai/storage/images/img-001-abcd-efgh.webp",
      "thumbnail_url": "https://powerpost.ai/storage/images/img-001-abcd-efgh-thumb.jpg",
      "width": 1024,
      "height": 1024
    }
  ]
}
```

Each image has a `media_id` which you use to attach the image to a post. The `url` is a preview link valid for 7 days. Always use the `media_id`, not the URL, when creating posts.

Show the user the image URLs so they can preview. Save the `media_id` values for creating posts.

**Partial failure:** If some images fail while others succeed, you get a partial result with a partial credit refund. The response status will be `failed` but may still contain an `images` array with the successful ones.

**Required scope:** `images:read`

---

### 8. Generate Videos

Use this when the user wants to create AI-generated videos. There are two input modes:

**Text-to-video:** Describe the video in `prompt`.
**Image-to-video:** Provide `prompt` + `source_image` (media ID of an uploaded image).

```bash
curl -X POST https://powerpost.ai/api/v1/videos/generate \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A golden retriever running through a field of wildflowers at sunset",
    "size": "landscape",
    "duration": 5,
    "model": "kling-3.0-pro",
    "has_audio": false
  }'
```

**Fields:**
- `prompt` (string, required) — Text description of the video.
- `size` (string) — `landscape` (16:9) or `portrait` (9:16). Default: `landscape`.
- `duration` (integer, required) — Duration in seconds. Must match one of the model's supported values (see table).
- `model` (string) — `kling-3.0-pro` (default), `veo-3.1`, or `runway-gen-4.5`.
- `has_audio` (boolean) — Generate with audio. Default: false. Only supported by some models.
- `enhance_prompt` (boolean) — Let AI optimize the prompt. Default: false.
- `source_image` (media ID, UUID) — Media ID of an uploaded image for image-to-video mode.

**Model details:**

| Model ID         | Name           | Sizes               | Audio | Durations |
|------------------|----------------|----------------------|-------|-----------|
| `kling-3.0-pro`  | Kling 3.0 Pro  | landscape, portrait | Yes   | 5s, 10s   |
| `veo-3.1`        | Google Veo 3.1 | landscape, portrait | Yes   | 4s, 8s    |
| `runway-gen-4.5` | Runway Gen-4.5 | landscape, portrait | No    | 5s, 10s   |

**Prompt limits by model:** Veo 3.1 = 3000 chars, Kling 3.0 Pro = 2500 chars, Runway Gen-4.5 = 1000 chars.

Credit costs depend on the model, duration, and audio. The exact cost is returned in the response.

Response:

```json
{
  "video_generation_id": "7a8b9c0d-e1f2-3456-abcd-ef7890123456",
  "status": "processing",
  "credits_used": 15,
  "remaining_credits": 85,
  "status_url": "/api/v1/videos/generations/7a8b9c0d-e1f2-3456-abcd-ef7890123456"
}
```

Tell the user that video generation has started and begin polling.

**Required scope:** `videos:generate`

---

### 9. Get Video Generation Status (Polling)

Poll this endpoint every 10 seconds until status is `completed` or `failed`. Video generation takes longer than images — do not poll more than 120 times.

```bash
curl https://powerpost.ai/api/v1/videos/generations/VIDEO_GENERATION_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**When completed:**

```json
{
  "video_generation_id": "7a8b9c0d-...",
  "status": "completed",
  "prompt": "A golden retriever running...",
  "size": "landscape",
  "duration": 5,
  "has_audio": false,
  "model": "kling-3.0-pro",
  "created_at": "2026-03-11T10:00:00Z",
  "video": {
    "media_id": "vid-001-abcd",
    "url": "https://powerpost.ai/storage/videos/vid-001-abcd.mp4",
    "thumbnail_url": "https://powerpost.ai/storage/thumbs/vid-001-abcd.jpg",
    "width": 1920,
    "height": 1080,
    "duration": 5
  }
}
```

The video has a `media_id` which you use to attach it to a post. The `url` is a preview link valid for 7 days. Always use the `media_id`, not the URL, when creating posts.

Show the user the video URL so they can preview. Save the `media_id` for creating posts.

**When failed:** The response includes an `error` object with `code` (`VIDEO_GENERATION_FAILED`) and `message`. Credits are refunded on failure.

**Required scope:** `videos:read`

---

### 10. Create Post

Use this to assemble captions and media into a draft post ready for review and publishing.

```bash
curl -X POST https://powerpost.ai/api/v1/posts \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "generation_id": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "post_type": "instagram-reel",
        "media_ids": ["img-001-abcd-efgh"]
      },
      {
        "post_type": "tiktok-video",
        "media_ids": ["img-001-abcd-efgh"]
      }
    ]
  }'
```

**Fields:**
- `generation_id` (string, optional) — Links to a completed caption generation. If provided, content is auto-filled from the generation outputs for each platform.
- `items` (array, required) — One item per post type you want to publish.

**Each item:**
- `post_type` (string, required) — The target post type (e.g., `instagram-reel`, `x-post`).
- `content` (string) — The caption text. Required if no `generation_id` is provided. If `generation_id` is provided, content is auto-filled but can be overridden.
- `title` (string) — Required for YouTube post types (`youtube-video`, `youtube-short`).
- `media_ids` (string array, optional) — Media to attach (uploaded or generated image IDs).

**Custom content example (no generation):**

```bash
curl -X POST https://powerpost.ai/api/v1/posts \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "post_type": "x-post",
        "content": "Just shipped the biggest update of the year."
      },
      {
        "post_type": "linkedin-post",
        "content": "Excited to announce our biggest product update of the year..."
      }
    ]
  }'
```

Response:

```json
{
  "post_id": "post-550e8400-e29b-41d4-a716-446655440000",
  "status": "draft",
  "created_at": "2026-01-10T18:30:00Z",
  "items": [
    {
      "item_id": "item-001",
      "post_type": "instagram-reel",
      "platform": "instagram",
      "content": "Dark mode is here! Your late-night scrolling just got easier... #DarkMode",
      "media_ids": ["img-001-abcd-efgh"],
      "status": "draft"
    }
  ]
}
```

After creating a post, show the user a summary of every item (platform, content preview, attached media) and ask if they want to publish or make changes.

**Required scope:** `posts:write`

---

### 11. Get Post

Use this to check the status of a post, especially after publishing.

```bash
curl https://powerpost.ai/api/v1/posts/POST_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

Response includes the post with all items and their individual statuses. After publishing, each item will show `posting`, `posted`, or `failed` with an optional `platform_post_id` for successfully published items.

Post statuses: `draft`, `scheduled`, `publishing`, `published`, `failed`.
Item statuses: `draft`, `posting`, `posted`, `failed`.

Note: the Get Post response does not currently include `scheduled_at` for scheduled posts. If you need that, save it from the Schedule response when the post was originally scheduled.

**Required scope:** `posts:read`

---

### 12. Publish Post

Use this to publish a draft post to connected social platforms. Always confirm with the user before calling this endpoint.

```bash
curl -X POST https://powerpost.ai/api/v1/posts/POST_ID/publish \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**Prerequisites:**
- The user's social platforms must be connected at https://powerpost.ai/settings/connections
- The post must be in `draft` or `failed` status.
- The user must have sufficient credits.
- The API key must have the `posts:publish` scope.

Response:

```json
{
  "post_id": "post-550e8400-...",
  "status": "publishing",
  "status_url": "/api/v1/posts/post-550e8400-..."
}
```

Publishing is asynchronous. After receiving the response, poll the Get Post endpoint every 3 seconds to check when each item has finished publishing.

Publishing costs vary by platform (premium platforms like X cost more). Credits are charged per item in the background as each one publishes, so the publish response itself does not include a cost figure. To see what was charged, fetch the credit balance after publishing completes.

Tell the user publishing is in progress. When all items show `posted` or `failed`, summarize the results.

**Required scope:** `posts:publish`

---

### 13. Schedule a Post

Use this to queue a draft post for automatic publishing at a future time, instead of publishing right now.

```bash
curl -X POST https://powerpost.ai/api/v1/posts/POST_ID/schedule \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "scheduled_at": "2026-03-25T14:00:00-07:00"
  }'
```

**Fields:**
- `scheduled_at` (string, required) — ISO 8601 timestamp with a timezone offset. Must be at least 1 minute in the future and no more than 60 days out.

**Prerequisites:**
- Same as Publish: platforms connected, post in `draft` status, items ready.
- Workspace must have fewer than 100 posts already scheduled. Hitting that cap returns 400.
- Credits aren't charged at schedule time. The credit check happens when the scheduled job fires.

Response:

```json
{
  "post_id": "post-550e8400-...",
  "status": "scheduled",
  "scheduled_at": "2026-03-25T21:00:00.000Z",
  "status_url": "/api/v1/posts/post-550e8400-..."
}
```

The returned `scheduled_at` is normalized to UTC. The post stays in `scheduled` status until the job fires, at which point it transitions through `publishing` → `published` (or `failed`).

Tell the user when the post is scheduled to go out. If they want to back out before then, use Cancel Publish.

**Required scope:** `posts:publish`

---

### 14. Cancel Publish

Use this to cancel a scheduled or in-progress publish and revert the post to `draft`. Useful for "actually, hold off on that one" moments.

```bash
curl -X POST https://powerpost.ai/api/v1/posts/POST_ID/cancel-publish \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**Important constraints:**
- The post must be in `scheduled` or `publishing` status. Calling this on a plain `draft`, `published`, or `failed` post returns 400.
- No item can have started posting yet. The moment any item flips to `posting`, `posted`, or a terminal failure, the cancel call returns 400 — you can't unpublish something that already went out.

Response:

```json
{
  "post_id": "post-550e8400-...",
  "status": "draft",
  "reverted": true
}
```

Tell the user the post is back to draft and won't publish. They can edit it or schedule it for a different time.

**Required scope:** `posts:publish`

---

## Common User Commands

### "Post about X" / "Create a post about X"

Full flow:
1. Check credits.
2. Ask which platforms if not specified. Default to all if the user says "everywhere" or "all platforms".
3. Generate content with the user's topic as the prompt. Use `regular` research mode unless they ask for deep. If the user provides URLs as references, include them in `source_urls`.
4. Poll until complete.
5. Show the generated captions.
6. Ask if they want to generate images too.
7. Create the post.
8. Show the draft and ask for confirmation.
9. Publish on confirmation.

### "Write captions about X" / "Generate content about X"

Partial flow (no publishing):
1. Check credits.
2. Generate content.
3. Poll until complete.
4. Show the captions to the user.

### "Create an image" / "Generate an image of X"

1. Check credits.
2. If the user provides a text description, use text mode. If they reference a previous generation, use post mode. If they have reference images, use reference mode.
3. Ask about size preference if not specified (square is a safe default).
4. Generate the image.
5. Poll until complete.
6. Show the image URLs to the user.

### "Create a video" / "Generate a video of X"

1. Check credits.
2. If the user has an image they want to animate, use image-to-video mode (upload first, then pass `source_image`). Otherwise use text-to-video mode.
3. Ask about duration if not specified. Default to 5 seconds.
4. Ask about size if not specified (landscape is a safe default for video).
5. Generate the video.
6. Poll until complete (video takes longer than images — up to a few minutes).
7. Show the video URL to the user.

### "Check my credits" / "How many credits do I have?"

1. Call the credits endpoint.
2. Tell the user their balance.

### "Upload this image/video"

1. Upload the file using the media upload endpoint.
2. Tell the user the upload succeeded and show the media ID.
3. Ask what they want to do with it (generate captions from it, use it in a post, etc.).

### "Show my recent posts" / "List my generations"

1. Call the list generations endpoint.
2. Show a summary of recent generations.
3. If the user wants details on one, fetch it with the get generation endpoint.

### "Publish my post" / "Send it live"

1. If there is a draft post from this session, publish it.
2. If not, ask the user which post to publish.
3. Always confirm before publishing.

### "Schedule this post for X" / "Post this on Friday at 9am"

1. Convert the user's time into ISO 8601 with their timezone offset. If they didn't say a timezone, ask.
2. Check the same prerequisites as publishing (platforms connected, post is `draft`).
3. Call the schedule endpoint with `scheduled_at`.
4. Confirm back: "Scheduled for [their local time]. I can cancel it before then if you change your mind."

### "Cancel that scheduled post" / "Don't publish that"

1. Call cancel-publish on the post.
2. If you get a 400, the post already started going out — tell the user and don't retry.
3. On success, the post is back to draft. Mention they can edit it or reschedule.

### "How did my post do?" / "Show me the analytics"

1. Fetch the post to get its items.
2. For each item with `status: "posted"`, call the analytics endpoint.
3. Show views, likes, comments per platform. Flag any item where `metrics` is null — that means metrics haven't been collected yet (usually for newly published items).

---

## Polling Strategy

Content generation, image generation, and video generation are all asynchronous. After starting any of them:

1. Wait 2 seconds.
2. Call the status endpoint.
3. If status is `processing` or `pending`, wait 3 seconds and poll again.
4. If status is `completed`, show the results.
5. If status is `failed`, show the error and tell the user credits were refunded.
6. Do not poll more than 60 times for content/images, or 120 times for video (it takes longer). If it times out, tell the user to try again later.

Publishing is also asynchronous. After calling publish:
1. Wait 3 seconds.
2. Poll the Get Post endpoint.
3. Check each item's status. When all are either `posted` or `failed`, stop polling.

---

## Error Handling

All errors return this format:

```json
{
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE"
  }
}
```

Handle these errors:

| HTTP Status | Code                     | What to Tell the User                                                  |
|-------------|--------------------------|------------------------------------------------------------------------|
| 400         | `VALIDATION_ERROR`       | The request was invalid. Check the fields and try again.               |
| 401         | `INVALID_API_KEY`        | The API key is missing or invalid. Check POWERPOST_API_KEY.            |
| 402         | `INSUFFICIENT_CREDITS`   | Not enough credits. Check balance and suggest upgrading.               |
| 403         | `INSUFFICIENT_SCOPE`     | The API key is missing the scope this endpoint needs. The response body includes a `missing_scopes` array listing which scope(s) to add at https://powerpost.ai/settings/api |
| 403         | `FORBIDDEN`              | Other access denial (e.g., the workspace doesn't belong to this account). |
| 404         | `NOT_FOUND`              | The resource was not found. Check the ID.                              |
| 409         | `ALREADY_PUBLISHED`      | This post was already published.                                       |
| 413         | `FILE_TOO_LARGE`         | The file exceeds the size limit (10 MB for images, 500 MB for video).  |
| 413         | `STORAGE_QUOTA_EXCEEDED` | Storage quota exceeded (10 GB limit). Delete unused media or contact support. |
| 422         | `PLATFORM_NOT_CONNECTED` | The target platform is not connected. Direct user to https://powerpost.ai/settings/connections |
| 429         | `RATE_LIMIT_EXCEEDED`    | Too many requests. Wait the duration in `retryAfter` seconds and retry. |
| 500         | `INTERNAL_ERROR`         | Server error. Wait a moment and try again.                             |

For rate limit errors (429), the response includes a `retryAfter` field in seconds. Wait that long before retrying.

Every response includes an `X-Request-Id` header. If the user needs support, give them this ID.

---

### 15. List Calendar Entries

Use this to pull up what's on the user's content calendar.

```bash
curl "https://powerpost.ai/api/v1/calendar/entries?start_date=2026-03-01&end_date=2026-03-31" \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**Query parameters (both required):**
- `start_date` (string) — Start of range, `YYYY-MM-DD`.
- `end_date` (string) — End of range, `YYYY-MM-DD`.

The date range can't exceed 366 days.

Response:

```json
{
  "entries": [
    {
      "entry_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Product launch announcement",
      "description": "Share the new feature across all channels",
      "scheduled_date": "2026-03-25",
      "scheduled_time": "14:00",
      "platforms": ["instagram", "tiktok", "x"],
      "created_at": "2026-03-19T10:00:00Z",
      "updated_at": "2026-03-19T10:00:00Z"
    }
  ]
}
```

Show the entries grouped by date with their title and platforms.

**Required scope:** `calendar:read`

---

### 16. Create Calendar Entry

Use this to plan a future post on the calendar.

```bash
curl -X POST https://powerpost.ai/api/v1/calendar/entries \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product launch announcement",
    "description": "Share the new feature across all channels",
    "scheduled_date": "2026-03-25",
    "scheduled_time": "14:00",
    "platforms": ["instagram", "tiktok", "x"]
  }'
```

**Fields:**
- `title` (string, required) — What the post is about (max 500 chars).
- `description` (string, optional) — Extra notes or details (max 5000 chars).
- `scheduled_date` (string, required) — Target date, `YYYY-MM-DD`.
- `scheduled_time` (string, optional) — Target time, `HH:MM` (24-hour).
- `platforms` (string array, optional) — Target platforms: `instagram`, `tiktok`, `youtube`, `x`, `facebook`, `linkedin`.

Response:

```json
{
  "entry_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Product launch announcement",
  "description": "Share the new feature across all channels",
  "scheduled_date": "2026-03-25",
  "scheduled_time": "14:00",
  "platforms": ["instagram", "tiktok", "x"],
  "created_at": "2026-03-19T10:00:00Z",
  "updated_at": "2026-03-19T10:00:00Z"
}
```

Confirm the entry was created and show the date, title, and platforms.

**Required scope:** `calendar:write`

---

### 17. Get Calendar Entry

Use this to fetch a specific calendar entry by ID.

```bash
curl https://powerpost.ai/api/v1/calendar/entries/ENTRY_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

Response is the same shape as the create response. Returns 404 if the entry doesn't exist.

**Required scope:** `calendar:read`

---

### 18. Update Calendar Entry

Use this to change details on an existing calendar entry. Only include the fields you want to update.

```bash
curl -X PATCH https://powerpost.ai/api/v1/calendar/entries/ENTRY_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated launch announcement",
    "scheduled_date": "2026-03-28"
  }'
```

**Fields (all optional):**
- `title` (string) — Max 500 chars.
- `description` (string, nullable) — Max 5000 chars. Pass `null` to clear.
- `scheduled_date` (string) — `YYYY-MM-DD`.
- `scheduled_time` (string, nullable) — `HH:MM`. Pass `null` to clear.
- `platforms` (string array) — Replaces the full list.

At least one field must be provided.

Response returns the full updated entry.

**Required scope:** `calendar:write`

---

### 19. Delete Calendar Entry

Use this to remove a calendar entry.

```bash
curl -X DELETE https://powerpost.ai/api/v1/calendar/entries/ENTRY_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

Response:

```json
{
  "success": true
}
```

Returns 404 if the entry doesn't exist.

**Required scope:** `calendar:write`

---

### 20. Get Post Item Analytics

Use this to pull performance metrics for a single published post item (one platform's worth of a post).

```bash
curl https://powerpost.ai/api/v1/post-items/ITEM_ID/analytics \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

The `ITEM_ID` is the `item_id` of a post item, not the parent post ID. Get item IDs from a Get Post response.

Response:

```json
{
  "post_item_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "post_type": "instagram-reel",
  "platform": "instagram",
  "status": "posted",
  "metrics": {
    "views": 12450,
    "likes": 318,
    "comments": 24,
    "fetched_at": "2026-03-25T18:00:00Z"
  }
}
```

A few things to keep in mind:

- `metrics` is `null` when the item hasn't been posted yet or hasn't been polled. Don't treat null as "zero" — it means "not collected".
- Numbers are best-effort. If the platform doesn't return a value for a field, it comes back as 0.
- Metrics refresh roughly daily for up to 90 days after the item was posted. There's no on-demand refresh — calling this endpoint twice in a row returns the same numbers.
- `fetched_at` tells you how fresh the snapshot is.

When the user asks how a post is doing, fetch the post first, then call this for each item that has `status: "posted"`.

**Required scope:** `analytics:read`

---

## Things to know

- Always show the user what will be posted and where, and get explicit confirmation before publishing. This goes to real social accounts.
- YouTube posts need a `title` field in addition to the caption.
- If the user picks both `instagram-reel` and `instagram-feed`, they share one Instagram caption. The post type controls the publishing format, not the caption.
- Image and video URLs from generation expire after 7 days. Always use `media_id` when creating posts, not the URL.
- Credits are shared across all workspaces on an account.
- Workspaces are isolated from each other. Generations, posts, media, and connections in one workspace aren't visible in another.
- Users can set up webhooks at https://powerpost.ai/settings/api for real-time notifications instead of polling. Not needed for agent usage, but useful for production integrations.
- A workspace can hold up to 100 scheduled posts at once. If the schedule endpoint returns 400 with that reason, the user has to cancel an existing scheduled post or wait for one to fire before queuing another.
- Scheduled posts can be scheduled up to 60 days in the future, and must be at least 1 minute out.
- Analytics metrics refresh roughly once per day for up to 90 days after a post goes out. There's no on-demand refresh, so don't poll the analytics endpoint repeatedly.
- The `posts:publish` scope covers all three of publish, schedule, and cancel-publish. A `read_only` key can't do any of them.

## External endpoints

All requests go to one domain: `https://powerpost.ai/api/v1/*`. Nothing is sent anywhere else.

## Security and privacy

- Your API key and workspace ID are sent to `powerpost.ai` as HTTP headers with every request. They're not logged, displayed, or sent anywhere else.
- Prompts, uploaded media, and generated content are stored on PowerPost's servers, scoped to your workspace.
- This skill only uses `curl` over HTTPS. It doesn't write files, run scripts, or touch your system.

## Trust

When you use this skill, your prompts, images, videos, and credentials go to `powerpost.ai` over HTTPS. PowerPost uses third-party AI models on their servers to process your content. Their privacy policy is at https://powerpost.ai/terms and support is at https://powerpost.ai/contact

## Tips

- Always check the credit balance before starting a generation. Better to warn the user upfront than hit an insufficient credits error mid-flow.
- Default to `regular` research mode. Only use `deep` when the user asks for it or says the post matters.
- Default to `square` for image size if the user doesn't say. It works on most platforms.
- Default to `nano-banana-2` for the image model (it's the API default and is fast). Switch to `flux2-flex` if the user wants multi-reference control, `ideogram-3` for logos and text-heavy designs, or `gpt-image-2` for photorealism.
- If a generation fails, credits are refunded. Let the user know and suggest trying again.
- When the user says "all platforms," use one post type per platform: `instagram-feed`, `tiktok-video`, `youtube-short`, `x-post`, `facebook-post`, `linkedin-post`.
- If the user's image description is short or vague, suggest setting `enhance_prompt: true` to let the AI fill in the details.
- Default to `kling-3.0-pro` for video generation. It handles both sizes and supports audio.
- Default to `landscape` and 5 seconds for video unless the user says otherwise.
- Video generation is slower than images. Tell the user it may take a couple minutes.
- If the user provides URLs as references for a post, pass them as `source_urls` in the content generation request. Each URL adds to the cost.
