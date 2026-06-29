# Changelog

Release history for music-craft. Operating guidance lives in the topic
references; this file is history only.

## v1.5.0

v1.5.0 is a **breaking change** that aligns the base skill with
`music-craft-minimax` v1.5.0: both skills are now audio-only.

**Changed:**
- "When to redirect to music-craft-minimax" no longer mentions
  "audio download from YouTube, JioSaavn, or other URL"
- Audio input must be a local file path; URLs are not accepted
- Image free-tool flow removed (album art / OCR / face / VLM are gone)
- `references/input-workflows.md` deletes Input Type 4 (YouTube URL)
  and Input Type 8 (image)
- `references/free-tool-inputs.md` deletes the `image` tool section
  and the YouTube/JioSaavn download rows
- `references/quality-and-revision.md` deletes the LRCLib "Web Lyrics
  Lookup" subsection

**Companion private skill:**
- `publish/music-source-fetch/` is a new unpublished skill that holds
  the YouTube/JioSaavn/mx3.ch/LRCLib download code Luis uses personally.
  It is never `clawhub publish`-ed.
