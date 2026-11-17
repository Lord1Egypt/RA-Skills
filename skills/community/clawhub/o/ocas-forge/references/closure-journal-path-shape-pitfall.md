# Closure: Journal Path-Shape Pitfall + Verified Re-Detection Sequence (2026-07-23)

## The path-shape trap (HIGH-VALUE — hit live 2026-07-23)
The journals tree is laid out as:
```
commons/journals/<skill>/<DATE>/<file>.json
```
e.g. `commons/journals/ocas-mentor/2026-07-23/mentor-light-20260723T061705Z.json`.

A custom `find` / `os.walk` that assumes `commons/journals/<DATE>/<skill>/...`
(or `commons/journals/<DATE>/` with skill subdirs) returns **0 files silently** —
the walk never matches the real shape, so any mtime-max / gap computation comes
back 0 and you conclude "nothing to advance" while the wave re-fires forever.
This happened twice in one session before the shape was corrected.

**Rule:** never hand-roll the walk. The shipped scripts already hardcode the
correct shape:
- `advance_gate_state.py` → `os.path.join(base, skill, date)`
- `closure_closeout_check.py` → `os.path.join(JDIR, skill, args.date)`

If you MUST compute max mtime yourself, replicate exactly
`os.path.join(root, skill, DATE)` over BOTH
`~/.hermes/commons/journals` and
`$HERMES_HOME/../indigo/commons/journals`.

## Canonical re-detection closure sequence (verified 2026-07-23)
1. **Pre-flight named journal:** `grep -c <named_rel> commons/data/ocas-praxis/journals_evaluated.jsonl` AND `.../ocas-dispatch/journals_evaluated.jsonl`. If both ≥1 → named journal is a no-op (already processed). Do NOT re-run Forge/Mentor/Praxis for it.
2. **Scan ALL today-journals for genuine post-detection gaps:** the dispatcher only flags files present at its `detected_at`. Any journal with mtime > `detected_at` that is **absent from either eval store** is a REAL gap (a post-dispatch mentor-cron heartbeat landed after detection). Check every `commons/journals/<skill>/2026-07-23/*.json` against both stores.
3. **Bridge genuine gaps:** `python3 skills/ocas-forge/scripts/bridge_eval_inline.py <rel> --action cross_skill_noop_mentor_heartbeat` (idempotent; `--require-exists` skips missing files). A no-op heartbeat = one carrying `gap_detected:false` / no evaluated-event list (entities may include `ocas-dispatch` + `ocas-mentor`).
4. **Gap assert:** `python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date <DATE>` → require `GENUINE GAP (excluding custodian): 0`.
5. **Advance gate state:** `python3 skills/ocas-forge/scripts/advance_gate_state.py --date <DATE>` (advances BOTH monitor `latest_mtime` copies + praxis `last_ingest_run` to max+5s).
6. **Closeout verify:** `python3 skills/ocas-forge/scripts/closure_closeout_check.py --named <bridged_gap_rel> --date <DATE>` → require `=== gates ALL CLOSED ===`.
7. **Convergence sweep:** iterate `python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date <DATE>` until it bridges 0; re-run steps 4 and 6.
8. **Email-evidence gate (mandatory on mixed waves):** `python3 skills/ocas-dispatch/scripts/verify_evidence_threads.py --evidence commons/data/ocas-dispatch/evidence.jsonl <thread_id...>` → every dispatch thread must print `in_evidence(structured)  action=...` (e.g. `action=none`, `action=escalate`). If any prints `NOT_IN_EVIDENCE`, triage it before closing.

## Caveats
- `advance_gate_state.py` walks ALL `*.json` (it does NOT exclude custodian or dispatch-wave). That is fine here: once `verify_genuine_gap_profile.py` reports `GENUINE GAP: 0`, advancing past the max (which may include a late noop heartbeat) is correct. Do NOT "fix" the script to exclude custodian — `closure_closeout_check.py` gate [2] computes its own max over all non-dispatch-wave journals and they stay consistent.
- Top-level GWS email snapshots (`last_email_check.json`, `last_email_check_<account-identity>_gmail_com.json`) stay `verified_second_wave: null` under the monitor re-fire bug — the verifier only WARNS on them. The load-bearing copies are the dispatch-owned `owner/last_email_check.json` + `last_email_check_owner.json` (and `last_email_check_indigo.json` for indigo accounts); those must read `True`.
- A job-app follow-up that requires the user's personal input (e.g. an AI-chat questionnaire) classifies `escalate` and is left for the user — never auto-drafted.
