---
name: poyo-wan-2-7-image-pro
description: Wan 2.7 Image Pro generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan-2.7-image-pro`, text-to-image, image editing with one to four reference images, preset sizes, custom size objects, image count, seed, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/wan-2-7-image-pro","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Wan 2.7 Image Pro Generation and Editing

Use this skill for Wan 2.7 Image Pro jobs on PoYo. It helps agents prepare text-to-image and reference-image editing payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Wan 2.7 Image Pro, Wan Image Pro, or `wan-2.7-image-pro`.
- The task is text-to-image, prompt-based image editing, product image variation, campaign visual generation, character image variation, or social image generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `wan-2.7-image-pro`: use for Wan 2.7 Image Pro text-to-image and image editing through PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional. Omit it for text-to-image; include one to four images for editing.
- `size` is optional and may use a documented preset string or a custom width and height object.
- `n` is optional and controls the requested number of images.
- `seed` is optional for supported deterministic workflows.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_wan_2_7_image_pro.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Wan 2.7 Image Pro, include:

- chosen model id
- whether the request is text-to-image or image editing
- final payload or concise parameter summary
- selected size and image count when relevant
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
