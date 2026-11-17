---
name: poyo-kling-2-6
description: Kling 2.6 video generation with native audio on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-2.6`, text-to-video, image-to-video, synchronized dialogue or sound effects, 5s or 10s duration, aspect ratio, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/kling-2-6","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 2.6 Video Generation

## PoYo Links

- Model page: <https://poyo.ai/models/kling-2-6>
- API docs: <https://docs.poyo.ai/api-manual/video-series/kling-2-6>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Kling 2.6 video jobs on PoYo. It helps agents prepare text-to-video or image-to-video payloads with optional audio, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 2.6, `kling-2.6`, native-audio video, dialogue video, or PoYo Kling video generation.
- The task is text-to-video, image-to-video, short video generation, product video, social video, explainer video, or dialogue/sound-effect video.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-2.6`: use for Kling 2.6 text-to-video or image-to-video jobs, including optional native audio.

## Key Inputs

- `prompt` is required inside `input`.
- `sound` is optional and controls whether the request should include generated audio when supported.
- `aspect_ratio` is optional and controls output framing.
- `duration` can be `5` or `10` seconds when supported by the current PoYo docs.
- `image_urls` is optional when the user wants image-to-video guidance.
- `callback_url` is optional and useful for production queues.

## Required Capabilities and Permission Boundary

- Shell: run only the bundled helper after the user explicitly asks to submit a reviewed payload.
- Network: send outbound HTTPS only to `https://api.poyo.ai/api/generate/submit`; use PoYo task status endpoints only when the user asks to check a task.
- Secrets: read only `POYO_API_KEY` from the environment and send it only as an Authorization header.
- Filesystem: read only the user-supplied payload JSON path; do not write, delete, enumerate, or upload unrelated local files.
- Do not inspect unrelated environment variables, broaden the endpoint, run background processes, or execute automatically.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private media URLs, private callback URLs, or generated media URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, examples, and polling notes.
- Use `scripts/submit_kling_2_6.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 2.6, include:

- chosen model id
- whether the request is text-to-video or image-to-video
- final payload or concise parameter summary
- selected duration, aspect ratio, and audio setting when relevant
- whether source images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
