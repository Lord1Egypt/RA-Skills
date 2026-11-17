# Run Mixed Wave Closure Crash: os import missing

## Symptom
`run_mixed_wave_closure.py` crashes at module load with:
```
NameError: name 'os' is not defined
```
on line 2, which uses `os.environ` before `import os`.

## Root Cause
The script uses `os.environ` on module line 2 but `import os` does not appear until later in the file, after it has already been consumed. This is a real source bug — retrying will fail identically.

## Response
Do NOT retry the script. Handle the closure manually:
1. Verify each dispatched journal in both eval stores (bare relpath grep)
2. Bridge missing ones via manual JSONL append
3. Skip `bridge_eval_inline.py` (also has `<hermes-home>` placeholder bug)
4. Run `verify_genuine_gap_profile.py --date <DATE>` 
5. Run `closure_closeout_check.py` manually

See `references/dispatch-closure-sequence.md` or `references/redetection-stale-state-closure-oneshot.md` for the full manual bridge recipe.