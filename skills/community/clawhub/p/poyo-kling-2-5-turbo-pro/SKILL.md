---
name: poyo-kling-2-5-turbo-pro
description: Kling 2.5 Turbo Pro video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-2.5-turbo-pro`, text-to-video, image-to-video, first and last frame guidance, duration, aspect ratio, negative prompt, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-2-5-turbo-pro","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 2.5 Turbo Pro Video Generation

Use this skill for Kling 2.5 Turbo Pro video jobs on PoYo. It helps agents prepare prompt-based and frame-guided payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 2.5 Turbo Pro, Kling 2.5, `kling-2.5-turbo-pro`, or PoYo Kling 2.5 video generation.
- The task is text-to-video, image-to-video, first-frame guidance, or first/last-frame video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-2.5-turbo-pro`: use for Kling 2.5 Turbo Pro video generation.

## Key Inputs

- `prompt` is required inside `input`.
- `duration` controls output length when supported by the current PoYo docs.
- `start_image_url` is optional for first-frame image-to-video.
- `end_image_url` is optional for last-frame guidance.
- `aspect_ratio` controls output framing when supported.
- `negative_prompt` is optional for excluding unwanted visual traits.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private source images, private callback URLs, or private generated media URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_2_5_turbo_pro.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 2.5 Turbo Pro, include:

- chosen model id
- whether the request is text-to-video, first-frame image-to-video, or first/last-frame video
- final payload or concise parameter summary
- selected duration, aspect ratio, and negative prompt when relevant
- whether source frames are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
