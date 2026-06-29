---
name: poyo-wan-animate
description: Wan Animate video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan-animate-replace`, `wan-animate-move`, character animation, character replacement, one source video URL, one target image, 480p, 580p, or 720p output, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/wan-animate","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Wan Animate Video Generation

Use this skill for Wan Animate jobs on PoYo. It helps agents prepare character animation and character replacement payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Wan Animate, `wan-animate-replace`, or `wan-animate-move`.
- The task needs a character image animated by a source video or a character replacement workflow.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `wan-animate-replace`: use when replacing a character in a source video with the character from a target image.
- `wan-animate-move`: use when animating a character image with motion from a source video.

## Key Inputs

- `video_url` is required and points to the source video.
- `image_urls` is required and must contain exactly one target image.
- `resolution` is optional and supports documented output values.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit private likeness images, private videos, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_wan_animate.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Wan Animate, include:

- chosen model id
- whether the request uses character replacement or character animation
- final payload or concise parameter summary
- source video and target image roles
- selected resolution when relevant
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
