---
name: poyo-kling-3-0-4k
description: Kling 3.0 4K video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-3.0/4K`, text-to-video, start-frame and optional end-frame image-to-video, multi_shots, multi_prompt, native audio flag, duration control, element references, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-3-0-4k","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 3.0 4K Video Generation

Use this skill for Kling 3.0 4K video jobs on PoYo. It helps agents prepare text-to-video, image-to-video, and multi-shot payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 3.0 4K, Kling 4K, or `kling-3.0/4K`.
- The task is high-resolution text-to-video, start-frame image-to-video, optional end-frame image-to-video, multi-shot storytelling, or element-reference video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-3.0/4K`: use for Kling 3.0 4K video generation through PoYo.

## Key Inputs

- `prompt` is used when `multi_shots` is false.
- `multi_shots` enables multi-shot mode and uses `multi_prompt`.
- `multi_prompt` is required when `multi_shots` is true.
- `duration` is required by the documented request schema.
- `sound` is required by the documented request schema.
- `image_urls` is optional for start-frame and optional end-frame workflows.
- `kling_elements` is optional for supported element-reference workflows.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, private videos, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_3_0_4k.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 3.0 4K, include:

- chosen model id
- whether the request is text-to-video, image-to-video, or multi-shot
- final payload or concise parameter summary
- selected duration and sound flag when relevant
- whether reference images or element references are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
