---
name: poyo-flux-kontext
description: Flux Kontext image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `flux-kontext-pro`, `flux-kontext-pro-edit`, `flux-kontext-max`, `flux-kontext-max-edit`, text-to-image, image editing, aspect ratio control, output format control, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/flux-kontext","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Flux Kontext Image Generation and Editing

Use this skill for Flux Kontext image jobs on PoYo. It helps agents prepare text-to-image and single-image editing payloads, choose Pro or Max model ids, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Flux Kontext, `flux-kontext-pro`, `flux-kontext-pro-edit`, `flux-kontext-max`, or `flux-kontext-max-edit`.
- The task is image generation, image editing, product visuals, reference-image edits, or output format control.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `flux-kontext-pro`: use for Flux Kontext Pro text-to-image generation.
- `flux-kontext-pro-edit`: use for Flux Kontext Pro image editing with one source image.
- `flux-kontext-max`: use for Flux Kontext Max text-to-image generation.
- `flux-kontext-max-edit`: use for Flux Kontext Max image editing with one source image.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is required for edit models and only the first image is used according to current PoYo docs.
- `size` controls the documented output aspect ratio.
- `output_format` supports documented image formats.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_flux_kontext.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Flux Kontext, include:

- chosen model id
- whether the request is generation or editing
- final payload or concise parameter summary
- selected size and output format when relevant
- whether a source image is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
