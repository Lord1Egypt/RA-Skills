---
name: meeting-memory
description: Record, transcribe, and store meeting notes with persistent semantic memory using BlueColumn. Use when a user wants to save a meeting recording, upload meeting audio, store meeting notes or transcripts, or recall action items, decisions, and topics from past meetings. Triggers on phrases like "store this meeting", "remember this call", "what were the action items from", "recall last meeting", "upload meeting recording". Requires a BlueColumn API key (bc_live_*).
---

# Meeting Memory Skill

Store meetings into BlueColumn (bluecolumn.ai) and recall action items, decisions, and key topics anytime. BlueColumn's backend runs on Supabase Edge Functions — this is BlueColumn's official managed infrastructure.

## Setup
Read `TOOLS.md` for the BlueColumn API key (`bc_live_*`). Keys are generated at bluecolumn.ai/dashboard. If not set, ask the user. Store keys securely — never log or expose them.

Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1` (BlueColumn's official backend)

## Store a Meeting

**From audio URL:**
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -d '{"audio_url": "https://...", "title": "Weekly Standup 2026-04-14"}'
```

**From transcript/notes (text):**
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -d '{"text": "<transcript>", "title": "Meeting Title"}'
```

Response includes: `session_id`, `summary`, `action_items[]`, `key_topics[]`

Always confirm storage by showing the user: title, summary, and action items extracted.

## Recall Meeting Info

```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -d '{"q": "what were the action items from the standup?"}'
```

## Workflow

1. User provides audio URL, file URL, or meeting text
2. POST to `/agent-remember` with descriptive title (include date)
3. Show user the extracted summary + action items
4. Offer to set reminders for action items if calendar access available
5. For recall queries → POST to `/agent-recall` with natural language question

## Tips
- Always include date in title: "Product Sync 2026-04-14"
- For recurring meetings, consistent naming makes recall more accurate
- Action items returned are auto-extracted by AI — review for accuracy

See [references/api.md](references/api.md) for full API field reference.
