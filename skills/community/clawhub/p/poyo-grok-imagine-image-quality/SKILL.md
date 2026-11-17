---
name: poyo-grok-imagine-image-quality
description: Grok Imagine Image Quality generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use when the user explicitly requests PoYo or `grok-imagine-image-quality` for text-to-image, reference-image editing, aspect ratio, 1K or 2K output, output format, async polling, or webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/grok-imagine-image-quality","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Grok Imagine Image Quality Generation and Editing

## PoYo Links

- Model page: <https://poyo.ai/models/grok-imagine-image-quality>
- API docs: <https://docs.poyo.ai/api-manual/image-series/grok-imagine-image-quality>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Grok Imagine Image Quality jobs through PoYo. It helps agents prepare text-to-image or reference-image editing payloads, validate documented output controls, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly asks for PoYo, `grok-imagine-image-quality`, or the PoYo Grok Imagine Image Quality API.
- The user wants that PoYo model for text-to-image generation or editing with up to three reference images.
- The workflow needs a PoYo request payload, async task submission, status polling, or callback guidance.

## Model Selection

- `grok-imagine-image-quality`: use for both text-to-image generation and reference-image editing.
- Omit `input.image_urls` for text-to-image; include one to three image URLs for editing.

## Key Inputs

- `input.prompt` is required.
- `input.image_urls` is optional and supports up to three reference images for editing.
- `input.aspect_ratio` supports documented presets: `1:1`, `2:3`, `3:2`, `9:16`, and `16:9`.
- `input.resolution` supports `1K` or `2K`.
- `input.output_format` supports `png`, `jpeg`, `jpg`, or `webp`.
- `input.n` controls the requested output count when supported by the current service.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret and keep it in a server-side environment variable or secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not submit confidential prompts, private image URLs, or private callback URLs unless the user trusts PoYo and the callback receiver.
- Do not make a live API call unless the user explicitly requests it and provides a safe server-side environment.
- Confirm that the user has the right to process every reference image.

## Required Capabilities and Permission Boundary

- Shell: run only the bundled `scripts/submit_grok_imagine_image_quality.sh` helper after the user explicitly approves a live submission.
- Network: allow outbound HTTPS only to `https://api.poyo.ai/api/generate/submit`; use `https://api.poyo.ai/api/generate/status/{task_id}` only when the user asks to poll a returned task.
- Secret: read only `POYO_API_KEY` from the process environment and send it only in the PoYo `Authorization` header.
- Filesystem: read only the payload JSON file path explicitly supplied by the user. The helper does not write, delete, enumerate, or upload other local files.
- Do not broaden the endpoint, inspect unrelated environment variables, run background processes, or execute the helper automatically.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, response shape, and polling notes.
- Use `scripts/submit_grok_imagine_image_quality.sh` only when the user wants to submit a reviewed JSON payload from a trusted shell.
- If the user only needs an example, adapt one from `references/api.md` without making a live request.
- After submission, report the returned `task_id` clearly.

## Output Expectations

When helping with this model, include:

- exact model id
- generation or editing mode
- final payload or concise parameter summary
- reference-image count when editing
- selected aspect ratio, resolution, output format, and output count
- returned `task_id` if a request was submitted
- next step: poll status or wait for webhook
