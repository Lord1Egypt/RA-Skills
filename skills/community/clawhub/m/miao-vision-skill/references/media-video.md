# Data Story Video Workflow

Use this workflow only after an explicit `$miao-vision` request for a data-story video or dynamic explanation. The video supplements an evidence-backed artifact; it is not evidence.

## 1. Define One Continuous Shot

Use the same source priority as the image workflow: verified delivery, current verified evidence, locally analyzed data, then user-authored description. Explain exactly one verified trend, structure, process, comparison, or ranking relationship.

The final prompt must specify the starting state, visible transformation, ending state, camera movement, rhythm, and exclusions. Create one continuous shot only. Do not request cuts, montage, subtitles, narration, dialogue, music, chart labels, numbers, logos, or additional conclusions.

Default to 8 seconds, `1280x720`, and `16:9`. Accept an explicit integer duration from 4 through 15 seconds. Use `9:16` only when the user clearly requests portrait output. `standard` uses the configured fast model; `high` uses the configured high-quality model without changing other parameters.

## 2. Select Text-to-Video or Image-to-Video

Text-to-video is the default. Accept at most one local absolute PNG, JPEG, or WebP reference, no larger than 30 MB, only when it is a no-text illustration, photo, or user-approved visual scene.

Never upload a Miao Vision screenshot or other image containing exact charts, numbers, tables, labels, or body copy for a video model to redraw. Switch to text-to-video after translating its verified aggregate relationship into a scene, or ask for one text-free reference image. Validate real MIME content, not the extension, and reject remote/data URLs before a remote request.

## 3. Consent, Generate, and Deliver

Run `scripts/check-ai-media.mjs video standard` or `high`. Present the model tier, duration, resolution, ratio, one-video count, live catalog pricing summary, final prompt, and upload scope. Explain that prompt/reference content is sent through Vercel AI Gateway to the model provider. Ask for explicit confirmation for this request.

After confirmation, write the schema-version-1 request and invoke `scripts/run-ai-media.mjs` with absolute request/output paths and `--confirm-remote`. Do not put a model ID in the request. Deliver an inline video preview when supported, otherwise a local MP4 link, plus `media-generation.json`.

If the video invents numbers or text, say they are not data evidence and direct the user to the verified report. A failed video must not affect its source report or a successful image.
