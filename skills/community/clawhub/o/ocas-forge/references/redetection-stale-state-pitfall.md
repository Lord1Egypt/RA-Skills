# Re-Detection Closure: Stale `last_ingest_run` Perpetual Re-Fire Pitfall

## Symptom
A `new_journals`+`new_emails` mixed wave (or any second-wave / no_op re-detection) keeps
re-firing every dispatcher cycle (~5 min) even though GENUINE GAP=0 was already asserted
and all files are present in both eval stores. The dispatch log shows the SAME file set
de-queued repeatedly.

## Root cause (observed 2026-07-15)
A `mixed_no_op`/`mixed_second_wave` closure bridged the sibling journals and asserted
`GENUINE GAP=0` but **never advanced `ingest_state.last_ingest_run` past the processed
files' mtimes**. The dispatcher's detection window is `file.mtime > last_ingest_run`, so a
file whose mtime is ABOVE `last_ingest_run` is perpetually "new". A later `mentor-light`
cron heartbeat (one lands every ~5 min) also writes above the stale `last_ingest_run`,
guaranteeing a new detection each cycle.

Concrete values from the 2026-07-15 incident:
- `last_ingest_run` was stuck at `2026-07-15T04:45:15.844Z`
- processed files: `dispatch-wave-20260715T045016Z.json` (mtime 04:50:16Z),
  `mentor-light-20260715T045019Z.json` (mtime 04:50:19Z)
- a `mentor-light-20260715T045515Z.json` heartbeat landed mid-closure (mtime 04:55:15Z)
- the prior no_op wave (`dispatch-wave-20260715T045016Z`) had bridged the sibling but
  skipped the state-advance step → `last_ingest_run` never moved → re-fire loop.

## The fix (mandatory closeout for EVERY re-detection / no_op closure)
1. Run `closure_convergence_sweep.py` and iterate until it bridges 0.
2. Compute `max_mtime` across **ALL** today-dated `*.json` under
   `commons/journals/` (use `os.walk`, include `dispatch-wave-*` and the mentor-cron
   heartbeat that landed mid-run — do NOT exclude it).
3. Advance `ingest_state.json`:
   - read via `json.load(open(STATE))` — NEVER `read_file` (returns stale/commons copy)
   - set `last_ingest_run` = ISO of `max_mtime`
   - resync `journals_evaluated_count` + `last_eval_file_line` to actual `wc -l` of both
     eval stores
   - write via full-file `json.dump` — NEVER `patch` (duplicate-key corruption)
4. Re-affirm email second-wave state (`commons/data/ocas-dispatch/<acct>/last_email_check.json`)
   via full-file `write_file`: `verified_second_wave=true`, `last_dispatch_wave=<prior real
   wave id>`, `last_dispatch_note="re-detection closure; no re-triage, no sends"`.
5. Assert `python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date <DATE>`
   → `GENUINE GAP (excluding custodian): 0`.

## Pre-flight signal that the loop is happening
During re-detection pre-flight, if `last_ingest_run` < max(dispatcher new_files mtime)
(the gaps in this session: `04:45:15Z` < `04:50:16Z`), the prior closure skipped the
state-advance step. This is the loop cause — NOT a reason to re-run pipelines (that would
mint duplicate journals and re-fire the dispatcher). Do closure-only: bridge residuals,
sweep to 0, advance state past the max mtime, re-affirm email, assert gap=0.

## Why "bridge then forget" is insufficient
Bridging sibling journals into the eval stores makes `verify_genuine_gap_profile.py` pass
(GENUINE GAP=0) but does NOT move `last_ingest_run`. The dispatcher never consults the eval
stores for the re-fire decision — it consults `last_ingest_run` vs file mtimes. So a closure
that bridges but doesn't advance produces a green gap report AND an infinite re-fire. Both
steps are required.