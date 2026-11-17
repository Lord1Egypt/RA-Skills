---
name: poyo-generate-lyrics
description: Generate song lyrics on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-lyrics`, lyric drafts, verses and choruses, theme-based songwriting, mood or genre guidance, music-generation preparation, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/generate-lyrics","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Generate Lyrics

## PoYo Links

- Model page: <https://poyo.ai/models/generate-lyrics>
- API docs: <https://docs.poyo.ai/api-manual/music-series/generate-lyrics>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill to turn a theme, mood, genre, or story direction into a PoYo `generate-lyrics` request and retrieve the resulting lyric text.

## Use When

- The user asks for generated lyrics, lyric ideas, verses, choruses, a song theme, or `generate-lyrics`.
- The output will feed a later Generate Music request.
- The workflow needs an async task, callback, or music-detail lookup.

## Key Inputs

- `model` must be `generate-lyrics`.
- `input.prompt` is required and should state the theme, mood, genre feel, language, or story direction.
- Keep the prompt within the current documented limit of 200 words.
- `callback_url` is optional and useful for production workflows.

## Security Rules

- Keep `POYO_API_KEY` server-side and out of browser code, repositories, logs, screenshots, and chat output.
- Do not include private customer information, unreleased lyrics, or confidential campaign text unless sharing it with PoYo is acceptable.
- Make live calls only when the user explicitly asks in a trusted environment.

## Execution

- Read `references/api.md` for the request and result flow.
- Use `scripts/submit_generate_lyrics.sh` with a reviewed payload file.
- Save the returned `task_id` and query music detail or wait for the callback.
- Treat generated lyrics as a draft that may need originality, rights, and policy review before publication.

## Output Expectations

Include the final prompt or payload summary, returned `task_id` when submitted, result retrieval method, and whether the lyrics will be passed into a music-generation workflow.
