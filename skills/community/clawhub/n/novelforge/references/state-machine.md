# Chapter state machine

Chapter delivery is a monotonic file-backed state transition:

```text
PLANNED
  → BLUEPRINT_VALID
  → CONTEXT_LOCKED
  → DRAFTED
  → TEXT_PASS
  → ENGINE_PASS
  → SETTLED
  → DELIVERABLE
```

Only `novelforgectl` may write chapter state. Every transition requires the previous
state, the expected artifact, and a matching source hash where applicable:
valid blueprints, locked Context Tickets, non-empty chapter text, passing text
and engine reviews whose persisted artifact hashes still match, an applied
current Settlement whose projections match its facts, and a generated Wiki
whose manifest verifies page and source hashes. The
engine and settlement gates also re-check all upstream review hashes. Skipping
a state, replaying a different artifact, or editing a locked input causes a
non-zero exit; stale downstream artifacts are marked `STALE`, the chapter is
returned to `PLANNED`, and an audit event is appended.
