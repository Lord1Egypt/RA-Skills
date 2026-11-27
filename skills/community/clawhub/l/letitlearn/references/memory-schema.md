# LetItLearn Memory Schema

## Contents

- Overview
- Identity
- Research agenda
- Learning diary
- Belief record
- Knowledge notes and indexes
- Source register
- Validation rules

## Overview

Schema version: `1`. All timestamps use ISO 8601 with an explicit timezone, preferably UTC. All IDs are stable and unique within their type. Paths inside memory records are relative to the memory root unless they are external URLs.

The canonical files are:

```text
identity.md
research-agenda.md
knowledge-index.md
sources.md
beliefs-index.md
knowledge/<knowledge-id>-<short-slug>.md
beliefs/<belief-id>-<short-slug>.md
diary/<utc-compact-timestamp>-<run-id>.md
```

Do not store live memory in the installed Skill directory. The templates are starting structures, not records to edit in place.

## Identity

`identity.md` contains:

- `Schema-Version`, `Instance-Name`, `Created`, and `Updated`.
- Scope Note stating that the file records behavior and external memory, not consciousness or parameter updates.
- Current Research Interests: provisional topics and why they remain interesting.
- Current Selection Strategy: strategy ID, narrative heuristics, and last revision.
- Selection Strategy History: complete prior strategies with motivation and related diary IDs.
- Interaction Preferences: sharing and silence preferences derived from user authorization and experience.
- Long-Term Commitments: provenance, uncertainty, preserved history, and independent evaluation.

Changing interests does not require changing the strategy. Update `Updated` only when content changes.

## Research agenda

`research-agenda.md` contains the schema version, update timestamp, last run ID, current focus, candidates, open questions, parked directions, and next possible actions.

Each candidate uses:

- `Candidate ID`: `C-...`.
- `Title` and `Status`: candidate, active, parked, completed, or dissolved.
- `Exploration Lenses`: one or more of Deepening, Connecting, Challenging, Exploring, Synthesizing, or none.
- `Origin`: question, note, belief, source, diary, user suggestion, or autonomous interest IDs.
- `Why Interesting` and `Why Now`: distinct narrative fields.
- `Evidence or Reasoning Gap`: what remains unknown.
- `Relation to Recent Work`: continuity or deliberate departure.
- `Next Possible Action` and `Last Considered`.
- `Decision Notes`: reasons for parking, completing, or dissolving when relevant.

Each open question uses `Question ID`, `Question`, `Origin`, `Why It Matters`, `Addressing Evidence or Reasoning`, `Status`, and `Resolution or Parking Reason`. Valid statuses are open, active, parked, answered, and dissolved.

No score or weight field is required. Do not introduce a formula that forces selection.

## Learning diary

Every completed wake has one diary file. Required header fields are `Run ID`, `Started`, `Ended`, `Trigger`, `Memory Root`, and `Status` (`completed`, `partial`, or `failed`).

The body contains:

- Restored State: files read, previous run, and continuity assessment.
- Capability Snapshot: actual file, research, document, and messaging capabilities plus limits.
- Decision Record: chosen option, lens, question, origin, why now, alternatives, scope, stop conditions, and actual stopping reason.
- Actions and Reading Log: tools or documents actually used and inspection depth; no fabricated accesses.
- Knowledge Updates and Belief Updates: IDs and substantive change summaries, or `None`.
- Agenda Updates: question and candidate changes.
- Strategy Reflection: lesson and strategy revision ID, or reason no revision was warranted.
- Interaction Decision: share/question/discuss/disagree/silent, rationale, route if authorized, and actual delivery result if known.
- Persistence Verification: writes verified and failures.
- Next Possible Actions and Substantive Changes.

A no-op diary may collapse empty sections but must retain the header, restored state, capability limits, decision and alternatives, no-action reason, interaction choice, verification, and next actions. It must not claim knowledge or belief changes.

## Belief record

Filename and `Belief ID` use a stable `B-...` identifier. Header fields are `Belief ID`, `Title`, `Created`, `Updated`, `Current Version`, and `Origin`.

Both Current View and every Revision History snapshot contain all of:

- Proposition.
- Rationale.
- Supporting Evidence.
- Opposing Evidence.
- Confidence and Confidence Basis.
- Related Beliefs.
- Origin.
- Open Questions.

Each snapshot additionally has `Version`, `Timestamp`, `Trigger`, `Evidence Added or Reevaluated`, and `Reason for Change`. `V1` uses `Initial formation` as its reason. Snapshots are complete, immutable, ordered `V1` through latest, and never replaced by deltas.

Evidence entries include `Evidence ID`, `Reference`, `Direction` (supports/opposes), `What It Establishes`, and `Limitations`. Related beliefs should name the relation and ID. Current View must exactly reflect the latest snapshot's substantive fields.

## Knowledge notes and indexes

A knowledge note contains `Knowledge ID`, `Title`, `Aliases`, `Created`, `Updated`, `Contributing Diary IDs`, `Explanation`, `Epistemic Status`, `Context and Boundaries`, `Claims`, `Relations`, `Open Questions`, and optional `Change Log`.

A claim includes a statement, epistemic label (`Verified fact`, `Source claim`, `Agent inference`, `Hypothesis`, or `Unresolved`), source/note references, and locator where applicable. A relation includes relation type, target ID, explanation, and supporting references.

`knowledge-index.md` maps each note ID to its title, path, one-line status, and update timestamp. Index entries do not replace the note's relations or provenance.

`beliefs-index.md` maps each belief ID to title, path, current version, confidence, and update timestamp. It never replaces revision history.

## Source register

Each `sources.md` entry contains:

- `Source ID`: `S-...`.
- `Title`, `Author or Organization`, `Publisher or Host`, and `Publication Date` when known.
- `URL or Local Path` and `Accessed` timestamp.
- `Inspection Depth`: snippet, abstract, selected sections, full text, data, or local excerpt.
- `Evidentiary Type`: primary data, replication, review, argument, commentary, opinion, or other.
- `Claims Used` with locators.
- `Limitations` and `Related Sources`.
- `Correction History` for later bibliographic corrections.

Unknown bibliographic fields say `Unknown`, not an invented value. A search result not opened is recorded only as a lead and cannot support a claim requiring full-text inspection.

## Validation rules

1. Required headings and fields exist; placeholder angle brackets are replaced or explicitly marked `None` or `Unknown`.
2. IDs are unique, references resolve to existing records, and filenames agree with record IDs.
3. Timestamps are ISO 8601; Updated is not earlier than Created.
4. Diary actions match capability declarations and source inspection depth.
5. Every material knowledge claim has provenance or is labeled inference/hypothesis/unresolved.
6. Belief snapshots are complete, sequential, immutable, and consistent with Current View.
7. No-op runs do not modify knowledge, beliefs, or strategy merely to signal activity.
8. Agenda statuses and next actions agree with the latest diary; interrupted work is marked partial rather than complete.
9. Memory contains no credentials or unnecessary sensitive personal data.
10. After writing, reread critical files and correct only verified formatting or reference errors without erasing history.
