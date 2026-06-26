---
name: kling-3
description: Kling 3.0 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-3.0/standard`, `kling-3.0/pro`, text-to-video, image-to-video, multi-shot prompts, element references, sound-enabled output, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/kling-3-0","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Kling 3.0 Multi-Shot Video Generation

Use this skill for Kling 3.0 jobs on PoYo. It covers text-to-video, image-to-video, single-shot video, multi-shot video generation, element-referenced prompting, and sound-enabled output.

## Use When

- The user explicitly asks for Kling 3.0, `kling-3.0/standard`, or `kling-3.0/pro`.
- The task needs text-to-video, image-to-video, multi-shot storytelling, or structured `multi_prompt` input.
- The workflow depends on `kling_elements`, reference frames, native sound control, status polling, or webhook integration.

## Model Selection

- `kling-3.0/standard`: use for standard Kling 3.0 video generation.
- `kling-3.0/pro`: use when the user explicitly asks for the pro model or higher-detail output.

## Key Inputs

- `prompt` is required when `multi_shots` is `false`.
- `multi_prompt` is required when `multi_shots` is `true`.
- `sound`, `multi_shots`, and `duration` drive the main workflow.
- `image_urls` should be used only when the request depends on source frames or element references.
- `kling_elements` can define reusable visual elements that prompts reference by name.
- `aspect_ratio` supports `1:1`, `16:9`, and `9:16`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not pass API keys as command-line arguments.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private callback URLs, or proprietary prompts unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_kling_3_0.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with this model family, include:

- chosen model id
- whether the request is text-to-video, image-to-video, or multi-shot
- final payload or concise parameter summary
- whether reference images or elements are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
