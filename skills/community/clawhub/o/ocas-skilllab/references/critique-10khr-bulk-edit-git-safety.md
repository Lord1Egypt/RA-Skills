# Bulk Script Edits Across Skills — Corruption & Safe Recovery (2026-07-15 incident)

## What went wrong
A grind of 24 ocas/util skills needed `--help` guards on scripts (D9). Instead of fixing
one script at a time, a helper script (`d9_fix.py`) iterated every skill's `scripts/` and
rewrote files lacking a help token.

Bug: the injection regex matched only `if __name__ == "__main__":` (double quotes). On
scripts using single quotes or indentation, it failed to find the block and **appended a
second `if __name__ == "__main__":`**, producing invalid syntax. Result: **41 scripts across
9 skills stopped parsing.**

Worse: to "recover," `git checkout -- .` was run (correct — reverted tracked files) **and
`git clean -fd`** (disastrous — deleted 9 pre-existing untracked skill files with no git
history to restore them). The fixer only writes to existing files, so it never created
those untracked files; `clean` destroyed them.

## Rules
1. **Fix scripts one skill, one file at a time.** After each `patch`, verify
   `python3 -c "import ast; ast.parse(open('scripts/X.py').read())"` AND
   `python3 scripts/X.py --help` exits 0, before touching the next file.
2. **Never run a bulk edit script across many skills without per-file verification.**
   Test the edit script on ONE file first; confirm parse + behavior; then expand.
3. **Recovery from a corrupted-script incident = `git checkout -- .` ONLY.**
   Run it per skill repo (`git -C <skill> checkout -- .`). This reverts tracked modifications.
4. **NEVER `git clean -fd` as a recovery tool.** It deletes untracked files irreversibly.
   Before any `clean`, list first: `git clean -nd` or `git status --short`. Only remove
   files YOU created this session. Pre-existing untracked skill files (configs, sources,
   generated artifacts) are lost forever once cleaned.
5. **Edit-script regexes must match both quote styles + indentation:**
   `re.search(r'if\s+__name__\s*==\s*["\']__main__["\']\s*:\s*\n', txt)`
   Insert the guard immediately after `m.end()`.

## Safe per-file D9 fix loop (the correct approach)
```
for sk in <skill-list>; do
  for s in "$sk"/scripts/*.{py,sh}; do
    [ -f "$s" ] || continue
    # check importers first; if found, only add guard inside __main__, never top-level
    grep -rE "import $(basename "$s" .*)|from $(basename "$s" .*) import" "$sk"/scripts/ && continue
    # patch guard (python: inside __main__; bash: case after set -u)
    # VERIFY before next:
    python3 -c "import ast; ast.parse(open('$s').read())"   # must succeed
    python3 "$s" --help || bash "$s" --help                 # must exit 0
  done
done
```

## Files lost in the 2026-07-15 incident (audit trail)
- ocas-bower/scripts/bower_drive_sdk_light_scan.py
- ocas-taste/scripts/styx_taste_feed.py
- ocas-usercontext/scripts/cron_calendar_fetch.py
- ocas-haiku/scripts/verify_follows.py
- ocas-reach/scripts/sources/dahd_open_data.py
- ocas-reach/scripts/sources/metmuseum.py
- ocas-styx/scripts/backfill_merchant_entity_id.py
- ocas-styx/scripts/build_merchant_master.py

(Not in any git history, not referenced by other scripts — no broken imports, but the files
themselves are unrecoverable. Treat as a permanent lesson, not a retryable error.)