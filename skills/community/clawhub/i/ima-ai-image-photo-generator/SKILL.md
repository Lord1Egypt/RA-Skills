---
name: "IMA AI Image & Photo Generator — Poster, Thumbnail, Logo, Art, Illustration, Product & Social Media Graphic Design"
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, AI image generator, image generator, AI photo generator, product photo, poster generator, thumbnail generator, logo generator, AI art generator, illustration, graphic design, social media image, text to image, image to image
argument-hint: "[text prompt or image URL]"
description: >
  AI image generator and photo generator with SeeDream 4.5, Midjourney, Nano Banana 2, and
  Nano Banana Pro. Generate AI images for posters, thumbnails, logos, art, illustrations,
  product photos, and social media graphic design. Text-to-image and image-to-image AI
  generation with intelligent model selection and knowledge base support. AI poster generator,
  AI thumbnail generator, AI logo generator, AI art generator, AI illustration generator,
  product photo generator, and social media image generator in one unified tool. Supports
  1K/2K/4K resolution and custom aspect ratios. Better alternative to DALL-E, Stable Diffusion,
  or standalone image generation skills.
requires:
  env:
    - IMA_API_KEY
  runtime:
    - python3
  packages:
    - requests
  primaryCredential: IMA_API_KEY
metadata:
  openclaw:
    primaryEnv: IMA_API_KEY
    homepage: https://imastudio.com
    requires:
      bins:
        - python3
      env:
        - IMA_API_KEY
persistence:
  readWrite:
    - ~/.openclaw/memory/ima_prefs.json
    - ~/.openclaw/logs/ima_skills/
instructionScope:
  crossSkillReadOptional:
    - ~/.openclaw/skills/ima-knowledge-ai/references/*
---

# IMA AI Image & Photo Generator

**⚠️ MANDATORY: You MUST `read("SKILL-DETAIL.md")` (full file — do NOT pass `limit` parameter) before your first image generation call.** It contains the full API payload structure, error translation tables, upload flow, UX protocol, and FAQ that this summary omits. Skipping it causes parameter errors and poor user experience.

## Model ID Reference (CRITICAL)

Use **exact model_id**. Do NOT infer from friendly names.

| Name | model_id | Cost | Best For |
|------|----------|------|----------|
| SeeDream 4.5 🌟 | `doubao-seedream-4.5` | 5 pts | Default, product photos, posters, social media graphics |
| Midjourney 🎨 | `midjourney` | 8-10 pts | Art, illustrations, creative graphic design |
| Nano Banana2 💚 | `gemini-3.1-flash-image` | 4-13 pts | Budget thumbnails, quick social media images |
| Nano Banana Pro | `gemini-3-pro-image` | 10-18 pts | Premium 4K photos, logos, product images |

**Aliases:** 可梦/SeeDream → `doubao-seedream-4.5` · MJ/Midjourney → `midjourney` · 香蕉/Banana → `gemini-3.1-flash-image` · 香蕉Pro → `gemini-3-pro-image`

## Task Types

| User intent | task_type | Use case |
|-------------|-----------|----------|
| Text only → image | `text_to_image` | Generate poster, thumbnail, logo, art from description |
| Input image + edit | `image_to_image` | Style transfer, product photo editing, graphic design refinement |

## Visual Consistency (IMPORTANT)

For "same character" / "series" / "same product" across multiple images:
- **Do NOT use text_to_image** (produces different-looking results each time)
- Use `image_to_image` with previous result as reference
- Read `ima-knowledge-ai/references/visual-consistency.md` if available

## Knowledge Base (if ima-knowledge-ai installed)

Read before generating: `visual-consistency.md` (character/product continuity), `model-selection.md` (cost/quality), `workflow-design.md` (multi-step projects).

## Parameter Support

| Model | Aspect Ratio | Sizes | Notes |
|-------|-------------|-------|-------|
| SeeDream 4.5 | ✅ 8 ratios (1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9) | adaptive | Best value for posters & social media |
| Nano Banana2 | ✅ 5 ratios (1:1, 16:9, 9:16, 4:3, 3:4) | 512px/1K/2K/4K | Budget image & thumbnail generator |
| Nano Banana Pro | ✅ 5 ratios | 1K/2K/4K | Premium photo & logo generator |
| Midjourney 🎨 | ❌ 1:1 only | 480p/720p | Art & illustration generator |

If user asks for custom aspect ratio with Midjourney → recommend SeeDream 4.5 or Nano Banana. No model supports 8K (max 4K).

## Default Models

| Scenario | Model | model_id | Cost |
|----------|-------|----------|------|
| General image/photo | SeeDream 4.5 | `doubao-seedream-4.5` | 5 pts |
| Art/illustration | Midjourney | `midjourney` | 8-10 pts |
| Budget/fast thumbnail | Nano Banana2 | `gemini-3.1-flash-image` | 4 pts |
| Premium 4K product photo | Nano Banana Pro | `gemini-3-pro-image` | 10-18 pts |

## Model Selection Priority

1. **User preference** (if explicitly stated) → highest priority
2. **ima-knowledge-ai recommendation** (if installed)
3. **Fallback defaults** above

## Script Usage

```bash
# AI image generator — text to image (poster, thumbnail, social media graphic)
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type text_to_image \
  --model-id doubao-seedream-4.5 --prompt "product photo for social media" \
  --user-id {user_id} --output-json

# AI photo generator — image to image (product photo editing, logo refinement)
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type image_to_image \
  --model-id doubao-seedream-4.5 --prompt "enhance and refine" \
  --input-images https://example.com/photo.jpg \
  --user-id {user_id} --output-json

# List available image models
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type text_to_image --list-models
```

## Sending Results to User

```python
# ✅ CORRECT: Use remote URL directly for inline image display
message(action="send", media=image_url, caption="✅ 图片生成成功！\n• 模型：[Name]\n• 耗时：[X]s\n• 积分：[N pts]\n🔗 原始链接：[url]")

# ❌ WRONG: Never download to local file
```

## UX Protocol (Brief)

1. **Acknowledge:** Short reply ("好的！来帮你画 🎨")
2. **Pre-gen:** Model, time, cost via `message` tool
3. **Progress:** Every 15-30s: "⏳ [P]%" (cap 95%)
4. **Success:** Send `media=url` + include link in caption
5. **Failure:** Natural language + suggest alternatives
6. **Done:** No further action

**Never expose:** script names, API endpoints, attribute_id, technical params.

## User Preferences

Storage: `~/.openclaw/memory/ima_prefs.json`
- **Save** on explicit: "用XXX" / "默认用XXX" / "always use XXX"
- **Clear** on: "推荐一个" / "自动选择" / "用最好的"
- **Never save** auto-selected models

## Core Flow

1. `GET /open/v1/product/list?category=<task_type>` → `attribute_id`, `credit`, `form_config`
2. [image_to_image only] Upload local files → get CDN URL
3. `POST /open/v1/tasks/create` → `task_id`
4. `POST /open/v1/tasks/detail` → poll until `resource_status==1`

**MANDATORY:** Always query product list first. Missing `attribute_id` → task fails.

## Environment

Base URL: `https://api.imastudio.com`
Headers: `Authorization: Bearer $IMA_API_KEY` · `x-app-source: ima_skills` · `x_app_language: en`

---

**⚠️ REMINDER: `read("SKILL-DETAIL.md")` (full file, no `limit`) is required before generating images.** This summary covers model selection and routing — SKILL-DETAIL.md has complete API payloads, error handling, upload flow, parameter details, aspect ratio FAQ, and UX protocol needed for correct execution.
