# Dispatch Bridge Re-run Pitfalls

Captured from a 2026-07-13 explicit-run multi-skill dispatch where a caller-side
bridge (the 2026-07-13 override path that skips `run_dispatch_pipeline.py`) both
WROTE new pipeline journals AND bridged them into the eval files. Two failures
occurred that the existing override notes do not cover.

## Pitfall 1 — Bridge re-run writes duplicate journals

**Symptom:** After a bridge script crashed in a later verification step and was
re-run, the eval files contained TWO sets of the same pipeline journals — e.g.
`forge-scan-20260713T054847Z.json` AND `forge-scan-20260713T054909Z.json`,
`praxis-dispatch-...T054847Z` AND `...T054909Z`, `dispatch-wave-...T054847Z` AND
`...T054909Z` — with 6 redundant eval entries.

**Root cause:** The bridge script composed `TS = datetime.now().strftime("%Y%m%dT%H%M%SZ")`
and wrote the new journals with that timestamp at the TOP of the script. A re-run
(after a crash in a step that ran AFTER the writes) recomposed a fresh timestamp
and wrote a second journal set, then re-bridged BOTH sets. The idempotent-by-
`journal_id` guard only blocks re-adding the SAME journal_id; the new timestamp
makes them different ids, so they slip through.

**Note:** The 2026-07-13 override already says "compose all timestamps in the SAME
Python block" — that guards against MULTIPLE calls in ONE run. It does NOT guard
against re-running the SAME script in a LATER turn. This pitfall is the later-turn case.

**Fix A — split write from bridge (preferred):**
1. Script A: write journals + run heartbeat. Run once. Capture the exact filenames (write them to `/tmp`).
2. Script B: bridge + verify (idempotent by `journal_id`). Safe to re-run any number of times — it only appends missing entries.

**Fix B — idempotent journal write (single-script):** before writing each new journal,
guard with `if not os.path.exists(path): write_json(path, obj)`. A re-run then skips
already-written journals and only re-runs the bridge, which is idempotent.

**Fix C — lock the run timestamp:** write `TS` to a `/tmp` file on first run; on re-run,
read it instead of recomposing. Avoids the duplicate entirely.

## Pitfall 2 — Phantom-guard crashes on `None` journal_id

**Symptom:** `TypeError: join() argument must be str, bytes, or os.PathLike object,
not 'NoneType'` in the post-bridge "assert every bridged journal_id exists on disk" loop.

**Root cause:** `all_ids = praxis_ids | dispatch_ids` includes `None` because some
legacy eval entries (June backfill) have `journal_id: null` or a missing key.
`os.path.join(JDIR, None)` raises.

**Fix:** in the phantom loop, `for jid in all_ids: if not jid: continue`.

**Do NOT bulk-remove the "phantom" entries you find.** Most `None`/missing-file
journal_ids are HISTORICAL legacy backfill artifacts (e.g.
`ocas-finch/2026-07-12/scan-1813.json`) whose on-disk files were compacted/moved
long ago. The dispatch-pipeline-guide already warns against unscoped historical
`--fix` cleanup (it can drop tens of thousands of unrelated entries). Only assert
on-disk existence for the entries YOUR bridge just added; leave legacy gaps alone
unless the user asks for historical cleanup.

## Why this matters

A duplicate dispatch-wave journal pollutes the audit trail and can confuse future
classifiers (two "waves" for one dispatch). The split write/bridge pattern is the
cheapest reliable fix and matches the existing "verify before exit" discipline in
the override notes.