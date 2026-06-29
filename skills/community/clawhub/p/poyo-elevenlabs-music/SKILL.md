---
name: poyo-elevenlabs-music
description: Generate music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `elevenlabs-music`, text-to-music, instrumental music, structured composition plans, section timing, audio output formats, async task submission, callbacks, and task status retrieval.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/music-series/elevenlabs-music","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo ElevenLabs Music

Use this skill for `elevenlabs-music` jobs on PoYo. It helps agents prepare text-to-music or structured composition-plan payloads, submit async tasks, and explain result retrieval through PoYo task status.

## Use When

- The user mentions PoYo ElevenLabs Music, `elevenlabs-music`, text-to-music, instrumental tracks, composition plans, section timing, or music output formats.
- The workflow needs a PoYo music payload, async task submission, a callback URL, or task status retrieval guidance.
- The user wants server-side curl or shell examples for PoYo music generation.

## Model Selection

- `elevenlabs-music`: use for PoYo music generation from either a text brief or a structured composition plan.

## Key Inputs

- `text` is the single-brief path. Use it for natural-language music descriptions.
- `composition_plan` is the structured path. Use it for section-level arrangement control.
- Send exactly one of `text` or `composition_plan`.
- `duration` and `is_instrumental` are only valid with `text`.
- `respect_sections_durations` is only valid with `composition_plan`.
- `output_format` controls the returned audio format.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not log private prompts, lyrics, callback URLs, task ids, or generated audio URLs unless the product policy allows it.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_elevenlabs_music.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with ElevenLabs Music, include:

- chosen model id
- text brief or composition-plan path
- instrumental and duration choices when applicable
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query task status or wait for webhook
