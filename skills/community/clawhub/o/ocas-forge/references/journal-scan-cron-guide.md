# Journal Scan — Cron Mode Guide

The `forge:journal-scan` cron job (`*/5 * * * *`) runs without a user present.
This means **`execute_code` is blocked at runtime**. Do not call it.

## What to use instead

| Task | Tool | Example |
|------|------|---------|
| Scan directories for JSON files | `terminal()` with `find`, `ls` | `find ... -name "*.json"` |
| Read proposal/decision file contents | `read_file()` | Read individual `.json` files |
| Compare file lists (intake vs processed) | `terminal()` with shell `grep` | Loop + `grep -q` |
| Write journal entry | `write_file()` | Write JSON journal to `commons/journals/ocas-forge/` |
| Apply fixes to target skills | `patch()` | Targeted edits to target skill files |
| Append to decisions.log | `terminal()` with `echo >>` | `echo '{...}' >> decisions.jsonl` |

## Where proposals can land

Mentor drops VariantProposal and VariantDecision files in multiple locations.
Check ALL of these during a scan:

1. `{agent_root}/commons/data/ocas-forge/intake/` — primary intake directory
2. `{agent_root}/commons/data/ocas-forge/proposals/` — subdirectory where newer proposals may land
3. `{agent_root}/commons/data/ocas-forge/` (data root) — stale copies can linger here

## Cross-reference against processed

Check BOTH locations for already-processed filenames:
- `{agent_root}/commons/data/ocas-forge/intake/processed/`
- `{agent_root}/commons/data/ocas-forge/processed/`

Any `.json` file in the scan locations above that is NOT in either processed
directory is unprocessed and should be handled.

## After processing

