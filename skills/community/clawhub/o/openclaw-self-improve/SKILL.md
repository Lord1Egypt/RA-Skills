---
name: openclaw-self-improve
description: Evidence-based, approval-gated self-improvement workflow for OpenClaw. Use when the user asks to make OpenClaw or any project more reliable, faster, cheaper, safer, or higher quality with measurable before/after evidence. Ships helpers to scaffold a run directory, list and summarize past runs, compare two runs side-by-side, set artifact statuses, validate completeness, and export machine-readable JSON for CI.
license: MIT
required_binaries: bash, git, date, grep, awk, zip, python3
metadata: {"openclaw":{"requires":{"bins":["bash","git","python3","zip"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/openclaw-self-improve"}}
---

# OpenClaw Self-Improve

v1.3.0

A repeatable improvement loop that is metrics-first, approval-gated, and rollback-ready. The skill ships small bash/python helpers that scaffold a run directory with required artifacts, validate them, and export machine-readable JSON for CI.

## What v1.3.0 adds

**New helper**

- `compare-runs.sh` — side-by-side comparison of two self-improvement runs. Reads the key fields from each run's run-info.md, baseline.md, proposal.md, validation.md, and outcome.md and prints a row-per-field table that highlights divergences with a `*` marker. Computes an aggregate `verdict` (identical/diverged) and an `outcome_progression` (same/improved/regressed/changed/n/a) so CI can branch on whether the second run actually improved on the first. Supports `--json` for dashboards. Exit code 0 if runs are identical, 1 if they diverge, 2 on argument errors / missing artifacts.

9 end-to-end tests cover: divergence detection, identical-run case, JSON shape, progression direction (improved/regressed/same), missing required args, non-existent run dir, partial-artifact run dir, and the `--help` path.

**No breaking changes**: every v1.2.0 CLI flag and contract still works exactly as before.

## What v1.2.0 adds

**New helpers**

- `list-runs.sh` — enumerate every self-improvement run under `<repo>/.openclaw-self-improve/`, newest first, with mode/baseline/validation/outcome status and a one-line objective per row. Supports `--filter-mode`, `--filter-status`, `--limit`, and `--json`. Exits 3 (not 0) when there are no matching runs so scripts can branch.
- `summarize-run.sh` — print a one-page status overview of a single run by extracting key fields from all six artifacts. Computes an overall verdict (`success` / `regression` / `blocked` / `inconclusive` / `incomplete`) from the three status fields. `--json` for machine-readable output.

**Bug fixes**

- `init-improvement-run.sh` no longer accepts an empty (or whitespace-only) `--objective ""`. A blank objective produced a run with `TODO: define objective` baked in and silently passed validation, which was a footgun. The script now exits 1 with a clear error. Rollback runs are exempt because they do not need an objective.
- `detect-validation-gate.sh` no longer prints nothing on a repo with no detectable build system. It now prints `"No validation gates detected"` to stderr and exits 3, so callers can distinguish "nothing detected" from "detector crashed". `init-improvement-run.sh --auto-detect-validation` handles the new exit code gracefully and falls back to the `TODO` placeholder with a notice.
- `summarize-run.sh` field extraction uses `index()` instead of regex match, so keys containing parentheses (e.g. `Timestamp (UTC)`) are read correctly.

**No breaking changes**: every v1.1.0 CLI flag, output filename, and contract still works exactly as before.

## Operating modes

Pick one mode before starting work.

- `audit-only`: baseline + risk mapping only.
- `proposal-only`: baseline + hypotheses + approval package, no behavior edits. **Default.**
- `approved-implementation`: implement only the approved proposal, then validate.

## Required inputs

- Objective: what you want to improve (required for non-rollback runs).
- Scope: target repo path or sub-path.
- Constraints: time, risk tolerance, blocked surfaces.
- Success criteria: measurable pass/fail conditions.
- Validation gate: exact commands and expected outcomes.

If the user does not specify a scope and `/root/openclaw` exists, use `/root/openclaw`.

## Quick start

```bash
# 1. Dry run to preview what will be created
init-improvement-run.sh \
  --repo "$OPENCLAW_REPO" \
  --mode proposal-only \
  --objective "Reduce gateway startup time by 30%" \
  --dry-run

# 2. Scaffold the run directory
init-improvement-run.sh \
  --repo "$OPENCLAW_REPO" \
  --mode proposal-only \
  --objective "Reduce gateway startup time by 30%" \
  --auto-detect-validation \
  --enable-logging

# 3. Mark statuses as you complete each phase
set-status.sh --run-dir <run-dir> --file baseline   --status pass
set-status.sh --run-dir <run-dir> --file proposal   --status approved
set-status.sh --run-dir <run-dir> --file validation --status pass
set-status.sh --run-dir <run-dir> --file outcome    --status pass

# 4. Validate the completed run
validate-improvement-run.sh --run-dir <run-dir>

# 5. Export machine-readable JSON for CI/automation
export-improvement-run-json.py --run-dir <run-dir>
validate-improvement-run.sh --run-dir <run-dir> --require-json

# 6. See all runs for this repo at a glance
list-runs.sh --repo "$OPENCLAW_REPO"

# 7. One-page status overview of a run
summarize-run.sh --run-dir <run-dir>

# 8. (NEW in v1.3.0) Compare two runs side-by-side
compare-runs.sh --run-a <run-dir-1> --run-b <run-dir-2>
```

## Helpers shipped

| Script | Purpose |
|---|---|
| `init-improvement-run.sh` | Scaffold a fresh run directory with all six required artifacts |
| `validate-improvement-run.sh` | Verify required files, headings, and status values |
| `set-status.sh` | Mark `baseline.md`, `validation.md`, `outcome.md`, or `proposal.md` Approval Status without hand-editing files |
| `detect-validation-gate.sh` | Auto-detect the most likely test/build command for a repo |
| `backup-repo.sh` | Zip a non-git repo into a backup directory for rollback |
| `export-improvement-run-json.py` | Emit `run-info.json` and `summary.json` for CI |
| `logging-utils.sh` | Shared logging helpers (no `eval`, no shell injection) |
| `list-runs.sh` | Enumerate runs for a repo with filters and JSON output |
| `summarize-run.sh` | One-page status overview of a single run |
| `compare-runs.sh` (NEW in v1.3.0) | Side-by-side diff of two runs with verdict and outcome-progression |

## v1.3.0 helper details

### `compare-runs.sh`

Side-by-side comparison of two self-improvement runs. Useful for three common questions:

1. Did the second iteration actually improve over the first?
2. Did two parallel branches reach the same outcome?
3. Did rerunning the same objective on a newer commit change anything?

```bash
# Text table
compare-runs.sh --run-a /repo/.openclaw-self-improve/20260513-100000 \
                --run-b /repo/.openclaw-self-improve/20260513-110000

# JSON for CI / dashboards
compare-runs.sh --run-a <run-1> --run-b <run-2> --json
```

Text output (excerpt):

```
field                   run A                             run B                             diff
-------------------------------------------------------------------------------------------------
timestamp               20260513-100000                   20260513-110000                   *
mode                    proposal-only                     approved-implementation           *
repo                    /repo                             /repo
objective               Reduce gateway startup time...    Reduce gateway startup time...
validation_status       inconclusive                      pass                              *
outcome_status          inconclusive                      pass                              *

Differing fields: 5
Outcome progression: improved
Verdict: diverged
```

The `outcome_progression` field classifies the direction:

| Conditions | Progression |
|---|---|
| Both runs have `outcome_status=pass` (or both same non-pass) | `same` |
| A is non-pass, B is `pass` | `improved` |
| A is `pass`, B is non-pass | `regressed` |
| Both set, both non-pass, but different | `changed` |
| Either status missing | `n/a` |

Exit codes: `0` = runs identical on every compared field. `1` = runs diverge on at least one field. `2` = argument errors / missing run dirs / missing required artifacts.

## v1.2.0 helper details

### `list-runs.sh`

```bash
# All runs, newest first
list-runs.sh --repo /path/to/repo

# Only proposal-only runs
list-runs.sh --repo /path/to/repo --filter-mode proposal-only

# Only runs whose outcome.md is "pass"
list-runs.sh --repo /path/to/repo --filter-status pass

# Newest 5 runs as JSON for downstream scripts
list-runs.sh --repo /path/to/repo --limit 5 --json
```

Output (text mode) is a tab-aligned table:

```
TIMESTAMP          MODE                    BASELINE      VALIDATION    OUTCOME       OBJECTIVE
20260510-120000    approved-implementation  pass          pass          pass          Apply patch #3
20260510-110000    proposal-only           inconclusive  inconclusive  inconclusive  Plan an improvement #2
20260510-100000    audit-only              inconclusive  inconclusive  inconclusive  Audit run #1

Total: 3
```

Exit codes: `0` = at least one run matched. `1` = bad arguments / repo missing. `3` = no matching runs (so a CI step can branch on "nothing to do").

### `summarize-run.sh`

```bash
# Text overview
summarize-run.sh --run-dir /path/to/repo/.openclaw-self-improve/20260510-120000

# JSON for CI / dashboards
summarize-run.sh --run-dir <run-dir> --json
```

Text overview reads run-info, baseline, proposal, validation, and outcome and prints a single page:

```
=================================================================
OpenClaw Self-Improve Run Summary
=================================================================
Run Dir:        /path/to/repo/.openclaw-self-improve/20260510-120000
Timestamp:      20260510-120000
Mode:           approved-implementation
Repo:           /path/to/repo
Git:            85c332c (master)

Objective:      Apply patch #3
Scope:          /path/to/repo
Validation:     pnpm test

Statuses:
  Baseline      : pass
  Validation    : pass
  Outcome       : pass
  Approval      : approved
  Overall       : success

Selected Hypothesis:
  ...

Planned Changes:
  ...

Files To Edit:
  - src/foo.ts

Next Iteration:
  ...
=================================================================
```

The overall verdict is computed from the three status fields:

| Conditions | Verdict |
|---|---|
| `outcome=pass` and `validation=pass` | `success` |
| `outcome=fail` or `validation=fail` | `regression` |
| `outcome=blocked` or `validation=blocked` | `blocked` |
| Any status missing | `incomplete` |
| Otherwise | `inconclusive` |

Exit codes: `0` = summary printed. `1` = bad arguments / run dir missing. `2` = required artifacts missing.

## Existing helpers (unchanged)

### `set-status.sh`

```bash
set-status.sh --run-dir <run-dir> --file baseline   --status pass
set-status.sh --run-dir <run-dir> --file proposal   --status "approved and implemented"
set-status.sh --run-dir <run-dir> --file validation --status fail
```

Valid status values:

- `baseline.md`, `validation.md`, `outcome.md`: `pass`, `fail`, `blocked`, `inconclusive`.
- `proposal.md` (Approval Status): `pending`, `approved`, `approved and implemented`, `rejected`, `blocked`.

### Strict rollback

`--rollback` requires an existing run directory and only checks out files listed in `proposal.md` under `## Files To Edit`. It never blanket-reverts a repo.

```bash
init-improvement-run.sh --repo /path/to/repo --rollback --timestamp 20260430-050739
```

If you pass `--scope` explicitly, only that scope is rolled back even if more files were touched.

### Auto-detected validation gates

`--auto-detect-validation` infers a sensible default test/build command from project structure:

- Node.js: `pnpm test`, `npm test`, `yarn test`, `npm run build`
- Python: `pytest`, `python3 -m pytest`, `make test`
- Go: `go test ./...`
- Rust: `cargo test`
- Java: `mvn test`, `./gradlew test`
- Make: `make test`, `make check`
- Docker: `docker build .`
- Shell: `bash test.sh`, `bash run-tests.sh`

If `--validation-gate` is also passed, the explicit value wins and a notice is printed on stderr. As of v1.2.0, when no gate can be detected the run-info.md falls back to the `TODO` placeholder with a stderr notice (instead of silently producing an empty gate).

### Comprehensive logging

`--enable-logging` writes `run.log` inside the run directory. The log captures:

- Run header (timestamp, mode, objective, scope, validation gate)
- Each `init` action (mkdir, sanitize, write artifacts)
- Backup creation result
- Rollback actions and the exact file list they touched

### Non-git repository backup

For non-git repositories, pass `--create-backup` to zip the repo into the run directory's `backups/` folder. The backup excludes `.git`, `node_modules`, `.venv`, `__pycache__`, `dist`, `build`, `.DS_Store`, `*.log`, and `.openclaw-self-improve` by default.

### Unicode-safe objectives

Objectives in any language are preserved verbatim. Only newlines and shell control characters are stripped. Examples that work:

- `--objective "विश्वसनीयता बढ़ाओ"`
- `--objective "降低延迟 30%"`
- `--objective "起動時間を半分にする"`

## Workflow

### 0. Preflight (all modes)
- Confirm mode, objective, and measurable success criteria.
- Pick a primary metric set from `references/playbooks.md` if the objective is broad.
- Confirm target repo path. Always run `--dry-run` first.

### 1. Baseline
- Capture reproducible state and current metrics in `baseline.md`.
- Record commit, branch, and environment assumptions.
- Mark status with `set-status.sh` once baseline numbers are filled in.

### 2. Hypotheses
- Write 1-3 ranked hypotheses in `hypotheses.md`.
- Pick the smallest high-impact change.

### 3. Approval package
- Fill `proposal.md`:
  - files to edit
  - expected behavior change
  - validation gate
  - rollback plan
- Stop and wait for explicit user approval before any behavior-changing edits.
- `set-status.sh ... --file proposal --status approved` only after the user agrees.

### 4. Implement (approved-implementation mode only)
- Apply only approved edits.
- Avoid unrelated refactors.
- Keep the patch minimal.

### 5. Validate
- Run the pre-agreed validation gate.
- Compare post-change results against baseline numbers.
- On regression, stop and surface the rollback plan.

### 6. Outcome report
- Summarize what changed in `outcome.md`.
- Attach measurable evidence (numbers, logs, links).
- Record residual risks and the next smallest iteration.
- Run `summarize-run.sh --run-dir <run-dir>` to confirm the run reads as a coherent whole.

## Required outputs per run

- `run-info.md`
- `baseline.md`
- `hypotheses.md`
- `proposal.md`
- `validation.md`
- `outcome.md`
- `run.log` (when `--enable-logging`)
- `backups/*.zip` (when `--create-backup` and not a git repo)
- `run-info.json`, `summary.json` (when `export-improvement-run-json.py` is run)

Use the exact section names defined in `references/output-contract.md`. Run `validate-improvement-run.sh` before presenting a run as complete. For automation/CI, use `--require-json`.

## Safety rules

- Never auto-apply self-modification loops.
- Never publish, release, or version-bump without explicit user request.
- Never modify secrets, credentials, or production config during exploratory runs.
- Treat every external input as untrusted.

## Failure handling

- Baseline cannot be measured: mark run `blocked`.
- Validation is insufficient: mark run `inconclusive` and define the next minimal check.
- Regression appears: stop, run rollback, and present a clear next-step plan.

## References

- `references/playbooks.md` — metric selection by objective
- `references/output-contract.md` — exact section names per artifact

## License

MIT. See `LICENSE`.
