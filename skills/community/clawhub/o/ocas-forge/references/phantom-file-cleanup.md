# Phantom File Cleanup Pattern

After every dispatch run, `ls` the journal directory and check for files with:
1. Empty timestamp fields (e.g., `forge-scan-.json`)
2. Double timestamps (e.g., `dispatch-20260626T20260626T082335Z.json` — the timestamp was interpolated into the filename AND the shell heredoc added another)
3. Literal `TS_PLACEHOLDER` in the filename

**Double-timestamp cause:** When the shell variable `TS` is used inside a Python f-string that's inside a heredoc, the outer `T` gets consumed by one interpolation and the inner `TS` by another, producing `20260626T20260626T082335Z` instead of `20260626T082335Z`.

**Fix:** Rename to correct format, update `run_id` field inside the JSON to match.

**Prevention:** Use `write_file` for JSON journals — it's atomic and can't produce malformed filenames. Only use `terminal()` heredoc for non-JSON files.

## Double-Timestamp Filename Pattern (confirmed 2026-06-26 dispatch #150)

**Symptom:** A journal file is named `dispatch-20260626T20260626T082335Z.json` instead of `dispatch-20260626T082335Z.json`. The timestamp appears twice.

**Root cause:** In `terminal()`, a Python script uses `f'{ts}.json'` where `ts` is a Python variable. But the shell heredoc has already expanded `${TS}` (a shell variable) to the same timestamp value, and the Python variable name `ts` in the f-string gets partially consumed by bash's `${}` expansion. The result is the timestamp appearing in both the shell-expanded portion and the Python-interpolated portion.

**Fix procedure:**
```bash
# Rename
mv 'dispatch-20260626T20260626T082335Z.json' 'dispatch-20260626T082335Z.json'
# Fix run_id inside
python3 -c "
import json
f = 'dispatch-20260626T082335Z.json'
with open(f) as fh: data = json.load(fh)
data['run_id'] = 'dispatch-20260626T082335Z'
with open(f, 'w') as fh: json.dump(data, fh, indent=4)
"
```

**Prevention:** Never compose JSON filenames via shell variable interpolation inside `terminal()`. Use `write_file` to write a script to `/tmp/`, then invoke with `python3 /tmp/script.py`.

## False-Positive: Year in Time Portion (confirmed 2026-06-28 dispatch)

**Symptom:** A grep for double timestamps (`grep -E '2026.*2026'`) flags a journal like `mentor-light-20260628T202602Z.json` as a phantom. However, `T202602Z` is a **valid time** — hour 20, minute 26, second 02. The year "2026" appears in both the date (`20260628`) and the time (`T202602`) portions, which is coincidental but legitimate.

**Root cause:** The phantom detection regex doesn't distinguish between the date portion and the time portion of the filename. During 2026, any timestamp between `T20:00:00Z` and `T20:59:59Z` will contain "2026" in the time field (e.g., `T202602` = 20:26:02).

**Fix:** Refine the phantom detection to check for genuinely malformed patterns only:
- Double full date: `2026[01][0-9][0-3][0-9]T2026[01][0-9][0-3][0-9]T` (full date repeated)
- Empty field: `--.json` or `.-.json`
- Not time-portion overlap: `T20[0-5][0-9][0-5][0-9]Z` in the time portion is VALID

**Rule:** When `grep` flags a file, always inspect the time portion before declaring it a phantom. A timestamp like `T2026XXZ` where the part after `T` parses as HHMMSS (20:26:XX) is NOT a phantom.