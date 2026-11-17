# QA run coverage vs integrity

Session lesson: `validate_run.py` proves that each JSONL record is internally checkable, but it does not prove the full QA battery was actually executed.

A run can mechanically pass integrity while still being low-value if the executor fills unrun tests with `INCONCLUSIVE` placeholder arm dirs. That is honest only if the report clearly says the battery was not executed past the stop point; it is not evidence about the skill.

## Rule for future QA runs

1. Keep `validate_run.py` as the integrity gate: empty arms, cross-run paths, control contamination, false identical claims, and false tool-output claims must fail.
2. Add a separate coverage gate before publishing: compare `results.jsonl` against the expected test manifest from `templates/qa-prompt-final.md`.
3. For every expected test, require one of:
   - both arms have real model-produced files and `api_calls_control >= 1`, `api_calls_treatment >= 1`;
   - `CANNOT-RUN` with a technical prerequisite recorded before dispatch;
   - `INCONCLUSIVE` with actual dispatch evidence and a concrete infra failure, such as timeout after waiting for files.
4. Do not create unexecuted placeholder arms simply to reach the expected test count. If the run must stop early, say `battery incomplete` and list the unexecuted tests separately.
5. Treat `validate_run.py: exit 0` as necessary but not sufficient. The final report should include both `integrity: pass/fail` and `coverage: complete/incomplete`.

## Reporting wording

Use this distinction in `REPORT.md`:

- `Integrity`: every recorded verdict is backed by artifacts inside this RUN_DIR.
- `Coverage`: the requested battery was actually executed. If not, name the first test where execution stopped and mark later tests as `not executed`, not as behavioral evidence.

This prevents an integrity-clean but mostly unexecuted run from being mistaken for a complete skill evaluation.
