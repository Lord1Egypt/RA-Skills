# Artifact Format — progress.md

Created first, before any other work. Updated at the start and end of every phase.

```markdown
# Progress — <slug>

**Source:** <file path or "inline text">
**Slug:** <the derived slug — folder name and HTML filename>
**Author:** <@handle or "none">
**Mode:** <review | auto>
**Started:** <timestamp>

## Stages

phase1: pending
phase2: pending
phase3: pending
phase4: pending

## Decisions Log

<!-- Key decisions and AUTO checkpoint logs recorded here as execution proceeds -->
```

**Status values:** `pending` → `in-progress` → `done` / `awaiting-approval` / `approved` / `approved-auto`

**Update rule:** To change a phase status, find the line `phaseN: <old>` and replace only the status value.
Do not rewrite the entire Stages block. Example: `phase2: pending` → `phase2: in-progress`.
This format is intentionally simple — no table alignment, no padding — so any text replacement
operation can match it reliably.

**Source field:** The init script cannot know the source path — it is always a placeholder after script execution.
The model must update it in Phase 1 Step 4 with the actual file path or `"inline text"`.

**AUTO HITL log formats:**

HITL-1 (after Phase 2):

```
[AUTO] HITL-1: <N> slides
  Core thesis: "<thesis>"
  Slide jobs: Cover | <job2> | <job3> | ... | Conclusion
```

HITL-2 (after Phase 3):

```
[AUTO] HITL-2: <direction name> — <one-sentence reason>
```
