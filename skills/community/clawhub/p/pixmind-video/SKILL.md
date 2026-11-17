---
name: pixmind-video
description: Generate AI videos via Pixmind API (text-to-video and image-to-video)
metadata: {"openclaw": {"requires": {"env": ["PIXMIND_API_KEY"]}, "primaryEnv": "PIXMIND_API_KEY"}}
---

# Pixmind Video Generation Skill

Generate AI videos using [Pixmind](https://www.pixmind.io). Supports text-to-video and image-to-video generation.

> **Note:** The API endpoint `aihub-admin.aimix.pro` is the official Pixmind API gateway. Result URLs on `chatmix.top` are Pixmind's CDN for generated content.

## When to use

- User asks to generate or create a video
- User wants to animate an existing image into a video
- User requests video content from a text description

## Prerequisites

1. Register at [pixmind.io](https://www.pixmind.io/) — 注册即送 200 积分免费试用
2. Create an API key in the [API Platform dashboard](https://www.pixmind.io/api-platform/dashboard/keys)
3. Set env `PIXMIND_API_KEY` with your key

## API Details

**Endpoint**: `POST https://aihub-admin.aimix.pro/api-platform/v1/generations`
**Auth**: Header `Authorization: Bearer {API_KEY}` (from env `PIXMIND_API_KEY`)

## Request Body (JSON)

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `type` | Yes | string | Fixed value: `video` |
| `prompt` | Yes | string | Video description / prompt |
| `model` | No | string | Model ID (default: `seedance-2.0-pro`) |
| `duration` | No | number | Video duration in seconds (allowed values vary by model) |
| `aspectRatio` | No | string | Aspect ratio (allowed values vary by model) |
| `resolution` | No | string | Resolution: `480p`, `720p`, `1080p` (required for Seedance models) |
| `generateType` | No | string | `text2video` (default) or `img2video` |
| `imageUrl` | No | string | Reference image URL (required for `img2video`) |

### Available Models

Fetch the current model catalog from `GET /api-platform/v1/models`. The list below was verified against the API Platform generation service on 2026-08-10.

| Model ID | Text-to-Video | Image-to-Video | Aspect Ratios | Duration (s) | Resolution | Notes |
|----------|:---:|:---:|---------------|--------------|------------|-------|
| `seedance-2.0-pro` | ✓ | ✓ | (see Seedance) | 3–10 | 480p / 720p / 1080p | ByteDance flagship. **Default model.** Maps to `doubao-seedance-2-0` upstream. |
| `seedance-2.0-fast` | ✓ | ✓ | (see Seedance) | 3–10 | 480p / 720p / 1080p | Fast variant. Maps to `doubao-seedance-2-0-fast`. |
| `seedance-1.5-pro` | ✓ | ✓ | (see Seedance) | 3–10 | 480p / 720p / 1080p | Previous flagship. Maps to `doubao-seedance-1-5-pro`. |
| `veo-3.1` | ✓ | ✓ | `16:9`, `9:16` | (see Veo) | — | Google Veo 3.1, latest. |
| `veo-3.1-eco` | ✓ | ✓ | `16:9`, `9:16` | (see Veo) | — | Cheaper Veo 3.1 variant. |
| `veo-3.0` | ✓ | ✓ | `16:9`, `9:16` | (see Veo) | — | Google Veo 3.0. |
| `veo-3` | ✓ | ✓ | `16:9`, `9:16` | (see Veo) | — | Alias of `veo-3.0`. |
| `veo-3.0-fast` | ✓ | ✓ | `16:9`, `9:16` | (see Veo) | — | Fast variant of Veo 3.0. |
| `sora-2` | ✓ | ✓ | (see Sora) | `4`, `8`, `12` only | — | OpenAI Sora 2. Only accepts durations 4, 8, or 12. |
| `sora-2-eco` | ✓ | ✓ | (see Sora) | `4`, `8`, `12` only | — | Cheaper Sora 2. Provider availability varies. |
| `sora-2-pro` | ✓ | ✓ | (see Sora) | `4`, `8`, `12` only | — | Pro variant. Currently paused upstream — may error. |
| `wan2.6-t2v` | ✓ | ✗ | `16:9`, `9:16`, `1:1`, `4:3`, `3:4` | 3–10 | — | Alibaba Wan 2.6 text-to-video. |
| `wan2.6-i2v` | ✗ | ✓ | `16:9`, `9:16`, `1:1`, `4:3`, `3:4` | 3–10 | — | Alibaba Wan 2.6 image-to-video. |
| `wan2.6-i2v-flash` | ✗ | ✓ | `16:9`, `9:16`, `1:1`, `4:3`, `3:4` | 3–10 | — | Faster Wan 2.6 image-to-video. |

### Unsupported Models (removed or never published in API)

The following slugs are **rejected** by the API with `不支持的模型`. Do not use:

- All `seedance-1.0*` (1.0, 1.0-pro, 1.0-lite) — removed
- `seedance-1.5`, `seedance-1.5-lite`, `seedance-1.5-turbo` — only `seedance-1.5-pro` survives
- `seedance-2.0`, `seedance-2.0-lite`, `seedance-2.0-mini`, `seedance-2.0-turbo`, `seedance-2.0-eco`
- All `kling-*` (kling-v1.5, v1.6, std-1.6, v2, v2-master, v2-pro, v3, v3-motion-control, etc.) — Kling no longer exposed via this API
- All `pixverse-*` (1.0, 2.0, 3.0, 4.0, video, v5) — slugs partially recognized but route is broken (500 error: `Cannot read properties of undefined (reading 'internalModel')`)
- `wan2.1-t2v`, `wan2.5-t2v`, `wan2.7-video`, `wan2.7-t2v`, `wan2.7-i2v`
- All `minimax-*`, `hailuo`, `hidream-*`
- `veo`, `veo-2`, `veo-3.2`, `veo-3.1-fast`, `veo-3.1-pro`, `veo-3.1-ultra`, `veo-3.0-pro`, `veo-3.0-ultra`
- `sora`, `sora-1`, `sora-3`, `sora-2.5`, `sora-2-fast`, `sora-2-mini`, `sora-2-ultra`

### Model Introductions

**Seedance (ByteDance Doubao)** — Flagship video generation series with smooth motion and realistic physics. **Resolution parameter required.**
- `seedance-2.0-pro` — Latest flagship. Best for professional-grade video.
- `seedance-2.0-fast` — Faster, lower cost variant of 2.0.
- `seedance-1.5-pro` — Previous flagship, still high quality.

**Google Veo** — Cinematic video generation with native audio support. **Only `16:9` and `9:16` aspect ratios.**
- `veo-3.1` / `veo-3.1-eco` — Latest Veo 3.1 generation.
- `veo-3.0` / `veo-3` / `veo-3.0-fast` — Veo 3.0 generation.

**OpenAI Sora** — Strong at complex scenes and physical accuracy. **Only durations `4`, `8`, or `12` seconds accepted.**
- `sora-2` — Latest stable Sora.
- `sora-2-eco` — Cheaper variant (provider availability varies).
- `sora-2-pro` — Pro tier (currently paused upstream).

**Wan 2.6 (Alibaba)** — Alibaba's video diffusion model. Supports all common aspect ratios.
- `wan2.6-t2v` — Text-to-video.
- `wan2.6-i2v` — Image-to-video.
- `wan2.6-i2v-flash` — Faster image-to-video variant.

## Usage

Use `curl` or the included helper script:

```bash
# Text to video (via curl) — Seedance requires resolution
curl -X POST https://aihub-admin.aimix.pro/api-platform/v1/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PIXMIND_API_KEY" \
  -d '{"type": "video", "prompt": "ocean waves", "model": "seedance-2.0-pro", "duration": 5, "resolution": "1080p", "aspectRatio": "16:9"}'

# Sora 2 — duration MUST be 4, 8, or 12
curl -X POST https://aihub-admin.aimix.pro/api-platform/v1/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PIXMIND_API_KEY" \
  -d '{"type": "video", "prompt": "city night drive", "model": "sora-2", "duration": 8, "aspectRatio": "16:9"}'

# Veo 3.1 — only 16:9 or 9:16
curl -X POST https://aihub-admin.aimix.pro/api-platform/v1/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PIXMIND_API_KEY" \
  -d '{"type": "video", "prompt": "timelapse", "model": "veo-3.1", "duration": 8, "aspectRatio": "16:9"}'

# Or use the helper script
node {baseDir}/video-generate.js --prompt "描述文字" --model seedance-2.0-pro --duration 5 --resolution 1080p
```

## Task Status Polling

After generation, poll for results:

```bash
# Via curl
curl https://aihub-admin.aimix.pro/api-platform/v1/tasks/<TASK_ID> \
  -H "Authorization: Bearer $PIXMIND_API_KEY"

# Or use the helper script
node {baseDir}/task-status.js --task-id <TASK_ID> --poll
```

## Response Format

Generate response:
```json
{"code": 1000, "data": {"taskId": 19401, "status": "processing"}}
```

Task status response:
```json
{
  "code": 1000,
  "data": {
    "taskId": 19401,
    "status": "ready",
    "progress": 100,
    "videoUrl": "https://chatmix.top/...",
    "coverUrl": "https://chatmix.top/..."
  }
}
```

- `data.taskId` — Use this to poll status
- Status values: `processing` → `ready` (success)
- On success: `data.videoUrl` contains the video URL, `data.coverUrl` has the cover image

## Error Responses

- `code: 400` with `不支持的模型: <model>` — Unsupported model slug.
- `code: 500` with `the parameter resolution specified in the request is not valid for model <X>` — Seedance models require an explicit `resolution` of `480p`, `720p`, or `1080p`.
- `code: 500` with `Invalid aspect ratio: <X>` — Aspect ratio not supported by this model. Veo only accepts `16:9` / `9:16`.
- `code: 500` with `invalid duration: <N>s (model sora-2-preview only supports duration=[4 8 12])` — Sora only accepts durations of 4, 8, or 12 seconds.
- `code: 1001` with `请输入提示词` — Empty prompt.
- `code: 1001` with `速率限制：每minute最多60次请求` — Rate limited; back off.

## Guidelines

1. Always confirm the prompt, duration, and model with the user before generating
2. Default to `seedance-2.0-pro` with `resolution: 1080p` and `aspectRatio: 16:9` unless user specifies otherwise
3. **Seedance models** require `resolution` (`480p` / `720p` / `1080p`) — requests without it fail
4. **Veo models** only accept `16:9` or `9:16` aspect ratios
5. **Sora 2 models** only accept `duration` of `4`, `8`, or `12` seconds — pick one of these explicitly
6. If user provides a reference image, automatically use `img2video` mode and pick an image-to-video capable model (`wan2.6-i2v`, `wan2.6-i2v-flash`, or any Veo / Sora / Seedance model)
7. Video generation takes longer than images — use `--poll` with appropriate interval (recommend 5–10s)
8. After getting the task ID, poll until completion and return video URL
9. For faster results on a budget, prefer `seedance-2.0-fast`, `wan2.6-i2v-flash`, or `veo-3.0-fast`
10. Avoid probing the API by sending requests with arbitrary model names — many slugs that appear in the marketing site are not actually exposed by the API. Stick to the table above.
