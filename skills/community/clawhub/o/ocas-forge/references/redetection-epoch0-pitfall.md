# Re-detection closure: epoch-0 state-advance trap (2026-07-15)

## The bug
`scripts/dispatch_redetection_close.py` derives the new `last_ingest_run` from
`max_mtime`, which `discover_gaps()` populates while walking today's journal dirs.
The ORIGINAL code computed mtime only for *gap* files:

```python
rel = "%s/%s/%s" % (skill, DATE, fn)
if rel in prax and rel in disp:          # <-- skip already-evaluated
    continue
try:
    mt = os.path.getmtime(os.path.join(sdir, fn))
except Exception:
    continue
if mt > max_mtime:                       # only gaps ever update max_mtime
    max_mtime = mt
```

When a closure run bridges every gap and the RE-SWEEP finds **0 gaps**,
`max_mtime` is still `0.0`. The script then writes
`last_ingest_run = datetime.fromtimestamp(0.0) -> 1970-01-01T00:00:00+00:00`.

## Why it's worse than the original loop
A stale `last_ingest_run` BELOW the journal mtimes re-fires the dispatcher on the
same wave every ~5 min (the `redetection-stale-state-pitfall`). Epoch 0 is BELOW
*every* journal ever written, so the next sweep classifies ALL journals as new and
re-fires far harder than the original brief loop. The closure "succeeds" (`GENUINE
GAP=0`, `DONE`) while corrupting state.

## The fix (applied 2026-07-15)
Compute and record mtime for EVERY today-journal BEFORE the membership branch:

```python
rel = "%s/%s/%s" % (skill, DATE, fn)
try:
    mt = os.path.getmtime(os.path.join(sdir, fn))
except Exception:
    continue
if mt > max_mtime:                       # ALL files, not just gaps
    max_mtime = mt
if rel in prax and rel in disp:
    continue
# ... gap classification below
```

After this fix, a 0-gap re-sweep advances `last_ingest_run` to the true MAX mtime
(21:25:19Z in the 2026-07-15T21:25Z run), and re-running confirms idempotency.

## Mandatory verification discipline (any closure / state-advance run)
`GENUINE GAP=0` proves gaps are bridged. It does NOT prove state was advanced
correctly — the buggy code printed `GENUINE GAP=0` while writing epoch 0.
ALWAYS, after any closure/state-advance script exits:

1. Re-read `ingest_state.json` via `json.load(open(...))` — NEVER `read_file`
   (cron-safe state truth; read_file can return a cached/commons-scoped copy).
2. Compute the true MAX `os.path.getmtime()` across
   `commons/journals/*/YYYY-MM-DD/*.json` (ungated — no mtime filter).
3. Assert `state['last_ingest_run'] == <that max>`.
4. If it is epoch 0 (1970-01-01) or below the max, correct it BY HAND:
   set it to the true max ISO timestamp, then re-sweep `verify_genuine_gap_profile.py
   --date YYYY-MM-DD` and assert `GENUINE GAP (excluding custodian): 0`.
   Do NOT declare closure until both (gap=0) AND (state==max mtime) hold.

## Reproduction (post-fix regression guard)
```bash
cd <hermes-home>/profiles/indigo/skills/ocas-forge
python3 scripts/dispatch_redetection_close.py \
  --new-files ocas-mentor/2026-07-15/mentor-light-20260715T212021Z.json \
  --wave-run-id wave-redet-20260715T2120Z
python3 -c "import json; s=json.load(open('<hermes-home>/profiles/indigo/commons/data/ocas-praxis/ingest_state.json')); print(s['last_ingest_run'])"
# expect 2026-07-15T21:25:19.381925+00:00 (NOT 1970-01-01)
```