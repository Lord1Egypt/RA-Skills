# Closure: Post-Ingest Caller-Journal Mtime Trap

**Confirmed:** 2026-07-17 mixed-wave closure (new_journals explicit-run + new_emails second-wave).

## The trap

The Praxis dispatch ingest template (`skills/ocas-praxis/templates/dispatch_ingest_template.py`)
sets `commons/data/ocas-praxis/ingest_state.json:last_ingest_run` to its OWN `NOW` at the
moment it runs — mid-pipeline, BEFORE the caller writes the pipeline's own journals.

The caller then writes two journals with LATER mtimes:
- `commons/journals/ocas-praxis/<DATE>/praxis-cron-<TS>.json`
- `commons/journals/ocas-dispatch/<DATE>/dispatch-wave-<TS>.json`

Because those mtimes exceed `last_ingest_run`, the closeout verifier's gate [2]
(`praxis last_ingest_run >= max today-journal mtime`) reports **False** — even though every
journal is already bridged into both eval stores and `verify_genuine_gap_profile.py` already
returned **GENUINE GAP = 0**. Result: the wave re-fires on every dispatcher scan, forever.

This is DISTINCT from the monitor-state half of gate [2] (root + profile `journal_ingest_state.json`
`latest_mtime` copies). Both halves must clear the SAME max mtime, and the praxis half is the one
this trap breaks.

It is also a different cause from the hand-typed-literal truncation trap
(`redetection-mtime-truncation-pitfall.md`): here the value is correct at write time but the
caller's own later journals outrun it. Same *symptom* (state < max -> re-fire), different *cause*.

## Symptom seen 2026-07-17

```
python3 skills/ocas-forge/scripts/closure_closeout_check.py --named ocas-praxis/2026-07-17/praxis-cron-20260717T005348Z.json --date 2026-07-17
[1] named journal in PRAXIS+DISPATCH eval stores: praxis=True dispatch=True
[2] praxis last_ingest_run >= max today mtime : False (2026-07-17T00:50:30.044923+00:00 vs 2026-07-17T00:53:48.617736+00:00)
[2] monitor ROOT    latest_mtime >= max       : True
[2] monitor PROFILE latest_mtime >= max       : True
... gates STALE - re-run sweep/advance/re-affirm
```
`closure_convergence_sweep.py` reported `GAPS BRIDGED: 0` and `verify_genuine_gap_profile.py`
reported `GENUINE GAP: 0` — yet the wave did NOT close, because gate [2] praxis-half was stale.

## The fix (sequence)

After writing the praxis-cron and dispatch-wave journals, RE-ADVANCE `last_ingest_run`
programmatically past the max mtime of ALL today's journals (incl. the ones just written),
then re-run the full close sequence:

```python
import os, glob, json, datetime
ROOT = "<hermes-home>/profiles/indigo"
DATE = "2026-07-17"
mt = max(os.path.getmtime(p) for d in [
    f"{ROOT}/commons/journals/ocas-praxis/{DATE}",
    f"{ROOT}/commons/journals/ocas-mentor/{DATE}",
    f"{ROOT}/commons/journals/ocas-forge/{DATE}",
    f"{ROOT}/commons/journals/ocas-dispatch/{DATE}",
] for p in glob.glob(d + "/*.json"))
NEW_TS = mt + 5.0                       # pad absorbs the journals just written
NEW_ISO = datetime.datetime.fromtimestamp(NEW_TS, datetime.timezone.utc).isoformat()
state = json.load(open(f"{ROOT}/commons/data/ocas-praxis/ingest_state.json"))
state["last_ingest_run"] = NEW_ISO
json.dump(state, open(f"{ROOT}/commons/data/ocas-praxis/ingest_state.json", "w"), indent=2)
```

Then re-run:
```
python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date <DATE>
python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date <DATE>
python3 skills/ocas-forge/scripts/closure_closeout_check.py --named <relpath> --date <DATE>
```
Expect `[2] praxis last_ingest_run >= max today mtime : True` and `gates ALL CLOSED`.

## End-to-end sequence that works (mixed explicit-run wave)

1. Forge no-op scan (0 unprocessed proposals) -> write `forge-scan-*.json`
2. Mentor heartbeat + `correct_active_skills_30d.py` + commons sync -> `mentor-light-*.json`
3. Praxis **gap_backfill BEFORE** the ingest template (template advances `last_ingest_run` to its NOW)
4. Run ingest template (sets `last_ingest_run` = NOW, finds 0 new — gap_backfill already caught them)
5. Noise-lesson cleanup (truncate `lessons.jsonl` when all events are no_signal)
6. Write `praxis-cron-*.json` + `dispatch-wave-*.json`
7. Bridge all new journals into BOTH eval stores (filename key on dispatch store, journal_id on praxis store)
8. Advance monitor `latest_mtime` (BOTH root + profile copies) past max today-journal mtime
9. **RE-ADVANCE praxis `last_ingest_run` past max today-journal mtime** (this trap)
10. sweep -> verify (GENUINE GAP=0) -> closeout (gates ALL CLOSED)

## Note on email second-wave

The two top-level GWS-snapshot files (`last_email_check.json`,
`last_email_check_<account-identity>_gmail_com.json`) report `verified_second_wave: null` under the
monitor re-fire bug. The 2026-07-17 `closure_closeout_check.py` correction reads BOTH monitor
copies and warns on those two top-level files but REQUIRES only the dispatch-owned account copies
(`owner/last_email_check.json`, `last_email_check_owner.json`, indigo equivalents) — those are the
load-bearing gate. Re-affirm the owner copies to `True`; do not chase permanently-green on the
top-level snapshots.