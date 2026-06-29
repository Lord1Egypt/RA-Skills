---
name: poyo-grok-imagine-video-1-5
description: Grok Imagine Video 1.5 image-to-video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `grok-imagine-video-1.5`, one source image, prompt-driven motion, 480p or 720p output, duration control, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/grok-imagine-video-1-5","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Grok Imagine Video 1.5 Image-to-Video

Use this skill for Grok Imagine Video 1.5 image-to-video jobs on PoYo. It helps agents prepare single-source-image payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Grok Imagine Video 1.5, Grok video 1.5, or `grok-imagine-video-1.5`.
- The task starts from one source image and needs prompt-driven motion, camera movement, scene changes, or product motion.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `grok-imagine-video-1.5`: use for Grok Imagine Video 1.5 image-to-video generation through PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is required and must contain exactly one source image.
- `resolution` is optional and supports documented output values.
- `duration` is optional and supports documented clip lengths for this model.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_grok_imagine_video_1_5.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Grok Imagine Video 1.5, include:

- chosen model id
- final payload or concise parameter summary
- source image role
- selected duration and resolution when relevant
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
