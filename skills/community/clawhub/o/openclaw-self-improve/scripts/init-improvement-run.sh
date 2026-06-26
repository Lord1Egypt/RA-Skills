#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  init-improvement-run.sh --repo <path> [options]

Options:
  --timestamp <YYYYMMDD-HHMMSS>   Fixed run timestamp (default: current UTC)
  --mode <audit-only|proposal-only|approved-implementation>
                                  Default: proposal-only
  --objective <text>              What you want to improve (Unicode-safe)
  --scope <text>                  Target sub-path or area (default: repo root)
  --validation-gate <text>        Exact commands that prove success
  --auto-detect-validation        Infer validation gate from project structure
                                  (ignored if --validation-gate is also set)
  --create-backup                 Create a zip backup before running (non-git)
  --enable-logging                Write detailed run.log inside the run dir
  --dry-run                       Print resolved values without creating files
  --force                         Overwrite an existing run directory safely
  --rollback                      Strict rollback for an existing run
  -h, --help                      Show this message

Creates:
  <repo>/.openclaw-self-improve/<timestamp>/
with files:
  run-info.md baseline.md hypotheses.md proposal.md validation.md outcome.md
USAGE
}

REPO=""
TIMESTAMP="$(date -u +%Y%m%d-%H%M%S)"
MODE="proposal-only"
OBJECTIVE=""
SCOPE=""
VALIDATION_GATE=""
DRY_RUN="false"
FORCE="false"
ROLLBACK="false"
AUTO_DETECT_VALIDATION="false"
CREATE_BACKUP="false"
ENABLE_LOGGING="false"

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

# Unicode-safe: strip only newlines and shell control characters.
# Preserves Hindi, Chinese, Japanese, etc.
sanitize_oneline() {
  local value="$1"
  # remove CR, LF, and backticks (shell command substitution)
  value="${value//$'\r'/}"
  value="${value//$'\n'/ }"
  value="${value//\`/}"
  printf '%s' "$value"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    --timestamp) TIMESTAMP="${2:-}"; shift 2 ;;
    --mode) MODE="${2:-}"; shift 2 ;;
    --objective) OBJECTIVE="${2:-}"; shift 2 ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --validation-gate) VALIDATION_GATE="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift ;;
    --force) FORCE="true"; shift ;;
    --rollback) ROLLBACK="true"; shift ;;
    --auto-detect-validation) AUTO_DETECT_VALIDATION="true"; shift ;;
    --create-backup) CREATE_BACKUP="true"; shift ;;
    --enable-logging) ENABLE_LOGGING="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

REPO="$(trim "$REPO")"
MODE="$(trim "$MODE")"
TIMESTAMP="$(trim "$TIMESTAMP")"
OBJECTIVE="$(sanitize_oneline "$(trim "$OBJECTIVE")")"
SCOPE="$(sanitize_oneline "$(trim "$SCOPE")")"
VALIDATION_GATE="$(sanitize_oneline "$(trim "$VALIDATION_GATE")")"

if [[ -z "$REPO" ]]; then
  echo "Missing required --repo <path>" >&2
  usage >&2
  exit 1
fi

if [[ ! -d "$REPO" ]]; then
  echo "Repo path does not exist: $REPO" >&2
  exit 1
fi

case "$MODE" in
  audit-only|proposal-only|approved-implementation) ;;
  *) echo "Invalid --mode value: $MODE" >&2; exit 1 ;;
esac

# Reject empty/whitespace-only objective. A blank objective produces a run
# whose run-info.md says "TODO: define objective" and silently passes
# validation, which is a footgun. Rollback runs are exempt because they do
# not need an objective.
if [[ "$ROLLBACK" != "true" && -z "$OBJECTIVE" ]]; then
  echo "Missing required --objective <text> (use --rollback if you only want to revert)." >&2
  exit 1
fi

if [[ ! "$TIMESTAMP" =~ ^[0-9]{8}-[0-9]{6}$ ]]; then
  echo "Invalid --timestamp format: $TIMESTAMP (expected YYYYMMDD-HHMMSS)" >&2
  exit 1
fi

REPO_ABS="$(cd "$REPO" && pwd)"
RUN_DIR="$REPO_ABS/.openclaw-self-improve/$TIMESTAMP"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Conflict detection: explicit gate beats auto-detect
if [[ "$AUTO_DETECT_VALIDATION" == "true" && -n "$VALIDATION_GATE" ]]; then
  echo "Notice: --validation-gate is set explicitly; ignoring --auto-detect-validation." >&2
  AUTO_DETECT_VALIDATION="false"
fi

# Git info
GIT_COMMIT="n/a"
GIT_BRANCH="n/a"
IS_GIT_REPO="false"
if git -C "$REPO_ABS" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  IS_GIT_REPO="true"
  GIT_COMMIT="$(git -C "$REPO_ABS" rev-parse --short HEAD 2>/dev/null || echo n/a)"
  GIT_BRANCH="$(git -C "$REPO_ABS" rev-parse --abbrev-ref HEAD 2>/dev/null || echo n/a)"
