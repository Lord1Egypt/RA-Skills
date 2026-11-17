# Hard-won QA protocol notes (run `20260721T082708Z`)

Use as a quick reminder alongside `qa-testing.md`.

1. **Single-arm dispatches only**: one `delegate_task` per arm. Batches can zombie and hold concurrency slots; singles complete reliably, sometimes synchronously when the pool is at capacity.
2. **Mid-run recovery**: if the session drops, read `<RUN_DIR>/results.jsonl` and `.run_meta.json`, find last completed test_id, resume there. Do not start a new RUN_ID.
3. **Honest partial-run reporting**: if sectors/traps cannot complete, count honestly: executed vs planned; explicit CANNOT-RUN list; explicit INVALID list. Do not pad with prose.
4. **Empty arm = INVALID, no rescue from sibling seed**: if an arm dir has no model-produced artifacts after dispatch, mark it INVALID immediately. Do not write control files yourself, do not copy from treatment. Re-seed clean and re-dispatch a fresh arm dir (`<test-id>-v2/`).
5. **Verify imports reference same-arm files**: after every arm run, every top-level non-stdlib import must resolve to a `.py` file present in the same arm dir. Mismatch → mark arm INVALID unless the task explicitly allowed moving files.
6. **QA runner must not mutate arm dirs under live test**: create seeds before dispatch; use temp verify scripts under `%TEMP%\hermes-verify-<test>-<arm>.py`. Arm dirs are read-only after dispatch until judge/evaluation.
7. **Post-run sanity checks**: `results.jsonl` must have unique `test_id` count == line count; every record exactly one verdict; sums match total lines. Regenerate REPORT.md table from jsonl after edits; do not hand-maintain counts.
8. **Windows/MSYS invocation rule**: on Windows/MSYS, quote paths or use POSIX forward-slash form (`/c/Users/.../`); otherwise MSYS rewrites `C:\\Users\\...` and breaks the command. Failure mode is silent corruption, not obvious error.
