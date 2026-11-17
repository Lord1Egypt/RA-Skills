---
name: poyo-extend-music
description: Extend existing music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `extend-music`, music continuation, audio_id based extension, custom style, title, prompt, continuation timing, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/extend-music","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Extend Music

## PoYo Links

- Model page: <https://poyo.ai/models/extend-music>
- API docs: <https://docs.poyo.ai/api-manual/music-series/extend-music>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `extend-music` jobs on PoYo. It helps agents continue an existing track from an `audio_id`, choose simple or custom mode, prepare a valid async payload, and explain result retrieval.

## Use When

- The user explicitly wants to extend existing music with PoYo, `extend-music`, an `audio_id`, a continuation point, or a custom style and title.
- The user asks for a PoYo Extend Music request payload, server-side curl command, integration notes, callback setup, or status retrieval.
- The user has already chosen PoYo as the execution provider for a music continuation workflow.

## Model Selection

- `extend-music`: use for extending or modifying an existing music track from a source audio identifier.

## Key Inputs

- `audio_id` identifies the existing source track.
- `mv` selects the documented music version for generation.
- `default_param_flag: false` uses simple mode.
- `default_param_flag: true` enables custom mode and requires `prompt`, `style`, `title`, and `continue_at`.
- `continue_at` sets the point in the source track where the extension begins.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, customer audio identifiers, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music generation unless the user explicitly wants a PoYo Extend Music API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_extend_music.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Extend Music, include:

- chosen model id
- simple or custom mode
- source audio identifier summary
- continuation timing and style summary when custom mode is used
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query status or wait for webhook
