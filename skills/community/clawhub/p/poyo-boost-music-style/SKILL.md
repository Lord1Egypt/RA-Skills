---
name: poyo-boost-music-style
description: Expand concise music-style ideas on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `boost-music-style`, music prompt enhancement, genre and mood expansion, instrumentation direction, production descriptors, Generate Music preparation, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/boost-music-style","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Boost Music Style

## PoYo Links

- Model page: <https://poyo.ai/models/boost-music-style>
- API docs: <https://docs.poyo.ai/api-manual/music-series/boost-music-style>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill to expand a compact genre, mood, instrument, or production idea into a richer style description for a later music-generation request.

## Use When

- The user mentions `boost-music-style`, music prompt enhancement, richer style tags, instrumentation direction, or production characteristics.
- A basic style such as "cinematic, tense, orchestral" needs more useful music-generation detail.
- The workflow needs async submission, callback handling, or music-detail retrieval.

## Key Inputs

- `model` must be `boost-music-style`.
- `input.content` is required and should contain concise genre, mood, instrument, tempo, or production keywords.
- `callback_url` is optional and useful for production workflows.

## Security Rules

- Keep `POYO_API_KEY` server-side and out of browser code, public repositories, logs, screenshots, and chat output.
- Do not include confidential campaign directions or private customer data unless sharing it with PoYo is acceptable.
- Make live calls only when explicitly requested in a trusted environment.

## Execution

- Read `references/api.md` for request and result handling.
- Use `scripts/submit_boost_music_style.sh` with a reviewed payload file.
- Save the returned `task_id`, then query music detail or wait for the webhook.
- Review the enhanced description before using it in Generate Music; keep only details that match the user's intent.

## Output Expectations

Include the source style idea, final payload or parameter summary, returned `task_id` when submitted, result retrieval method, and how the enhanced description should feed the next music-generation step.
