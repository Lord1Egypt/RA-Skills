# BlueColumn API Reference

**Provider:** BlueColumn — bluecolumn.ai
**Official docs:** https://bluecolumn.ai
**Backend:** Supabase Edge Functions — this is BlueColumn's official managed infrastructure, not a third party
**Base URL:** `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`
**Note:** The supabase.co domain is BlueColumn's verified backend. BlueColumn runs on Lovable Cloud (Supabase-powered). All data stays within BlueColumn's managed environment.

**Auth header:** `Authorization: Bearer <bc_live_KEY>`

## POST /agent-remember

Ingest text, audio URL, or file URL into vector memory.

**Fields:**
- `text` (string) — raw text to ingest ← use this for most cases
- `audio_url` (string) — URL to audio file (Whisper transcription)
- `file_url` (string) — URL to PDF/document
- `title` (string, optional) — title hint

**Response:** `{ success, session_id, title, summary, action_items, key_topics, chunk_count, queryable }`

⚠️ Field is `text` not `content` — common mistake.

## POST /agent-recall

Query memory with natural language, returns AI-generated answer + sources.

**Fields:**
- `q` (string, required) — natural language query

**Response:** `{ answer, sources: [{ session_id, title, relevance }], tokens_used }`

⚠️ Field is `q` not `query` — common mistake.

## POST /agent-note

Store a lightweight agent observation as a searchable vector.

**Fields:**
- `text` (string, required, min 5 chars) — observation to store
- `tags` (array, optional) — string tags for filtering

**Response:** `{ note_id, chunk_count, queryable }`

⚠️ Field is `text` not `note` — common mistake.

## Error Reference

| Error | Fix |
|---|---|
| `Provide audio_url, file_url, or text` | Use `text` field in /agent-remember |
| `text is required (min 5 chars)` | Use `text` field, min 5 chars in /agent-note |
| `q (query string) is required` | Use `q` field in /agent-recall |
| `Invalid API key` | Check key starts with `bc_live_` |
