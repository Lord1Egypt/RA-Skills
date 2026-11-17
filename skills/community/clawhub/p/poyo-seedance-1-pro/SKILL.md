---
name: poyo-seedance-1-pro
description: Seedance 1.0 Pro video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedance-1.0-pro`, text-to-video, image-to-video, 720p or 1080p clips, 5s or 10s duration, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/seedance-1-pro","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Seedance 1.0 Pro Video Generation

## PoYo Links

- Model page: <https://poyo.ai/models/seedance-1-pro>
- API docs: <https://docs.poyo.ai/api-manual/video-series/seedance-1.0-pro>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Seedance 1.0 Pro video jobs on PoYo. It helps agents prepare text-to-video or image-to-video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Seedance 1.0 Pro, `seedance-1.0-pro`, or PoYo Seedance video generation.
- The task is text-to-video, image-to-video, short creative video, product demo video, or social video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `seedance-1.0-pro`: use for Seedance 1.0 Pro text-to-video and image-to-video requests.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional when the user wants image-to-video guidance.
- `resolution` can be `720p` or `1080p` when supported by the current PoYo docs.
- `duration` can be `5` or `10` seconds when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Required Capabilities and Permission Boundary

- Shell: run only the bundled helper after the user explicitly asks to submit a reviewed payload.
- Network: send outbound HTTPS only to `https://api.poyo.ai/api/generate/submit`; use PoYo task status endpoints only when the user asks to check a task.
- Secrets: read only `POYO_API_KEY` from the environment and send it only as an Authorization header.
- Filesystem: read only the user-supplied payload JSON path; do not write, delete, enumerate, or upload unrelated local files.
- Do not inspect unrelated environment variables, broaden the endpoint, run background processes, or execute automatically.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private image URLs, private callback URLs, or generated media URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, examples, and polling notes.
- Use `scripts/submit_seedance_1_pro.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Seedance 1.0 Pro, include:

- chosen model id
- whether the request is text-to-video or image-to-video
- final payload or concise parameter summary
- selected resolution and duration when relevant
- whether source images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
