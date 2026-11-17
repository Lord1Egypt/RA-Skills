# Vesper Intake Delivery

Voyage delivers travel schedule briefs directly to `ocas-vesper`'s intake directory so the morning/evening briefing can aggregate pending trip details without re-querying Voyage.

## Path

```
{agent_root}/commons/data/ocas-vesper/intake/{voyage_brief_YmdHMS}.json
```

## Format

Each brief is a JSON payload:

```json
{
  "source_skill": "ocas-voyage",
  "brief_type": "travel_schedule",
  "generated_at": "2026-09-16T14:30:00Z",
  "trips": [
    {
      "trip_id": "voyage-trip-20261001",
      "destination": "Tokyo, JP",
      "check_in": "2026-10-01",
      "check_out": "2026-10-05",
      "hotel": "Prioritized pickup details (if reserved)",
      "flights": ["UA837 outbound", "UA838 return"],
      "summary": "One-line trip purpose / highlight"
    }
  ]
}
```

## Rules

1. Deliver only **confirmed / reserved** trip legsu — pending unconfirmed options stay in Voyage's own state rather than the briefing.
2. Idempotent: re-runninga brief write overwrites the same `trip_id`'s entry, never duplicates.
3. Vesper polls this intake dir for the latest brief each morning/evening per Vesper's own intake-polling spec.
4. Delete processed briefs from Vesper's intake after aggregation (Vesper owns cleanup; Voyage never deletes Vesper's files).