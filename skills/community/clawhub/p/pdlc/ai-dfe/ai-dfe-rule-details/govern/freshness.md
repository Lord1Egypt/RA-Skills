# Stage 3.2 — Freshness

> Phase 3 (Govern). Assess how current the data surface is, relative to its sources. Report-only.

## Purpose

Tell the user (and the `DFA__` agent) where data is stale, missing, or never generated — without changing anything.

## Inputs

- `dfe-state.md` (`lastGenerated`, cached `sourceFiles[]`).
- Source-file and data-file timestamps.

## Logic

For each package and demand, classify:

| Status | Meaning |
|--------|---------|
| `fresh` | data file `$generatedOn` ≥ newest source mtime |
| `stale` | a source changed after the last generation |
| `not-run` | package present but its sources don't exist yet (null-filled data) |
| `no-interface` | package installed but ships no `data-schema/` |
| `orphan` | data file exists but its package is no longer discovered |

Report a scannable table: package/demand · status · newest source · lastGenerated · lag.

## Output

A freshness report. No writes.

## Triggers

- `DAT__ status` — operations-side freshness summary.
- `DFA__ freshness` — the agent's deeper staleness/lag assessment (same data, agent framing + recommendations).
