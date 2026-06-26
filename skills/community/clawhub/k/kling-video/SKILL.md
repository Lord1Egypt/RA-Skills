---
name: kling-video
description: "Generate, animate, and edit AI videos using Kuaishou's Kling 3.0 and Kling Video O3 — featuring cinematic motion quality, physics simulation, reference-based generation, and natural-language video editing. Supports text-to-video, image-to-video, reference-to-video, and video editing in Pro and Standard tiers, up to 1080p resolution, 3-15 second duration, with optional synchronized sound generation. Available via Atlas Cloud API at 15% off standard pricing. Use this skill whenever the user wants to generate AI videos, create video clips, animate images, edit existing videos, produce short films, make video content, or mentions Kling, Kuaishou video, KwaiVGI, or video generation/editing. Also trigger when users ask to create product demos, marketing videos, social media reels, animated scenes, cinematic clips, talking head videos, edit video content, remove objects from video, change video backgrounds, or any video content using AI."
source: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
homepage: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
metadata:
  openclaw:
    requires:
      env:
        - ATLASCLOUD_API_KEY
    primaryEnv: ATLASCLOUD_API_KEY
---

# Kling 3.0 & O3 — AI Video Generation by Kuaishou

Generate, animate, and edit AI videos using Kuaishou's Kling 3.0 and Kling Video O3 — featuring cinematic motion quality, realistic physics simulation, reference-based generation, and natural-language video editing.

Kling 3.0 excels at creating cinematic short clips with realistic motion, complex camera movements, and faithful prompt adherence. Kling Video O3 adds MVL (Multi-modal Visual Language) technology with reference-based generation and video editing capabilities. All models support optional synchronized sound generation.

> **Data usage note**: This skill sends text prompts, image URLs, and video URLs to the Atlas Cloud API (`api.atlascloud.ai`) for video generation and editing. No data is stored locally beyond the downloaded output files. API usage incurs charges per second based on the model selected.

---

## Key Capabilities

- **Text-to-Video** — Generate video clips from text descriptions
- **Image-to-Video** — Animate still images into dynamic video with first/last frame control
- **Reference-to-Video** — Generate videos using character, prop, or scene reference images (O3)
- **Video Editing** — Natural-language video editing: remove/replace objects, change backgrounds, add effects (O3)
- **Sound Generation** — Optional synchronized sound effects and audio
- **Pro & Standard Tiers** — Pro for highest quality, Standard for cost-effective production
- **Multiple Aspect Ratios** — 16:9, 9:16, 1:1
- **Flexible Duration** — V3: 5 or 10 seconds; O3: 3-15 seconds
- **Negative Prompts** — Specify what to exclude from generated video (V3)

---

## Setup

1. Sign up at https://www.atlascloud.ai
2. Console → API Keys → Create new key
3. Set env: `export ATLASCLOUD_API_KEY="your-key"`

---

## Script Usage

This skill includes a Python script for video generation. Zero external dependencies required.

### List available video models

```bash
python scripts/generate_video.py list-models
```

### Generate a video (text-to-video)

```bash
python scripts/generate_video.py generate \
  --model "MODEL_ID" \
  --prompt "Your prompt here" \
  --output ./output \
  duration=5 resolution=720p
```

### Generate a video (image-to-video)

```bash
python scripts/generate_video.py generate \
  --model "MODEL_ID" \
  --image "https://example.com/photo.jpg" \
  --prompt "Animate this scene" \
  --output ./output
```

### Upload a local file

```bash
python scripts/generate_video.py upload ./local-file.jpg
```

Run `python scripts/generate_video.py generate --help` for all options. Extra model params can be passed as key=value (e.g. `duration=10 shot_type=multi_camera`).

---

## Pricing

All prices are per second of video generated. Atlas Cloud offers 15% off compared to standard API pricing.

### Kling V3.0

| Model | Tier | Original Price | Atlas Cloud | Best For |
|-------|------|:--------------:|:-----------:|----------|
| `kwaivgi/kling-v3.0-std/text-to-video` | Standard | ~~$0.18/s~~ | **$0.153/s** | Cost-effective text-to-video |
| `kwaivgi/kling-v3.0-std/image-to-video` | Standard | ~~$0.18/s~~ | **$0.153/s** | Cost-effective image animation |
| `kwaivgi/kling-v3.0-pro/text-to-video` | Pro | ~~$0.24/s~~ | **$0.204/s** | High-quality text-to-video |
| `kwaivgi/kling-v3.0-pro/image-to-video` | Pro | ~~$0.24/s~~ | **$0.204/s** | High-quality image animation |

