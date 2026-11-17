# Vesper Emit Format for Sands

Used by: `sands.brief`

---

## Delivery Path

Write file to:
the `briefing` payload field in the journal entry

Format: InsightProposal schema (spec-ocas-shared-schemas.md).

---

## Top-Level Schema

```json
{
  "proposal_id": "prop_{hash}",
  "proposal_type": "{see Proposal Type Rules below}",
  "description": "[SANDS BRIEF: EVENING | MORNING] {YYYY-MM-DD}",
  "confidence_score": 1.0,
  "supporting_entities": [],
  "supporting_relationships": [],
  "predicted_outcome": null,
  "suggested_follow_up": "{schedule payload — JSON-encoded string; see suggested_follow_up Payload below}",
  "target_skill": null,
  "created_at": "{ISO 8601}"
}
```

### Proposal Type Rules

| Brief type | `proposal_type` |
|---|---|
| Evening (next day) | `routine_prediction` |
| Morning (today) | `preparation_checklist` |

If `preparation_checklist` is not yet in the InsightProposal schema enum, use
`actionable_insight` as a fallback, or request the type be added to
`spec-ocas-shared-schemas.md`.

---

## `suggested_follow_up` Payload

The `suggested_follow_up` field carries the full schedule payload as a JSON-encoded string.
Vesper must JSON-parse this field to obtain the structured schedule data.
The InsightProposal schema defines this field as `string|null`; encoding the payload as a
string satisfies the type contract while allowing Vesper to carry structured schedule data
through the standard journal briefing payload.

```json
{
  "brief_type": "evening | morning",
  "target_date": "YYYY-MM-DD",
  "summary_note": "2-3 sentence narrative characterizing the day.",
  "day_overview": {
    "total_events": 5,
    "first_event": "HH:MM",
    "last_event": "HH:MM",
    "free_hours": 3.5,
    "prep_items_count": 2
  },
  "events": [
    {
      "title": "string",
      "start": "HH:MM",
      "end": "HH:MM",
      "location": "string | null",
      "calendar": "personal | family",
      "htmlLink": "string  // Google Calendar event.htmlLink from the API, so the briefing can deep-link to the event",
      "all_day": false,
      "conflict": false,
      "conflict_note": "string | null",
      "prep_required": false,
      "prep_note": "string | null",
      "travel_before": false,
      "travel_minutes": null
    }
  ],
  "work_busy_blocks": [
    { "start": "HH:MM", "end": "HH:MM" }
  ],
  "conflicts_detected": 0,
  "prep_items_count": 0
}
```

---

## Evening Brief Rules

- Include all events for the next day
- `summary_note`: 2-3 sentences characterizing the day, flag anything unusual
- `day_overview`: populate all fields based on the full event list
- Set `conflict: true` and populate `conflict_note` for any conflicts found
- Set `prep_required: true` for events matching preparation signals
- Include `work_busy_blocks` as unavailability overlay (no titles)

## Morning Brief Rules

- Include ALL events in the `events` array (not just prep items)
- Highlight prep items with `prep_required: true`; Vesper renders these distinctly
- `prep_note` should be action-oriented: "Review the agenda", "Confirm reservation"
- `day_overview`: populate all fields for a quick at-a-glance summary
- `summary_note` should combine overview with prep focus: "You have 5 events today from
  9:00 to 5:00, with about 3.5 free hours. 2 items need preparation."
- Include `work_busy_blocks` as unavailability overlay

## Event deep-links (added 2026-06-25)
Each event MUST include `htmlLink` — the `htmlLink` field returned by the Google Calendar API for that event. The briefing email renders the event title as a clickable (non-blue) link to it. If an event was created from / references an email, also include `email_link` (the Gmail message URL).
