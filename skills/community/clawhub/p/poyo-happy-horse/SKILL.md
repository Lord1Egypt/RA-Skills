---
name: poyo-happy-horse
description: Happy Horse video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `happy-horse`, text-to-video, image-to-video, reference-driven short video, video edit planning, task submission, polling, and webhook integration.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/happy-horse","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Happy Horse Video Generation

Use this skill for Happy Horse video jobs on PoYo. It helps agents prepare `happy-horse` payloads, choose text or source-media workflows, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Happy Horse, HappyHorse, `happy-horse`, or PoYo video generation.
- The task is text-to-video, image-to-video, reference-driven video, or short creative video drafting.
- The workflow needs a PoYo async submit payload, task status polling, or callback URL guidance.

## Model Selection

- `happy-horse`: use for text-to-video and source-media video workflows on PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional and should be used only when the task depends on source images or reference frames.
- `resolution` controls output resolution when supported by the current PoYo docs.
- `duration` controls clip length when supported by the current PoYo docs.
- `aspect_ratio` should match the target surface such as landscape, square, or vertical social formats.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Use current PoYo docs and model pages for request fields that may change.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_happy_horse.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Happy Horse, include:

- chosen model id
- whether the request is text-to-video or source-media video
- final payload or concise parameter summary
- whether source images or references are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
