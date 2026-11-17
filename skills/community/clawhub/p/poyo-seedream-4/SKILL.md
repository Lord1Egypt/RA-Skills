---
name: poyo-seedream-4
description: Seedream 4 image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedream-4`, `seedream-4-edit`, text-to-image, image editing, reference images, 1K/2K/4K output, async status polling, callbacks, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/seedream-4","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Seedream 4 Image Generation and Editing

## PoYo Links

- Model page: <https://poyo.ai/models/seedream-4>
- API docs: <https://docs.poyo.ai/api-manual/image-series/seedream-4>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Seedream 4 jobs on PoYo. It helps agents prepare text-to-image and image-editing payloads, submit async tasks, and describe safe server-side integration.

## Use When

- The user explicitly wants to use PoYo with Seedream 4, `seedream-4`, `seedream-4-edit`, or the PoYo async image API.
- The user asks for a PoYo Seedream 4 request payload, server-side curl command, integration notes, status polling, webhook setup, or response parsing.
- The user has already chosen PoYo as the execution provider for a Seedream 4 image workflow.

## Model Selection

- `seedream-4`: use for text-to-image generation and optional reference-guided generation.
- `seedream-4-edit`: use when the user explicitly wants to edit supplied images.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is required for `seedream-4-edit`; use it only when source or reference images are part of the request.
- `size` controls aspect ratio when supported by the current PoYo docs.
- `resolution` supports documented output presets.
- `n` controls output count within the documented limit.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, source image URLs, generated outputs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic image generation or editing unless the user explicitly wants a PoYo Seedream 4 API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, examples, and polling notes.
- Use `scripts/submit_seedream_4.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Seedream 4, include:

- chosen model id
- whether the request is generation, reference-guided generation, or editing
- final payload or concise parameter summary
- selected size and resolution when relevant
- whether source or reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
