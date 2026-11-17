---
name: poyo-generate-music-cover
description: Generate music cover versions on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-music-cover`, cover generation from a completed music task_id, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/generate-music-cover","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Generate Music Cover

## PoYo Links

- Model page: <https://poyo.ai/models/generate-music-cover>
- API docs: <https://docs.poyo.ai/api-manual/music-series/generate-music-cover>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `generate-music-cover` jobs on PoYo. It helps agents prepare cover-generation payloads from a completed music task, submit async tasks, and explain result retrieval.

## Use When

- The user explicitly wants to create a cover version of existing generated music with PoYo or `generate-music-cover`.
- The user has a completed PoYo music `task_id` and asks for a cover request payload, server-side curl command, callback setup, or status retrieval.
- The user has already chosen PoYo as the execution provider for a music cover workflow.

## Model Selection

- `generate-music-cover`: use for generating a cover version from a completed music generation task.

## Key Inputs

- `task_id` identifies the completed source music generation task.
- `callback_url` is required by the documented schema and should point to a server-side webhook.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, customer task ids, generated audio URLs, callback URLs, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music generation unless the user explicitly wants a PoYo Generate Music Cover API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_generate_music_cover.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Generate Music Cover, include:

- chosen model id
- source music task identifier summary
- callback setup summary
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query status or wait for webhook
