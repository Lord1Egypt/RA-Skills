---
name: pixmind-video-to-prompt
description: Extract a SaaS-style storyboard with local reference frames, timestamps, scripts, scene descriptions, and recreation prompts from one local video or remote URL. Use for video breakdowns, shot lists, storyboard tables, scene prompts, visual recreation, and reverse-engineering video structure.
metadata: {"openclaw":{"requires":{"env":["PIXMIND_API_KEY"]},"primaryEnv":"PIXMIND_API_KEY"}}
---

# Pixmind video to prompt

Turn one video into a portable structured storyboard. The bundled script submits and polls Pixmind, parses the returned scene nodes, extracts reference frames locally, and emits a generic table presentation that compatible clients can render without Pixmind-specific code.

## Required confirmation

This API costs 100 credits per started minute, rounded up. It accepts one video per request and rejects videos longer than 10 minutes.

Before submitting:

1. Identify the video URL or local file, output language, and requested scene limit.
2. State the billing rule. If the duration is known, show the estimate: `ceil(seconds / 60) * 100` credits.
3. Ask for explicit approval to start the paid analysis.
4. Do not run a submission command until the user approves. Polling an already-created task does not require a second approval.

## Submit and wait

Use one source only. Default to `zh-cn` and 100 scenes unless the user supplied other values.

The launchers use an existing Node.js installation when available. Otherwise they install a
portable, SHA-256-verified Node.js runtime in the Pixmind cache. Pixmind R2 is the primary
source and the matching nodejs.org release is the fallback; neither path modifies the system
`PATH`. On Windows use `run.ps1`; on macOS use `run.sh`.

Remote video on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "{baseDir}/scripts/run.ps1" --url "https://example.com/video.mp4" --language zh-cn --max-scenes 100 --yes --poll
```

Local video on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "{baseDir}/scripts/run.ps1" --file "C:\path\to\video.mp4" --language zh-cn --max-scenes 100 --yes --poll
```

Remote video on macOS:

```bash
sh "{baseDir}/scripts/run.sh" --url "https://example.com/video.mp4" --language zh-cn --max-scenes 100 --yes --poll
```

Local video on macOS:

```bash
sh "{baseDir}/scripts/run.sh" --file "/path/to/video.mp4" --language zh-cn --max-scenes 100 --yes --poll
```

Resume an existing task without resubmitting or charging again. Use the launcher for the current platform:

```bash
sh "{baseDir}/scripts/run.sh" --task-id 12345 --file "/path/to/original.mp4" --poll
```

Keep the original source when resuming if screenshots are required. Supplying `--task-id` never submits another paid task; `--file` or `--url` is used only for local frame extraction.

## Local screenshots and FFmpeg

The script takes the midpoint of every returned `splits[index]`, extracts a 9:16 centered JPEG, and pairs it with `data[index]`.

1. Prefer `--ffmpeg`, then `PIXMIND_FFMPEG_PATH`, then system `ffmpeg`.
2. On Windows x64, if FFmpeg is absent, download the preferred full build from the Pixmind R2 manifest. Validate size and SHA-256 before execution; fall back to the next manifest version if necessary.
3. Never overwrite the source video.
4. Save screenshots and `result.json` under `~/Downloads/pixmind-video-to-prompt/{taskId}/` unless `--output` is supplied.
5. Screenshot extraction is local and free. It must not create or retry a Pixmind task.

## Output handling

- Read the final JSON object from stdout. It contains `storyboard`, local `screenshots`, `attachments`, the original `raw` response, and a generic `presentation` object.
- Prefer `presentation` when the host supports structured results. It contains the SaaS-equivalent sections and seven-column table without requiring client-specific Pixmind logic.
- Otherwise attach every file in `attachments` and render the scenes in a Markdown table with: scene number, reference image, duration, shot type, script, scene description, and video prompt.
- Present the result in this order: video description, video summary, video prompt, full storyboard prompt, then the storyboard table.
- Report the task ID so an interrupted analysis can be resumed without creating a duplicate paid task.
- Report screenshot success and failure counts. Do not claim screenshots came from the Pixmind backend; the bundled script extracts them locally from the original video.
- Treat `ready`, `success`, and `completed` as successful terminal states.
- Treat `failed`, `error`, and `cancelled` as unsuccessful terminal states and report the API message.
- Do not invent missing storyboard fields or submit a replacement task after failure unless the user explicitly approves another paid request.

## Errors and security

- HTTP 400: check that exactly one valid video was supplied and that it is no longer than 10 minutes.
- HTTP 401: configure `PIXMIND_API_KEY`; never ask the user to paste the key into chat.
- HTTP 402: report insufficient credits and stop.
- The API key is configured in the environment or the client's Pixmind provider settings.
- If both portable runtime sources fail, report the launcher's official Node.js installation
  command. Do not install a system-wide runtime without separate user approval.