### Kling Video O3 Pro

| Model | Original Price | Atlas Cloud | Best For |
|-------|:--------------:|:-----------:|----------|
| `kwaivgi/kling-video-o3-pro/text-to-video` | ~~$0.24/s~~ | **$0.204/s** | MVL-enhanced text-to-video |
| `kwaivgi/kling-video-o3-pro/image-to-video` | ~~$0.24/s~~ | **$0.204/s** | MVL-enhanced image animation |
| `kwaivgi/kling-video-o3-pro/reference-to-video` | ~~$0.24/s~~ | **$0.204/s** | Reference-based video generation |
| `kwaivgi/kling-video-o3-pro/video-edit` | ~~$0.36/s~~ | **$0.306/s** | Professional video editing |

### Kling Video O3 Standard

| Model | Original Price | Atlas Cloud | Best For |
|-------|:--------------:|:-----------:|----------|
| `kwaivgi/kling-video-o3-std/text-to-video` | - | **$0.153/s** | Cost-effective MVL text-to-video |
| `kwaivgi/kling-video-o3-std/image-to-video` | - | **$0.153/s** | Cost-effective MVL image animation |
| `kwaivgi/kling-video-o3-std/reference-to-video` | - | **$0.085/s** | Cost-effective reference-based generation |
| `kwaivgi/kling-video-o3-std/video-edit` | - | **$0.238/s** | Budget video editing |

---

## Parameters

### Kling V3.0 — Text-to-Video

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `prompt` | string | Yes | - | Video description |
| `negative_prompt` | string | No | - | What to exclude from the video |
| `duration` | integer | No | 5 | 5, 10 seconds |
| `aspect_ratio` | string | No | 16:9 | 16:9, 9:16, 1:1 |
| `cfg_scale` | number | No | 0.5 | 0-1, controls prompt adherence |
| `sound` | boolean | No | false | Generate synchronized audio |

### Kling V3.0 — Image-to-Video

Same as V3.0 text-to-video, plus:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | Yes | URL of the source image (jpg/jpeg/png, max 10MB, min 300px, aspect ratio 1:2.5 to 2.5:1) |
| `end_image` | string | No | URL of the target end frame (for guided motion) |

### Kling Video O3 — Text-to-Video

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `prompt` | string | Yes | - | Video description |
| `aspect_ratio` | string | No | 16:9 | 16:9, 9:16, 1:1 |
| `duration` | integer | No | 5 | 3-15 seconds |
| `sound` | boolean | No | false | Generate synchronized audio |

### Kling Video O3 — Image-to-Video

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Video description |
| `image` | string | Yes | - | First frame image URL |
| `end_image` | string | No | - | Last frame image URL |
| `duration` | integer | No | 5 | 3-15 seconds |
| `generate_audio` | boolean | No | false | Auto-add audio to video |

### Kling Video O3 — Reference-to-Video

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Video description |
| `images` | array | No | - | Reference images (up to 7 without video, up to 4 with video) |
| `video` | string | No | - | Reference video URL |
| `keep_original_sound` | boolean | No | true | Keep original sound from reference video |
| `sound` | boolean | No | false | Generate new audio |
| `aspect_ratio` | string | No | 16:9 | 16:9, 9:16, 1:1 |
| `duration` | integer | No | 5 | 3-15 seconds |

### Kling Video O3 — Video Editing

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Editing instruction in natural language |
| `video` | string | Yes | - | Source video URL (max 10s duration) |
| `images` | array | No | - | Reference images for element, scene, or style (max 4) |
| `keep_original_sound` | boolean | No | true | Keep original audio from the video |

---

## Workflow: Submit → Poll → Download

### Text-to-Video Example (V3.0 Pro)

```bash
# Step 1: Submit
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kwaivgi/kling-v3.0-pro/text-to-video",
    "prompt": "A golden retriever running through a sunlit meadow, camera tracking alongside, wildflowers swaying in the breeze",
    "aspect_ratio": "16:9",
    "duration": 5,
    "cfg_scale": 0.5,
    "sound": true
  }'
# Returns: { "code": 200, "data": { "id": "prediction-id" } }

# Step 2: Poll (every 5 seconds until "completed" or "succeeded")
curl -s "https://api.atlascloud.ai/api/v1/model/prediction/{prediction-id}" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY"
# Returns: { "code": 200, "data": { "status": "completed", "outputs": ["https://...video-url..."] } }

# Step 3: Download
curl -o output.mp4 "VIDEO_URL_FROM_OUTPUTS"
```

