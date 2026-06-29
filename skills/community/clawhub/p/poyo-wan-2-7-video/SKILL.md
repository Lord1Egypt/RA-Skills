---
name: poyo-wan-2-7-video
description: Wan 2.7 video generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan2.7-text-to-video`, `wan2.7-image-to-video`, `wan2.7-reference-to-video`, `wan2.7-edit-video`, text-to-video, image-to-video, reference media, video editing, audio URL, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/wan-2-7-video","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Wan 2.7 Video Generation and Editing

Use this skill for Wan 2.7 video jobs on PoYo. It helps agents prepare text-to-video, image-to-video, reference-to-video, and video edit payloads, then submit async tasks and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Wan 2.7, `wan2.7-text-to-video`, `wan2.7-image-to-video`, `wan2.7-reference-to-video`, or `wan2.7-edit-video`.
- The task is text-to-video, first/last-frame animation, reference-guided video, video editing, or audio-guided video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `wan2.7-text-to-video`: generate video from a text prompt.
- `wan2.7-image-to-video`: animate one or two input images.
- `wan2.7-reference-to-video`: generate video from reference images or videos.
- `wan2.7-edit-video`: edit an existing video with an optional image reference.

## Key Inputs

- `prompt` is required for text, reference, and edit workflows.
- `image_urls` is required for image-to-video and supports one or two image URLs.
- `reference_image_urls` and `reference_video_urls` are used for reference-to-video workflows.
- `video_url` is required for edit-video and optional in image-to-video where supported.
- `audio_url` can guide supported text and image workflows.
- `aspect_ratio`, `resolution`, `duration`, `multi_shots`, `audio_setting`, `seed`, and `enable_safety_checker` are optional controls depending on workflow.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private images, private videos, private audio, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, workflow fields, example payloads, and polling notes.
- Use `scripts/submit_wan_2_7_video.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Wan 2.7 Video, include:

- chosen model id
- workflow type: text-to-video, image-to-video, reference-to-video, or edit-video
- final payload or concise parameter summary
- selected duration, resolution, aspect ratio, and audio inputs when relevant
- whether source images, source videos, reference media, or audio URLs are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
