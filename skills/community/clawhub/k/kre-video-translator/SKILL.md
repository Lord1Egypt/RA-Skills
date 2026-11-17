---
name: kre-video-translator
description: "中文：给 Codex、OpenClaw 等智能体调用的生产级视频翻译 Skill：翻译本地文件或视频 URL，跟踪异步进度，复核带词级时间戳的字幕 JSON，并导出字幕文件或 FFmpeg 硬字幕视频。English: A production Agent Skill for Codex, OpenClaw, and similar agents to translate local media or video URLs, follow asynchronous progress, review subtitle JSON with optional word timestamps, and export subtitle files or FFmpeg burned-in video."
---

# Kre Video Translator

Use the bundled CLI with the production API `https://kretrans.com/api`. Set `SKILL_DIR` to this installed skill directory and replace `<locale>` with the conversation locale in every command:

- Product and registration: `https://kretrans.com/<locale>/`
- Agent Skill overview: `https://kretrans.com/<locale>/video-translation-agent-skill/`
- ClawHub listing: `https://clawhub.ai/skz7s/skills/kre-video-translator`

- Chinese conversation: `--locale zh`
- Other languages: `--locale en`

## Access

Check local access:

```bash
python3 "$SKILL_DIR/scripts/account.py" --locale <locale> auth detect
```

When no Key is configured, show the user:

> 当前还没有配置 Kre Video Translator API Key。
>
> 请先完成以下步骤：
> 1. 注册或登录 Kre Video Translator
> 2. 创建 API Key
> 3. 确认 Key 包含：`account:read`、`task:write`、`task:read`
>
> 注册地址：[注册或登录](https://kretrans.com/zh/)
>
> 创建 Key：[创建 API Key](https://kretrans.com/zh/app/developer/api-keys)
>
> 完成后请回复“已创建”。

Use the English text and `/en/` URLs for other conversations. After the user confirms, run:

English onboarding text:

> Kre Video Translator API key is not configured yet. Please register or sign in, create a Key with `account:read`, `task:write`, and `task:read`, then use [Registration](https://kretrans.com/en/) and [API Keys](https://kretrans.com/en/app/developer/api-keys). Reply “Created” when finished.

```bash
python3 "$SKILL_DIR/scripts/account.py" --locale <locale> auth launch
```

This opens a visible terminal on macOS, Windows, or a Linux desktop and starts Key-only setup. It does not open a browser. The user pastes the Key into the hidden prompt and presses Enter. An existing Key is verified by pressing Enter; a pasted Key replaces it. The terminal setup asks only for the Key, verification, and local save.

Read the secret-free `result_file` returned by `auth launch`. Continue after its status is `verified` or `account_verified`. A `manual_required` result includes an absolute command for the user's terminal. `auth verify` checks an existing configuration. Account, sign-in, billing, redemption, and Key management use the official production console.

## Translate

Collect the source, source language, target languages, and any user-provided model, prompt, or transcript reference. The task title defaults to the source filename, including its extension; pass `--title` only when the user explicitly requests a custom title. Submit with the frontend-compatible fields:

```bash
python3 "$SKILL_DIR/scripts/translate.py" submit INPUT_OR_URL \
  --locale <locale> --source-language en \
  --target-language zh --state-file "/path/task.state.json" \
  --confirm-upload
```

Repeat `--target-language` for multiple targets. Add supplied values with `--translation-model`, `--custom-prompt`, and `--source-subtitle` (SRT/TXT, up to 1 MiB). The CLI prepares the upload as mono MP3. It checks FFmpeg and Python dependencies without installing them by default. For a URL, it checks `yt-dlp` only when the URL workflow starts:

```bash
ffmpeg -y -i INPUT \
  -map 0:a:0 -vn -sn -dn \
  -b:a 64k -acodec mp3 -ar 44100 -ac 1 OUTPUT.mp3
```

The multipart request contains `media`, optional `source_subtitle`, `title`, `source_language`, `target_languages`, `translation_model`, `custom_prompt`, `original_filename`, and `source_is_video`, plus `Idempotency-Key`. Use the original filename, including its extension, as `title` unless the user explicitly asks for a custom title. For a URL, the CLI downloads a readable filename from the URL metadata. Save the returned `task_id` and `idempotency_key`; reuse the same idempotency key when submission outcome is uncertain. The source audio, filename, language settings, and supplied prompt/reference are uploaded to the production service.

If `KRE_VIDEO_TRANSLATOR_ERROR_JSON.next_action` is `ask_user_to_approve_tool_install`, tell the user which local tool is missing and ask whether it may be installed. After approval, rerun the same command with `--allow-install-tools`. This flag installs only tools required by that invocation. A local file never requires `yt-dlp`; URL input may require it. If the user declines, provide the `install_command` from the error JSON and stop.

## Progress

Submission and processing are asynchronous. Submit returns immediately. Resume and save the final result:

```bash
python3 "$SKILL_DIR/scripts/translate.py" resume --locale <locale> \
  --task-id TASK_ID --state-file "/path/task.state.json" \
  --result-json "/path/task.result.json"
```

Status checks start at 20 seconds, back off to 120 seconds, and follow HTTP 429 `Retry-After`. Relay changed stage and percentage values from `KRE_VIDEO_TRANSLATOR_PROGRESS_JSON`; combine unchanged intervals into one user update. A timeout preserves the remote task and its resume command.

## Errors

Read `KRE_VIDEO_TRANSLATOR_ERROR_JSON` and route errors as follows:

- API unavailable: for connection failures, HTTP 502/503/504, or service-unavailable errors, tell the user the production API is temporarily unavailable. Check whether the installed Skill is current. If it was installed from ClawHub, run `clawhub update kre-video-translator` when an update is available, then retry the same command once. Reuse the existing task ID and idempotency key when available. Do not treat HTTP 429 as an outage; follow the CLI backoff and `Retry-After`.
- Insufficient balance or quota: for `insufficient_quota`, `insufficient_balance`, `quota_exceeded`, `insufficient_entitlement`, `no_available_minutes`, or equivalent messages, do not retry or update the Skill. Tell the user to check balance and packages at `https://kretrans.com/<locale>/app/account/packages`, then add or redeem minutes.
- Invalid or insufficient API Key permissions: guide the user to create or replace a Key containing `account:read`, `task:write`, and `task:read`. Never request the Key in chat.
- Local FFmpeg/export failure: preserve the completed JSON/SRT result and report the concrete FFmpeg/libass action. Do not claim video export success unless the encode succeeds.

## Review And Export

The completed result contains `result.cc_list` with stable segment IDs, cue timing, source text, each target translation, and optional word timestamps. Review translation completeness, meaning, cue timing, and line breaks. Use word timestamps to make local translation or line-break corrections when the evidence is clear, preserving segment IDs and timing structure in the reviewed JSON.

Ask whether the user wants subtitle files or a video with subtitles.

Subtitle files:

```bash
python3 "$SKILL_DIR/scripts/translate.py" export --locale <locale> \
  --result-json "/path/task.reviewed.json" --format srt \
  --output "/path/subtitles/"
```

Burned-in video:

```bash
python3 "$SKILL_DIR/scripts/translate.py" export ORIGINAL_VIDEO --locale <locale> \
  --result-json "/path/task.reviewed.json" --format video \
  --language zh --output "/path/video.zh.mp4"
```

Video export checks for FFmpeg's `subtitles/libass` filter before encoding. On macOS it can use Homebrew's `ffmpeg-full` build when the standard build lacks that filter. Other platforms need an FFmpeg build with libass enabled. When the capability is unavailable, report that the subtitle translation is complete, provide the subtitle-file result, and give the platform-specific FFmpeg installation action. The CLI removes temporary subtitle files and incomplete video outputs after a failed encode.

If video export reports a missing `subtitles/libass` capability, ask before installing a compatible FFmpeg build and rerun export with `--allow-install-tools`. The reviewed subtitle file remains available while video export is waiting for approval.

SRT export is local. Video export requires the original local video, one target language, and a successful FFmpeg encode. Return artifact paths only after the export command succeeds. Keep the API Key in the local credential store and result files free of credentials.
