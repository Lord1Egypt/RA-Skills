---
name: poyo-replace-section
description: Replace a section of generated music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `replace-section`, music section editing, infill_start_s, infill_end_s, task_id plus audio_id inputs, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/replace-section","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Replace Section

## PoYo Links

- Model page: <https://poyo.ai/models/replace-section>
- API docs: <https://docs.poyo.ai/api-manual/music-series/replace-section>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `replace-section` jobs on PoYo. It helps agents prepare music section replacement payloads, define an exact time range, submit async requests, and explain result retrieval.

## Use When

- The user explicitly wants to replace a section of an existing PoYo-generated music track.
- The user has a completed PoYo music `task_id` and `audio_id` and asks for an edit payload, server-side curl command, callback setup, or result retrieval.
- The user has already chosen PoYo as the execution provider for a music editing workflow.

## Model Selection

- `replace-section`: use for replacing a time range in a generated music track with new musical content.

## Key Inputs

- `task_id` identifies the completed source music generation task.
- `audio_id` identifies the specific audio track to edit.
- `prompt` describes the replacement content.
- `tags` describe style or mood for the replacement section.
- `title` names the resulting track.
- `infill_start_s` and `infill_end_s` define the section to replace in seconds.
- `full_lyrics` is required by the documented schema when the workflow modifies lyrics.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, lyrics, customer task ids, audio identifiers, generated file URLs, callback URLs, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music editing unless the user explicitly wants a PoYo Replace Section API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_replace_section.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Replace Section, include:

- chosen model id
- source task and audio identifier summary
- replacement time range
- prompt, title, style, and lyrics summary
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query status or wait for webhook
