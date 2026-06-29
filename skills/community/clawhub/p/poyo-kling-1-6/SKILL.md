---
name: poyo-kling-1-6
description: Kling 1.6 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-1.6/standard`, `kling-1.6/pro`, text-to-video, image-to-video, start and end frame guidance, elements with reference images, duration, aspect ratio, negative prompt, cfg scale, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-1-6","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 1.6 Video Generation

Use this skill for Kling 1.6 video jobs on PoYo. It helps agents prepare Standard and Pro payloads for text-to-video, image-to-video, and element-reference workflows, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 1.6, Kling 1.6 Standard, Kling 1.6 Pro, `kling-1.6/standard`, or `kling-1.6/pro`.
- The task is prompt-based video, first-frame image-to-video, Pro first/last-frame video, or element-guided video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-1.6/standard`: use for Standard text-to-video, image-to-video, or element reference workflows.
- `kling-1.6/pro`: use for Pro text-to-video, image-to-video, first/last-frame, or element reference workflows.

## Key Inputs

- `prompt` is required inside `input`.
- `duration` is required and should use a documented value.
- `aspect_ratio` is optional and support depends on the selected workflow.
- `negative_prompt` is optional for excluding unwanted visual traits.
- `cfg_scale` is optional for text-to-video and image-to-video workflows and should not be combined with `image_urls`.
- `start_image_url` is optional for image-to-video.
- `end_image_url` is available for Pro image-to-video when supported and requires `start_image_url`.
- `image_urls` is used for element reference workflows and should not be combined with `start_image_url`, `end_image_url`, or `cfg_scale`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private source images, private reference images, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_1_6.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 1.6, include:

- chosen model id
- whether Standard or Pro is selected
- whether the request is text-to-video, image-to-video, first/last-frame, or elements
- final payload or concise parameter summary
- selected duration, aspect ratio, negative prompt, and cfg scale when relevant
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
