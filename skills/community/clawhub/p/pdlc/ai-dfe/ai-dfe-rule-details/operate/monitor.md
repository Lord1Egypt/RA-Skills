# Stage 2.4 — Monitor

> Phase 2 (Operate). The cheap continuous loop — detect stale data and refresh only what changed.

## Purpose

Avoid re-gathering everything every pass. Compare each cached source's timestamp against the data file's `$generatedOn`; refresh only stale files.

## Inputs

- `dfe-state.md` (`discovered.{pkg}.sourceFiles[]`, `lastGenerated`).
- Filesystem timestamps of the declared source files.

## Logic

1. For each package, find the most-recent modification time across its cached `sourceFiles[]`.
2. If that time > the data file's `$generatedOn` → mark **stale**; re-run gather (2.1) for that package, then shape (2.2) for any DEMAND that draws on it, then distribute (2.3).
3. If fresh → skip (no work).
4. Two signals can start a pass: a **FLO signal** ("package X completed") triggers an immediate check; otherwise DFE catches changes on the next timestamp pass. DFE decides which to act on.

## Output

Refreshed deltas only; unchanged files untouched.

## `DAT__ status`

Reports, per package/demand: `fresh | stale | not-run | no-interface`, the source that is newest, and the last-generated time. Report-only — no writes.
