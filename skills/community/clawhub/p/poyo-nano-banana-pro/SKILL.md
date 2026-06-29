---
name: poyo-nano-banana-pro
description: Nano Banana Pro image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `nano-banana-pro`, `nano-banana-pro-edit`, text-to-image, image editing, multi-reference image workflows, output format control, and 1K/2K/4K output.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/nano-banana-2","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Nano Banana Pro Image Generation and Editing

Use this skill for Nano Banana Pro jobs on PoYo. It covers text-to-image generation, image editing, multi-reference workflows, output format control, and higher-resolution output through PoYo's async generation API.

## Use When

- The user explicitly mentions Nano Banana Pro, `nano-banana-pro`, or `nano-banana-pro-edit`.
- The task is image generation, image-to-image, or editing one or more supplied images.
- The workflow needs production-oriented image payloads, output format control, 1K/2K/4K output, polling, or webhook guidance.

## Model Selection

- `nano-banana-pro`: text-to-image generation and optional reference-guided generation.
- `nano-banana-pro-edit`: editing based on one or more source images and a text instruction.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` should be used when editing or when references are part of the task.
- `size` controls aspect ratio or automatic sizing when supported by the current PoYo docs.
- `resolution` supports the quality tiers documented by PoYo for this model family.
- `output_format` can be used when the docs support explicit output format selection.
- `enable_web_search` should only be used when the user needs real-world grounding and understands that the prompt may be enriched with external context.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Use current PoYo docs and model pages for request fields that may change.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, examples, and polling notes.
- Use `scripts/submit_nano_banana_pro.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Nano Banana Pro, include:

- chosen model id
- whether the request is generation, reference-guided generation, or editing
- final payload or concise parameter summary
- selected size, resolution, and output format when relevant
- whether source or reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
