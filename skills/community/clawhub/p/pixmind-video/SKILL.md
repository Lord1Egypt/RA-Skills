---
name: pixmind-video
description: Generate AI videos via Pixmind API (text-to-video and image-to-video)
homepage: https://www.pixmind.io
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
2. Create an API key at [pixmind.io/api-keys](https://www.pixmind.io/api-keys)
3. Set env `PIXMIND_API_KEY` with your key

## API Details

**Endpoint**: `POST https://aihub-admin.aimix.pro/open-api/v1/video/generate`
**Auth**: Header `X-API-Key: {API_KEY}` (from env `PIXMIND_API_KEY`)

## Request Body (JSON)

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `prompt` | Yes | string | Video description / prompt |
| `model` | No | string | Model ID (default varies) |
| `duration` | No | number | Video duration in seconds |
| `aspectRatio` | No | string | Aspect ratio: `16:9`, `9:16`, `1:1` |
| `resolution` | No | string | Resolution: `1080p`, `720p` |
| `generateType` | No | string | `text2video` (default) or `img2video` |
| `imageUrl` | No | string | Reference image URL (required for `img2video`) |

### Available Models

| Model ID | Name | Text-to-Video | Image-to-Video | Notes |
|----------|------|:---:|:---:|-------|
| `seedance-1.5-pro` | Seedance 1.5 Pro | ✓ | ✓ | Latest ByteDance flagship video model |
| `seedance-1.5` | Seedance 1.5 | ✓ | ✓ | ByteDance Seedance 1.5 standard |
| `seedance-1.5-lite` | Seedance 1.5 Lite | ✓ | ✓ | Lightweight variant |
| `seedance-1.5-turbo` | Seedance 1.5 Turbo | ✓ | ✓ | Fast generation variant |
| `seedance-1.0-pro` | Seedance 1.0 Pro | ✓ | ✓ | Previous generation, high quality |
| `seedance-1.0` | Seedance 1.0 | ✓ | ✓ | Previous generation standard |
| `seedance-1.0-lite` | Seedance 1.0 Lite | ✓ | ✓ | Economy variant |
| `veo-3.0` | Veo 3.0 | ✓ | ✓ | Google Veo 3.0 |
| `veo-3` | Veo 3 | ✓ | ✓ | Google Veo 3 |
| `veo-3.0-fast` | Veo 3.0 Fast | ✓ | ✓ | Fast variant of Veo 3.0 |
| `veo-2` | Veo 2 | ✓ | ✓ | Google Veo 2 |
| `sora-2` | Sora 2 | ✓ | ✓ | OpenAI Sora 2 |
| `pixverse-4.0` | Pixverse 4.0 | ✓ | ✓ | Latest Pixverse model |
| `pixverse-3.0` | Pixverse 3.0 | ✓ | ✓ | Pixverse 3.0 |
| `pixverse-2.0` | Pixverse 2.0 | ✓ | ✓ | Pixverse 2.0 |
| `pixverse-1.0` | Pixverse 1.0 | ✓ | ✓ | Pixverse 1.0 |
| `pixverse-video` | Pixverse Video | ✓ | ✓ | Pixverse default |
| `kling-v1.6` | Kling 1.6 | ✓ | ✓ | Kuaishou Kling v1.6 |
| `kling-v1.5` | Kling 1.5 | ✓ | ✓ | Kuaishou Kling v1.5 |
| `kling-std-1.6` | Kling 1.6 Standard | ✓ | ✓ | Standard quality |
| `minimax-t2v-01` | MiniMax T2V 01 | ✓ | ✗ | MiniMax text-to-video |
| `minimax-t2v-01-live` | MiniMax T2V 01 Live | ✓ | ✗ | MiniMax live mode |
| `wan2.1-t2v` | Wan 2.1 T2V | ✓ | ✗ | Alibaba Wan 2.1 text-to-video |

### Model Introductions

**Seedance (ByteDance)** — Flagship video generation series. Known for smooth motion, realistic physics, and high visual fidelity.
- `seedance-1.5-pro` — Latest and highest quality. Best for professional-grade video production.
- `seedance-1.5` / `seedance-1.5-lite` / `seedance-1.5-turbo` — Quality, cost, and speed tradeoffs within the 1.5 generation.
- `seedance-1.0` series — Previous generation, still capable for general use.

**Google Veo** — Google's state-of-the-art video generation models.
- `veo-3.0` / `veo-3` — Latest Veo 3 series with highest realism and instruction following.
- `veo-3.0-fast` — Faster generation with slightly reduced quality.
- `veo-2` — Previous generation, reliable quality.

**OpenAI Sora** — OpenAI's video generation model.
- `sora-2` — Latest Sora version, strong at complex scenes and physical accuracy.

**Pixverse** — Specialized creative video model with strong artistic style.
- `pixverse-4.0` — Latest version with best quality and style control.
- `pixverse-3.0` / `2.0` / `1.0` — Previous generations.

**Kling (Kuaishou)** — Chinese video generation platform with strong performance.
- `kling-v1.6` — Latest version with improved motion and consistency.
- `kling-v1.5` — Previous stable version.
- `kling-std-1.6` — Standard quality variant for cost efficiency.

**MiniMax** — Efficient text-to-video generation.
- `minimax-t2v-01` — Base model, text-to-video only.
- `minimax-t2v-01-live` — Optimized for real-time or near-real-time generation.

**Wan (Alibaba)** — Alibaba's video generation diffusion model.
- `wan2.1-t2v` — Text-to-video model with good visual quality.

## Usage

Use `curl` or the included helper script:

```bash
# Text to video (via curl)
curl -X POST https://aihub-admin.aimix.pro/open-api/v1/video/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PIXMIND_API_KEY" \
  -d '{"prompt": "ocean waves", "duration": 5, "aspectRatio": "16:9"}'

# Or use the helper script
node {baseDir}/video-generate.js --prompt "描述文字" --duration 5 --aspect-ratio 16:9
```

## Task Status Polling

After generation, poll for results:

```bash
# Via curl
curl https://aihub-admin.aimix.pro/open-api/v1/task/<TASK_ID> \
  -H "X-API-Key: $PIXMIND_API_KEY"

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

## Guidelines

1. Always confirm the prompt and duration with the user before generating
2. Default to `seedance-1.5` or `sora-2` unless user specifies otherwise
3. Use `16:9` aspect ratio by default for video content
4. If user provides a reference image, automatically use `img2video` mode
5. Video generation takes longer than images — use `--poll` with appropriate interval (recommend 5–10s)
6. After getting the task ID, poll until completion and return video URL
7. For longer videos, consider `seedance-1.5-lite` or `kling-std-1.6` for faster results
