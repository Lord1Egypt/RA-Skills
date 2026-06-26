---
name: "IMA AI Creative Content Generator — Image, Video, Music, Ad, Marketing, Social Media Content Creation"
version: 1.0.1
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, AI content generator, AI creative generator, AI ad generator, AI image generator, AI video generator, AI music generator, content creation, marketing content, social media generator, multimodal AI, all in one
argument-hint: "[text prompt, image URL, or music description]"
description: >
  All-in-one AI content generator for creative, marketing, and social media content creation.
  AI image generator with SeeDream 4.5, Midjourney, Nano Banana 2/Pro. AI video generator
  with Wan 2.6, Kling O1/2.6, Google Veo 3.1, Sora 2 Pro, Hailuo 2.0/2.3, Pixverse V5.5,
  SeeDance 1.5 Pro, Vidu Q2, Ima Sevio. AI music generator with Suno sonic v5 and DouBao.
  Text-to-speech/TTS with seed-tts. Unified multimodal AI content creation platform for
  ad generation, marketing content creation, social media content generation, and complete
  creative workflows. Intelligent model selection, cross-media orchestration, character
  consistency via reference images, and knowledge base guidance via ima-knowledge-ai.
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

# IMA AI Creative Content Generator

**⚠️ MANDATORY: You MUST `read("SKILL-DETAIL.md")` (full file — do NOT pass `limit` parameter) before your first content generation call.** It contains the full API payload structure, error translation tables, upload flow, and UX protocol that this summary omits. Skipping it causes parameter errors and poor user experience.

## Capabilities

All-in-one AI content generator across four media types:

| Media | Models | Content Creation Use Cases |
|-------|--------|--------------------------|
| **Image** | SeeDream 4.5, Midjourney, Nano Banana 2/Pro | Ad creatives, social media graphics, product photos, posters |
| **Video** | Wan 2.6, Kling O1/2.6, Veo 3.1, Sora 2 Pro, Hailuo 2.3/2.0, Pixverse, SeeDance, Vidu, Ima Sevio | Promo videos, short videos, marketing clips, product demos |
| **Music** | Suno sonic v5, DouBao BGM/Song | Ad jingles, background music, social media audio |
| **TTS** | seed-tts-2.0 | Voiceovers, narration, ad audio |

## Model ID Reference (CRITICAL)

Use **exact model_id**. Do NOT infer from friendly names.

### Image Models

| Name | model_id | Cost |
|------|----------|------|
| SeeDream 4.5 🌟 | `doubao-seedream-4.5` | 5 pts |
| Midjourney 🎨 | `midjourney` | 8-10 pts |
| Nano Banana2 💚 | `gemini-3.1-flash-image` | 4-13 pts |
| Nano Banana Pro | `gemini-3-pro-image` | 10-18 pts |

### Video Models

| Name | model_id (t2v / i2v) | Cost |
|------|---------------------|------|
| Wan 2.6 🔥 | `wan2.6-t2v` / `wan2.6-i2v` | 25-120 pts |
| Kling O1 | `kling-video-o1` | 48-120 pts |
| Kling 2.6 | `kling-v2-6` | 80+ pts |
| Hailuo 2.3 | `MiniMax-Hailuo-2.3` | 32+ pts |
| Hailuo 2.0 | `MiniMax-Hailuo-02` | 5+ pts |
| Veo 3.1 | `veo-3.1-generate-preview` | 70-330 pts |
| Sora 2 Pro | `sora-2-pro` | 122+ pts |
| Pixverse V5.5 | `pixverse` | 12-48 pts |
| SeeDance 1.5 Pro | `doubao-seedance-1.5-pro` | 20+ pts |
| Vidu Q2 | `viduq2` / `viduq2-pro` | 5-70 pts |
| IMA Video Pro | `ima-pro` | varies |
| IMA Video Pro Fast | `ima-pro-fast` | varies |

**Aliases:** 万/Wan→`wan2.6-*` · 可灵/Kling→`kling-video-o1` · 海螺/Hailuo→`MiniMax-Hailuo-2.3` · Veo→`veo-3.1-generate-preview`

### Music & TTS Models