1. Copy (don't move) processed files to `processed/` — originals may stay in `proposals/`
2. Write journal to `{agent_root}/commons/journals/ocas-forge/YYYY-MM-DD/`
3. Append decision to `decisions.jsonl` via `echo >>`

## Common pitfall: proposals/ not intake/

As of May 2026, Mentor dropped proposals into `proposals/` subdirectory rather
than `intake/`. If you only check `intake/` and the data root, you will miss
these. Always include `proposals/` in the scan.

## Common pitfall: path mismatch in cross-reference

When using `comm` to compare file lists between `proposals/` and `processed/`
directories, **strip the directory prefix first**. `comm` compares lines
literally — `proposals/vp_0625cecd.json` will never match `vp_0625cecd.json`,
making every file appear unprocessed.

**Wrong:**
```bash
comm -23 <(ls proposals/*.json | sort) <(ls processed/*.json | sort)
```

**Right:**
```bash
comm -23 <(ls proposals/*.json | sed 's|proposals/||' | sort) \
         <(ls processed/*.json | sed 's|processed/||' | sort)
```

Or use `basename`:
```bash
comm -23 <(for f in proposals/*.json; do basename "$f"; done | sort) \
         <(for f in processed/*.json; do basename "$f"; done | sort)
```

After running the comparison, **verify with a spot-check**: pick one filename
from the "unprocessed" list and `ls` it in the processed dir to confirm it's
actually missing before taking action.

## Common pitfall: unifying two processed directories for cross-reference

There are TWO processed directories: `intake/processed/` and `processed/`. Both
must be unified into a single deduplicated set before comparing against the
proposals list. If you `ls` both dirs in a single pipeline without dedup, a
file that exists in both processed dirs will appear twice on the right side —
but that's harmless. The real danger is the opposite: if you only check ONE
of the two processed dirs, files that were copied to the other will appear
as false positives (unprocessed).

**Wrong (only checks one processed dir):**
```bash
comm -23 <(ls proposals/*.json | xargs -I{} basename {} | sort) \
         <(ls processed/*.json | xargs -I{} basename {} | sort)
```

**Right (unifies both processed dirs with dedup):**
```bash
comm -23 \
  <(ls proposals/*.json | xargs -I{} basename {} | sort -u) \
  <(cat <(ls intake/processed/*.json 2>/dev/null | xargs -I{} basename {}) \
        <(ls processed/*.json 2>/dev/null | xargs -I{} basename {}) \
   | sort -u)
```

The `2>/dev/null` guards against the case where one of the processed dirs
doesn't exist yet (e.g., fresh Forge install). The `sort -u` on each side
ensures clean comparison even if a file exists in both processed dirs.

## Common pitfall: `config.json` false positive in data root scan

When scanning `{agent_root}/commons/data/ocas-forge/*.json` for unprocessed
proposal/decision files, the `config.json` file (Forge's own config) will appear
as a "new" file if you only check against processed directories. It is NOT a
proposal or decision — skip it.

**Fix:** When scanning the data root, exclude `config.json`:

```bash
find {agent_root}/commons/data/ocas-forge/ -maxdepth 1 -name "*.json" \
  ! -name "config.json" -type f
```

Or filter it out in the cross-reference step: after building the list of
candidate files, remove any filename that is exactly `config.json` before
comparing against processed.

## Common pitfall: `write_file` does not resolve template placeholders in paths

When writing the journal entry with `write_file()`, the `path` parameter is taken
literally -- template placeholders like `{{unix}}`, `{{timestamp}}`, or similar
are **not** auto-resolved. Using `path:
".../r_20260605_journal-scan-{{unix}}.json"` will create a file with a literal
`{{unix}}` in the name, requiring a manual `mv` to fix.

**Always resolve timestamps before calling `write_file`:**

```bash
# Resolve the timestamp first via terminal
TS=$(date +%Y%m%d%H%M%S)
# Then use the resolved value in the write_file path
```

Or get a UNIX timestamp:
```bash
date +%s   # returns e.g. 1780707441
```

**Wrong:**
```
write_file(path=".../journal-scan-{{unix}}.json", ...)
```

**Right:**
```
# Step 1: terminal("date +%s") -> e.g. 1780707441
# Step 2: write_file(path=".../journal-scan-1780707441.json", ...)
```

## Common pitfall: single-quoted heredoc prevents variable expansion

When writing JSON journal entries via `cat > file << 'EOF'`, the single quotes
around `EOF` prevent ALL shell variable expansion. `$VAR`, `$(date ...)`, and
`${TS}` are written as literal strings — not their expanded values.

**Wrong (single-quoted heredoc — variables NOT expanded):**
```bash
cat > "$JOURNAL_DIR/forge-scan-${TS}.json" << 'EOF'
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.000000+00:00)",
  "run_id": "forge-scan-${TS}"
}
EOF
```
Result: `timestamp` field contains literal `$(date -u +%Y-%m-%dT%H:%M:%S.000000+00:00)`.

**Right (use write_file for JSON, or double-quoted heredoc with care):**

Option A — use `write_file()` (preferred for JSON):
```python
# Resolve timestamp in Python, write via write_file
now = datetime.now(timezone.utc)
ts = now.strftime('%Y%m%dT%H%M%SZ')
path = f"{journal_dir}/forge-scan-{ts}.json"
content = json.dumps({"timestamp": now.isoformat(), "run_id": f"forge-scan-{ts}"}, indent=2)
write_file(path=path, content=content)
```

Option B — if you must use heredoc, use double quotes (but escape inner `"` and `$`):
```bash
cat > "$JOURNAL_DIR/forge-scan-${TS}.json" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.000000+00:00)",
  "run_id": "forge-scan-${TS}"
}
EOF
```
Note: Double-quoted heredoc expands variables but requires escaping `\"` inside JSON strings.

**Best practice: Use `write_file()` for all JSON journal writes.** It avoids heredoc quoting issues entirely and produces valid JSON without manual escaping.

## Second-Wave Self-Referential Dispatch Pattern (confirmed 2026-06-26)

When the dispatcher triggers on journals written by its own prior waves:

1. **Read the journal content first** — if `type` contains "dispatch.wave", "multi-skill", "heartbeat", or `result: "no_op"` → it's an output journal, skip without loading skills
2. **Check `journals_evaluated.jsonl`** — if all listed journals are already evaluated → log as `all_already_evaluated`, write no-op journal, exit
3. **If genuinely new journals exist** — process only the unevaluated ones
4. **After processing** — add ALL dispatch-output journals to eval file and advance `last_ingest_run`

**Confirmed 2026-06-26 wave ~#24:** Dispatch listed 5 journal files (forge-scan, mentor-light ×2, praxis-dispatch, dispatch-wave). All were outputs from waves 22-23. All already in eval file. Clean no-op.

### Eval File Gap Edge Case (confirmed 2026-06-26 dispatch #142)

Even when `last_ingest_run` is set to a timestamp AFTER a journal's file timestamp, that journal can still be MISSING from the eval file. The Praxis state's `last_ingest_run` is updated at the END of a dispatch wave, but individual journals from that wave may not have been added if the eval check was skipped or if the journal was written by a different pipeline (e.g., Mentor cron) that doesn't update Praxis state.

**Fix:** During second-wave handling, ALWAYS check each dispatcher `new_file` individually against the eval file with `grep -q "filename" eval_file` — never assume `last_ingest_run` coverage. If a journal is missing from eval file, add it before writing no-op journals.

**Detection:** `grep -q "filename" journals_evaluated.jsonl` returns exit code 1 if missing.

### Partial Cycle Gap Between Sibling Pipelines (confirmed 2026-06-26 dispatch #146)

A sub-variant of the cron journal gap where one cron pipeline's journal is in the eval file but another cron pipeline's journal from the SAME cycle is absent. Example: `mentor-light-20260626T073205Z` present in eval, but `praxis-cron-20260626T073343Z` (written 90 seconds later) missing.

**Root cause:** Praxis cron ingest processed the mentor journal but completed before the praxis-cron journal was written, or the eval check only covered journals already in the state's `last_ingest_run` window. The two pipelines (mentor and praxis) write independently and their journals may straddle an ingest boundary.

**Fix:** Same universal rule — `grep -q "filename" journals_evaluated.jsonl` for EVERY `new_file` individually, regardless of whether sibling journals from the same cycle are already present. Never infer that "if mentor-light is evaluated, praxis-cron from the same cycle must be too."

### Third-Wave Mitigation Scope (confirmed 2026-06-26)

After second-wave handling, add ALL relevant journals to the eval file — not just the 4 dispatcher `new_files`, but also the 3 dispatch-output journals written by the current wave (forge-scan, mentor-light, praxis-dispatch). This prevents the next wave from detecting its own outputs as "new".

**Pattern:** Add 7 total journals (4 prior-wave + 3 current-wave) to eval file, then advance `last_ingest_run` past all of them.

## Phantom file cleanup after every dispatch run (confirmed 2026-06-25)

After writing any journal or eval file during a dispatch run, `ls` the target directory and check for:
1. **Typo phantom files** — filenames similar to expected but with a character transposition or suffix difference (e.g., `journals_evaligated.jsonl` vs `journals_evaluated.jsonl`, `forge-scan-.json` vs `forge-scan-20260625T154905Z.json`)
2. **Empty-timestamp files** — `forge-scan-.json`, `mentor-light-.json` (bash `${}` expansion consumed by shell)
3. **TS_PLACEHOLDER files** — literal `TS_PLACEHOLDER` in filename from failed Python string interpolation in `terminal()`
4. **Zero-byte JSON files** — write failures that created the file but wrote no content

**Detection:**
```bash
# Check for files with empty timestamp fields
ls /path/to/journals/ | grep -E "^-*\.json$"
ls /path/to/journals/ | grep "PLACEHOLDER"
find /path/to/journals/ -name "*.json" -size 0
```

**Fix:** Delete phantom files immediately. They will be detected as "new" by the next dispatcher wave and cause spurious re-processing.

**Root cause:** Python f-strings inside `terminal()` are vulnerable to bash `${}` expansion. `f'forge-scan-{TS}.json'` where `${TS}` is a shell variable produces `forge-scan-.json`. Always use string concatenation (`'forge-scan-' + ts + '.json'`) or `write_file` to compose paths in `terminal()`.