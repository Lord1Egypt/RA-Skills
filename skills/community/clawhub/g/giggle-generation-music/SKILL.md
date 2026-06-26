---
name: giggle-generation-music
description: "Use when the user wants to create, generate, or compose music—whether from text description, custom lyrics, or instrumental background music. Triggers: generate music, write a song, compose, create music, AI music, background music, instrumental, beats."
version: "0.0.10"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  openclaw:
    emoji: "📂"
    requires:
      bins: [python3]
      env: [GIGGLE_API_KEY]
      pip: [requests]
    primaryEnv: GIGGLE_API_KEY
---

[简体中文](./SKILL.zh-CN.md) | English

# Giggle Music

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · API: [giggle.pro](https://giggle.pro/)

Generates AI music via giggle.pro. Supports simplified and custom modes. Submit task → query when ready. No polling or Cron.

**API Key**: Set system environment variable `GIGGLE_API_KEY`. Log in to [Giggle.pro](https://giggle.pro/) and obtain the API Key from account settings.

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

---

## Interaction Guide

### Mode Selection (priority: high to low)

| User input | Mode | Description |
|------------|------|-------------|
| User provides full **lyrics** | Custom mode (B) | Must be lyrics, not description |
| User requests instrumental/background music | Instrumental mode (C) | No vocals |
| Other cases (description, style, vocals, etc.) | **Simplified mode (A)** | Use user description as prompt; AI composes |

> **Key rule**: If the user does not provide lyrics, always use **simplified mode A**. Use the user's description exactly as `--prompt`; **do not add or rewrite**. E.g. user says "female voice, 1 min, ancient romance", use `--prompt "female voice, 1 min, ancient romance"` directly.

### Guidance when info is lacking

Only when the user input is very vague (e.g. "generate music" with no description), ask:

```
Question: "What type of music would you like to generate?"
Options: AI compose (describe style) / Use my lyrics / Instrumental
```

---

## Execution Flow: Submit and Query

Music generation is asynchronous (typically 1–3 minutes). **Submit** a task to get `task_id`, then **query** when the user wants to check status.

---

### Step 1: Submit Task

**First send a message to the user**: "Music generation submitted. Usually takes 1–3 minutes. You can ask me about the progress anytime."

#### A: Simplified Mode
```bash
python3 scripts/giggle_music_api.py --prompt "user description"
```

#### B: Custom Mode
```bash
python3 scripts/giggle_music_api.py --custom \
  --prompt "lyrics content" \
  --style "pop, ballad" \
  --title "Song Title" \
  --vocal-gender female
```

#### C: Instrumental
```bash
python3 scripts/giggle_music_api.py --prompt "user description" --instrumental
```

Response example:
```json
{"status": "started", "task_id": "xxx"}
```

**Store task_id in memory** (`addMemory`):
```
giggle-generation-music task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### Step 2: Query When User Asks

When the user asks about music progress (e.g. "is my music ready?", "progress?"), run:

```bash
python3 scripts/giggle_music_api.py --query --task-id <task_id>
```

**Output handling**:

| stdout pattern | Action |
|----------------|--------|
| Plain text with music links (🎶 音乐已就绪) | Forward to user as-is |
| Plain text with error | Forward to user as-is |
| JSON `{"status": "processing", "task_id": "..."}` | Tell user "Still in progress, please ask again in a moment" |

**Link return rule**: Audio links in stdout must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). Correct: `https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...`. Keep as-is when forwarding.

---

## Recovery

When the user asks about previous music progress:

1. **task_id in memory** → Run `--query --task-id xxx` directly. **Do not resubmit**
2. **No task_id in memory** → Tell the user, ask if they want to regenerate

---

## Parameter Reference

| Parameter | Description |
|-----------|-------------|
| `--prompt` | Music description or lyrics (required in simplified mode) |
| `--custom` | Enable custom mode |
| `--style` | Music style (required in custom mode) |
| `--title` | Song title (required in custom mode) |
| `--instrumental` | Generate instrumental |
| `--vocal-gender` | Vocal gender: male / female (custom mode only) |
| `--query` | Query task status |
| `--task-id` | Task ID (use with --query) |
