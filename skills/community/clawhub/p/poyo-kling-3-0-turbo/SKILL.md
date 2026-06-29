---
name: poyo-kling-3-0-turbo
description: Kling 3.0 Turbo video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-3.0-turbo/standard`, `kling-3.0-turbo/pro`, text-to-video, single first-frame image-to-video, multi_prompt storyboards, duration control, aspect ratios, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-3-0-turbo","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 3.0 Turbo Video Generation

Use this skill for Kling 3.0 Turbo video jobs on PoYo. It helps agents prepare text-to-video, first-frame image-to-video, and multi-shot storyboard payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling 3.0 Turbo, Kling Turbo, `kling-3.0-turbo/standard`, or `kling-3.0-turbo/pro`.
- The task is text-to-video, first-frame image-to-video, short product motion, cinematic concept video, or multi-shot storytelling.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-3.0-turbo/standard`: use for standard Kling 3.0 Turbo video generation.
- `kling-3.0-turbo/pro`: use for pro Kling 3.0 Turbo video generation.

## Key Inputs

- `prompt` is used for a single-shot prompt workflow.
- `multi_prompt` is used for multi-shot storyboards and should not be combined with `prompt`.
- `image_urls` is optional and supports at most one first-frame image.
- `duration` supports documented clip lengths for this model.
- `aspect_ratio` is for text-to-video mode.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_3_0_turbo.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling 3.0 Turbo, include:

- chosen model id
- whether the request is text-to-video, image-to-video, or multi-shot
- final payload or concise parameter summary
- selected duration and aspect ratio when relevant
- whether a reference image is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
