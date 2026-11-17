# Forge Gotchas / Pitfalls (compact)

## `proposals/` and `processed/` are mirrors, not pending work
Count ONLY files in `commons/data/ocas-forge/intake/` excluding `intake/processed/`. Use `scripts/forge_count_unprocessed.py` — never `find`/`os.walk` the whole tree (overcounts both mirrors, falsely flips `routine_no_op`→`genuine`).

## `<hermes-home>` placeholder bug in closure scripts
`closure_closeout_check.py`, `verify_genuine_gap_profile.py`, `closure_convergence_sweep.py`, `bridge_eval_inline.py` all contain the literal `<hermes-home>` placeholder and crash at runtime with `FileNotFoundError`. Do NOT retry — manually verify gates and bridge instead. See `references/closure-script-path-placeholder-bug.md`.

## `run_mixed_wave_closure.py` crashes with `NameError: name 'os' is not defined`
Uses `os.environ` before `import os`. Retrying fails identically. Handle closure manually. See `references/run-mixed-wave-closure-crash-os-import.md`.

## Eval-store grep must use bare relpath
Always grep with `ocas-mentor/2026-07-16/file.json`, NEVER `commons/journals/ocas-mentor/...`. Store keys by bare relpath; prefix-grepping returns ABSENT for present journals.

## JSON structural edits: use `write_file`, not `patch`
`patch` can produce nested duplicates and trailing-comma JSON errors that the tool reports as success. Rewrite whole file, then validate with `python3 -c "import json; json.load(open(path))"`.

## Programmatic SKILL.md surgery can eat `---` fence
A stray slice that includes the frontmatter closing `---` silently destroys the YAML delimiter. Re-run `score_skill()` after any programmatic edit and watch D1/D2 — a sudden drop means the fence is gone.

## Tool-layer flake: `skill_view`/`read_file`/`write_file`/`search_files` return `DaemonThreadPoolExecutor` error
Intermittent API flake affecting read/write tools but NOT `terminal()`. After 1-2 failures, route around it with `terminal()` `cat`/`find`/`grep` — do NOT burn 3+ retries.

## Never recursive-glob `commons/journals/**/*.json` for closure diagnosis
Symlink loop nests directories to arbitrary depth. Use bounded per-skill `commons/journals/<skill>/<DATE>/*.json` globs.

## `verify_eval_no_phantoms.py --fix` destroys historical eval entries
The script walks the ENTIRE eval store, not date-scoped. Running `--fix` mass-deletes historical lines. Use only for dedicated audits, never during closure passes.

## Re-detection recurs because wave writer doesn't advance gates atomically
`dispatch-wave-*.json` is written but monitor `latest_mtime` + praxis `last_ingest_run` stay at pre-wave values. Manual `closure_closeout_check.py` + dual-copy state advance is the stopgap. ALWAYS advance both monitor copies PROFILE-relative and root.

## Mtime-advance truncation trap
NEVER hand-type the float/ISO mtime literal — truncation below 1e-5 causes `state < max_journal_mtime` and perpetual re-fire. ALWAYS recompute `max(os.path.getmtime(p) for p in glob(...))` programmatically + ≥1s pad.

## Scheduled dispatcher re-fires mid-closure clobbers email-state files
Re-flag `verified_second_wave` after EACH state file write batch. Do NOT chase permanently-green `[3]` on top-level GWS-snapshot files — they're known un-closeable under the re-fire bug.

## Recursive `**/last_email_check*.json` over-pertains indigo
During owner-specific closure, target owner files by EXPLICIT paths only. Never a blanket recursive glob.

## Dispatch eval-store entries keyed three (four) ways
DISPATCH store keys `"filename"`, `"journal_id"`, `"journal"`, and `"journal_file"`. Scanners must union ALL keys and normalize `journals/` prefixes. Any new writer must either use one of these keys or update both scanners.

## Fork-pr-fix dispatch pattern
When a GitHub CI failure is traced to a fork PR (not an internal commit), the dispatch must: (1) identify the fork owner + branch from CI metadata, (2) open a PR from that fork, (3) merge, (4) document the fix as `fix_forward` action. Do NOT treat as routine CI failure — the fork PR is the delivery mechanism, not the incident.