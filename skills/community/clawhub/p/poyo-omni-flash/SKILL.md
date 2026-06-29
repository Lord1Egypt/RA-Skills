---
name: poyo-omni-flash
description: Omni Flash video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `omni-flash`, text-to-video, single-image video, three-image reference fusion, video-input generation, 720p, 1080p, 4k, duration control, aspect ratio control, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/omni-flash","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Omni Flash Video Generation

Use this skill for Omni Flash video jobs on PoYo. It helps agents prepare text-to-video, image-to-video, three-image reference fusion, and video-input payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Omni Flash or `omni-flash`.
- The task is text-to-video, single-image video generation, three-image reference fusion, or video-input generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `omni-flash`: use for Omni Flash video generation through PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional and supports exactly one image or exactly three images when provided.
- `video_urls` is optional and supports at most one video.
- `resolution` is optional and supports documented output values.
- `duration` is optional for prompt and image workflows; omit it when `video_urls` is provided.
- `aspect_ratio` is optional and supports documented framing values.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private videos, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_omni_flash.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Omni Flash, include:

- chosen model id
- whether the request is text-to-video, image-to-video, reference fusion, or video-input generation
- final payload or concise parameter summary
- selected duration, resolution, and aspect ratio when relevant
- whether source images or source video are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
