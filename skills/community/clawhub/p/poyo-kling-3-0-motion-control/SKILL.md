---
name: poyo-kling-3-0-motion-control
description: Kling 3.0 motion control video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-3.0-motion-control`, one reference image plus one reference video, character orientation control, optional prompts, 720p or 1080p output, optional element references, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-3-0-motion-control","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 3.0 Motion Control

Use this skill for Kling 3.0 motion control video jobs on PoYo. It helps agents prepare payloads that combine one reference image and one reference video, choose character orientation, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 3.0 Motion Control, Kling 3 motion control, or `kling-3.0-motion-control`.
- The task needs to apply motion from a reference video while preserving a character, subject, or style from a reference image.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-3.0-motion-control`: use for Kling 3.0 motion control video generation through PoYo.

## Key Inputs

- `image_urls` is required and should contain exactly one reference image.
- `video_urls` is required and should contain exactly one reference video.
- `character_orientation` is required and must be `image` or `video`.
- `prompt` is optional and can describe the intended result.
- `resolution` is optional and supports documented output values.
- `kling_elements` is optional for supported element-reference workflows when `character_orientation` is `video`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private videos, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_3_0_motion_control.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 3.0 Motion Control, include:

- chosen model id
- final payload or concise parameter summary
- reference image and reference video roles
- selected `character_orientation`
- selected resolution when relevant
- whether optional element references are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
