---
name: idea-vault
description: Save and organize links, notes, and timestamps into a searchable Idea Vault. Use when a user drops a YouTube/web link (or just notes), then says “/vault” or “vault” to save; also use for vault queries like “what did I save this week?”, channel/source filters, and keyword search in notes.
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":"IDEA_VAULT_TRANSCRIPTAPI_KEY"}}
---

# Idea Vault (Public)

A lightweight capture → organize → retrieve workflow.

## Goal

Turn messy chat drops (links + rough notes + timestamps) into structured markdown entries and a searchable index.

## One-time setup (required)

Run this once after cloning the skill so OpenClaw can execute it reliably:

```bash
cd ~/.openclaw/skills/idea-vault
python3 --version
python3 -m pip install -r requirements.txt
```

Environment setup (recommended):

```bash
cp .env.example .env
# then set IDEA_VAULT_TRANSCRIPTAPI_KEY and IDEA_VAULT_DIR in your shell/env manager
```

Notes:
- Python 3 is required.
- `requests` from `requirements.txt` is required.
- `IDEA_VAULT_TRANSCRIPTAPI_KEY` is strongly recommended for reliable YouTube transcripts.
- `yt-dlp` is optional fallback for some videos/environments.

## Privacy and network behavior

This skill can make outbound network calls to:
- `youtube.com` (video/transcript fallback paths)
- `transcriptapi.com` (when `IDEA_VAULT_TRANSCRIPTAPI_KEY` is set)
- source/asset URLs included in captured messages

Security notes:
- The helper uses `subprocess.run([...], shell=False)` for `yt-dlp` (no shell string execution).
- Do not use this skill with sensitive private chat content unless you are comfortable with these external calls.
- Keep API keys in environment variables only; never commit secrets.

## Inputs supported

- YouTube links + notes + optional timestamps
- Web links + notes
- Note-only captures (no link)

## Recommended path setup (portable)

Use an environment variable or local default path:

```bash
VAULT_DIR="${IDEA_VAULT_DIR:-$HOME/workspace/idea-vault}"
CACHE_DIR="$VAULT_DIR/_cache"
```

## Core flow (triggered by `/vault` or `vault`)

1) Read recent messages in the current chat.
2) Extract the newest capture block.
3) If source is YouTube, fetch transcript + optional clips around timestamps.
4) Write summary/elaboration/tags/associations.
5) Upsert into vault (append addendum on duplicate URL/video).

## Commands

### Extract capture

```bash
python3 ./scripts/idea_vault.py extract --user-id <author.id> --fallback-messages 30 < messages.json > capture.json
```

### Fetch transcript (YouTube only)

Preferred source is TranscriptAPI via `IDEA_VAULT_TRANSCRIPTAPI_KEY`.

```bash
python3 ./scripts/idea_vault.py fetch --cache-dir "$CACHE_DIR" < capture.json > youtube.json
```

### Save / upsert entry

```bash
python3 ./scripts/idea_vault.py upsert --vault-dir "$VAULT_DIR" < save_request.json > saved.json
```

### Query vault

```bash
python3 ./scripts/idea_vault.py query --vault-dir "$VAULT_DIR" --limit 50
python3 ./scripts/idea_vault.py query --vault-dir "$VAULT_DIR" --since 2026-03-01
python3 ./scripts/idea_vault.py query --vault-dir "$VAULT_DIR" --channel "podcast" --text "pricing"
```

### Annotate latest entry

```bash
python3 ./scripts/idea_vault.py annotate --vault-dir "$VAULT_DIR" --last --star true --priority high --add-tag actionable
```

## save_request.json shape

```json
{
  "capture": {"...": "from extract"},
  "source": {
    "kind": "youtube|web|note",
    "url": "https://... (optional)",
    "title": "string (optional)",
    "author": "string (optional)",
    "id": "string (optional)",
    "transcript_txt": "/path/to/transcript.txt (youtube only, optional)",
    "transcript_json": "/path/to/raw.json (youtube only, optional)",
    "clips": [{"center_sec": 123, "window_sec": 60, "text": "..."}]
  },
  "summary": "string",
  "elaboration": "string",
  "tags": ["tag"],
  "associations": [{"timestamp_sec": 1461, "note": "..."}]
}
```

## Output layout

Under `VAULT_DIR`:

- `entries/YYYY/YYYY-MM-DD__<slug>__[<suffix>].md`
- `transcripts/YYYY/<id>.transcript.txt` (YouTube only)
- `assets/YYYY/MM/*` (optional attachments)
- `index.json`
- `_cache/`

## Agent response style after save

Reply with:

- title + link
- 3–6 concise bullets
- relevant clips for flagged timestamps (if present)
- saved file path
