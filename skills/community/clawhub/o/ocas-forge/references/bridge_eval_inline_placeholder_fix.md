# bridge_eval_inline.py `<hermes-home>` Placeholder Fix

**Confirmed 2026-07-27**: `bridge_eval_inline.py` in `ocas-forge/scripts/` contains the literal string `<hermes-home>` in its path resolution instead of `os.path.expanduser('~')`. It crashes when `--require-exists` is used, silently skipping valid on-disk journals and returning `total bridged: 0`.

## Symptom

```
SKIP (missing on disk): ocas-mentor/2026-07-27/mentor-light-20260727T154546Z.json
total bridged: 0
```

Despite the journal existing on disk at the expected path.

## Manual Bridge (universal fallback for ALL `<hermes-home>` script failures)

```python
import json
JOURNAL = "ocas-mentor/2026-07-27/mentor-light-20260727T154546Z.json"
ENTRY = json.dumps({"journal_id": JOURNAL, "evaluated_at": "2026-07-27T15:52:09.944704+00:00", "action_taken": "dispatch-new_journals-bridge", "source": "dispatcher"}) + "\n"
for path in [
    "$HERMES_HOME/commons/data/ocas-praxis/journals_evaluated.jsonl",
    "$HERMES_HOME/commons/data/ocas-dispatch/journals_evaluated.jsonl",
]:
    with open(path, "a") as f:
        f.write(ENTRY)
```

## Affected Scripts (complete list)

| Script | Symptom |
|--------|---------|
| `closure_closeout_check.py` | `FileNotFoundError: '<hermes-home>/profiles/indigo/commons/journals'` |
| `verify_genuine_gap_profile.py` | Same |
| `closure_convergence_sweep.py` | Same |
| `bridge_eval_inline.py` | SKIP for valid on-disk journals, 0 bridged |

## See Also

- `references/closure-script-path-placeholder-bug.md` — full per-gate manual fallback procedure
- `ocas-forge/SKILL.md` Gotchas section — placeholder-then-patch anti-pattern