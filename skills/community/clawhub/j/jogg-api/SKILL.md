---
name: jogg-api
description: Use when working with JoggAI v2 APIs and workflow execution for avatar videos, product videos, templates, assets, avatars, webhooks, translation, and account lookups. Covers endpoint lookup plus guided workflow routing, while keeping lip sync in its own dedicated skill.
license: Proprietary
compatibility: Requires curl, jq, a local shell environment, and JOGG_API_KEY to call the Jogg API.
metadata: { "author": "JoggAI", "version": "0.1.0", "openclaw": { "requires": { "bins": ["curl", "jq"], "env": ["JOGG_API_KEY"] }, "primaryEnv": "JOGG_API_KEY", "os": ["darwin", "linux"] } }
---

# Jogg API

Use this skill when the task is about JoggAI v2 endpoint execution or one of the main multi-step API workflows.

All paths in this document are relative to the current skill root directory.

Runner:

- `bash "scripts/jogg-v2.sh"`

Do not use this skill for lip sync. Use `jogg-lip-sync` instead.

## Trigger

- User wants to call a JoggAI v2 endpoint directly
- User asks to generate avatar videos, product videos, template videos, scripts, photo avatars, or product avatars
- User asks to translate a video
- User wants to upload local media and reuse the returned `asset_url`
- User wants webhook setup, event listing, endpoint updates, or quota/account lookups
- User already has an async ID and wants the current result without writing integration code

## Hard Rules

- Use `scripts/jogg-v2.sh` as the execution entrypoint
- Prefer `--workflow` for scenario requests and `--op` for direct endpoint requests
- Do not write ad hoc `curl` commands when the runtime already supports the operation
- Do not poll list endpoints
- Poll only status endpoints for async tasks
- Poll no faster than every `10` seconds
- Always keep polling bounded by both `max_wait_seconds` and `max_poll_attempts`
- If the latest state is still non-terminal after the limit, return the last payload and stop
- If the user only wants status, use `workflow get-result` or the specific `*-get` operation

## Required Inputs

- `JOGG_API_KEY` is required
- `JOGG_BASE_URL` is optional and defaults to `https://api.jogg.ai`
- `JOGG_API_PLATFORM` is optional and defaults to `openclaw`

Polling defaults:

- `JOGG_API_DEFAULT_POLL_INTERVAL_SECONDS=15`
- `JOGG_API_DEFAULT_MAX_WAIT_SECONDS=1800`
- `JOGG_API_DEFAULT_MAX_POLL_ATTEMPTS=90`

## Intent Routing

- “查某个接口 / 调 voices / 看模板列表 / 查用户额度”
  Use `--op`
- “帮我做商品视频 / 做数字人口播 / 创建照片数字人 / 建 webhook / 翻译视频”
  Use `--workflow`
- “我已经有 task_id/video_id/batch_id，帮我查结果”
  Use `--workflow get-result`

## Endpoint Mode

List supported endpoint operations:

```bash
bash "scripts/jogg-v2.sh" --list-ops
```

Generic pattern:

```bash
bash "scripts/jogg-v2.sh" \
  --op "<operation>" \
  --body-json '<json>' \
  --query-json '<json>' \
  --path-json '<json>'
```

Examples:

```bash
bash "scripts/jogg-v2.sh" \
  --op "voices-list" \
  --query-json '{"language":"en-US","gender":"Male"}'
```

```bash
bash "scripts/jogg-v2.sh" \
  --op "avatar-video-get" \
  --path-json '{"id":"video_123456"}' \
  --poll
```

For the full endpoint catalog, see `references/endpoints.md`.

## Workflow Mode

List supported workflows:

```bash
bash "scripts/jogg-v2.sh" --list-workflows
```

Generic pattern:

```bash
bash "scripts/jogg-v2.sh" \
  --workflow "<workflow>" \
  --body-json '<json>' \
  --poll
```

Supported workflows:

- `upload-media`
- `ai-scripts`
- `create-photo-avatar`
- `photo-avatar-motion`
- `avatar-video`
- `avatar-video-with-photo-avatar`
- `avatar-video-with-custom-audio`
- `avatar-video-transparent`
- `url-to-video`
- `create-template-video`
- `video-translation`
- `product-avatar`
- `webhook-integration`
- `get-result`

For the flow definitions and step order, see `references/workflows.md`.

## Workflow Inputs

### `upload-media`

- required: `file_path`
- optional: `content_type`

### `ai-scripts`

- same payload as `POST /v2/ai_scripts`
- returns either submit result or final script payload

### `create-photo-avatar`

- same payload as `POST /v2/photo_avatar/photo/generate`
- optional convenience field: `image_path`

### `photo-avatar-motion`

- required: `name`, `voice_id`, `model`
- one of:
  - `image_url`
  - `photo_id`

### `avatar-video`

- same payload as `POST /v2/create_video_from_avatar`
- optional convenience field: `voice.audio_path`

### `url-to-video`

- `product`: create-product payload
- `product_update`: optional update-product payload without `product_id`
- `render_mode`: `direct` or `preview`
- `create_request`: required in `direct` mode
- `preview_request`: required in `preview` mode
- `preview_index`: optional, defaults to `0`

### `create-template-video`

- same payload as `POST /v2/create_video_with_template`
- optional convenience field: `variables[].properties.local_path`

### `video-translation`

- same payload as `POST /v2/video_translate/`
- optional convenience field: `video_path`

### `product-avatar`

- `generation`: payload for `POST /v2/product_avatar/generation`
- `motion`: payload for `POST /v2/product_avatar/add_motion` without `generation_id`
- optional convenience field: `product_image_path`

### `webhook-integration`

- `action`: `list`, `events`, `create`, `update`, or `delete`
- `create`: payload for `POST /v2/endpoint`
- `update`: payload for `PUT /v2/endpoint/{endpoint_id}` plus `endpoint_id`
- `delete`: needs `endpoint_id`

### `get-result`

- required: `kind`
- plus the corresponding async identifier

## Output Contract

- `stdout` returns machine-readable JSON only
- `stderr` is reserved for progress logs
- create workflows return submit info plus the final result when polling is enabled
- timed-out polls return the last known payload with `poll_timeout: true`

## Examples

Create AI scripts:

```bash
bash "scripts/jogg-v2.sh" \
  --workflow "ai-scripts" \
  --body-json '{
    "language":"english",
    "video_length_seconds":"30",
    "script_style":"Storytime",
    "product_info":{
      "source_type":"details",
      "data":{
        "name":"Amazing Smart Bottle",
        "description":"Self-cleaning bottle for travel and fitness use"
      }
    }
  }'
```

Create photo avatar and stop after submit:

```bash
bash "scripts/jogg-v2.sh" \
  --workflow "create-photo-avatar" \
  --body-json '{
    "age":"Adult",
    "avatar_style":"Professional",
    "gender":"Female",
    "model":"modern",
    "aspect_ratio":"portrait",
    "image_path":"/tmp/portrait.jpg"
  }' \
  --no-poll
```

Create product video through preview flow:

```bash
bash "scripts/jogg-v2.sh" \
  --workflow "url-to-video" \
  --body-json '{
    "product":{
      "url":"https://example.com/product-page"
    },
    "render_mode":"preview",
    "preview_request":{
      "visual_styles":["Simple Product Switch","Dynamic Showcase"],
      "video_spec":{"aspect_ratio":"landscape","length":"30","caption":true},
      "avatar":{"id":1,"type":0},
      "voice":{"id":"en-US-ChristopherNeural"},
      "audio":{"music_id":13},
      "script":{"style":"Storytime","language":"english"}
    }
  }'
```
