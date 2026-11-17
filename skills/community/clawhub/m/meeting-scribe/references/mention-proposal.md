# Mention proposal shape

Every mention `meeting-scribe` extracts from a transcript, matched or not, is expressed as one JSON
object with this shape. This is a portability contract: a future platform/brain version of this skill
consumes the exact same shape, so treat field names and the `matched` enum as fixed.

```json
{
  "entity_type": "person",
  "entity_name": "Jordan Lee",
  "matched": "exact",
  "candidates": [],
  "quote": "Jordan mentioned they'd have the updated forecast by Friday.",
  "meeting_date": "2026-08-14",
  "meeting_source": "meetings/2026-08-14-q3-check-in.md",
  "follow_ups": [
    {
      "action": "send the updated forecast",
      "owner": "Jordan Lee",
      "due": "2026-08-21"
    }
  ]
}
```

## Fields

- `entity_type` — one of `person`, `organization`, `meeting`. Matches the entity folder taxonomy.
- `entity_name` — the name as it appears in the entity file's `name` field (or the raw transcript name
  if unmatched).
- `matched` — one of:
  - `exact` — matched an entity file's `name` field.
  - `alias` — matched one of an entity file's `aliases` entries.
  - `none` — no entity file matched; this is a proposed new entity. No file is written for it.
  - `ambiguous` — matched more than one entity file. No mention line is written for it.
- `candidates` — populated only when `matched` is `ambiguous`. A list of the entity file paths (or
  names) that all matched, so a human can disambiguate.
- `quote` — a direct quote from the transcript that grounds the mention. Required for every object
  regardless of `matched` value. No quote, no mention — see `SKILL.md`'s Error handling section.
- `meeting_date` — the date of the meeting the transcript covers, `YYYY-MM-DD`.
- `meeting_source` — path to the meeting note this mention came from.
- `follow_ups` — zero or more commitments tied to this entity from the meeting, each with `action`,
  `owner` (a name, or the literal string `"owner?"` when the transcript doesn't state one), and `due`
  (a date, or empty when not stated).

## Why this exists

The skill in this repo is files-first: it writes markdown, not JSON. But the same identify /
match / propose / flag logic is the shape a future platform version (writing to a brain/DB instead of
markdown files) would need to consume. Freezing this shape now means that future version can read the
same proposals this skill's reasoning produces, without re-deriving the extraction logic.
