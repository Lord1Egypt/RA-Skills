---
name: giggle-generation-image
description: "Supports text-to-image and image-to-image. Use when the user needs to create or generate images. Use cases: (1) Generate from text description, (2) Use reference images, (3) Customize model, aspect ratio, resolution. Triggers: generate image, draw, create image, AI art."
version: "0.0.10"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📂",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "GIGGLE_API_KEY"
    }
  }
---

[简体中文](./SKILL.zh-CN.md) | English

# Giggle Image Generation (Multi-Model)

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · API: [giggle.pro](https://giggle.pro/)

Generates AI images via giggle.pro's Generation API. Supports multiple models (Seedream, Midjourney, Nano Banana). Submit task → query when ready. No polling or Cron.

**API Key**: Set system environment variable `GIGGLE_API_KEY`. The script will prompt if not configured.

> **No inline Python**: All commands must be executed via the `exec` tool. **Never** use `python3 << 'EOF'` or heredoc inline code.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

## Supported Models

| Model | Description |
|-------|-------------|
| seedream45 | Seedream, realistic and creative |
| midjourney | Midjourney style |
| nano-banana-2 | Nano Banana 2 |
| nano-banana-2-fast | Nano Banana 2 fast |

---

## Execution Flow: Submit and Query

Image generation is asynchronous (typically 30–120 seconds). **Submit** a task to get `task_id`, then **query** when the user wants to check status.

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

---

### Step 1: Submit Task

```bash
# Text-to-image (default seedream45)
python3 scripts/generation_api.py \
  --prompt "description" --aspect-ratio 16:9 \
  --model seedream45 --resolution 2K \
  --no-wait --json

# Text-to-image - Midjourney
python3 scripts/generation_api.py \
  --prompt "description" --model midjourney \
  --aspect-ratio 16:9 --resolution 2K \
  --no-wait --json

# Image-to-image - Reference URL
python3 scripts/generation_api.py \
  --prompt "Convert to oil painting style, keep composition" \
  --reference-images "https://example.com/photo.jpg" \
  --model nano-banana-2-fast \
  --no-wait --json

# Batch generate multiple images
python3 scripts/generation_api.py \
  --prompt "description" --generate-count 4 \
  --no-wait --json
```

Response example:
```json
{"status": "started", "task_id": "xxx"}
```

**Store task_id in memory** (`addMemory`):
```
giggle-generation-image task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

**Tell the user**: "Image generation started. It usually takes 30–120 seconds. You can ask me 'is it ready?' to check the status."

---

### Step 2: Query Task (when user asks for status)

```bash
python3 scripts/generation_api.py --query --task-id <task_id>
```

**Behavior**:
- **completed**: Output image links for user
- **failed/error**: Output error message
- **processing/pending**: Output JSON `{"status": "...", "task_id": "xxx"}`; user can query again later

---

## New Request vs Query Old Task

**When the user initiates a new image generation request**, run submit to create a new task. Do not reuse old task_id from memory.

**When the user asks about a previous task's progress** (e.g. "is it ready?", "check status"), query the task_id from memory.

---

## Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--prompt` | required | Image description prompt |
| `--model` | seedream45 | seedream45, midjourney, nano-banana-2, nano-banana-2-fast |
| `--aspect-ratio` | 16:9 | 16:9, 9:16, 1:1, 3:4, 4:3, 2:3, 3:2, 21:9 |
| `--resolution` | 2K | Text-to-image: 1K, 2K, 4K (image-to-image partially supported) |
| `--generate-count` | 1 | Number of images to generate |
| `--reference-images` | - | Image-to-image reference; supports URL, base64, asset_id |
| `--watermark` | false | Add watermark (image-to-image) |

---

## Image-to-Image Reference: Three Input Methods

The image-to-image API's `reference_images` is an array of objects. Each element can be one of these three formats (can be mixed):

### Method 1: URL

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "url": "https://assets.giggle.pro/private/example/image.jpg?Policy=EXAMPLE_POLICY&Key-Pair-Id=EXAMPLE_KEY_PAIR_ID&Signature=EXAMPLE_SIGNATURE"
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

### Method 2: Base64

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

> Base64 format: Pass the raw Base64 string directly. Do not add the `data:image/xxx;base64,` prefix.

### Method 3: asset_id

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "asset_id": "vvsdsfsdf"
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

> For multiple reference images, add more objects to the `reference_images` array.

---

## Interaction Guide

**When the user request is vague, guide per the steps below. If the user has provided enough info, run the command directly.**

### Step 1: Model Selection

```
Question: "Which model would you like to use?"
Title: "Image Model"
Options:
- "seedream45 - Realistic & creative (recommended)"
- "midjourney - Artistic style"
- "nano-banana-2 - High quality"
- "nano-banana-2-fast - Fast generation"
multiSelect: false
```

### Step 2: Aspect Ratio

```
Question: "What aspect ratio do you need?"
Title: "Aspect Ratio"
Options:
- "16:9 - Landscape (wallpaper/cover) (recommended)"
- "9:16 - Portrait (mobile)"
- "1:1 - Square"
- "Other ratios"
multiSelect: false
```

### Step 3: Generation Mode

```
Question: "Do you need reference images?"
Title: "Generation Mode"
Options:
- "No - Text-to-image only"
- "Yes - Image-to-image (style transfer)"
multiSelect: false
```

### Step 4: Execute and Display

Submit task → store task_id → inform user. When user asks for status, run query and forward stdout to user.

**Link return rule**: Image links in results must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). Correct: `https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...`. Wrong: do not return unsigned URLs with only the base path (no query params).
