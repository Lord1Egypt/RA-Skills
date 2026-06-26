# Classification rubric

Classify one note at a time. Prefer explicit uncertainty over confident mislabeling.

Subagents that use this rubric return candidates only; the main agent verifies and applies.
See `references/status-schema.md` for the `confidence` rule when emitting per-note recommendations.

## Step 1: Determine `doc_kind`

Ask what the note is trying to be:

- `reference` — source of truth, stable facts, config, paths, commands
- `howto` — procedure to achieve a task
- `explanation` — why something works, tradeoffs, reasoning
- `tutorial` — guided learning sequence
- `research` — collected findings, comparisons, external material
- `adr` — a decision with context and consequences
- `log` — diary, changelog, working notes, progress trail
- `index` — hub page or navigation page
- `concept` — target design or future plan

## Step 2: Determine `status`

### `current`
Use when the note is still valid and should be trusted now.
Signals:
- verified paths, commands, hostnames, versions, or architecture
- referenced by 2 or more inbound wikilinks from notes that are already `status: current`
- clearly reflects the live environment

### `historical`
Use when the note is not current but still valuable.
Signals:
- documents a previous setup, migration path, or decision history
- useful for recovery, comparison, or context
- replaced by a newer page

### `concept`
Use when the note describes a desired future state.
Signals:
- signal words in the title or opening section, in German or English, such as Zielbild, Soll, Plan, Proposal, Vision, target state, draft, or future state
- contains intended rather than verified state

### `needs-review`
Use when status is unclear.
Signals:
- mixed old and new facts
- no verification date, or `last_verified` older than 90 days for a note claiming `status: current`
- conflicts with better evidence
- unclear whether the note is still active

### `reactivatable`
Use when the note is dormant but likely reusable.
Signals:
- currently inactive workflow or system
- likely to return later
- should stay discoverable without being treated as live

## Canonical page test

A note is a good canonical candidate when most of these are true:

- it has the clearest scope for a topic
- it is easier to update than the alternatives
- it already attracts links or should attract them
- it can safely point outward to detail pages
- it is not mostly historical baggage

If no note qualifies, propose creating a small new index or reference page instead of forcing a bad canonical page.

## Supersession rules

- Do not erase old context when a new page replaces it.
- Mark older pages with `superseded_by`.
- Mark the new leading page with `supersedes`.
- Prefer short transition notes over giant merge rewrites.

## Conflict handling

When two notes disagree:

1. trust live evidence over prose
2. trust the note with recent verification over the undated one
3. downgrade uncertain notes to `needs-review`
4. do not silently merge contradictions away
5. if a note appears to contain sensitive content (see `references/subagents.md` glossary), flag it as a `needs-review` candidate until the main agent verifies the exact text

## Smell list

Be careful when a note contains:

- old hostnames, paths, containers, or OS assumptions
- ambiguous words like "current", "latest", "new" without a date
- copied research without integration into a leading page
- multiple unrelated topics in one note
- operational instructions mixed with speculative design
