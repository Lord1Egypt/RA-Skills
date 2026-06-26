---
name: granola-direct-api
version: 1.0.3
description: >
  Access Granola meeting notes, summaries, transcripts, and attendees via the official
  Granola public REST API (public-api.granola.ai/v1). Use this skill when the user asks
  about meetings, meeting notes, Granola, wants to look up what was discussed, find
  meetings with a specific person, retrieve action items from a meeting, get a transcript,
  or search recent meeting history. Also trigger when the user mentions "Granola" by name,
  asks "what did we talk about in [meeting]", "who was in [meeting]", or wants to review
  meeting summaries. Requires a Granola API key (Business or Enterprise plan).
homepage: https://docs.granola.ai/introduction
permissions:
  - network
requires:
  - curl
  - jq
metadata:
  openclaw:
    primaryEnv: GRANOLA_API_KEY
    requirements:
      binaries:
        - curl
        - jq
      env:
        - GRANOLA_API_KEY
tags:
  - meetings
  - notes
  - granola
  - transcripts
  - api
---

# Granola Meeting Notes API

Read-only access to meeting notes, summaries, transcripts, and attendee info from the
official Granola REST API. See README.md for setup and API key configuration.

## Security and Data Handling

This skill is **read-only** — it cannot create, edit, or delete any data in Granola.

**Network access:** HTTPS requests only to `public-api.granola.ai`. No other domains
are contacted.

**Credential handling:** API key read from `GRANOLA_API_KEY` environment variable, passed only in the HTTP `Authorization` header. The skill itself does not write the key to disk at runtime. Credentials are handled securely via standard OpenClaw environment variables, and users should follow established best practices for secret management on their host environment.

**No external code execution:** Uses only `curl` and `jq`. No downloads, no scripts,
no binaries.

## Authentication

```
-H "Authorization: Bearer $GRANOLA_API_KEY"
```

If the user gets a 401 error, the key is missing or invalid. Direct them to README.md
for setup instructions.

## Base URL

```
https://public-api.granola.ai/v1
```

## Rate Limits

Burst: 25 requests per 5 seconds. Sustained: 5 req/sec (300/min).
On 429, back off a few seconds and retry.

## Important Behaviors

- Only notes with a **completed AI summary and transcript** are returned. Notes still
  processing or never summarized are excluded (List omits them; Get returns 404).
- Note IDs follow the pattern `not_[a-zA-Z0-9]{14}` (e.g., `not_1d3tmYTlCICgjy`).

---

## Endpoints

### 1. List Notes

```
GET /v1/notes
```

**Query parameters:**

| Parameter        | Type              | Default | Description                                    |
|------------------|-------------------|---------|------------------------------------------------|
| `page_size`      | integer (1–30)    | 10      | Max notes per page                             |
| `created_after`  | ISO 8601 date/datetime | —  | Notes created after this date                  |
| `created_before` | ISO 8601 date/datetime | —  | Notes created before this date                 |
| `updated_after`  | ISO 8601 date/datetime | —  | Notes updated after this date                  |
| `cursor`         | string            | —       | Pagination cursor from previous response       |

**Example:**

```bash
curl -s "https://public-api.granola.ai/v1/notes?page_size=20&created_after=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)" \
  -H "Authorization: Bearer $GRANOLA_API_KEY" | jq .
```

> On macOS, replace `-d '7 days ago'` with `-v-7d`.

**Response:**

```json
{
  "notes": [
    {
      "id": "not_1d3tmYTlCICgjy",
      "object": "note",
      "title": "Weekly sync with engineering",
      "owner": { "name": "Jane Smith", "email": "jane@example.com" },
      "created_at": "2026-04-14T15:30:00Z",
      "updated_at": "2026-04-14T16:45:00Z"
    }
  ],
  "hasMore": true,
  "cursor": "eyJjcmVkZW50aWFsfQ=="
}
```

When `hasMore` is `true`, pass the `cursor` value to fetch the next page.

---

### 2. Get a Single Note

```
GET /v1/notes/{note_id}
```

**Path parameter:** `note_id` (required, pattern: `not_[a-zA-Z0-9]{14}`)

**Query parameter:**

| Parameter | Type           | Description                              |
|-----------|----------------|------------------------------------------|
| `include` | `"transcript"` | Include the full transcript in response  |

**Example:**

```bash
curl -s "https://public-api.granola.ai/v1/notes/not_1d3tmYTlCICgjy?include=transcript" \
  -H "Authorization: Bearer $GRANOLA_API_KEY" | jq .
```

**Response:**

