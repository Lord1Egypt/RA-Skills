---
name: poyo-minimax-music-2-6
description: MiniMax Music 2.6 generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `minimax-music-2.6`, complete music tracks, lyrics, lyrics optimization, instrumental mode, audio output settings, callbacks, and status polling.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/minimax-music-2-6","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo MiniMax Music 2.6

## PoYo Links

- Model page: <https://poyo.ai/models/minimax-music-2-6>
- API docs: <https://docs.poyo.ai/api-manual/music-series/minimax-music-2.6>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `minimax-music-2.6` jobs on PoYo. It helps agents prepare complete music-generation payloads, choose lyrics or instrumental mode, submit async tasks, and explain status retrieval.

## Use When

- The user explicitly wants to use PoYo with MiniMax Music 2.6, `minimax-music-2.6`, complete music generation, lyrics-based songs, lyrics optimization, or instrumental track generation.
- The user asks for a PoYo MiniMax Music 2.6 request payload, server-side curl command, integration notes, callback setup, or status polling.
- The user has already chosen PoYo as the execution provider for a MiniMax music workflow.

## Model Selection

- `minimax-music-2.6`: use for generating a complete audio track from a music prompt, optional lyrics, lyrics optimization, or instrumental mode.

## Key Inputs

- `prompt` is required and should describe style, mood, genre, instrumentation, tempo, vocal direction, or scene.
- `lyrics` is optional for vocal tracks and should be omitted for instrumental mode.
- `lyrics_optimizer` can be used when the user wants a vocal track but does not provide exact lyrics.
- `is_instrumental` should be `true` for instrumental-only music.
- `audio_setting` can set documented output sample rate, bitrate, and format.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private lyrics, customer prompts, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music generation unless the user explicitly wants a PoYo MiniMax Music 2.6 API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_minimax_music_2_6.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with MiniMax Music 2.6, include:

- chosen model id
- vocal, lyrics-optimized, or instrumental mode
- prompt and audio setting summary
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
