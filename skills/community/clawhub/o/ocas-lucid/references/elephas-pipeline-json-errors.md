# Elephas Pipeline — JSON Parse Error Pattern

Observed 2026-06-19: the `elephas_cron_pipeline.py` silently skips ~43% of `mentor-light-*` journal files due to JSON parse errors.

## Symptom

```
SKIP mentor-light-20260606T035357Z.json: parse error: Expecting ',' delimiter: line 4 column 31 (char 99)
SKIP mentor-light-20260606T214328Z.json: parse error: Expecting value: line 13 column 26 (char 350)
SKIP mentor-light-20260607T093727Z.json: parse error: Expecting value: line 13 column 28 (char 364)
SKIP mentor-light-20260614T115612Z-caller.json: parse error: Invalid control character at: line 19 column 86 (char 965)
```

Common error types:
- `Expecting ',' delimiter` — trailing comma before `}` or `]`
- `Expecting value` — embedded `null` without quotes, or truncated file
- `Invalid control character` — literal newline/tip in a string value (common in `notes` fields with unescaped newlines)
- `Extra data` — multiple JSON objects concatenated without array wrapper

## Root Cause

The `ocas-mentor` skill writes journal files using `json.dump()` but some fields (particularly `notes` and `reasoning_summary`) contain raw text from LLM output that includes:
1. Unescaped newlines (literal `\n` characters in strings)
2. Trailing commas from Python dict serialization
3. Multiple JSON objects in one file (streaming append without array structure)

## Impact on Elephas

- Files with parse errors are logged as `SKIP` and the ingestion log entry is still written (with `entities_count: 0, signals_count: 0`)
- The elephas pipeline does NOT fix or report these errors upstream
- Over time, the fraction of skipped files accumulates, reducing elephas's effective coverage

## Impact on Lucid

- Lucid's dream cycle script uses `try/except (json.JSONDecodeError, IOError)` to gracefully skip unreadable files
- This is sufficient — Lucid does not need to parse elephas-specific entity data, only classify by narrative content
- The parse errors are a Lucid non-issue (files just get skipped with a log entry)

## Recommended Mitigation

When running elephas pipeline and observing >20% parse error rate:
1. Sample 2-3 of the skipped files to confirm the error pattern
2. Report to <operator> that `ocas-mentor` is producing malformed JSON (this is a mentor skill bug, not an elephas bug)
3. Do NOT attempt to fix the JSON files in-place — this corrupts the source data for other consumers
4. The pipeline's graceful skip behavior is correct; the fix belongs in the producer (mentor skill)

## Pipeline Output Verbosity

The `elephas_cron_pipeline.py` prints extensive `DEBUG:` lines to stdout:
```
DEBUG: Decision log written
DEBUG: journal_dir = <hermes-home>/commons/journals/ocas-elephas/2026-06-19
DEBUG: journal_dir created/exists
DEBUG: journal_path = ...
DEBUG: journal_path.exists() before = False
DEBUG: journal_path.exists() after = True
DEBUG: journal_path.absolute().exists() = True
DEBUG: os.path.exists = True
DEBUG: os.path.isfile = True
```

This is expected behavior (not a bug). In cron mode, this output is captured in the job log. The DEBUG lines are harmless but verbose — do not treat them as errors.