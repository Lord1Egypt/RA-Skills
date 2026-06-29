---
name: poyo-kling-o1-image
description: Kling O1 image editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-o1-image-edit`, reference-image editing, element descriptors, character or object control, 1K, 2K output, aspect ratio, output format, image count, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/kling-o1","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling O1 Image Editing

Use this skill for Kling O1 image editing jobs on PoYo. It helps agents prepare reference-image editing payloads with optional element descriptors, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling O1 Image, Kling O1 image editing, `kling-o1-image-edit`, or PoYo reference-image editing.
- The task is image editing, character or object preservation, reference-guided visual generation, or multi-reference creative image editing.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-o1-image-edit`: use for image editing with one or more reference images.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is required and should contain one to ten reference images.
- `elements` is optional for subject or object control when the prompt references `@Element1`, `@Element2`, and similar labels.
- `resolution` supports documented output presets.
- `size` controls output aspect ratio.
- `output_format` controls the returned image format.
- `n` controls the requested number of images.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, private callback URLs, or private generated image URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_o1_image.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling O1 Image, include:

- chosen model id
- whether the request uses plain reference editing or element-guided editing
- final payload or concise parameter summary
- selected resolution, size, output format, and image count when relevant
- whether reference images or elements are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
