---
name: poyo-flux-dev
description: FLUX Dev image generation and single-image editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use when the user explicitly requests PoYo or `flux-dev` for text-to-image, image-to-image editing, output size, image count, PNG or JPEG output, async polling, or webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/flux-dev","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo FLUX Dev Image Generation and Editing

## PoYo Links

- Model page: <https://poyo.ai/models/flux-dev>
- API docs: <https://docs.poyo.ai/api-manual/image-series/flux-dev>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for FLUX Dev jobs through PoYo. It helps agents prepare text-to-image or single-image editing payloads, validate output controls, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly asks for PoYo, `flux-dev`, or the PoYo FLUX Dev API.
- The user wants that PoYo model for text-to-image generation or editing from exactly one source image.
- The workflow needs a PoYo request payload, async task submission, status polling, or callback guidance.

## Model Selection

- `flux-dev`: use for both text-to-image generation and single-image editing.
- Omit `input.image_urls` for text-to-image; provide exactly one image URL for editing.

## Key Inputs

- `input.prompt` is required.
- `input.image_urls` is optional; when present, it must contain exactly one source image URL.
- `input.size` controls documented presets or a supported custom `WIDTHxHEIGHT` value.
- `input.n` controls the requested output count when supported by the current service.
- `input.output_format` supports `png` or `jpeg`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret and keep it in a server-side environment variable or secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not submit confidential prompts, private source-image URLs, or private callback URLs unless the user trusts PoYo and the callback receiver.
- Do not make a live API call unless the user explicitly requests it and provides a safe server-side environment.
- Confirm that the user has the right to process the source image.

## Required Capabilities and Permission Boundary

- Shell: run only the bundled `scripts/submit_flux_dev.sh` helper after the user explicitly approves a live submission.
- Network: allow outbound HTTPS only to `https://api.poyo.ai/api/generate/submit`; use `https://api.poyo.ai/api/generate/status/{task_id}` only when the user asks to poll a returned task.
- Secret: read only `POYO_API_KEY` from the process environment and send it only in the PoYo `Authorization` header.
- Filesystem: read only the payload JSON file path explicitly supplied by the user. The helper does not write, delete, enumerate, or upload other local files.
- Do not broaden the endpoint, inspect unrelated environment variables, run background processes, or execute the helper automatically.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, response shape, and polling notes.
- Use `scripts/submit_flux_dev.sh` only when the user wants to submit a reviewed JSON payload from a trusted shell.
- If the user only needs an example, adapt one from `references/api.md` without making a live request.
- After submission, report the returned `task_id` clearly.

## Output Expectations

When helping with FLUX Dev, include:

- exact model id
- generation or editing mode
- final payload or concise parameter summary
- source-image count when editing
- selected size, output count, and output format
- returned `task_id` if a request was submitted
- next step: poll status or wait for webhook
