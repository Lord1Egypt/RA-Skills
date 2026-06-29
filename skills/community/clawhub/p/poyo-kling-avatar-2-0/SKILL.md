---
name: poyo-kling-avatar-2-0
description: Kling Avatar 2.0 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-avatar-2.0/standard`, `kling-avatar-2.0/pro`, audio-driven avatar video, one reference image, one driving audio URL, optional prompt guidance, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-avatar-2-0","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling Avatar 2.0 Video Generation

Use this skill for Kling Avatar 2.0 jobs on PoYo. It helps agents prepare one-image plus one-audio avatar video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Kling Avatar 2.0, `kling-avatar-2.0/standard`, or `kling-avatar-2.0/pro`.
- The task needs an audio-driven avatar video from one reference image and one driving audio file.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `kling-avatar-2.0/standard`: use for standard avatar video generation.
- `kling-avatar-2.0/pro`: use for pro avatar video generation.

## Key Inputs

- `image_urls` is required and must contain exactly one avatar reference image.
- `audio_url` is required and points to the driving audio file.
- `prompt` is optional for avatar video guidance.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit private likeness images, confidential audio, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_kling_avatar_2_0.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Kling Avatar 2.0, include:

- chosen model id
- final payload or concise parameter summary
- avatar image and driving audio roles
- whether optional prompt guidance is included
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
