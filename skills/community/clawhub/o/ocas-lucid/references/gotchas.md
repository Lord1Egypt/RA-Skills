# Gotchas — Lucid Dream Cycle

Operational pitfalls discovered during actual dream cycle runs.

## Journal Discovery

### Alphabetical ordering trap
Glob `**/*.json` sorted alphabetically places `ocas-custodian/deep-scan-*`, `ocas-finch/scan-*`, `ocas-forge/journal-scan-*`, `ocas-spot/sweep-*` **before** `ocas-mentor`, `ocas-praxis`, `ocas-vesper`. A 40-journal cap means early batches can be 100% scan files with zero interesting signals.

**Fix**: Separate scan from non-scan journals before capping. Process all non-scan journals first (there are typically ~70-75 vs ~300 scans), then process scans in subsequent runs.

### Priority ordering is MANDATORY, not optional
Without explicit priority sorting, the first 40 files in alphabetical order will be mostly dispatch/forge/praxis praxis-ingest files — all pure metrics. The interesting signals (mentor, vesper, custodian-light) are sorted LATE alphabetically and get cut off by the cap.

**Correct priority order** (implement as a sort key, not just "interesting first"):
1. `ocas-mentor` (highest priority — behavioral corrections in `notes`)
2. `ocas-vesper` (decisions + entity data)
3. `ocas-praxis` (reviews/debriefs with `reasoning_summary`)
4. `ocas-taste` (consumption patterns)
5. `ocas-dispatch` (triage/draft — usually skip but check)
6. `ocas-spot` (individual spot checks — usually skip)
7. `ocas-forge` (non-scan runs)
8. `ocas-custodian` (non-scan: deep-*, light-*)
9. Everything else (scans)

### Scan filename patterns to exclude
```
scan, sweep, watch-sweep, deep-scan, light-, daily-, weekly-, journal-scan
```
Also exclude `task-list.json` (not a journal entry).

**CRITICAL EXCEPTION**: The `light-` pattern matches `ocas-mentor/mentor-light-*` files, which are HIGH-VALUE interesting journals. Always apply skill-level exceptions before pattern matching:
- `mentor-light-*` → **NOT a scan** (interesting, priority 0)
- `mentor-light-caller-*` → **NOT a scan** (interesting)
- `ocas-vesper/*` → **NOT a scan** (all vesper files are interesting)
- `ocas-taste/*` → **NOT a scan** (all taste files are interesting)
- `praxis-review-*`, `praxis-debrief-*`, `praxis-update-*` → **NOT a scan** (interesting)
- `dispatch-triage-*`, `dispatch-draft-*` → **NOT a scan** (interesting, but low signal)

Better approach: check `skill name` in path first, then apply filename patterns only within scan-prone skills (custodian, finch, forge, spot).

### Non-obvious interesting files
- `ocas-custodian/deep-*.json` (without "scan" in name) — may contain actual findings
- `ocas-custodian/light-*.json` — **NOT pure scans**; starting ~June 14 these contain meaningful lesson/blocker content (scores 6-7). Always classify, never auto-skip.
- `ocas-forge/r_update.json` — update summary, may have substance
- `ocas-forge/r_*.json` (numeric prefix, no "journal-scan" in name) — may be actual forge runs
- `ocas-spot/spot-*.json` (without "sweep" or "watch" in name) — individual spot checks, may have findings

## Cursor Management

### First run cursor placement
The cursor should point to the **last file actually processed** (by the prioritized ordering), not the last file alphabetically. If you process interesting-first, the cursor should be the last interesting journal, not a scan file that was skipped.

### Cursor format
The `config.json` `cursor` field stores absolute path. The `cursor_file` field stores the relative path (from `source_journals_path`). Keep both in sync.

## Scoring / Classification

### `notes` field is the primary signal source
Most OCAS journals store meaningful content in a `notes` field (string), not in nested structures. Always extract `notes` for narrative analysis.

### `reasoning_summary` in dispatch journals
`ocas-dispatch` journals store the actual decision reasoning in `content["decision"]["reasoning_summary"]`, not at the top level. Check nested paths.

### Payload keys are NOT content
Do NOT serialize the full JSON and scan for keywords — this matches payload dictionary **key names** (like `lessons_extracted`, `signals_created`) which inflate scores for routine operational journals. Only scan narrative text fields.

### Low base rate of interesting content
Out of 374 journals, only ~15 (4%) scored >=3. This is normal. Most OCAS journals are operational records (scans, sweeps, routine runs). A run that files 0-2 journals and recirculates 10-15 is healthy.

### Scale: massive backlogs require multi-batch runs
As of June 2024, the journal directory contains **4,072+ journals** across all skills. The `ocas-mentor` directory alone has **2,659 files**. A single 40-journal batch can be entirely consumed by mentor scan files. **Mitigation**: Process 200+ journals per dream cycle run (5+ batches of 40). The cursor advances through scans in subsequent runs. Use the multi-batch script pattern from the June 20 run.

### `entities_observed` field type mismatch
Some journals store `entities_observed` as an **integer** (count) instead of a list. The `extract_entities()` function must guard:
```python
eo_list = journal.get("entities_observed", [])
if not isinstance(eo_list, list):
    eo_list = []
```
Without this guard, `TypeError: 'int' object is not iterable` crashes the entire batch.

### `ocas-spot/spot-*` files are interesting
Individual spot checks (`ocas-spot/spot-*.json`) without "sweep" or "watch" in the filename are **NOT scans** — they contain actual findings. Only `sweep-*`, `watch-sweep-*`, and `spot-watch-*` files are scans.

### Files at skill root level (not in date subdirs)
Some skills write journals directly in the skill directory (e.g., `ocas-custodian/esc-run-*.json`) without date subdirectories. The file discovery loop must handle both `date_dir/*.json` and `skill_dir/*.json` patterns.

## Data Integrity

### Decisions file grows fast
Each processed journal writes one decision record. With 374 journals and ~300 scans = ~374 decisions per full pass. Implement log rotation or compaction after 90 days.

### Ingestion log cursor tracking
The ingestion log tracks `run_id` + `filepath`. For cursor resumption, check which filepaths appear in the log and skip them. Don't rely solely on the `cursor` field — it's a hint, but the ingestion log is the source of truth.

## Cron Environment

### `execute_code` blocked
In cron mode, `execute_code` is blocked. Write Python scripts to `/tmp/` via `write_file`, then invoke via `terminal(command="python3 /tmp/script.py")`.

### Timeout management
A full dream cycle with 40 journals takes ~30-60 seconds when using `write_file` + `terminal` Python. The script itself typically completes in <10 seconds for 40 journals. Set `timeout=120` on terminal calls to be safe.