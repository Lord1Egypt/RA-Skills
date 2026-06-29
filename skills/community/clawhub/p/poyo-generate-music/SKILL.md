---
name: poyo-generate-music
description: Generate Music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-music`, AI music generation, background tracks, soundtrack drafts, instrumental songs, custom mode, music callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/music-series/generate-music","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Generate Music

Use this skill for `generate-music` jobs on PoYo. It helps agents prepare music generation payloads, choose simple or custom mode, submit async tasks, and explain callback or music detail retrieval.

## Use When

- The user mentions PoYo music generation, `generate-music`, soundtrack drafts, background tracks, instrumental music, song ideas, or custom music prompts.
- The workflow needs a PoYo music payload, async task submission, a callback URL, or result retrieval guidance.
- The user wants server-side curl or shell examples for PoYo music generation.

## Model Selection

- `generate-music`: use for text-driven music generation through PoYo's music API.

## Key Inputs

- `prompt` is required for simple mode and for custom mode with vocals.
- `custom_mode` controls whether the request uses only a compact prompt or explicit style/title fields.
- `instrumental` controls whether the generated track should omit vocals.
- `style` and `title` are required in custom instrumental mode.
- `mv` selects the documented music model version.
- `negative_tags` and `style_weight` are optional controls when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not log private lyrics, private customer prompts, callback URLs, or generated audio URLs unless the product policy allows it.

## Execution

- Read `references/api.md` for endpoint details, request fields, example payloads, and result retrieval notes.
- Use `scripts/submit_generate_music.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Generate Music, include:

- chosen model id
- simple mode or custom mode choice
- instrumental or vocal intent
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query music detail or wait for webhook
