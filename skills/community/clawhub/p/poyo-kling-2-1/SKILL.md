---
name: poyo-kling-2-1
description: Kling 2.1 image-to-video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-2.1/standard`, `kling-2.1/pro`, start-frame guided video, optional Pro end-frame guidance, duration, negative prompt, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/kling-2-1","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 2.1 Image-to-Video Generation
## PoYo Links

- Model page: <https://poyo.ai/models/kling-2-1>
- API docs: <https://docs.poyo.ai/api-manual/video-series/kling-2-1>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Kling 2.1 image-to-video jobs on PoYo. It helps agents prepare Standard and Pro payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 2.1, `kling-2.1/standard`, `kling-2.1/pro`, or PoYo Kling 2.1 video generation.
- The task is start-frame image-to-video or Pro start/end-frame video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-2.1/standard`: use for start-frame guided image-to-video.
- `kling-2.1/pro`: use for start-frame guided image-to-video with optional end-frame guidance.

## Key Inputs

- `prompt` is required inside `input`.
- `start_image_url` is required for both Standard and Pro.
- `duration` can be `5` or `10`.
- `end_image_url` is optional and only supported by `kling-2.1/pro`.
- `negative_prompt` is optional for excluding unwanted visual traits.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private source images, private end-frame images, private callback URLs, or generated media URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_2_1.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 2.1, include:

- chosen model id
- whether Standard or Pro is selected
- final payload or concise parameter summary
- selected duration and negative prompt when relevant
- whether an end frame is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
