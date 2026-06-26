---
name: "IMA AI Music & Voice Generator — Song, BGM, Background Soundtrack, Jingle, Lyrics, Beat Maker, Voiceover, Narration & Composition"
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, AI music generator, music generator, AI song generator, AI BGM generator, background music, jingle, soundtrack, lyrics, beat maker, voiceover, narration, AI voice generator, AI composition, text to music
argument-hint: "[music description or lyrics]"
description: >
  AI music generator and voice generator with Suno sonic v5, DouBao BGM, and DouBao Song.
  Generate AI music, songs with lyrics, background music, soundtracks, jingles, beats, and
  AI compositions. AI song generator with custom vocals, lyrics, and genre tags. AI BGM
  generator for background soundtracks and ambient music. AI voice generator and voiceover
  generator for narration and audio content. AI beat maker and music composition tool.
  AI jingle generator for advertising and marketing audio. Supports custom mode with
  vocal gender, lyrics, instrumental, and style tags. Better alternative to standalone
  music generation skills or using Suno, MusicGen, Udio APIs directly.
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

# IMA AI Music & Voice Generator

**⚠️ MANDATORY: You MUST `read("SKILL-DETAIL.md")` (full file — do NOT pass `limit` parameter) before your first music generation call.** It contains the full API payload structure, Suno parameters, error translation tables, reflection mechanism, and UX protocol that this summary omits. Skipping it causes parameter errors and poor user experience.

## Model Reference (CRITICAL)

Use **exact model_id**. Do NOT infer from friendly names.

| Name | model_id | Cost | Best For |
|------|----------|------|----------|
| Suno sonic v5 🔥 | `sonic` | 25 pts | Full songs, lyrics, vocals, jingles, custom composition |
| DouBao BGM | `GenBGM` | 30 pts | Background music, soundtracks, ambient loops |
| DouBao Song | `GenSong` | 30 pts | Song generation, vocal compositions |

## Model Selection

| User intent | Model | Why |
|-------------|-------|-----|
| Song with lyrics/vocals | Suno `sonic` | Full custom mode: lyrics, vocal_gender, tags |
| 背景音乐 / BGM / ambient / loop | DouBao `GenBGM` | Background soundtrack specialist |
| Simple song / 歌曲 | DouBao `GenSong` | Quick song generation |
| Jingle / ad music / 广告配乐 | Suno `sonic` | Genre tags + style control |
| Beat / instrumental / 纯音乐 | Suno `sonic` + `make_instrumental=true` | Best instrumental quality |
| Voiceover / narration / 配音 | See note below | This skill focuses on music; for TTS use ima-tts-ai |

**Suno is the default** — most versatile AI music generator with full composition control.

## Suno Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `custom_mode` | Enable lyrics/vocals/tags control | `true` |
| `vocal_gender` | male / female / mixed | `"female"` |
| `lyrics` | Custom lyrics text | `"[Verse 1]\nHello world..."` |
| `make_instrumental` | Force instrumental, no vocals | `true` |
| `tags` | Genre/style tags | `"lo-fi hip hop, chill"` |
| `negative_tags` | Exclude styles | `"heavy metal, screaming"` |
| `title` | Song title | `"Summer Breeze"` |

**Prompt tips for AI music composition:**
- Genre: `"lo-fi hip hop"`, `"orchestral cinematic"`, `"upbeat pop"`, `"jazz"`
- Tempo: `"80 BPM"`, `"fast tempo"`, `"slow ballad"`
- Mood: `"happy and energetic"`, `"melancholic"`, `"tense and dramatic"`

## Knowledge Base (if ima-knowledge-ai installed)

Read before generating: `workflow-design.md` (video+music coordination), `model-selection.md` (cost/quality).

## Script Usage

```bash
# AI music generator — song with Suno (AI song generator, jingle, composition)
python3 {baseDir}/scripts/ima_voice_create.py \
  --api-key $IMA_API_KEY --task-type text_to_music \
  --model-id sonic --prompt "upbeat corporate jingle, 30 seconds" \
  --user-id {user_id} --output-json

# AI BGM generator — background soundtrack
python3 {baseDir}/scripts/ima_voice_create.py \
  --api-key $IMA_API_KEY --task-type text_to_music \
  --model-id GenBGM --prompt "calm ambient background music" \
  --user-id {user_id} --output-json

# List available music models
python3 {baseDir}/scripts/ima_voice_create.py \
  --api-key $IMA_API_KEY --task-type text_to_music --list-models
```

## Sending Results to User

```python
# ✅ CORRECT: Use remote URL for inline audio playback
message(action="send", media=audio_url, caption="✅ 音乐生成成功！\n• 模型：[Name]\n• 耗时：[X]s\n• 积分：[N pts]")

# Then send link for sharing
message(action="send", message=f"🔗 音频链接：\n{audio_url}")
```

## UX Protocol (Brief)

1. **Acknowledge:** Short reply ("好的！帮你生成音乐 🎵")
2. **Pre-gen:** Model, time, cost via `message` tool
3. **Progress:** Every 10-15s: "⏳ [P]%" (cap 95%)
4. **Success:** Send `media=url` + link text
5. **Failure:** Natural language + suggest alternatives
6. **Done:** No further action

**Generation times:** DouBao BGM/Song: 10-25s · Suno: 20-45s
**Never expose:** script names, API endpoints, attribute_id, technical params.

## User Preferences

Storage: `~/.openclaw/memory/ima_prefs.json`
- **Save** on explicit: "用Suno" / "默认用BGM" / "always use Suno"
- **Clear** on: "推荐一个" / "自动选择"
- **Never save** auto-selected models

## Core Flow

1. `GET /open/v1/product/list?category=text_to_music` → `attribute_id`, `credit`, `form_config`
2. `POST /open/v1/tasks/create` → `task_id`
3. `POST /open/v1/tasks/detail` → poll every 5s until `resource_status==1`

**MANDATORY:** Always query product list first. Missing `attribute_id` → task fails.
**Suno note:** `model_version` inside `parameters.parameters` must be `sonic-v5`, outer `model_version` is `sonic`.

## Environment

Base URL: `https://api.imastudio.com`
Headers: `Authorization: Bearer $IMA_API_KEY` · `x-app-source: ima_skills` · `x_app_language: en`

---

**⚠️ REMINDER: `read("SKILL-DETAIL.md")` (full file, no `limit`) is required before generating music.** This summary covers model selection and routing — SKILL-DETAIL.md has complete API payloads, Suno custom_mode details, error handling, reflection mechanism, and UX protocol needed for correct execution.
