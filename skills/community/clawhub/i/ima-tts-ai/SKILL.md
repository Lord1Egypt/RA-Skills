---
name: "IMA TTS Generator"
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, tts, text-to-speech, speech synthesis, voice, voiceover, narration, 语音合成, 文字转语音, IMA, TTS, AI配音, 朗读, 播报, seed-tts, seed-tts-2.0, dubbing, audiobook
argument-hint: "[text to speak or 要朗读的文本]"
description: >
  Convert text, scripts, and captions into natural voiceovers for videos, explainers, product demos,
  and social posts.
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
  retention: Logs are auto-cleaned after 7 days; preferences remain until user deletes them.
---

# IMA TTS AI — Text-to-Speech Generator

**For complete API documentation, security details, all parameters, speaker list, and Python examples, read `SKILL-DETAIL.md`.**

## Model ID Reference (CRITICAL)

| Friendly Name | model_id | Notes |
|---------------|----------|-------|
| Seed TTS 2.0 | `seed-tts-2.0` | ✅ Default and only supported model |

**Sub-models (via extra-params):**
- `seed-tts-2.0-expressive` — More expressive, emotional (default)
- `seed-tts-2.0-standard` — More stable, neutral

## When User Says "帮我制作旁白/配音"

**Must ask first:**
| Question | Parameter | Required |
|----------|-----------|----------|
| 要朗读的内容/文案 | `prompt` | ✅ Yes |

**Recommend asking:**
| Question | Parameter | Options |
|----------|-----------|---------|
| 音色/发音人 | `speaker` | 魅力苏菲、Vivi、云舟、大壹 等 (see SKILL-DETAIL.md) |

**Optional:**
| Question | Parameter | Range |
|----------|-----------|-------|
| 情感/情绪 | `audio_params.emotion` | neutral, sad, angry |
| 语速 | `audio_params.speech_rate` | [-50, 100], 0=normal |
| 音量 | `audio_params.loudness_rate` | [-50, 100], 0=normal |

## User Input Parsing

| User says | Parameter | Value |
|-----------|-----------|-------|
| 旁白/配音/朗读 | prompt + speaker | Ask for content first |
| 女声/female | speaker | e.g. `zh_female_vv_uranus_bigtts` |
| 男声/male | speaker | e.g. `zh_male_sophie_uranus_bigtts` |
| 语速快/slow | audio_params.speech_rate | Positive/negative value |
| expressive/standard | model | Sub-model selection |

## Script Usage

```bash
# List available TTS models
python3 {baseDir}/scripts/ima_tts_create.py --api-key $IMA_API_KEY --list-models

# Generate speech (default model: seed-tts-2.0)
python3 {baseDir}/scripts/ima_tts_create.py \
  --api-key $IMA_API_KEY \
  --model-id seed-tts-2.0 \
  --prompt "Text to be spoken here." \
  --user-id {user_id} \
  --output-json

# With speaker and emotion
python3 {baseDir}/scripts/ima_tts_create.py \
  --api-key $IMA_API_KEY \
  --model-id seed-tts-2.0 \
  --prompt "阳光青年音色测试，你好世界。" \
  --extra-params '{"model":"seed-tts-2.0-expressive","speaker":"zh_male_sophie_uranus_bigtts","audio_params":{"emotion":"neutral"}}' \
  --user-id {user_id} \
  --output-json
```

## Sending Results to User

```python
# ✅ CORRECT: Use remote URL directly
message(action="send", media=audio_url, caption="✅ 语音合成成功！\n• 模型：[Name]\n• 耗时：[X]s\n• 积分：[N pts]\n\n🔗 原始链接：[url]")

# ❌ WRONG: Never download to local file
```

## UX Protocol (Brief)

1. **Pre-generation:** "🔊 开始语音合成… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"
2. **Progress:** Every 10-15s: "⏳ 语音合成中… [P]%"
3. **Success:** Send audio via `media=audio_url` + include link in caption
4. **Failure:** Natural language error + suggest retry. See SKILL-DETAIL.md for error translation.

**Never say to users:** script names, API endpoints, attribute_id, technical parameter names.

## Environment

Base URL: `https://api.imastudio.com`
Headers: `Authorization: Bearer $IMA_API_KEY` · `x-app-source: ima_skills` · `x_app_language: en`

## Core Flow

1. `GET /open/v1/product/list?app=ima&platform=web&category=text_to_speech` → get `attribute_id`, `credit`
2. `POST /open/v1/tasks/create` → get `task_id`
3. `POST /open/v1/tasks/detail` → poll every 2-5s until `resource_status==1`

**MANDATORY:** Always query product list first. `attribute_id` is required.

## Estimated Generation Time

| Model | Estimated Time | Poll Every |
|-------|---------------|------------|
| seed-tts-2.0 | 5~30s | 3s |

## User Preference Memory

Storage: `~/.openclaw/memory/ima_prefs.json`
- **Save** when user explicitly says "用XXX音色" / "默认用XXX"
- **Clear** when user says "换个音色" / "推荐一个"

## Popular Speakers (Quick Reference)

| Category | Speaker Name | speaker ID |
|----------|-------------|------------|
| 通用 | 魅力苏菲 | `zh_male_sophie_uranus_bigtts` |
| 通用 | Vivi | `zh_female_vv_uranus_bigtts` |
| 通用 | 云舟 | `zh_male_m191_uranus_bigtts` |
| 视频配音 | 大壹 | `zh_male_dayi_uranus_bigtts` |
| 角色扮演 | 知性灿灿 | `zh_female_cancan_uranus_bigtts` |

**Full speaker list:** See `volcengine_tts_timbre_list.json` in project or SKILL-DETAIL.md.

**⚠️ Important:** Use native format (`*_uranus_bigtts`), NOT `BV*_streaming` format.
