# 10khr Grind Workflow (operational)

Condensed procedure for grinding the lowest-scoring ocas-*/util-* skill to 50/50.
Companion to `scripts/critique_10khr_runner.py` and `references/critique-rubric.md`.

## Steps

1. **Rank:** Do NOT use `--report-only` if you need the skip rule intact — it calls
   `save_state()` and advances `last_run` to *now*, so the mtime/skip comparison
   becomes invalid (every skill reads as "modified since last_run"). Assess WITHOUT
   mutating state instead: import the runner and call its functions directly —
   `import importlib.util; spec=importlib.util.spec_from_file_location("runner", "scripts/critique_10khr_runner.py"); runner=importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)`
   then `runner.run_full_assessment()` / `runner.score_skill(name, path)`. This keeps
   `10khr-state.json:last_run` at the prior grind timestamp (the value the skip rule
   must compare against). Or snapshot `last_run` from the state file before the call
   and restore it after.
2. **Skip logic:** lowest skill below 50 — if its SKILL.md `stat` mtime is NOT newer than
   `10khr-state.json` `last_run` AND its heuristic score is `>= 44`, skip to the next lowest.
   If all below-50 skills are unmodified since `last_run` AND score `>= 44`, report
   "nothing to grind" and stop. (Verified in the 2026-07-18 finch:work pass: 8 eligible
   targets ground, 9 correctly skipped.)
3. **Find the WHY:** read `critique_10khr_runner.py:score_skill()` — the heuristic is
   mechanical, not semantic:
   - **D3** penalizes `total_lines > 450` (and code ratio >20%). Cut lines by extracting
     inline operational detail (already pointer-referenced) into `references/<topic>.md`.
   - **D9** flags any script lacking the token `--help` / `usage` / `argparse`. argparse
     scripts auto-provide `--help`, but enrich their `help=` text with flags + examples;
     shell scripts need an explicit `--help`/`usage` branch.
   - **D1/D2** drop hard if the frontmatter YAML fails to parse.
4. **Fix each dim < 5** using the rubric's per-dimension fix list (D1 metadata, D2
   When/Keywords/NOT, D3 extract to references/, D4 support-file-map, D5 checklists,
   D6 why-for-rules, D7 error table, D8 on-demand When-to-read, D9 --help, D10 gotchas).
5. **Re-score after every fix.** Iterate until ALL ten dimensions are 5/5 — 50/50 means
   every dimension, not "most fixed."

## Critical guard: frontmatter fence

Any programmatic SKILL.md edit (Python slice / `del` / reassembly) can eat the closing
`---` of the frontmatter, silently voiding the YAML and dropping D1->1 / D2->3.
**Always re-run `score_skill()` right after the edit** and verify with
`yaml.safe_load(content.split('---')[1])`. Re-insert `---` at the boundary if missing.
(First-class pitfall recorded in `ocas-forge`'s Gotchas as of 2026-07-16.)

## State bookkeeping

Record the fix in `10khr-state.json`: `last_target`, `last_score_before/after`,
append to `skill_history` (with the concrete fix text + `grounded: manual+D9-verified`),
increment `skills_improved`, and set `current_target` to the next lowest skill.