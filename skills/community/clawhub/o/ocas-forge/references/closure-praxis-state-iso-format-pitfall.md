# Praxis `last_ingest_run` ISO vs monitor `latest_mtime` float trap (2026-07-24)

## Symptom
After advancing gate state and re-running `python3 scripts/closure_closeout_check.py --named <wave> --date <DATE>`, gate [2] reports:
```
[2] praxis last_ingest_run >= max today mtime : False (MISSING vs 2026-07-24T15:10:20.630054+00:00)
[2] monitor ROOT    latest_mtime >= max       : True (...)
[2] monitor PROFILE latest_mtime >= max       : True (...)
```
Monitor copies pass; praxis shows `MISSING` even though a larger value was written.

## Root cause
`closure_closeout_check.py` reads the two state types with DIFFERENT parsers:
- praxis `ocas-praxis/ingest_state.json:last_ingest_run` → `datetime.fromisoformat(lir_raw.replace("Z","+00:00"))` — expects an **ISO string**. A float epoch raises inside the try/except and `lir_dt` stays `None` → prints `MISSING`.
- monitor `monitor_state/journal_ingest_state.json:latest_mtime` (both root + profile copies) → `datetime.fromtimestamp(latest_mtime)` — expects a **float epoch**.

So the same "advance the gate" step needs a **float for monitor** and an **ISO string for praxis**.

## The format contract (closure gate advancement)
Compute once:
```
max_mt = max(os.path.getmtime(p) for p in all today journals EXCLUDING dispatch-wave-*.json)
NEW = max_mt + 5.0   # pad for heartbeats landing during the write
```
- BOTH monitor copies: `latest_mtime = NEW` (float).
- praxis `ingest_state.json`: `last_ingest_run = datetime.datetime.fromtimestamp(NEW, tz=datetime.timezone.utc).isoformat()` (e.g. `"2026-07-24T15:10:25.630054+00:00"`). Also set `last_ingest_run_ts` to the same ISO.
- Never hand-type the literal (truncation re-fires the wave — see `redetection-mtime-truncation-pitfall.md`); compute `NEW` programmatically.

## Fix when you hit the MISSING gate
Rewrite praxis `last_ingest_run` as ISO (with the +5s pad); leave the monitor float copies alone. Re-run the verifier → gate [2] praxis becomes True.

## Note on `scripts/advance_gate_state.py`
That shipped advancer recomputes `max_mt` correctly and takes `--date`, but VERIFY it writes ISO to praxis `last_ingest_run` (the verifier demands ISO). If a run of it still leaves gate [2] praxis `MISSING`, the script is emitting a float there — patch it to emit ISO, or hand-advance per the contract above.
