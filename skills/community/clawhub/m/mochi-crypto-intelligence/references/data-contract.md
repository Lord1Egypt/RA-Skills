# Local event contract and incremental state

Use a user-owned task workspace, not the installed Skill folder. `collect` output is candidate material; research and source reads must happen before constructing `events.json`. The helper makes no AI request and has no independent claim-verification capability.

Example format (fictional; replace it with actual researched facts and links):

```json
{
  "events": [{
    "event_key": "example-project-proposal-123",
    "project": "Example Project",
    "chain": "Example Network",
    "title": "A proposed change",
    "summary": "The forum author proposes a change; a vote has not occurred.",
    "stage": "proposed",
    "evidence": "primary",
    "published_at": "2026-10-20",
    "event_at": null,
    "impact": "A conditional interpretation, not an established price effect.",
    "uncertainties": ["No execution date has been confirmed."],
    "sources": [{
      "url": "https://example.org/proposals/123",
      "publisher": "Example official governance forum",
      "checked_at": "2026-10-21T00:00:00Z",
      "supports": "A proposal was posted; no claim of approval or execution."
    }]
  }]
}
```

Allowed stages: `rumor`, `proposed`, `announced`, `scheduled`, `executed`, `cancelled`, `disputed`.
Evidence labels: `unverified`, `attributed`, `primary`, `corroborated`, `disputed`; definitions are in research-method.md. The script validates the labels but cannot decide whether they are justified. Retain the original qualified source claim in `supports`.

`published_at` and `event_at` accept ISO8601 with timezone or `YYYY-MM-DD` if only a date is known; unknown is null. Source `checked_at` must be a timezone-aware timestamp. Never relabel retrieval time as original publication time. User-facing ambiguous date text should stay in an additional note, rather than asserting an exact event time.

Preview with `ingest` before `--commit`. State JSON has a schema version, event keys, fingerprints, first-seen/last-changed timestamps and prior versions. Material summary/stage/evidence/source changes produce an update; refreshing a check timestamp or reordering the same sources does not. Rewording a summary can create an update, so preserve wording when no underlying fact changed. The same event repeated under a different key appears new; event identity is the researcher's responsibility.

Existing history is backed up before an atomic replacement. Concurrent commits are rejected by a sidecar `.lock`; inspect an interrupted lock and running process before removing it. A partial scan never deletes absent events. No retention purge is performed. Malformed input or unsupported state is rejected without replacing the existing state. Reports and caches remain local unless the user explicitly requests sharing them.
