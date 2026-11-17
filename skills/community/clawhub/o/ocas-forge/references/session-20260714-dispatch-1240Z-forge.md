# Session 2026-07-14T12:40Z — Explicit-run new_journals + new_emails dispatch

Confirmed the explicit-run override genuinely fires even when the dispatcher's named
`new_file` is already fully evaluated, because a NEW post-prior-wave cron heartbeat
appears after the prior recovery closed.

## Trigger
Dispatcher fired `new_journals` (explicit-run override: "run Forge journal scan / run Mentor
light heartbeat / run Praxis journal ingest") + `new_emails` at 2026-07-14T12:40Z.
- Journal `new_file`: `ocas-mentor/2026-07-14/mentor-light-20260714T123550Z.json` → ALREADY in BOTH eval stores.
- Email: 5 <operator> threads, all `is_new:false`.

## Context — prior recovery
The 12:21Z recovery wave (`dispatch-wave-20260714T121923Z.json`, rewritten
`fifth_wave_redetection_no_op_recovery_closed`) had run the real pipelines, bridged
forge/praxis outputs, stamped email state to 0, and advanced `last_ingest_run` to 12:25:39.
A second cron heartbeat `mentor-light-20260714T122538Z.json` had landed during that
recovery and was bridged. At 12:40Z the dispatcher re-detected because a THIRD heartbeat
(`mentor-light-20260714T124039Z.json`) had since appeared — MISSING from both eval stores.

## Decision
Named `new_file` already evaluated = completed re-detection for THAT file, but the
explicit-run override + a genuinely-new unevaluated cron heartbeat means the override still
applies. Ran the full pipeline (Forge scan + real Mentor heartbeat + Praxis ingest),
producing genuinely-new outputs (`forge-scan-20260714T124439Z.json`,
`mentor-light-20260714T124449Z.json`) that needed bridging.

## Procedure (verified)
1. Forge scan: intake empty, data-root empty, `proposals/` mirror excluded → 0 unprocessed →
   no-op. Wrote `forge-scan-20260714T124439Z.json`.
2. Mentor heartbeat via subprocess stdin (`python3 scripts/cron-heartbeat-light.py < /tmp/feed.txt`,
   feed = today+yesterday journals, `grep -v dispatch-wave`). 18 ingested, 0 errors. THEN
   `correct_active_skills_30d.py` (script=1 → true=20, OCAS:13).
3. Capture heartbeat journal via CONTENT-timestamp scan (max `timestamp` field), NOT `ls -t`
   (mtimes lag ~7h12m): `mentor-light-20260714T124449Z.json`.
4. Praxis ingest: 3 journals, 2 `no_signal` events, 0 lessons.
5. On-disk reconciliation (`os.listdir` per skill, NO recursive glob) → 3 gaps all missing from
   DISPATCH eval (praxis had them): forge-scan output, heartbeat output, post-dispatch cron
   `mentor-light-20260714T124039Z.json`. Bridged idempotently into dispatch eval
   (`dispatch_third_wave_mitigation` / `cross_skill_mitigation`).
6. Advanced `last_ingest_run` to max mtime of wave work (12:44:49); resynced counters to 21,174.
7. Convergence re-sweep (mtime >= last_ingest_run): 0 gaps.
8. Email: all `is_new=false` → second-wave. Stamped BOTH
   `last_email_check_<account-identity>_gmail_com.json` (canonical the dispatcher reads) +
   `last_email_check_owner.json` to `actionable:0` + `last_dispatch`.
9. Wrote `dispatch-wave-20260714T124439Z.json` (renamed from a malformed
   `dispatch-wave-20260714T1244.json` — see SKILL.md gotcha).

## Pitfalls confirmed this session
- **Malformed dispatch-wave filename**: a truncated `TS` (`20260714T1244`) missing seconds+`Z`
  yields `dispatch-wave-20260714T1244.json` with inconsistent `run_id`. Always derive the wave
  filename from the full `date +%Y%m%dT%H%M%SZ`.
- **Legacy bare-filename eval entries are NOT phantoms**: post-bridge naive
  `os.path.exists(join(journals_root, filename))` guard flagged 12,712 "phantoms" — all
  pre-standardization bare-filename entries (`mentor-light-20260628T...json`, `run_xxxx.json`,
  etc.). These track real journals at the standardized path; do NOT clean them during a routine wave.

## Result
GENUINE GAP=0 in both eval stores; no phantoms among current-wave entries (verified 1:1 on
disk); wave `state_updated:true`; email `actionable:0`. Re-fire loop closed. No drafts, no sends.