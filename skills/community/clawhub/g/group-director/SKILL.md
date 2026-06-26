---
name: group-director
description: "create short videos from claw-prepared prompts for feishu or lark group chat scenarios. use when claw already has the chat context in its own memory, has already summarized the discussion, and already has the final video prompt. this skill should not ask follow-up questions in normal group-director use, should not read chat history itself, and should call the senseaudio video api in two steps: create first, then poll by python every 30 seconds until completion. keep the model fixed to seedance-pro-1.5 with generate_audio=true. when returning to feishu, never send raw json; send a normal message and the final video url only."
---

# group-director

Use this skill only as a **video execution layer** for Feishu/Lark group-chat video generation.

## Hard rules

- Assume Claw already has enough context from its own memory and recent reading.
- Do not ask extra questions in normal group-director use.
- Do not ask the user to repeat or recap the group chat.
- Do not read Feishu/Lark history inside this skill.
- Do not summarize group chat inside this skill.
- Treat `final_video_prompt` as already finalized by Claw.
- Use exactly two steps:
  1. create the task
  2. poll by Python every 30 seconds until it finishes
- Keep the model fixed to `Seedance-Pro-1.5`.
- Always set `provider_specific.generate_audio=true`.
- Never send raw JSON back to Feishu.
- When the task finishes successfully, send only a normal natural-language message plus the final `video_url`.
- Do not send debug objects, raw provider payloads, or JSON-looking blocks to Feishu.

## What Claw is responsible for

Claw is responsible for:
- reading the group context
- using its own memory and recent context
- summarizing the discussion when needed
- turning that into the final video prompt
- calling this skill
- sending the final natural-language message back to Feishu/Lark

## What this skill is responsible for

This skill is responsible only for:
- creating the video task
- polling status until completion, failure, or timeout
- returning the final video URL or a plain-text failure message

## Fixed defaults

- model: `Seedance-Pro-1.5`
- duration: `12`
- resolution: `720p`
- allowed orientation: `portrait` or `landscape`
- poll interval: `30` seconds
- timeout: `600` seconds
- audio generation: always enabled

Do not expose square mode.
Do not let the model vary.
Do not omit `generate_audio`.

## Input expected from Claw

Required:
- `final_video_prompt`

Optional:
- `orientation`

If orientation is missing, default to `portrait`.
If orientation is present, it must be `portrait` or `landscape`.

## Calling pattern

### Step 1: create task

```bash
python3 scripts/main.py video-create \
  --final-video-prompt "这里放 Claw 已整理好的最终视频提示词" \
  --orientation portrait
```

This returns only the `task_id` as plain text.

### Step 2: poll by Python until done

```bash
python3 scripts/main.py video-poll --task-id "task_xxx"
```

This polls every 30 seconds until one of these happens:
- completed -> prints only the final `video_url`
- failed -> prints a plain-text failure message
- timeout -> prints a plain-text timeout message

## Feishu return rule

When Claw sends the result back to Feishu/Lark:
- use a normal message
- include the final `video_url`
- do not include raw JSON
- do not include provider payloads
- do not paste structured blobs

Good style:

```text
视频生成好了：
https://...
```

Bad style:

```text
{"status":"completed","task_id":"...","video_url":"https://..."}
```

## Environment variable

Only this variable is required:

```bash
export SENSEAUDIO_API_KEY="your_key"
```

Optional:

```bash
export SENSEAUDIO_BASE_URL="https://api.senseaudio.cn"
```

## Resource layout

- `scripts/main.py`: CLI entrypoint with plain-text outputs
- `scripts/video_api.py`: provider wrapper for create, status, and polling
- `references/provider_notes.md`: fixed model and parameter notes
- `references/integration_cn.md`: Chinese integration rules for Claw
