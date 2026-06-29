---
name: poyo-hunyuan-3d-3-1
description: Hunyuan 3D v3.1 asset generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `hunyuan-3d/v3.1/pro/text-to-3d`, `hunyuan-3d/v3.1/pro/image-to-3d`, `hunyuan-3d/v3.1/rapid/text-to-3d`, `hunyuan-3d/v3.1/rapid/image-to-3d`, text-to-3D, image-to-3D, PBR, geometry, face count, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/3d-series/hunyuan-3d-3-1","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Hunyuan 3D v3.1 Asset Generation

Use this skill for Hunyuan 3D v3.1 jobs on PoYo. It covers Pro and Rapid workflows for text-to-3D and image-to-3D asset generation.

## Use When

- The user explicitly mentions Hunyuan 3D v3.1, Hunyuan 3D 3.1, Hunyuan 3D Pro, Hunyuan 3D Rapid, or `hunyuan-3d/v3.1/*`.
- The task is prompt-to-3D, object image-to-3D, mesh generation, material generation, or 3D asset pipeline planning.
- The workflow needs PoYo async task submission, 3D task status polling, or callback URL guidance.

## Model Selection

- `hunyuan-3d/v3.1/pro/text-to-3d`: Pro 3D model from a prompt.
- `hunyuan-3d/v3.1/pro/image-to-3d`: Pro 3D model from one object image, with optional extra view URLs.
- `hunyuan-3d/v3.1/rapid/text-to-3d`: Rapid 3D model from a prompt.
- `hunyuan-3d/v3.1/rapid/image-to-3d`: Rapid 3D model from one object image.

## Key Inputs

- `prompt` is required for text-to-3D workflows.
- `image_urls` is required for image-to-3D workflows and should contain exactly one image URL.
- `generate_type` is available for Pro models when supported.
- `enable_pbr` controls PBR material generation when supported.
- `face_count` controls Pro mesh density within the documented range.
- `enable_geometry` is available for Rapid models when supported.
- Extra view URL fields can guide Pro image-to-3D when the user has aligned views of the same object.
- `callback_url` is optional and useful for production asset pipelines.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential object images, private asset URLs, proprietary prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, fields, examples, 3D result notes, and polling notes.
- Use `scripts/submit_hunyuan_3d_3_1.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Hunyuan 3D v3.1, include:

- chosen model id
- whether the request is text-to-3D or image-to-3D
- whether Pro or Rapid is selected
- final payload or concise parameter summary
- material, geometry, face-count, and extra-view settings when relevant
- returned `task_id` if a request was actually submitted
- next step: poll 3D status or wait for webhook
