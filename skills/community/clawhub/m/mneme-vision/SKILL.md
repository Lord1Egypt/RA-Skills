---
name: visual-memory
description: Use local visual memory tools to index and search photos and videos from creator media libraries.
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - mcporter
    emoji: "🧠"
    homepage: https://mneme.nepa-ai.com
---

# Visual Memory

Use this skill when the user wants to index, search, organize, or inspect local
photo and video libraries.

When the user provides an uploaded photo/video/reel as an attachment, treat it
as temporary session context first. Use its local path to answer the current
question or run visual similarity search when appropriate. Do not call
`media_index` or otherwise add the attachment to durable visual memory unless
the user explicitly asks to add, save, index, catalog, or remember it.

Prefer `media_index` when the user points at a folder that has not been indexed.
Prefer `media_search` for natural-language searches such as finding shots,
finished videos, thumbnails, archive images, or clips matching a description.
Prefer `media_search_by_image` when the user provides an image and wants visually
similar items. Use `media_describe` when the user asks what is in a specific
media file.

Use `gpu_status` before GPU-heavy local tasks when the user is coordinating
video work, image generation, upscaling, VLM tagging, or another local model
process. Use `gpu_release` to unload resident Ollama models and hand VRAM to
that workflow, and use `gpu_reclaim` with the returned token when the workflow
is done. Use `gpu_evacuate` only when the user asks to free VRAM immediately
without creating a lease.

Return media results as previewable content cards when the host supports rich
output. Each result should include:

- `title`: filename or human-readable clip name.
- `kind`: image, video, audio, or unknown.
- `path`: absolute local path, kept available for copy/reveal actions.
- `reason`: short explanation for why this media matched.
- `timestamp` or `time_range`: when available for video/audio hits.
- `preview`: true when the file can be rendered by the host UI.

Mneme returns neutral `media_artifacts.v1` JSON. Preserve the host application's
native styling; do not introduce custom colors, cards, gradients, or branding
unless the host already provides that UI.

Do not dump long bare paths as the main answer. Put the path behind a `Copy path`
or equivalent action when rich output is available, and show the user the actual
image/video/audio preview first. When rich output is not available, use concise
Markdown links or a compact table with path values.

Do not invent matches when the tool returns none.

Do not upload local media to a cloud service unless the user explicitly asks for
that separate action.
