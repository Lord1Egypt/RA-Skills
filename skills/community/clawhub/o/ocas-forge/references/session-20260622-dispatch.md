# Session 2026-06-22 — Forge Journal Scan via Multi-Skill Dispatch (Third-Wave Pattern)

## Summary
Dispatch-triggered journal scan at 2026-06-22T08:19Z. Clean scan — no unprocessed vp/vd files.

## Execution
- Data root: `<hermes-home>/profiles/indigo/commons/data/ocas-forge/`
- Unprocessed files in data root: 0
- All vp/vd files already in `processed/` or `intake/processed/`
- Result: `no_op` — no work to do
- Journal written: `forge-scan-20260622T081900Z.json`

## Multi-Skill Dispatch Context
Ran as part of Forge + Mentor + Praxis dispatch. This dispatch produced a **third-wave pattern**:

1. **Wave 1** (dispatcher trigger): 3 new journals detected → all 3 pipelines ran
2. **Wave 2** (self-referential): Dispatcher detected forge-scan, praxis-dispatch, and mentor-light journals written by Wave 1 → all already in eval file
3. **Wave 3** (timing gap): Dispatcher detected forge-scan (08:19:00Z) and praxis-dispatch (08:18:51Z) journals that were written AFTER the Praxis ingest ran (08:18:51Z) → not yet in eval file

**Root cause of Wave 3:** The Praxis ingest runs mid-dispatch and updates `last_ingest_run`, but the forge-scan and praxis-dispatch journals are written AFTER the ingest completes. These journals have mtimes after `last_ingest_run`, so the dispatcher picks them up on the next scan.

**Fix applied:** Manually added forge-scan and praxis-dispatch journals to `journals_evaluated.jsonl` and advanced `last_ingest_run` to clear the queue.

## Key Learning
The Forge scan journal is written at the END of the Forge pipeline, which runs BEFORE the Praxis ingest. But the Praxis ingest updates `last_ingest_run` to a timestamp BEFORE the forge-scan journal's mtime. This creates a persistent 1-2 journal gap that the dispatcher will always detect as "new."

**Mitigation:** After the Praxis ingest, the caller should also add the forge-scan journal (written during the dispatch) to the eval file, or the Praxis ingest should run AFTER all pipeline journals are written.

## Follow-up Dispatch — 2026-06-22T10:25Z

Second dispatch of the day at 10:25Z. Dispatcher detected 4 new journals (forge-scan, praxis-dispatch, 2x mentor-light), but Praxis `last_ingest_run` (10:24:52Z) was already PAST the dispatcher's `latest_ts` (10:24:07Z). All journals had already been ingested by the prior dispatch's Praxis run.

**New pattern:** When `last_ingest_run > dispatcher.latest_ts`, the Praxis ingest finds 0 new journals from the dispatcher's list. Only truly new journals (written after `last_ingest_run`) need evaluation. In this case, only 1 new mentor-light journal (10:25:52Z) was found and ingested.

**Third-wave mitigation confirmed:** Adding dispatch-output journals to `journals_evaluated.jsonl` with `action_taken: "dispatch_output_skip"` and advancing `last_ingest_run` to `now + 1s` prevents infinite re-detection loops.

## Follow-up Dispatch — 2026-06-22T10:30Z (Dispatch #22)

Third dispatch of the day at 10:30Z. Dispatcher detected 3 new journals (forge-scan-20260622T103000Z, 2x mentor-light). Praxis `last_ingest_run` (10:35:27Z) was already PAST the dispatcher's `latest_ts` (10:30:00Z) because a prior Praxis cron had advanced the state timestamp.

**Pattern confirmed:** When `last_ingest_run > dispatcher.latest_ts`, the Praxis mtime comparison finds 0 journals from the dispatcher's list. Only journals written AFTER `last_ingest_run` are discovered — in this case, 2 mentor-light journals (10:36:24Z and 10:38:18Z) from the current dispatch's own Mentor pipeline.

**Forge scan:** Clean — all 11 proposals already processed. No-op journal written: `forge-scan-20260622T103940Z.json`.

**Third-wave mitigation applied:** Praxis-dispatch journal added to eval list with `action_taken: "dispatch_output_skip"`, `last_ingest_run` advanced to `now + 1s`.

**Key insight:** The `last_ingest_run` can be in the future relative to dispatch timestamps because (a) Praxis cron runs advance it independently, and (b) the Mentor heartbeat script also updates it. The mtime-based discovery handles this correctly — it just means the current dispatch's journals won't be found by Praxis until they're written AFTER `last_ingest_run`. The third-wave mitigation (adding dispatch-output journals to eval + advancing `last_ingest_run`) remains the reliable fix.