```json
{
  "id": "not_1d3tmYTlCICgjy",
  "object": "note",
  "title": "Weekly sync with engineering",
  "owner": { "name": "Jane Smith", "email": "jane@example.com" },
  "created_at": "2026-04-14T15:30:00Z",
  "updated_at": "2026-04-14T16:45:00Z",
  "calendar_event": {
    "event_title": "Weekly sync with engineering",
    "invitees": [{ "email": "bob@example.com" }],
    "organiser": "jane@example.com",
    "scheduled_start_time": "2026-04-14T15:30:00Z",
    "scheduled_end_time": "2026-04-14T16:30:00Z"
  },
  "attendees": [
    { "name": "Jane Smith", "email": "jane@example.com" },
    { "name": "Bob Chen", "email": "bob@example.com" }
  ],
  "folder_membership": [
    { "id": "fol_4y6LduVdwSKC27", "object": "folder", "name": "Engineering" }
  ],
  "summary_text": "Discussed sprint progress and blockers. Decided to push the release to next week.",
  "summary_markdown": "## Weekly Sync\n\n- Sprint progress reviewed\n- Release pushed to next week",
  "transcript": [
    {
      "speaker": { "source": "microphone" },
      "text": "Let's start with the sprint update.",
      "start_time": "2026-04-14T15:30:12Z",
      "end_time": "2026-04-14T15:30:18Z"
    },
    {
      "speaker": { "source": "speaker" },
      "text": "We're about two days behind on the auth module.",
      "start_time": "2026-04-14T15:30:20Z",
      "end_time": "2026-04-14T15:30:28Z"
    }
  ]
}
```

**Key response fields:**

| Field               | Description                                                      |
|---------------------|------------------------------------------------------------------|
| `summary_text`      | Plain-text AI summary                                            |
| `summary_markdown`  | Markdown-formatted AI summary (may be null)                      |
| `attendees`         | Array of `{ name, email }` for meeting participants              |
| `calendar_event`    | Calendar metadata: title, invitees, organiser, scheduled times   |
| `folder_membership` | Folders the note belongs to                                      |
| `transcript`        | Speaker segments with `text`, `start_time`, `end_time`           |

**Transcript speaker sources:** `"microphone"` = local user, `"speaker"` = other
participants via meeting audio.

---

## Error Handling

| Status | Meaning                    | Action                                       |
|--------|----------------------------|----------------------------------------------|
| 401    | Invalid or missing API key | Check `GRANOLA_API_KEY` is set and valid      |
| 404    | Note not found             | Note may still be processing, or ID is wrong  |
| 429    | Rate limit exceeded        | Wait a few seconds and retry                  |
| 500    | Server error               | Retry after a brief delay                     |

---

## Workflow Recipes

### Find meetings from the last N days

```bash
DAYS=7
curl -s "https://public-api.granola.ai/v1/notes?page_size=30&created_after=$(date -u -d "${DAYS} days ago" +%Y-%m-%dT%H:%M:%SZ)" \
  -H "Authorization: Bearer $GRANOLA_API_KEY" | jq '.notes[] | {id, title, created_at}'
```

### Find meetings with a specific person

```bash
NOTE_IDS=$(curl -s "https://public-api.granola.ai/v1/notes?page_size=30&created_after=$(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)" \
  -H "Authorization: Bearer $GRANOLA_API_KEY" | jq -r '.notes[].id')

for ID in $NOTE_IDS; do
  RESULT=$(curl -s "https://public-api.granola.ai/v1/notes/$ID" \
    -H "Authorization: Bearer $GRANOLA_API_KEY")
  if echo "$RESULT" | jq -e '.attendees[]? | select(.name // "" | test("Bob"; "i"))' > /dev/null 2>&1; then
    echo "$RESULT" | jq '{id, title, created_at, attendees: [.attendees[].name]}'
  fi
done
```

### Get the AI summary

```bash
curl -s "https://public-api.granola.ai/v1/notes/not_XXXXXXXXXXXXXX" \
  -H "Authorization: Bearer $GRANOLA_API_KEY" | jq '.summary_markdown // .summary_text'
```

### Get full transcript

Only request when the user needs verbatim content — transcripts are large.

```bash
curl -s "https://public-api.granola.ai/v1/notes/not_XXXXXXXXXXXXXX?include=transcript" \
  -H "Authorization: Bearer $GRANOLA_API_KEY" | jq '.transcript[] | "\(.speaker.source): \(.text)"'
```

---

## Tips

- Use `summary_text` / `summary_markdown` for overviews. Only use `include=transcript`
  when the user needs the full conversation.
- The API has **no search endpoint**. To find meetings by topic, list recent notes and
  scan titles/summaries client-side.
