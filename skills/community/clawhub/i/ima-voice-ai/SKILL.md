---
name: "IMA Music Generator"
version: 1.2.2
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, ai music, text_to_music, music generation, Suno, DouBao, GenBGM, GenSong, AI作曲, 音乐生成, BGM, 背景音乐, song generator, AI composer
argument-hint: "[music description or style]"
description: >
  Generate voiceovers, narration, and spoken audio for videos, explainers, ads, and social content.
requires:
  env:
    - IMA_API_KEY
  runtime:
    - python3
  packages:
    - requests
  primaryCredential: IMA_API_KEY
  credentialNote: "IMA_API_KEY is required at runtime and sent only to api.imastudio.com."
metadata:
  openclaw:
    primaryEnv: IMA_API_KEY
    homepage: https://www.imaclaw.ai
    requires:
      bins:
        - python3
      env:
        - IMA_API_KEY
persistence:
  readWrite: []
  retention: No local preferences or logs are written by this skill script.
---

# IMA Voice AI — Music Generator

**For complete API documentation, security details, all parameters, and Python examples, read `SKILL-DETAIL.md`.**

## Model ID Reference (CRITICAL)

Use **exact model_id** from this table. Do NOT infer from friendly names.

| Friendly Name | model_id | Notes |
|---------------|----------|-------|
| Suno | `sonic` | ✅ Default, full songs with vocals |
| DouBao BGM | `GenBGM` | ⚠️ Instrumental only, background music |
| DouBao Song | `GenSong` | ⚠️ Songs with vocals |

**User input aliases:** BGM/背景音乐/纯音乐 → `GenBGM` · 歌曲/人声/Song → `sonic` or `GenSong` · 默认 → `sonic`

## Music Generation Mode

| User intent | model_id | When to use |
|-------------|----------|-------------|
| Background music, instrumental | `GenBGM` | "做一段BGM" / "纯音乐" / "背景音乐" |
| Song with vocals | `sonic` | "写首歌" / "带人声" / "歌曲" |
| Song (alternative) | `GenSong` | "豆包歌曲" / "GenSong" |

## Model Selection Priority

1. **User preference** (if explicitly stated) → highest priority
2. **Fallback default:** `sonic` (Suno)

| Task | Default Model | model_id | Notes |
|------|--------------|----------|-------|
| General music | Suno | `sonic` | Full songs, vocals |
| Instrumental/BGM | DouBao BGM | `GenBGM` | No vocals |
| Chinese songs | DouBao Song | `GenSong` | Alternative to Suno |

## Script Usage

```bash
# Generate music (default: sonic/Suno)
python3 {baseDir}/scripts/ima_voice_create.py \
  --model-id sonic \
  --prompt "upbeat lo-fi hip hop, 90 BPM, no vocals" \
  --output-json

# List available models
python3 {baseDir}/scripts/ima_voice_create.py --list-models

# Generate BGM
python3 {baseDir}/scripts/ima_voice_create.py \
  --model-id GenBGM \
  --prompt "calm piano background music for meditation" \
  --output-json
```

## Sending Results to User

```python
# ✅ CORRECT: Use remote URL directly for inline audio display
message(action="send", media=audio_url, caption="✅ 音乐生成成功！\n• 模型：[Name]\n• 耗时：[X]s\n• 积分：[N pts]\n\n🔗 原始链接：[url]")

# ❌ WRONG: Never download to local file
```

## UX Protocol (Brief)

1. **Pre-generation:** "🎵 开始生成音乐… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"
2. **Progress:** Every 30-60s: "⏳ 正在生成中… [P]%" (cap at 95%)
3. **Success:** Send audio via `media=audio_url` + include link in caption
4. **Failure:** Natural language error + suggest alternative models. See SKILL-DETAIL.md for error translation.

**Never say to users:** script names, API endpoints, attribute_id, technical parameter names. Only: model name · time · credits · result · status.

## Environment

Base URL: `https://api.imastudio.com`
Headers: `Authorization: Bearer $IMA_API_KEY` · `x-app-source: ima_skills` · `x_app_language: en`

## Core Flow

1. `GET /open/v1/product/list?app=ima&platform=web&category=text_to_music` → get `attribute_id`, `credit`, `model_version`
2. `POST /open/v1/tasks/create` → get `task_id`
3. `POST /open/v1/tasks/detail` → poll every 5s until `resource_status==1`

**MANDATORY:** Always query product list first. `attribute_id` is required.

## Defaults and Timeouts

- Task type: `text_to_music` (fixed)
- Poll interval: 5 seconds
- Max poll wait: 8 minutes
- Default model: `sonic` (if `--model-id` omitted)

## Estimated Generation Time

| Model | Estimated Time | Poll Every |
|-------|---------------|------------|
| Suno (sonic) | 60~180s | 5s |
| DouBao BGM (GenBGM) | 30~90s | 5s |
| DouBao Song (GenSong) | 60~120s | 5s |
