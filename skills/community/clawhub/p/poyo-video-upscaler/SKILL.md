---
name: poyo-video-upscaler
description: Upscale hosted videos on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `poyo-ai/video-upscaler`, public video URLs, scale control, async status polling, callbacks, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/video-upscaler","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Video Upscaler

## PoYo Links

- Model page: <https://poyo.ai/models/video-upscaler>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `poyo-ai/video-upscaler` jobs on PoYo. It helps agents prepare video-upscaling payloads, submit async tasks, and explain safe server-side integration.

## Use When

- The user explicitly wants to use PoYo with `poyo-ai/video-upscaler`, video upscaling, hosted video enhancement, scale control, or the PoYo async media utility API.
- The user asks for a PoYo video-upscaler request payload, server-side curl command, integration notes, status polling, webhook setup, or response parsing.
- The user has already chosen PoYo as the execution provider for a video-upscaling workflow.

## Model Selection

- `poyo-ai/video-upscaler`: use for increasing the resolution of an existing hosted video file.

## Key Inputs

- `video_url` is required and must point to a publicly accessible video file.
- `scale` is optional. The default is `2`; supported values are `1` through `8`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private source video URLs, generated outputs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic video editing unless the user explicitly wants a PoYo video-upscaling API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_video_upscaler.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with PoYo Video Upscaler, include:

- chosen model id
- source video URL handling notes
- selected scale value
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
