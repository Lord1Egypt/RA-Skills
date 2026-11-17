---
name: poyo-seedream-5-pro
description: Seedream 5.0 Pro image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedream-5.0-pro`, `seedream-5.0-pro-edit`, text-to-image, reference-image editing, 1K or 2K output, aspect-ratio control, and multi-image output.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/seedream-5-0-pro","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Seedream 5.0 Pro Image Generation and Editing

## PoYo Links

- Model page: <https://poyo.ai/models/seedream-5-0-pro>
- API docs: <https://docs.poyo.ai/api-manual/image-series/seedream-5-0-pro>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Seedream 5.0 Pro image jobs on PoYo. It helps agents select generation or edit mode, prepare an async request, and track the returned task.

## Use When

- The user mentions Seedream 5.0 Pro, `seedream-5.0-pro`, or `seedream-5.0-pro-edit`.
- The task is text-to-image generation or editing with reference images.
- The workflow needs PoYo request fields, shell submission, polling, or webhook guidance.

## Model Selection

- `seedream-5.0-pro`: generate images from a text prompt.
- `seedream-5.0-pro-edit`: edit or combine supplied reference images with a prompt.

## Key Inputs

- `prompt` is required for both models.
- `image_urls` is required for edit mode, accepts up to 10 images, and is not supported in generation mode.
- `size` accepts `1K`, `2K`, `1:1`, `3:4`, `4:3`, `16:9`, or `9:16`.
- `n` controls the output count from 1 to 6.
- `output_format` can be `jpeg` or `png`.
- `enable_safety_checker` is optional.

## Required Capabilities and Permission Boundary

- Shell: run only the bundled helper after the user explicitly asks to submit a reviewed payload.
- Network: send outbound HTTPS only to `https://api.poyo.ai/api/generate/submit`; use PoYo task status endpoints only when the user asks to check a task.
- Secrets: read only `POYO_API_KEY` from the environment and send it only as an Authorization header.
- Filesystem: read only the user-supplied payload JSON path; do not write, delete, enumerate, or upload unrelated local files.
- Do not inspect unrelated environment variables, broaden the endpoint, run background processes, or execute automatically.

## Security Rules

- Treat `POYO_API_KEY` as a secret and keep it in a server-side environment variable or secret manager.
- Never place the key in browser code, public repositories, logs, screenshots, or chat output.
- Do not submit private reference images or callback URLs unless the user trusts PoYo and the callback receiver.
- Make live API calls only when the user explicitly requests them in a trusted server-side environment.

## Execution

- Read `references/api.md` before preparing a request.
- Use `scripts/submit_seedream_5_pro.sh` only with a reviewed JSON payload.
- Report the returned `task_id` and the selected model clearly.
- Poll the unified task status endpoint or wait for the configured webhook.

## Output Expectations

Include the selected model, mode, final payload or parameter summary, reference-image count, output settings, returned `task_id` when submitted, and the next status-check step.
