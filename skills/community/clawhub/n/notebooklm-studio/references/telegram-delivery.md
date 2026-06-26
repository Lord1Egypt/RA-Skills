# Telegram Delivery Contract

## Goal
Ensure generated artifacts are delivered to Telegram with proper formatting and compatibility.

## Audio post-processing
After downloading audio, always run ffmpeg compression:

- Primary profile: mono, 24kHz, 64kbps MP3
- Fallback profile (if file > 45MB): mono, 22.05kHz, 48kbps MP3
- Telegram Bot API file size limit: 50MB

Reference script: `scripts/compress_audio.sh`

## Delivery types

### Text message (report summary + status table)
- `action`: send
- `channel`: telegram
- `target`: chat_id
- `text`: markdown-formatted summary

### File attachment (audio, video, quiz, flashcards, slides, infographic, data table, mind map)
- `action`: send
- `channel`: telegram
- `target`: chat_id
- `filePath`: local file path
- `caption`: short description

## Delivery order

Delivery happens in two rounds to avoid agent timeouts on slow artifacts.

### Round 1 — Tier 1 (Immediate)
Delivered as soon as Tier 1 generation completes:

1. Text summary (report + status table) — always first
   - If Tier 2 artifacts are pending, include: "Slides/Audio/Video are still generating, I'll send them when ready."
2. Report (Markdown)
3. Quiz file (JSON/Markdown)
4. Flashcards file (JSON/Markdown)
5. Mind Map file (JSON)
6. Infographic (PNG) — send as **photo** for better preview
7. Data Table (CSV)

### Round 2 — Tier 2 (Deferred)
Delivered individually as each artifact completes (via `artifact wait`):

8. Slides file (PDF/PPTX) — typically first to complete (2-10 min)
9. Video (MP4) — 5-30 min
10. Audio (MP3) — 5-30 min, compress before sending

Each Tier 2 artifact is sent with a follow-up caption, e.g.:
- "[Follow-up] Slide deck for <topic>"
- "[Follow-up] Podcast audio for <topic>"

On failure or timeout, send a text message with the error reason.

Only deliver artifacts that were requested and successfully generated.

## Special considerations

### Video
- Telegram 50MB file size limit applies
- No compression script available — if oversized, warn user and suggest downloading from NotebookLM directly
- Send as video (not document) for inline preview

### Infographic
- Send as **photo** (not document) for better Telegram preview
- If file is too large for photo upload, fallback to document

### Data Table
- Send as document with `.csv` extension
- Caption should note "UTF-8 CSV — opens in Excel/Google Sheets"

## Delivery confirmation checklist

"Delivery" means calling OpenClaw's `message` tool (the built-in messaging tool available in the agent runtime). Each artifact delivery must be verified before moving on:

1. Call `message` tool to send text or file to Telegram
2. Check the response — success means a `messageId` was returned
3. If failed → retry once
4. If still failed → send a text notification to the user explaining which artifact failed and why. If this notification itself also fails, log the error and continue to the next artifact — do not loop.
5. Track delivery status per artifact: `delivered` | `failed`

**The task is not complete until every requested artifact has a final delivery status.** This prevents the agent from saying "done" when artifacts are still undelivered.

### Per-artifact delivery tracking

Initialize `./output/<slug>/delivery-status.json` at the start of delivery (Step 8) with all requested artifacts set to `pending`, then update as each delivery completes. This prevents status from being lost in long conversations or agent crashes:

```json
{
  "report.md": "delivered",
  "quiz.json": "delivered",
  "slides.pdf": "pending",
  "podcast.mp3": "pending"
}
```

Valid statuses: `pending` | `delivered` | `failed`

After every delivery attempt, print the full status table to keep it visible in the context window. Only report completion when every entry has a terminal status (`delivered` or `failed`).

## Failure handling
- If compression fails, return `error_code=FFMPEG_COMPRESS_FAILED`.
- If upload fails, return `error_code=TELEGRAM_UPLOAD_FAILED`.
- Audio/Video failure must NOT block text artifact delivery.
- Report all failures in the status table with reason.
