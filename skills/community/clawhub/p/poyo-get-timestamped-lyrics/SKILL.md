---
name: poyo-get-timestamped-lyrics
description: Retrieve timestamped lyrics on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `get-timestamped-lyrics`, synchronized lyrics, word timing, waveform data, task_id plus audio_id inputs, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/get-timestamped-lyrics","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Get Timestamped Lyrics

## PoYo Links

- Model page: <https://poyo.ai/models/get-timestamped-lyrics>
- API docs: <https://docs.poyo.ai/api-manual/music-series/get-timestamped-lyrics>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `get-timestamped-lyrics` jobs on PoYo. It helps agents prepare synchronized-lyrics payloads from a generated music track, submit async requests, and explain timing results.

## Use When

- The user explicitly wants timestamped or synchronized lyrics for a PoYo-generated music track.
- The user has a completed PoYo music `task_id` and `audio_id` and asks for a request payload, server-side curl command, callback setup, or result retrieval.
- The user has already chosen PoYo as the execution provider for a lyrics timing workflow.

## Model Selection

- `get-timestamped-lyrics`: use for retrieving lyric timing and waveform data from a generated music track.

## Key Inputs

- `task_id` identifies the completed source music generation task.
- `audio_id` identifies the specific audio track.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private lyrics, customer task ids, audio identifiers, waveform data, callback URLs, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic lyric analysis unless the user explicitly wants a PoYo Get Timestamped Lyrics API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_get_timestamped_lyrics.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` or timing response clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Get Timestamped Lyrics, include:

- chosen model id
- source task and audio identifier summary
- final payload or concise parameter summary
- returned `task_id` or timing response if a request was actually submitted
- next step: query status or wait for webhook
