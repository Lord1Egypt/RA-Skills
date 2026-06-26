---
name: pixmind-image
description: Generate or edit AI images via Pixmind API (text-to-image and image-to-image)
homepage: https://www.pixmind.io
metadata: {"openclaw": {"requires": {"env": ["PIXMIND_API_KEY"]}, "primaryEnv": "PIXMIND_API_KEY"}}
---

# Pixmind Image Generation Skill

Generate AI images using [Pixmind](https://www.pixmind.io). Supports text-to-image and image-to-image generation with multiple models.

> **Note:** The API endpoint `aihub-admin.aimix.pro` is the official Pixmind API gateway. Result URLs on `chatmix.top` are Pixmind's CDN for generated content.

## When to use

- User asks to generate, create, or draw an image
- User wants to transform or edit an existing image
- User requests image variations or upscaling

## Prerequisites

1. Register at [pixmind.io](https://www.pixmind.io/) — 注册即送 200 积分免费试用
2. Create an API key at [pixmind.io/api-keys](https://www.pixmind.io/api-keys)
3. Set env `PIXMIND_API_KEY` with your key

## API Details

**Endpoint**: `POST https://aihub-admin.aimix.pro/open-api/v1/image/generate`
**Auth**: Header `X-API-Key: {API_KEY}` (from env `PIXMIND_API_KEY`)

## Request Body (JSON)

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `prompt` | Yes | string | Image description / prompt (max 20000 chars) |
| `model` | No | string | Model ID (default: `seedream-4.0`) |
| `aspectRatio` | No | string | Aspect ratio, e.g. `1:1`, `16:9`, `9:16` (varies by model, default: `1:1`) |
| `sampleCount` | No | number | Number of images to generate (default: 1, max varies by model) |
| `speed` | No | string | Generation speed: `relax`, `fast`, `turbo` (varies by model) |
| `seed` | No | number | Seed for reproducible generation (1–2147483647, if model supports) |
| `negativePrompt` | No | string | What to avoid in the image (if model supports) |
| `stylization` | No | number | Style strength 0–1000 (default: 100, for MJ & some models) |
| `weirdness` | No | number | Weirdness/creativity 0–3000 (default: 0, for MJ & some models) |
| `variety` | No | number | Variation 0–100 (default: 0, for MJ & some models) |
| `resolution` | No | string | Resolution type: `1K`, `2K`, `3K`, `4K` (varies by model) |
| `quality` | No | string | Quality: `medium`, `high` (for GPT Image models) |
| `generateType` | No | string | `text2img` (default) or `img2img` |
| `image` | No | string | Reference image URL (required for `img2img`) |

### Available Models

| Model ID | Name | Text-to-Image | Image-to-Image | Aspect Ratios | Notes |
|----------|------|:---:|:---:|---------------|-------|
| `nano-banana-2` | Nano Banana 2 | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 21:9, 2:3, 8:1, 1:8 | 1K/2K/4K, supports seed & negative prompt |
| `nano-banana-2-eco` | Nano Banana 2 Eco | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 8:1, 1:8 | 1K/2K/4K, 80% off |
| `seedream-5.0` | Seedream 5.0 | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 | 2K/3K, supports seed |
| `wan2.7-image-pro` | Wan 2.7 Image Pro | ✓ | ✓ | 1:1, 16:9, 9:16, 3:2, 2:3 | Sample count 1–4 |
| `wan2.7-image` | Wan 2.7 Image | ✓ | ✓ | 1:1, 16:9, 9:16, 3:2, 2:3 | Sample count 1–4 |
| `qwen-image-2.0-pro` | Qwen Image 2.0 Pro | ✓ | ✗ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9 | Sample count 1–6 |
| `qwen-image-2.0` | Qwen Image 2.0 | ✓ | ✗ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9 | Sample count 1–6 |
| `flux-kontext-pro` | Flux Kontext Pro | ✓ | ✓ | 1:1, 16:9, 4:3, 9:16, 3:4, 3:2, 2:3, 21:9 | 70% off |
| `pixmind-2.0` | Pixmind 2.0 | ✓ | ✓ | 1:1, 16:9, 4:3, 9:16, 3:4, 3:2, 2:3, 21:9 | Supports relax/fast speed |
| `z-image` | Z-Image | ✓ | ✗ | 1:1, 4:3, 3:4, 16:9, 9:16 | Alibaba Tongyi Lab's 6B-parameter efficient diffusion transformer (S3-DiT), supports relax/fast, seed |
| `nano-banana-pro-lite` | Nano Banana Pro Eco | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4 | 1K/2K/4K, 70% off |
| `nano-banana` | Nano Banana | ✓ | ✓ | — | Basic Gemini generation |
| `gpt-image-1.5` | GPT Image 1.5 | ✓ | ✓ | 1:1, 2:3, 3:2 | Supports medium/high quality, 30% off |
| `seedream-4.0` | Seedream 4.0 | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 5:6, 6:5, 2:1 | 1K/2K/4K |
| `nano-banana-pro` | Nano Banana Pro | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4 | 1K/2K/4K, supports seed & negative prompt |
| `seedream-4.5` | Seedream 4.5 | ✓ | ✓ | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 5:6, 6:5, 2:1 | ByteDance flagship, cinematic aesthetics, 2K/4K |
| `gpt-image-4o` | GPT Image 4o | ✓ | ✓ | 1:1, 2:3, 3:2, 1024×1024, 1024×1536, 1536×1024 | OpenAI latest, 70% off |
| `qwen-image-edit-plus` | Qwen Image Edit Plus | ✗ | ✓ | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 | Image editing only |
| `qwen-image-max` | Qwen Image Max | ✓ | ✗ | 16:9, 4:3, 1:1, 3:4, 9:16 | Text-to-image only |
| `qwen-image-edit-max` | Qwen Image Edit Max | ✗ | ✓ | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 | Image editing only |
| `qwen-image-plus` | Qwen Image Plus | ✓ | ✗ | 16:9, 4:3, 1:1, 3:4, 9:16 | Text-to-image only |
| `mj-v7` | Midjourney V7 | ✓ | ✓ | 1:1, 9:16, 2:3, 3:4, 5:6, 6:5, 4:3, 3:2, 16:9, 2:1 | Top artistic quality, supports relax/fast/turbo, stylization, weirdness, variety |
| `wan2.6-image` | Wan 2.6 Image | ✓ | ✓ | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 | Alibaba's diffusion model, supports editing |

### Model Introductions

**Seedream (ByteDance)** — Flagship series with cinematic aesthetics and realistic textures. Unified architecture for both generation and editing. Native 4K support (4096x4096).
- `seedream-5.0` — Latest generation, 2K/3K output, supports seed for reproducibility.
- `seedream-4.5` — Previous flagship, LM Arena Top 10. 2K/4K output.
- `seedream-4.0` — Proven high quality model, good balance of quality and speed. Default model. 1K/2K/4K.

**Midjourney** — Industry-leading artistic and creative image generation.
- `mj-v7` — Latest version, top aesthetic quality. Supports speed control (relax/fast/turbo), stylization, weirdness, and variety parameters for fine-grained creative control.

**OpenAI GPT Image** — Strong instruction following, excellent text rendering in images.
- `gpt-image-4o` — Latest OpenAI model, supports medium/high quality.
- `gpt-image-1.5` — Earlier generation, still solid quality.

**Alibaba / Qwen / Wan**
- `qwen-image-2.0-pro` / `qwen-image-2.0` — Latest Qwen VL image generation. Text-to-image only, up to 6 samples per request.
- `qwen-image-max` / `qwen-image-plus` — Previous generation Qwen models, text-to-image only.
- `qwen-image-edit-max` / `qwen-image-edit-plus` — Specialized for image editing (img2img only).
- `wan2.7-image-pro` / `wan2.7-image` — Wan 2.7 series, Alibaba's latest diffusion model with editing support.
- `wan2.6-image` — Wan 2.6, high-end generation with editing support.
- `z-image` — Alibaba Tongyi Lab's open-source 6B-parameter efficient diffusion transformer (S3-DiT). Photorealistic quality with low computational cost.

**Flux (Black Forest Labs)** — Strong prompt adherence and visual fidelity.
- `flux-kontext-pro` — Balanced quality and speed.

**Nano Banana** — Lightweight models with broad aspect ratio support.
- `nano-banana-2` — Latest generation, supports seed & negative prompt, 1K/2K/4K.
- `nano-banana-2-eco` — 80% cost reduction, great for bulk generation.
- `nano-banana-pro` — Higher quality variant with seed & negative prompt support.
- `nano-banana-pro-lite` — Lighter pro version, 70% off.
- `nano-banana` — Base model, basic Gemini-powered generation.

**Pixmind Native**
- `pixmind-2.0` — Pixmind's proprietary model, supports relax/fast speed modes.

## Usage

Use `curl` or the included helper script:

```bash
# Text to image (via curl)
curl -X POST https://aihub-admin.aimix.pro/open-api/v1/image/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PIXMIND_API_KEY" \
  -d '{"prompt": "描述文字", "model": "nano-banana-2", "aspectRatio": "16:9"}'

# Or use the helper script
node {baseDir}/image-generate.js --prompt "描述文字" --model nano-banana-2 --aspect-ratio 16:9
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
{"code": 1000, "data": {"taskId": 19399, "status": "processing"}}
```

Task status response:
```json
{
  "code": 1000,
  "data": {
    "taskId": 19399,
    "status": "ready",
    "progress": 100,
    "images": ["https://chatmix.top/..."]
  }
}
```

- `data.taskId` — Use this to poll status
- Status values: `processing` → `ready` (success)
- On success: `data.images` contains generated image URLs

## Guidelines

1. Always confirm the prompt with the user before generating
2. Default to `nano-banana-2` (high quality) or `seedream-4.0` unless user specifies otherwise
3. Use `1:1` aspect ratio by default, suggest alternatives when appropriate
4. If user provides a reference image, use `img2img` mode automatically
5. After getting the task ID, poll until completion and return image URLs
6. For image editing tasks, prefer models that support `image2image`: `nano-banana-2`, `seedream-5.0`, `gpt-image-4o`, `mj-v7`, `pixmind-2.0`
7. For Midjourney V7, you can also use `stylization`, `weirdness`, and `variety` parameters
8. Check the model's supported aspect ratios before sending the request — not all models support the same ratios
