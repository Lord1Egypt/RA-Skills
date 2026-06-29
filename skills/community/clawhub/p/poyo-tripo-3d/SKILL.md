---
name: poyo-tripo-3d
description: Tripo3D asset generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `tripo3d-h3.1-text-to-3d`, `tripo3d-h3.1-image-to-3d`, `tripo3d-h3.1-multiview-to-3d`, `tripo3d-p1-text-to-3d`, `tripo3d-p1-image-to-3d`, text-to-3D, image-to-3D, multiview-to-3D, mesh options, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/3d-series/tripo-h31-3d","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Tripo3D Asset Generation

Use this skill for Tripo3D jobs on PoYo. It covers H3.1 high-detail workflows and P1 lightweight workflows for text-to-3D, image-to-3D, and multiview-to-3D asset generation.

## Use When

- The user explicitly mentions Tripo3D, Tripo H3.1, Tripo P1, `tripo3d-h3.1-*`, or `tripo3d-p1-*`.
- The task is prompt-to-3D, object image-to-3D, multiview-to-3D, mesh generation, texture generation, or 3D asset pipeline planning.
- The workflow needs PoYo async task submission, 3D task status polling, or callback URL guidance.

## Model Selection

- `tripo3d-h3.1-text-to-3d`: high-detail 3D model from a prompt.
- `tripo3d-h3.1-image-to-3d`: high-detail 3D model from one object image.
- `tripo3d-h3.1-multiview-to-3d`: high-detail 3D model from 2 to 4 views of the same object.
- `tripo3d-p1-text-to-3d`: lightweight 3D model from a prompt.
- `tripo3d-p1-image-to-3d`: lightweight 3D model from one object image.

## Key Inputs

- `prompt` is required for text-to-3D workflows.
- `image_urls` is required for image and multiview workflows.
- `negative_prompt` is available for H3.1 text-to-3D when supported.
- `face_limit`, `texture`, `pbr`, `texture_quality`, `geometry_quality`, `auto_size`, and `quad` control mesh and material output when supported by the selected model.
- `model_seed`, `image_seed`, and `texture_seed` can help reproduce supported generation stages.
- `callback_url` is optional and useful for production asset pipelines.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential object images, private asset URLs, or proprietary prompts unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, fields, examples, 3D result notes, and polling notes.
- Use `scripts/submit_tripo_3d.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Tripo3D, include:

- chosen model id
- whether the request is text-to-3D, image-to-3D, or multiview-to-3D
- final payload or concise parameter summary
- texture, material, geometry, and face-limit settings when relevant
- whether source images are involved
- returned `task_id` if a request was actually submitted
- next step: poll 3D status or wait for webhook
