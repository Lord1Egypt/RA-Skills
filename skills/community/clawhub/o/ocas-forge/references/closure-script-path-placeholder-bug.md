# Closure Script Path Placeholder Bug

**Confirmed 2026-07-27**: `closure_closeout_check.py` and `verify_genuine_gap_profile.py` in `ocas-forge/scripts/` contain the literal string `<hermes-home>` in their path resolution instead of `os.path.expanduser('~')` or a config-based path lookup. Both scripts crash with `FileNotFoundError: [Errno 2] No such file or directory: '<hermes-home>/profiles/indigo/commons/journals'` at runtime.

## Symptoms

```
FileNotFoundError: [Errno 2] No such file or directory: '<hermes-home>/profiles/indigo/commons/journals'
```

The scripts fail before reaching any gate check. This is NOT a transient tool-layer flake — it's a hardcoded placeholder that never resolves.

## Manual Fallback Procedure

When closure scripts crash, verify gates manually in this order:

### Gate [1]: Named journal in both eval stores
```bash
# Check praxis eval store
grep -c "MENTOR_REL" $HERMES_HOME/commons/data/ocas-praxis/journals_evaluated.jsonl
# Check dispatch eval store
grep -c "MENTOR_REL" $HERMES_HOME/commons/data/ocas-dispatch/journals_evaluated.jsonl
```
Use bare relpath (NO `commons/journals/` prefix). If missing, bridge manually:
```bash
python3 -c "
import json
eval_path = '$HERMES_HOME/commons/data/ocas-dispatch/journals_evaluated.jsonl'
entry = {'journal_id': 'RELPATH', 'evaluated_at': 'NOW_ISO', 'action_taken': 'cross_skill_mitigation'}
with open(eval_path, 'a') as f:
    f.write(json.dumps(entry) + '\n')
"
```

### Gate [2]: State advanced past max journal mtime
```bash
# Compute max mtime programmatically (never hand-type)
python3 -c "
import os, glob
max_mtime = max(os.path.getmtime(p) for p in glob.glob('$HERMES_HOME/commons/journals/*/2026-07-27/*.json'))
print(f'max_mtime: {max_mtime}')
print(f'max_mtime + 2s pad: {max_mtime + 2.0}')
"
# Advance both monitor copies and praxis ingest_state
```

### Gate [3]: verified_second_wave re-asserted
```bash
# Check all 4 state files have verified_second_wave: true
for f in $HERMES_HOME/commons/data/ocas-dispatch/last_email_check_<operator-account>.json \
         $HERMES_HOME/commons/data/ocas-dispatch/last_email_check_indigo.json \
         $HERMES_HOME/commons/data/ocas-dispatch/last_email_check.json \
         $HERMES_HOME/commons/data/ocas-dispatch/last_email_check_<operator-account>.json; do
  python3 -c "import json; d=json.load(open('$f')); print('$f:', d.get('verified_second_wave'))"
done
```

## Root Cause

`closure_closeout_check.py` line ~91 uses `JDIR = '<hermes-home>/profiles/indigo/commons/journals'` as a hardcoded path template. The `<hermes-home>` placeholder was never replaced with an actual path resolver at build time or runtime. The script should use `os.path.expanduser('~')` to construct the path dynamically, matching the pattern used in other ocas-forge scripts.

## See Also

- `references/closure-email-state-refire-pitfalls.md` — monitor re-fire bug details
- `references/dispatch-integration-pitfalls-skillmd.md` — expanded gotchas for dispatch integration
- `references/redetection-stale-state-closure-oneshot.md` — MODE C stale-state closure manual steps