### Image-to-Video Example (V3.0 Pro)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kwaivgi/kling-v3.0-pro/image-to-video",
    "image": "https://example.com/landscape.jpg",
    "prompt": "The camera slowly pans across the landscape as clouds drift by and trees sway gently",
    "aspect_ratio": "16:9",
    "duration": 5,
    "sound": false
  }'
```

### Reference-to-Video Example (O3 Pro)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kwaivgi/kling-video-o3-pro/reference-to-video",
    "prompt": "A young woman walks through a cherry blossom garden, camera follows from behind",
    "images": ["https://example.com/character-ref.jpg"],
    "aspect_ratio": "16:9",
    "duration": 5,
    "sound": false
  }'
```

### Video Editing Example (O3 Pro)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kwaivgi/kling-video-o3-pro/video-edit",
    "video": "https://example.com/original-video.mp4",
    "prompt": "Remove the person in the background and replace with a blooming cherry tree",
    "keep_original_sound": true
  }'
```

### Standard Tier Example (Cost-Effective)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kwaivgi/kling-v3.0-std/text-to-video",
    "prompt": "Ocean waves crashing on a rocky shore at sunset, seagulls flying overhead",
    "aspect_ratio": "16:9",
    "duration": 5,
    "cfg_scale": 0.5
  }'
```

### Polling Logic

- `processing` / `starting` / `running` → wait 5s, retry (typically takes ~60-120s)
- `completed` / `succeeded` → done, get URL from `data.outputs[]`
- `failed` → error, read `data.error`

### Atlas Cloud MCP Tools (if available)

If the Atlas Cloud MCP server is configured, use built-in tools:

```
atlas_generate_video(model="kwaivgi/kling-v3.0-pro/text-to-video", params={...})
atlas_get_prediction(prediction_id="...")
```

---

## Implementation Guide

1. **Determine task type**:
   - Text-to-video: user describes a scene/action in text
   - Image-to-video: user provides an image to animate
   - Reference-to-video: user wants to generate video using character/prop/scene references
   - Video editing: user wants to modify an existing video

2. **Choose model family**:
   - **Kling V3.0** for standard text-to-video and image-to-video with negative prompts and cfg_scale control
   - **Kling Video O3** for MVL-enhanced generation, reference-based video, video editing, and longer durations (3-15s)

3. **Choose tier**:
   - **Pro** for final output, client-facing content, or quality-critical use
   - **Standard** for most production use, cost-effective generation

4. **Extract parameters**:
   - Prompt: describe scene, action, camera movement, and visual details
   - Negative prompt (V3 only): specify undesired elements (e.g., "blurry, distorted faces, watermark")
   - Aspect ratio: infer from context (social reel→9:16, YouTube→16:9, square→1:1)
   - Duration: V3 supports 5 or 10s; O3 supports 3-15s
   - cfg_scale (V3 only): 0.5 default; increase toward 1.0 for stricter prompt adherence
   - Sound: enable if user wants audio; disabled by default

5. **Execute**: POST to generateVideo API → poll result → download MP4

6. **Present result**: show file path, offer to play

## Prompt Tips

Kling produces best results with detailed, descriptive prompts:

- **Scene + Action**: "A chef flips a pancake in a busy kitchen, steam rising from the pan"
- **Camera direction**: "Camera slowly pans left to reveal...", "Close-up tracking shot of...", "Aerial view sweeping over..."
- **Style**: "cinematic", "documentary style", "slow motion", "timelapse", "anime style"
- **Negative prompts** (V3): Use to avoid common issues — "blurry, low quality, distorted, watermark, text overlay"
- **cfg_scale tuning** (V3): Lower values (0.3-0.5) give more creative freedom; higher values (0.7-1.0) follow the prompt more strictly
- **Reference-to-video** (O3): Provide clear character/prop reference images for consistent results

---

## Image Requirements for Image-to-Video

When using image-to-video models, the source image must meet these requirements:

- **Format**: JPG, JPEG, or PNG
- **Size**: Maximum 10MB
- **Dimensions**: Minimum 300px on shortest side
- **Aspect ratio**: Between 1:2.5 and 2.5:1
