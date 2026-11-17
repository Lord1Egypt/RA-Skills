# Dispatch re-fire closure — continuous ocas-reach feed (2026-07-25)

**Trigger:** dispatcher re-fires `dispatch-wave-20260725T033419Z` (detected 03:34:49Z; prior wave written 03:34:19Z). Profile monitor copy stale since 07-23 → re-fire loop.

## Diagnosis
- **Email gate PASS:** `verify_evidence_threads.py --evidence commons/data/ocas-dispatch/evidence.jsonl <tids>` → all 3 threads `in_evidence(structured) action=...` (Tartine=none, Docusign=escalate, Roller=none). No re-triage needed.
- `verify_genuine_gap_profile.py --date 2026-07-25` → genuine gaps GROWING (44 → 68 → …) all `ocas-reach/...`. Forge `forge_count_unprocessed.py` = 0 (no variant work).
- The gaps are **ocas-reach observation journals** from a live OCAS data feed: ~12 journals/min, one every ~5s, 00:58Z→03:45Z+. It is a **CONTINUOUS STREAM**, not a finite burst.

## Key learning: do NOT wait for a continuous feed to settle
- Watching mtime showed it advancing every 15–20s (1529→1537 files in 45s). It never stops within a session.
- Correct move (matches the 07-24 live-stream pattern): run the genuine pipeline, bridge the on-disk tail, advance gate state — accept that a few post-run tail journals carry to the **NEXT** wave as genuine gaps. Expected, not a failure.

## Closure sequence that worked
1. `python3 skills/ocas-forge/scripts/run_mixed_wave_closure.py --dispatch-ts 20260725T033449Z --date 2026-07-25 --new-files <ocas-reach relpaths>` — writes forge-scan + mentor-light + dispatch-wave journals, runs Praxis ingest (bridged 134 reach journals into BOTH eval stores), re-affirms email second-wave, advances gate state.
2. After step 1, the live feed had written NEW journals (max mtime 03:43:49 → 03:44:42 → 03:45:04). So loop:
   - re-run `closure_convergence_sweep.py --date 2026-07-25` (bridged 37 more tail journals)
   - re-run `advance_gate_state.py --date 2026-07-25` (recomputes max mtime programmatically +5s pad, writes BOTH monitor copies + praxis)
   - re-run `closure_closeout_check.py --named <wave-rel> --date 2026-07-25` → `=== gates ALL CLOSED ===`
3. Repeat step 2 until the post-run tail is small; residual few carry to next wave.

## Pitfall: monitor-state verification via relative `cat` is misleading
- Monitor state has TWO authoritative copies: root `~/.hermes/commons/data/monitor_state/journal_ingest_state.json` AND profile `$HERMES_HOME/../indigo/commons/data/monitor_state/journal_ingest_state.json`.
- A relative `cat profiles/indigo/commons/...` from cwd `$HERMES_HOME/../indigo` resolved to a **STALE mirror** (printed 07-23 value) while the absolute read showed the advanced 03:43:54Z value. `advance_gate_state.py` output and `closure_closeout_check.py` gate [2] (both read absolute copies) are authoritative.
- **Always trust `closure_closeout_check.py` gate [2] over a hand-rolled relative-path `cat`.** Verify with absolute paths only.

## Outcome
- Gates ALL CLOSED at state 03:45:09Z. Email escalate item (Docusign <employer> separation agreement, sent 07-14) preserved for <operator>'s personal signature.
