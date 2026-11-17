# Re-detection Closure: Mtime-Advance Truncation Trap

**Confirmed:** 2026-07-16 MODE-C mixed-wave closure.

## The trap

When closing a `new_journals` re-detection, you MUST advance BOTH state
gates past the max journal mtime:
- `commons/data/monitor_state/journal_ingest_state.json` → `latest_mtime`
- `commons/data/ocas-praxis/ingest_state.json` → `last_ingest_run`

A naive closure hand-types the value read earlier (e.g. from a `grep` of
one file). That literal **truncates**:

```
hand-typed: 1784232657.4915      # = 1784232657.4915000
true max : 1784232657.4915047     # 4.7e-6 HIGHER
=> state.mtime < max_journal_mtime  => verifier reports FALSE
=> dispatcher RE-FIRES the same wave every cycle
```

The under-bite is invisible to the eye (`1784232657.4915` looks ≥
`1784232657.4915047`) but the float compare fails. Same *class* of failure
as the epoch-0 bug (state < max) but a different *cause* (hand-typed
truncation vs. bad arithmetic on a 0-gap re-sweep).

## The fix

Recompute the mtime programmatically — never copy a literal:

```python
import os, glob, json, datetime
ROOT = "<hermes-home>/profiles/indigo"
mt = max(os.path.getmtime(p)
         for p in glob.glob(f"{ROOT}/commons/journals/*/2026-07-16/*.json"))
NEW = mt + 1.0   # >=1s pad absorbs any heartbeat landing during/after write
NEW_ISO = datetime.datetime.fromtimestamp(
    NEW, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
# write NEW (float) into monitor_state journal_ingest_state.json:latest_mtime
# write NEW_ISO (ISO) into ocas-praxis ingest_state.json:last_ingest_run
```

The `+1.0s` pad closes the window where a mentor-cron heartbeat writes a
new journal between your pre-advance sweep and the state write.

## Verify

```
python3 skills/ocas-forge/scripts/closure_closeout_check.py \
    --named "ocas-mentor/<DATE>/<journal>.json" --date <DATE>
# expect:
#   [2] praxis last_ingest_run >= max today mtime : True
#   [2] monitor latest_mtime   >= max today mtime : True
```

If either reads `False`, your state value under-bites the true max —
recompute programmatically, do NOT nudge the literal by hand.