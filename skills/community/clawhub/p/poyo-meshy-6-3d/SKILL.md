---
name: poyo-meshy-6-3d
description: Meshy 6 3D asset generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `meshy-6-text-to-3d`, `meshy-6-image-to-3d`, `meshy-6-multi-image-to-3d`, prompt-to-3D assets, image-to-3D, polling, and webhook integration.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/3d-series/meshy-6-3d","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Meshy 6 3D Asset Generation

Use this skill for Meshy 6 3D jobs on PoYo. It helps agents prepare text-to-3D, image-to-3D, and multi-image-to-3D payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Meshy 6, `meshy-6-text-to-3d`, `meshy-6-image-to-3d`, or `meshy-6-multi-image-to-3d`.
- The task is prompt-to-3D asset generation, source-image-to-3D, or multi-reference 3D asset generation.
- The workflow needs returned 3D asset URLs, preview files, polling, or callback URL guidance.

## Model Selection

- `meshy-6-text-to-3d`: use when the user has a prompt and no source image.
- `meshy-6-image-to-3d`: use when the user has one source image.
- `meshy-6-multi-image-to-3d`: use when the user has multiple source images or views.

## Key Inputs

- `prompt` is required for text-to-3D.
- `image_urls` is required for image-to-3D and multi-image-to-3D workflows.
- `mode`, `topology`, `target_polycount`, and texture options should follow current PoYo docs.
- Rigging, animation, and safety options should only be used when the current docs support them for the selected workflow.
- `callback_url` is optional and useful for production asset pipelines.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Use current PoYo docs and model pages for request fields that may change.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, examples, and polling notes.
- Use `scripts/submit_meshy_6_3d.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Meshy 6 3D, include:

- chosen model id
- whether the request is text-to-3D, image-to-3D, or multi-image-to-3D
- final payload or concise parameter summary
- whether source images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
