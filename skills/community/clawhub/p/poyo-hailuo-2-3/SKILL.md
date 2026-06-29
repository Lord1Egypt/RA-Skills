---
name: poyo-hailuo-2-3
description: Hailuo 2.3 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `hailuo-2.3`, text-to-video, optional first-frame image guidance, duration control, resolution control, prompt optimization, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/hailuo-2-3","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Hailuo 2.3 Video Generation

Use this skill for Hailuo 2.3 video jobs on PoYo. It helps agents prepare prompt-only and optional first-frame guided payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Hailuo 2.3, Hailuo23, or `hailuo-2.3`.
- The task is text-to-video, first-frame guided video, short social video generation, or video concept drafting.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `hailuo-2.3`: use for Hailuo 2.3 text-to-video with optional first-frame guidance.

## Key Inputs

- `prompt` is required inside `input`.
- `duration` controls supported clip length.
- `resolution` controls supported output resolution.
- `start_image_url` is optional for first-frame guided generation.
- `prompt_optimizer` is optional when the user wants PoYo to optimize the prompt.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_hailuo_2_3.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Hailuo 2.3, include:

- chosen model id
- whether the request is prompt-only or first-frame guided
- final payload or concise parameter summary
- selected duration and resolution when relevant
- whether `prompt_optimizer` is enabled
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
