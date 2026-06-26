---
name: poyo-wan-2-6
description: Wan 2.6 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan2.6-text-to-video`, `wan2.6-image-to-video`, `wan2.6-video-to-video`, text-to-video, image-to-video, video-to-video, and `multi_shots` control.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/wan-2-6", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Wan 2.6 Video Generation

Use this skill for Wan 2.6 jobs on PoYo. It routes between text-to-video, image-to-video, and video-to-video within one model family.

## Use When

- The user explicitly asks for `Wan 2.6` or one of the `wan2.6-*` model ids.
- The task needs one family that covers text-to-video, image-to-video, and video-to-video.
- The workflow needs `multi_shots`, resolution control, or source-video transformation.

## Model Selection

- `wan2.6-text-to-video`: prompt-only video generation.
- `wan2.6-image-to-video`: one-image guided video generation.
- `wan2.6-video-to-video`: source-video transformation with up to 3 reference videos.

## Key Inputs

- `prompt` is required.
- `image_urls` is only for `wan2.6-image-to-video` and supports one image.
- `video_urls` is only for `wan2.6-video-to-video` and supports up to 3 videos.
- `duration` supports `5`, `10`, `15`.
- `resolution` supports `720p`, `1080p`; `multi_shots` controls single-shot vs multi-shot composition.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_wan_2_6.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