| Name | model_id | Cost |
|------|----------|------|
| Suno sonic v5 | `sonic` | 25 pts |
| DouBao BGM | `GenBGM` | 30 pts |
| DouBao Song | `GenSong` | 30 pts |
| seed-tts-2.0 | `seed-tts-2.0` | query product list |

## Media Type Routing

Determine media type **first**, then choose task_type:

| User keywords | Type | task_type |
|---------------|------|-----------|
| 画/图/image/poster/thumbnail/ad graphic | image | `text_to_image`, `image_to_image` |
| 视频/video/promo/short/宣传片/clip | video | `text_to_video`, `image_to_video`, `first_last_frame_to_video`, `reference_image_to_video` |
| 音乐/BGM/music/jingle/歌 | music | `text_to_music` |
| 语音/TTS/voiceover/narration/配音 | speech | `text_to_speech` |

For multi-media (e.g. promo video + BGM), read `ima-knowledge-ai/references/workflow-design.md` first.

## Video Modes

| Intent | task_type |
|--------|-----------|
| Text only → video | `text_to_video` |
| Image as first frame | `image_to_video` |
| Image as style reference | `reference_image_to_video` |
| Two images (start+end) | `first_last_frame_to_video` |

**Visual consistency:** For "same character" / "series" / "multi-shot" — use `image_to_video` or `reference_image_to_video` with previous result as reference. Never use `text_to_video` for continuity.

## Knowledge Base (if ima-knowledge-ai installed)

Read before generating: `workflow-design.md` (multi-media), `visual-consistency.md` (character continuity), `video-modes.md` (mode differences), `model-selection.md` (cost/quality).

## Default Models

| Task | Default | model_id | Cost |
|------|---------|----------|------|
| text_to_image | SeeDream 4.5 | `doubao-seedream-4.5` | 5 pts |
| text_to_video | Wan 2.6 | `wan2.6-t2v` | 25 pts |
| image_to_video | Wan 2.6 | `wan2.6-i2v` | 25 pts |
| first_last_frame | Kling O1 | `kling-video-o1` | 48 pts |
| text_to_music | Suno | `sonic` | 25 pts |

## Script Usage

```bash
# AI image generator — ad/social media content creation
python3 {baseDir}/scripts/ima_create.py \
  --api-key $IMA_API_KEY --task-type text_to_image \
  --model-id doubao-seedream-4.5 --prompt "product photo" --output-json

# AI video generator — promo/marketing video content
python3 {baseDir}/scripts/ima_create.py \
  --api-key $IMA_API_KEY --task-type text_to_video \
  --model-id wan2.6-t2v --prompt "product promo, cinematic" --output-json

# AI music generator — ad jingle/marketing audio
python3 {baseDir}/scripts/ima_create.py \
  --api-key $IMA_API_KEY --task-type text_to_music \
  --model-id sonic --prompt "upbeat corporate BGM" --output-json

# TTS — voiceover for content creation
python3 {baseDir}/scripts/ima_create.py \
  --api-key $IMA_API_KEY --task-type text_to_speech \
  --prompt "Welcome to our product" --output-json
```

## UX Protocol (Brief)

1. **Acknowledge:** Short reply ("好的！🎨")
2. **Pre-gen:** Model, time estimate, cost via `message` tool
3. **Progress:** Every 15-60s: "⏳ [P]%" (cap 95%)
4. **Success:** Send `media=url` + link text
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
2. [Image tasks] Upload local files → get CDN URL
3. `POST /open/v1/tasks/create` → `task_id`
4. `POST /open/v1/tasks/detail` → poll until `resource_status==1`

**MANDATORY:** Always query product list first. Missing `attribute_id` → task fails.

## Environment

Base URL: `https://api.imastudio.com`
Headers: `Authorization: Bearer $IMA_API_KEY` · `x-app-source: ima_skills` · `x_app_language: en`

---

**⚠️ REMINDER: `read("SKILL-DETAIL.md")` (full file, no `limit`) is required before generating content.** This summary covers routing and model selection — SKILL-DETAIL.md has complete API payloads, error handling, upload flow, and parameter details needed for correct execution.
