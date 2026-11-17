---
name: poyo-nano-banana-2-lite
description: Nano Banana 2 Lite image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `nano-banana-2-lite`, `nano-banana-2-lite-edit`, fast text-to-image drafts, lightweight image editing, image-to-image workflows, and server-side async task submission.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/nano-banana-2-lite","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Nano Banana 2 Lite Image Generation and Editing

## PoYo Links

- Model page: <https://poyo.ai/models/nano-banana-2-lite>
- API docs: <https://docs.poyo.ai/api-manual/image-series/nano-banana-2-lite>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Nano Banana 2 Lite jobs on PoYo. It helps agents prepare lightweight image generation and edit payloads, submit async tasks, and describe safe server-side integration.

## Use When

- The user mentions Nano Banana 2 Lite, `nano-banana-2-lite`, or `nano-banana-2-lite-edit`.
- The task is fast visual drafting, text-to-image, image-to-image, lightweight image editing, or high-volume concept iteration.
- The workflow needs a server-side curl example, webhook callback guidance, or task polling notes for PoYo.

## Model Selection

- `nano-banana-2-lite`: use for fast text-to-image generation and prompt-only image drafts.
- `nano-banana-2-lite-edit`: use when the user supplies source images and wants lightweight image transformation.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is required for `nano-banana-2-lite-edit`; use it only when source or reference images are part of the request.
- `size` controls aspect ratio when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.
- Save the returned `task_id` immediately for status checks.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, source image URLs, callback URLs, generated outputs, or raw authorization headers unless the user or product policy explicitly allows it.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, examples, and polling notes.
- Use `scripts/submit_nano_banana_2_lite.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Nano Banana 2 Lite, include:

- chosen model id
- whether the request is generation or edit
- final payload or concise parameter summary
- whether source or reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
