---
name: poyo-kling-o3-4k
description: Kling O3 4K video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-o3/4K`, text-to-video, image-to-video, reference-to-video, multi_shots, multi_prompt, sound, aspect ratio control, element references, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-o3-4k","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling O3 4K Video Generation

Use this skill for Kling O3 4K video jobs on PoYo. It helps agents prepare text-to-video, image-to-video, reference-to-video, and multi-shot payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling O3 4K, Kling O3/4K, or `kling-o3/4K`.
- The task is 4K text-to-video, image-to-video with start or end anchors, reference-image guided video, multi-shot storytelling, or element-reference video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-o3/4K`: use for Kling O3 4K video generation through PoYo.

## Key Inputs

- `prompt` is used when `multi_shots` is false.
- `multi_shots` enables multi-shot mode and uses `multi_prompt`.
- `multi_prompt` is required when `multi_shots` is true.
- `duration` is required by the documented request schema.
- `sound` is required by the documented request schema.
- `image_urls` supports up to two primary image anchors.
- `reference_image_urls` supports up to four reference images and enables reference-to-video mode.
- `aspect_ratio` is used for text-to-video and reference-to-video.
- `kling_elements` is optional for supported reference-to-video workflows.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, private videos, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_o3_4k.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling O3 4K, include:

- chosen model id
- whether the request is text-to-video, image-to-video, reference-to-video, or multi-shot
- final payload or concise parameter summary
- selected duration, aspect ratio, and sound flag when relevant
- whether source images, reference images, or element references are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
