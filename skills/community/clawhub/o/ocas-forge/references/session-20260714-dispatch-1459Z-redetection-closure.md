# Dispatch 2026-07-14T14:59Z — Re-detection closure of a concurrent sibling wave

**Trigger:** Dispatcher fired `has_work:true` at `detected_at` 2026-07-14T14:50:52Z with 2 dispatches (`new_journals` 2 files + `new_emails` 7 owner threads). Explicit-run override (prompt said "run Forge/Mentor/Praxis" + "load ocas-dispatch").

**Classification pre-flight:**
- Both `new_file`s (`dispatch-wave-20260714T144904Z.json`, `mentor-light-20260714T144548Z.json`) present in BOTH eval stores → already processed.
- Prior wave `dispatch-wave-20260714T144904Z.json` already recorded pipeline reconciliation (3 gaps bridged, GENUINE GAP=0, `state_updated:true`).
- **Key discovery:** a NEWER sibling wave `dispatch-wave-20260714T145500Z.json` (timestamp 14:55:00 > detected_at 14:50:52) ALREADY processed this exact detection — triaged Kyra Jones thread `<thread-id>` as `action:none`, bridged `mentor-light-20260714T145055Z` gap, recorded `genuine_gap=0`. → Current wave is redundant work performed by a concurrent wave.

**Root cause of re-fire loop:** `ingest_state.json` `last_ingest_run` was STALE at `2026-07-14T14:41:05` despite the 144904Z wave's claimed `state_updated:true`. The stale gate (not the journals) is what kept the dispatcher re-detecting.

**Closure actions taken (no pipeline re-run, no new wave journal minted):**
1. Ran `verify_genuine_gap_profile.py --date 2026-07-14` → GENUINE GAP=1: `mentor-light-20260714T145549Z.json` (post-wave cron heartbeat — mentor-cron convergence loop).
2. Phantom-guarded (confirmed on disk), bridged via `bridge_eval_both_stores.py --action cross_skill_mitigation ocas-mentor/2026-07-14/mentor-light-20260714T145549Z.json` → ADDED dispatch=1 praxis=1.
3. Advanced `last_ingest_run` to 14:59:20 (past all mtimes) via `json.load` + `json.dump`, synced counters (praxis=21224, dispatch=13507). Concurrent-cron guard: only wrote because state was actually stale.
4. Fixed email state `commons/data/ocas-dispatch/owner/last_email_check.json` (bridge script NEVER touches it): `last_dispatch→14:59:20`, `last_dispatch_wave→145500Z`, `verified_second_wave=true`, `actionable=0`. All 7 threads `is_new=false` → email second-wave; inbox untouched (hard rule).
5. Re-ran `verify_genuine_gap_profile.py` → GENUINE GAP=0.

**Verification:** gap=0; `last_ingest_run` past both new_file mtimes; email `last_dispatch` ≥ detected_at; no third wave journal minted (kept 144904Z + 145500Z).

**Lessons:**
- When opening a re-detection, ALSO check for a NEWER dispatch-wave journal (timestamp > detected_at) that already closed the same detection (same journal paths + same email threads). If present, do closure-only — do NOT re-run pipelines, do NOT mint/rewrite a wave journal.
- Trust-but-verify `last_ingest_run` via `json.load` even when a prior wave claims `state_updated:true`. A stale gate re-fires the dispatcher regardless of journal state.
- The bridge script never updates email state files — always fix them in closure or the email item re-fires forever.