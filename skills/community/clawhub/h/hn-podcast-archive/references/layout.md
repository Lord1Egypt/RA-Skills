# Archive layout

Expected output tree:

```text
<output-dir>/
  audio/
  transcripts/
  episodes/
  state.json
  run-log.jsonl
  index.md
```

## File roles

### `audio/`
Original downloaded episode files. Keep original extension when practical.

### `transcripts/`
Plain-text transcript output from Whisper. Name should align with episode slug.

### `episodes/`
One markdown file per episode with frontmatter-style metadata section and links to local artifacts.

### `state.json`
Machine-readable dedupe state. Store processed GUIDs / enclosure URLs / hashes as needed.

### `run-log.jsonl`
Append-only operational log, one JSON object per line.

### `index.md`
Human-friendly archive index sorted newest first.

## Markdown archive shape

Suggested per-episode markdown:

```markdown
# <episode title>

- Published: <iso or source date>
- GUID: <guid>
- Audio URL: <url>
- Audio File: `audio/<file>`
- Transcript File: `transcripts/<file>`

## Transcript

<transcript text>
```

## Idempotency strategy

Treat `guid` as primary identifier when present; fall back to enclosure URL, then episode link/title combination.
