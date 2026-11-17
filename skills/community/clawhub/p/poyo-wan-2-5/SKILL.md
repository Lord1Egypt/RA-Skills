---
name: poyo-wan-2-5
description: Wan 2.5 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan2.5-text-to-video`, `wan2.5-image-to-video`, text-to-video, image-to-video, 5s or 10s clips, size presets, resolution, audio string, negative prompt, seed control, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/wan-2-5","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Wan 2.5 Video Generation
## PoYo Links

- Model page: <https://poyo.ai/models/wan-2-5>
- API docs: <https://docs.poyo.ai/api-manual/video-series/wan2.5-text-to-video>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Wan 2.5 video jobs on PoYo. It helps agents prepare text-to-video and image-to-video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Wan 2.5, `wan2.5-text-to-video`, `wan2.5-image-to-video`, or PoYo Wan 2.5 video generation.
- The task is prompt-based video or single-image animation with duration and size controls.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `wan2.5-text-to-video`: generate video from a text prompt.
- `wan2.5-image-to-video`: animate one input image.

## Key Inputs

- `prompt` is required inside `input`.
- `aspect_ratio` is used by text-to-video and accepts documented size presets.
- `image_urls` is required for image-to-video and supports exactly one URL.
- `resolution` is used by image-to-video and supports documented output values.
- `duration` can be `5` or `10`.
- `audio` is an optional string. Do not send a boolean value.
- `negative_prompt` and `seed` are optional controls.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private image URLs, private callback URLs, or generated media URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_wan_2_5.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Wan 2.5, include:

- chosen model id
- whether the request is text-to-video or image-to-video
- final payload or concise parameter summary
- selected duration, size or resolution, audio string, negative prompt, and seed when relevant
- whether a source image is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
