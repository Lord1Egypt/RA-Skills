---
name: poyo-kling-o3-image
description: Kling O3 image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-o3-image`, `kling-o3-image-edit`, prompt-only image generation, reference-image editing, element descriptors, 1K, 2K, 4K output, aspect ratio control, output format, image count, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/kling-o3","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling O3 Image Generation and Editing

Use this skill for Kling O3 image jobs on PoYo. It helps agents prepare prompt-only image generation and reference-image editing payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling O3 Image, Kling O3 image editing, `kling-o3-image`, or `kling-o3-image-edit`.
- The task is prompt-only image generation, reference-image editing, campaign visual generation, character/object consistency, or high-resolution creative image generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-o3-image`: use for prompt-only image generation.
- `kling-o3-image-edit`: use for image editing with one or more reference images.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is required for `kling-o3-image-edit` and omitted for prompt-only generation.
- `elements` is optional for subject or object control when the request needs consistency.
- `resolution` supports documented output presets.
- `size` controls output aspect ratio. Use `auto` only for edit workflows.
- `output_format` controls the returned image format.
- `n` controls the requested number of images.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_o3_image.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling O3 Image, include:

- chosen model id
- whether the request is prompt-only generation or image editing
- final payload or concise parameter summary
- selected resolution, size, output format, and image count when relevant
- whether reference images or elements are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
