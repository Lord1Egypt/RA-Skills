---
name: poyo-vocal-remover-api
description: Separate vocals and instrument stems on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `separate-vocals`, `stem-split`, `upload-and-separate-vocals`, vocal remover workflows, stem isolation, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/vocal-remover-api","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Vocal Remover API

## PoYo Links

- Model page: <https://poyo.ai/models/vocal-remover-api>
- API docs: <https://docs.poyo.ai/api-manual/music-series/vocal-remover/separate-vocals>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for PoYo vocal-removal and stem-separation jobs. It helps agents choose the right model id, prepare payloads, submit async tasks, and explain callback or music detail retrieval.

## Use When

- The user explicitly wants to use PoYo with Vocal Remover, `separate-vocals`, `stem-split`, `upload-and-separate-vocals`, vocal isolation, instrumental extraction, or multi-stem audio separation.
- The user asks for a PoYo vocal-removal request payload, server-side curl command, integration notes, callback setup, or music result retrieval.
- The user has already chosen PoYo as the execution provider for an audio separation workflow.

## Model Selection

- `separate-vocals`: use when the user has a completed PoYo music task and needs a two-stem vocal/accompaniment split by `task_id` and `audio_id`.
- `stem-split`: use when the user has a completed PoYo music task and needs a multi-stem split by `task_id` and `audio_id`.
- `upload-and-separate-vocals`: use when the user has a public audio URL and wants to upload it directly for separation.

## Key Inputs

- For `separate-vocals` and `stem-split`, `task_id` and `audio_id` are required.
- For `upload-and-separate-vocals`, `audio_url` is required.
- `title` is optional for upload-based separation.
- `model_name` is optional for upload-based separation; documented values include `base`, `enhanced`, and `instrumental`.
- `output_type` is optional for upload-based separation; documented values include `general`, `bass`, `drums`, `other`, `piano`, `guitar`, and `vocals`.
- `callback_url` is useful for receiving completion results and separated-file URLs.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private audio URLs, generated stem URLs, callback URLs, task ids, audio ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic audio editing unless the user explicitly wants a PoYo Vocal Remover API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, model ids, request fields, examples, and result retrieval notes.
- Use `scripts/submit_vocal_remover_api.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with PoYo Vocal Remover API, include:

- chosen model id
- whether the workflow uses an existing PoYo music result or a public audio URL
- required `task_id` and `audio_id`, or required `audio_url`
- selected stem or output type when relevant
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query music detail or wait for webhook
