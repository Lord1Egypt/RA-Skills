# Dreaming Integration

## Goal

Define how `memory-governor` should coexist with OpenClaw Dreaming without creating duplicate promotion paths, conflicting memory layers, or unclear ownership.

## Core Split

Treat the two systems as different layers:

- `memory-governor` governs capture, routing, staging, and manual hardening rules
- Dreaming governs background consolidation from short-term memory into long-term memory

In short:

- `memory-governor` decides **what should be written where**
- Dreaming decides **which short-term signals are worth consolidating into long-term memory**

## What Dreaming Is

For governance purposes, Dreaming should be treated as:

- an optional consolidation engine
- host-owned behavior
- downstream of short-term capture

It is **not**:

- a new target class
- a replacement for `learning_candidates`
- a replacement for `reusable_lessons`
- a direct writer of system-governance files

## Canonical Boundaries

### Engine-Owned Artifacts

These should be treated as Dreaming-owned artifacts, not standard memory targets:

- `DREAMS.md`
- `memory/.dreams/`

Interpretation:

- `DREAMS.md` is a human-readable dreaming artifact
- `memory/.dreams/` is machine state for the dreaming engine

Skills should not write directly to either path unless they are explicitly implementing Dreaming infrastructure.

### Other Compiled / Runtime Surfaces

Dreaming is not the only official surface that is downstream of the memory contract. Newer OpenClaw builds add more, and the same boundary applies to all of them:

- Active Memory: runtime recall layer, not a target class
- Memory Wiki, Claim / Evidence artifacts, Contradiction / Staleness reports: compiled knowledge views
- People Wiki, Person Cards, Relationship Graphs: entity-compiled views
- Memory Palace, Imported Insights: UI / navigation surfaces
- Provenance Views: a property of compiled claims, not a target class

None of these is a capture layer. The full list and the capture-vs-compile rule live in [compiled-surfaces.md](compiled-surfaces.md).

A privacy note specific to recall: Active Memory Filters (such as `allowedChatIds` / `deniedChatIds`) control what may be recalled where. That is a recall-time control. Capture-time governance still needs to record scope on the target class entry, otherwise a compiled surface can widen a scoped memory into a global view.

### Canonical Durable Memory

Dreaming may help decide what enters long-term memory, but the canonical durable memory layer remains:

- `MEMORY.md`

`DREAMS.md` is not a substitute for `MEMORY.md`.

## Responsibility Split

### `memory-governor` should own

- memory classification
- target classes
- adapter boundaries
- exclusion rules
- explicit correction staging
- candidate review and manual hardening
- system-rule promotion boundaries

### Dreaming should own

- background processing of daily signals
- consolidation from short-term traces
- long-term promotion from daily/context signals
- explainability for why something was or was not promoted from short-term memory

## Recommended Promotion Authority

### Dreaming-preferred

Use Dreaming as the preferred authority for:

- `daily_memory -> long_term_memory`

This avoids duplicating the same long-term promotion path in both systems.

### Manual-only

Keep manual authority for:

- `learning_candidates -> reusable_lessons`
- `reusable_lessons -> system_rules`
- `reusable_lessons -> tool_rules`
- promotion into `AGENTS.md`, `TOOLS.md`, or `SOUL.md`

Reason:

- these paths involve explicit correction review and governance hardening
- they should not be silently derived from background consolidation

## Input Separation

To avoid overlap:

- explicit corrections should enter `learning_candidates`
- first-sighting emerging lessons should enter `learning_candidates`
- ordinary same-day events should stay in `daily_memory`
- reusable cross-task lessons may enter `reusable_lessons` when already proven

Do not rely on Dreaming to clean up explicit correction staging.

## Read Separation

Do not treat Dreaming artifacts as normal startup memory.

Default rule:

- do not read `DREAMS.md` during normal startup
- inspect it only when reviewing Dreaming behavior, promotion quality, or consolidation traces

## Anti-Patterns

- modeling `DREAMS.md` as a target class
- letting Dreaming replace `learning_candidates`
- letting Dreaming write directly into `AGENTS.md` / `TOOLS.md` / `SOUL.md`
- running both manual daily promotion and Dreaming as competing default authorities
- using Dreaming as an excuse to skip explicit correction review

## Host Guidance

Dreaming should be treated as:

- host-specific
- optional
- downstream of the governance contract

If a host enables Dreaming, update its profile and operating notes so that:

1. Dreaming is the preferred daily-to-long-term path
2. candidate review stays manual
3. system-rule hardening stays manual