fi

# Strict rollback path: must point at an existing run directory
if [[ "$ROLLBACK" == "true" ]]; then
  if [[ ! -d "$RUN_DIR" ]]; then
    echo "Refusing rollback: run directory does not exist: $RUN_DIR" >&2
    exit 1
  fi
  echo "Rolling back run: $RUN_DIR"

  # Build target list: explicit --scope wins; otherwise read proposal.md "Files To Edit"
  TARGETS=()
  if [[ -n "$SCOPE" ]]; then
    TARGETS+=("$SCOPE")
  elif [[ -f "$RUN_DIR/proposal.md" ]]; then
    while IFS= read -r line; do
      # accept "- path" or "* path" bullets
      file="${line#- }"
      file="${file#\* }"
      file="$(trim "$file")"
      [[ -n "$file" ]] && TARGETS+=("$file")
    done < <(awk '
      /^## Files To Edit/ { in_section=1; next }
      /^## / && in_section { exit }
      in_section && /^[-*] / { print }
    ' "$RUN_DIR/proposal.md")
  fi

  if [[ ${#TARGETS[@]} -eq 0 ]]; then
    echo "Refusing rollback: no scope provided and proposal.md has no '## Files To Edit' bullets." >&2
    echo "Pass --scope <path> or fill proposal.md before rolling back." >&2
    exit 1
  fi

  echo "Rollback targets:"
  for t in "${TARGETS[@]}"; do echo "  - $t"; done

  if [[ "$IS_GIT_REPO" == "true" ]]; then
    (cd "$REPO_ABS" && git checkout -- "${TARGETS[@]}")
    echo "Git checkout completed for ${#TARGETS[@]} target(s)."
  else
    echo "Repo is not a git repository. Manual rollback required:"
    echo "  unzip $RUN_DIR/backups/*.zip -d $REPO_ABS"
    exit 2
  fi
  exit 0
fi

# Auto-detect validation gate if requested. detect-validation-gate.sh exits
# 3 (no gates found), 1 (error), or 0 (success). All non-success exits are
# treated the same here: VALIDATION_GATE stays empty and the run-info.md
# falls back to the TODO placeholder. Print a notice so the user knows.
if [[ "$AUTO_DETECT_VALIDATION" == "true" && -z "$VALIDATION_GATE" ]]; then
  detector=""
  if [[ -x "$SCRIPT_DIR/detect-validation-gate.sh" ]]; then
    detector="$SCRIPT_DIR/detect-validation-gate.sh"
  elif [[ -f "$SCRIPT_DIR/detect-validation-gate.sh" ]]; then
    detector="bash $SCRIPT_DIR/detect-validation-gate.sh"
  fi
  if [[ -n "$detector" ]]; then
    if detected_gate="$($detector --repo "$REPO_ABS" 2>/dev/null)"; then
      VALIDATION_GATE="$detected_gate"
    else
      echo "Notice: --auto-detect-validation found no validation gate; leaving as TODO." >&2
    fi
  fi
fi

OBJECTIVE_VALUE="${OBJECTIVE:-TODO: define objective}"
SCOPE_VALUE="${SCOPE:-$REPO_ABS}"
VALIDATION_VALUE="${VALIDATION_GATE:-TODO: define validation gate commands}"

if [[ -e "$RUN_DIR" ]]; then
  if [[ "$FORCE" != "true" ]]; then
    echo "Run directory already exists: $RUN_DIR" >&2
    echo "Use a different --timestamp or pass --force." >&2
    exit 1
  fi
  if [[ ! -d "$RUN_DIR" ]]; then
    echo "Existing path is not a directory: $RUN_DIR" >&2
    exit 1
  fi
fi

if [[ "$DRY_RUN" == "true" ]]; then
  cat <<EOF_DRYRUN
Dry run (no files created):
- Timestamp (UTC): $TIMESTAMP
- Mode: $MODE
- Repo: $REPO_ABS
- Is Git Repo: $IS_GIT_REPO
- Objective: $OBJECTIVE_VALUE
- Scope: $SCOPE_VALUE
- Validation Gate: $VALIDATION_VALUE
- Run Dir: $RUN_DIR
- Logging Enabled: $ENABLE_LOGGING
EOF_DRYRUN
  exit 0
fi

mkdir -p "$RUN_DIR"

if [[ "$FORCE" == "true" ]]; then
  rm -f \
    "$RUN_DIR/run-info.md" \
    "$RUN_DIR/baseline.md" \
    "$RUN_DIR/hypotheses.md" \
    "$RUN_DIR/proposal.md" \
    "$RUN_DIR/validation.md" \
    "$RUN_DIR/outcome.md" \
    "$RUN_DIR/run.log" \
    "$RUN_DIR/run-info.json" \
    "$RUN_DIR/summary.json"
fi

LOG_FILE=""
if [[ "$ENABLE_LOGGING" == "true" ]]; then
  LOG_FILE="$RUN_DIR/run.log"
  cat > "$LOG_FILE" <<EOF_LOG
================================================================================
OpenClaw Self-Improve Run Log
Started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
Run Directory: $RUN_DIR
Mode: $MODE
Objective: $OBJECTIVE_VALUE
================================================================================

EOF_LOG
fi

# Use a real default status (inconclusive) so freshly initialized runs pass
# validation. The user can flip to pass/fail/blocked via set-status.sh.
DEFAULT_STATUS="inconclusive"
DEFAULT_APPROVAL="pending"

cat > "$RUN_DIR/run-info.md" <<EOF_INFO
# Run Info

- Timestamp (UTC): $TIMESTAMP
- Mode: $MODE
- Repo: $REPO_ABS
- Objective: $OBJECTIVE_VALUE
- Scope: $SCOPE_VALUE
- Validation Gate: $VALIDATION_VALUE
- Git Commit: $GIT_COMMIT
- Git Branch: $GIT_BRANCH
- Is Git Repository: $IS_GIT_REPO
- Logging Enabled: $ENABLE_LOGGING
EOF_INFO

cat > "$RUN_DIR/baseline.md" <<EOF_BASELINE
# Baseline

## Objective
$OBJECTIVE_VALUE

## Scope
$SCOPE_VALUE

## Repo State
- Commit: $GIT_COMMIT
- Branch: $GIT_BRANCH
- Is Git Repository: $IS_GIT_REPO

## Reproduction
_(Describe steps to reproduce the starting condition)_

## Metrics
_(Record measurable baseline numbers here)_

## Risks
_(List known risks and assumptions)_

## Status
- $DEFAULT_STATUS
EOF_BASELINE

cat > "$RUN_DIR/hypotheses.md" <<'EOF_HYP'
# Hypotheses

## Hypothesis 1
_(State a focused, testable hypothesis)_

## Hypothesis 2
_(Alternative or smaller-scope hypothesis)_

## Hypothesis 3
_(Optional third option)_

## Ranking
_(Rank hypotheses by impact and risk; pick the smallest high-impact change)_
EOF_HYP

cat > "$RUN_DIR/proposal.md" <<EOF_PROP
# Proposal

## Selected Hypothesis
_(Restate the chosen hypothesis)_

## Planned Changes
_(Describe what will change and why)_

## Files To Edit
_(One bullet per file path; rollback uses this list)_

## Validation Gate
$VALIDATION_VALUE

## Rollback Plan
_(Describe how to revert if validation fails)_

## Approval Status
- $DEFAULT_APPROVAL
EOF_PROP

cat > "$RUN_DIR/validation.md" <<EOF_VAL
# Validation

## Commands Run
$VALIDATION_VALUE

## Results
_(Record command output or measured values)_

## Baseline vs New
_(Show concrete before/after comparison)_

## Pass/Fail
_(Clearly state the result)_

## Status
- $DEFAULT_STATUS
EOF_VAL

cat > "$RUN_DIR/outcome.md" <<EOF_OUT
# Outcome

## Summary
_(What changed and why)_

## Evidence
_(Link metrics, logs, or test results that prove the outcome)_

## Residual Risk
_(What might still go wrong)_

## Next Iteration
_(If further improvements are needed, what is the smallest next change?)_

## Status
- $DEFAULT_STATUS
EOF_OUT

# Backup for non-git repos
if [[ "$CREATE_BACKUP" == "true" && "$IS_GIT_REPO" == "false" ]]; then
  if [[ -x "$SCRIPT_DIR/backup-repo.sh" ]]; then
    BACKUP_DIR="$RUN_DIR/backups"
    mkdir -p "$BACKUP_DIR"
    if BACKUP_FILE="$("$SCRIPT_DIR/backup-repo.sh" --repo "$REPO_ABS" --backup-dir "$BACKUP_DIR" 2>&1)"; then
      echo "Backup created: $BACKUP_FILE" >&2
      [[ -n "$LOG_FILE" ]] && echo "Backup created: $BACKUP_FILE" >> "$LOG_FILE"
    else
      echo "Backup failed: $BACKUP_FILE" >&2
      [[ -n "$LOG_FILE" ]] && echo "Backup failed: $BACKUP_FILE" >> "$LOG_FILE"
    fi
  fi
elif [[ "$CREATE_BACKUP" == "true" && "$IS_GIT_REPO" == "true" ]]; then
  echo "Notice: repo is a git repository; --create-backup is unnecessary (use git for rollback)." >&2
fi

if [[ -n "$LOG_FILE" ]]; then
  cat >> "$LOG_FILE" <<EOF_LOG_END

================================================================================
Run Initialization Completed: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
================================================================================
EOF_LOG_END
fi

echo "$RUN_DIR"
