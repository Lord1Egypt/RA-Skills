---
name: poyo-convert-to-wav
description: Convert generated music tracks to WAV on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `convert-to-wav`, WAV export from a completed music task_id plus audio_id, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/convert-to-wav","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Convert to WAV

## PoYo Links

- Model page: <https://poyo.ai/models/convert-to-wav>
- API docs: <https://docs.poyo.ai/api-manual/music-series/convert-to-wav>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `convert-to-wav` jobs on PoYo. It helps agents prepare WAV conversion payloads from completed PoYo music tasks, submit async requests, and explain result retrieval.

## Use When

- The user explicitly wants to convert a PoYo-generated music track to WAV.
- The user has a completed PoYo music `task_id` and `audio_id` and asks for a request payload, server-side curl command, callback setup, or result retrieval.
- The user has already chosen PoYo as the execution provider for a music export workflow.

## Model Selection

- `convert-to-wav`: use for converting a generated music track to WAV format from a source music task and audio identifier.

## Key Inputs

- `task_id` identifies the completed source music generation task.
- `audio_id` identifies the specific audio track to convert.
- `callback_url` is required by the documented schema and should point to a server-side webhook.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, customer task ids, audio identifiers, generated file URLs, callback URLs, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic audio conversion unless the user explicitly wants a PoYo Convert to WAV API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_convert_to_wav.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Convert to WAV, include:

- chosen model id
- source task and audio identifier summary
- callback setup summary
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query status or wait for webhook
