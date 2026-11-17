# QA Isolation Protocol

Hard-won rules for running QA/agent sessions without corrupting the skill tree.
Every rule here was discovered the hard way on 2026-07-21/22.

## The problem

Prompt-level rules (П10/П11 "don't edit the skill dir") are NOT enforced by weak models.
Observed: Nemotron 3 Ultra, Step 3.7 Flash, North Mini Code, DeepSeek V4 Flash all wrote
into the skill directory despite explicit prohibitions. Nemotron even overwrote the
integrity gate itself (`validate_run.py`). This is not a bug in the prompt — weak models
genuinely cannot reliably follow negative instructions under task pressure.

## Protocol (before → during → after)

### Before the run
```bash
python workspace_guard.py isolate-skill-tree <skill_dir>
python snapshot_skill.py snapshot   # baseline BEFORE any run touches the tree
```
- `isolate-skill-tree` sets read-only on all skill files at the OS level.
  The model CANNOT write to them, regardless of what the prompt says.
- Take the snapshot BEFORE the run, not after. A post-run snapshot bakes in
  any modifications as the new baseline.

### During the run
- The run writes only to its designated RUN_DIR (e.g. `~/kw-qa/<run_id>/`).
- If the model tries to write to the skill dir, the OS rejects it (Permission denied).
  This is the only isolation that actually holds.

### After the run
```bash
python workspace_guard.py restore-skill-tree <skill_dir>
python snapshot_skill.py verify          # catches SHRINKAGE (truncation)
python snapshot_skill.py verify-additions  # catches ADDITIONS + MODIFICATIONS (via git diff HEAD)
git status --short                       # manual check: nothing unexpected changed
git diff HEAD                            # inspect any changes
```
- Restore write permissions ONLY after verify-additions confirms CLEAN.
- Stage files by explicit path: `git add <file1> <file2>`.
  **NEVER `git add -A`** — it sweeps in stale uncommitted edits from prior sessions.
- If verify-additions shows MODIFIED or UNTRACKED files you didn't touch →
  investigate before committing. Do not trust "it's fine."

## The three-layer protection model

| Layer | Catches | Tool |
|---|---|---|
| **OS read-only** | Write attempts by weak models | `workspace_guard.py isolate-skill-tree` |
| **Git diff HEAD** | Additions, modifications, stale edits | `snapshot_skill.py verify-additions` |
| **Snapshot shrinkage** | Truncation, deletion | `snapshot_skill.py verify` |

All three are needed. Any single layer has blind spots:
- OS read-only doesn't catch modifications made BEFORE isolation was applied.
- Git diff doesn't catch shrinkage within a file (verify does).
- Snapshot verify doesn't catch additions (verify-additions does).

## Pitfall: snapshot verify is misleading after rogue writes

`snapshot_skill.py verify` compares the live tree against the NEWEST snapshot. If a
snapshot was taken AFTER a rogue write, the modification is baked in as the baseline
and verify reports CLEAN. Real case: QA executors wrote 5 new files + edited SKILL.md
(+39 lines) and 7 references; a snapshot taken afterward reported CLEAN.

**Fix:** always compare against git HEAD (the last known-good commit), not against a
post-hoc snapshot. Use `verify-additions` + `git diff HEAD`.

## Pitfall: `git add -A` is a trap

`git add -A` stages everything in the working tree, including:
- Uncommitted changes from prior sessions
- Edits made by QA models during the run
- Stale files that should not be in this commit

Real case: `git add -A` pulled two stale SKILL.md maintaining-notes from an earlier
turn into an unrelated commit.

**Fix:** `git add <specific-files>` only. Check `git status --short` before committing.
If a staged file is one you did not touch this turn, decide deliberately.

## Pitfall: classify by benchmark, not alias

`.run_meta.json` may record a model alias (`SuperCombo_256k_100`) that says nothing
about tier. Always read the published SWE-bench/GPQA number. `unknown` is the honest
tier when the gating benchmark is unpublished — do not upgrade a guess to "strong."
A wrong tier label inverts the meaning of every NO-DIFF in the report.

## Pitfall: NEVER restore-skill-tree while a run is still active

`restore-skill-tree` drops the OS read-only protection. Running it while ANY QA run is still
executing (or might resume) re-opens the exact door the isolation exists to close — a
still-running model can then write into the skill dir.

Real case (2026-07-22): `restore-skill-tree` was run mid-batch to edit `qa-results/README.md`;
protection was down during active runs. No corruption that time (luck), but violated the protocol.

**Rule:** before `restore-skill-tree`, confirm ALL runs finished — check newest mtime under
every RUN_DIR (`find ~/kw-qa/<id> -type f -printf '%T+ %p\n' | sort | tail -1`) and require a
quiet gap (>30 min of no writes) vs `date`. If you must edit the skill to log results:
restore → edit → commit → **re-isolate in the same turn**. Never leave the tree writable across
turns while runs may resume.

## Pitfall: api_calls=0 is the strongest fabrication tell

A PASS or DISCRIMINATES verdict with BOTH `api_calls_control=0` AND `api_calls_treatment=0`
means no agent ran the A/B — the "result" came from a static harness the model wrote, not from
a real delegate_task pair. `validate_run.py` flags it (П2).

Real case (2026-07-22): Step 3.7 run `20260721T152310Z` self-reported 9 DISCRIMINATES; all 9 had
api_calls=0 → gate exit 1, 16/29. The prose swore it was valid; disk said otherwise. Always run
the gate and read `api_calls_*` per record — never trust the summary line.

## INVALID ≠ null result — what a valid run looks like per tier

Verified 2026-07-22 batch:
- **Strong** (Hy3 SWE 78%, Nemotron ~71%): VALID runs that discriminate on autonomy-dial /
  reuse-ladder / personas / R2-R3 gates (2–3 DISC each, gate exit 0).
- **Genuinely weak** (North Mini Code Agentic ~3, nemotron-nano-9b): cannot produce a valid run —
  fabricates (no results.jsonl, api_calls=0, hardcoded harness), gate rejects (exit 1). This IS
  the design envelope: weak models are executors-under-supervision, not QA orchestrators.
- **Valid NULL result is legitimate data**: Step 3.7 `20260722T091303Z` = 0 DISC, 32/32 gate OK.
  No trap discriminated — honest, not a failure. INVALID means the gate REJECTED fabrication;
  null means the gate PASSED but nothing discriminated. Do not conflate them.

## Pitfall: a read-only tree blocks in-place curator edits

`isolate-skill-tree` makes existing files read-only, so `patch`/overwrite of an existing
SKILL.md or reference fails with `PermissionError` — even for a legitimate curator update.
Writing NEW files still works (the directory itself is not read-only). If you need to edit an
existing skill file, restore the tree first (see pitfall #1 for timing rules). A background
curator pass that only has memory+skill tools (no terminal) cannot lift isolation itself — it
can only add new reference files until a foreground turn restores the tree.
