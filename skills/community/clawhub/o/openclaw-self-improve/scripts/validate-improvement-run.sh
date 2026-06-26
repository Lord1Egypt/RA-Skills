#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  validate-improvement-run.sh --run-dir <path> [--require-json] [--quiet]

Checks:
  - Required artifact files exist
  - Required headings exist in each artifact
  - run-info fields are present and non-empty
  - Status values are valid (pass/fail/blocked/inconclusive)
  - proposal Approval Status is one of the allowed values
  - When --require-json is set, JSON artifacts exist and are coherent

Options:
  --run-dir <path>   Run directory to validate
  --require-json     Also validate run-info.json and summary.json
  --quiet            Suppress success message
  -h, --help         Show this message
USAGE
}

fail() {
  echo "$1" >&2
  exit 1
}

require_line() {
  local file="$1"
  local line="$2"
  grep -Fqx -- "$line" "$file" || fail "Missing required line '$line' in $(basename "$file")"
}

require_prefix() {
  local file="$1"
  local prefix="$2"
  grep -Fq -- "$prefix" "$file" || fail "Missing required field prefix '$prefix' in $(basename "$file")"
}

# Extract the first bullet under a "## ..." heading. Bullet may start with
# "- " or "* ". Returns empty string if no bullet found.
extract_section_bullet() {
  local file="$1"
  local heading="$2"
  awk -v heading="$heading" '
    $0 == heading { in_section=1; next }
    /^## / && in_section { exit }
    in_section && /^[-*] / {
      sub(/^[-*] /, "", $0)
      gsub(/^[ \t]+|[ \t]+$/, "", $0)
      print $0
      exit
    }
  ' "$file"
}

require_value_in_set() {
  local label="$1"
  local value="$2"
  shift 2
  local allowed
  for allowed in "$@"; do
    if [[ "$value" == "$allowed" ]]; then
      return 0
    fi
  done
  fail "Invalid $label value: '$value'"
}

RUN_DIR=""
REQUIRE_JSON="false"
QUIET="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir) RUN_DIR="${2:-}"; shift 2 ;;
    --require-json) REQUIRE_JSON="true"; shift ;;
    --quiet) QUIET="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown argument: $1" ;;
  esac
done

if [[ -z "$RUN_DIR" ]]; then
  usage >&2
  fail "Missing required --run-dir <path>"
fi

if [[ ! -d "$RUN_DIR" ]]; then
  fail "Run directory does not exist: $RUN_DIR"
fi

REQUIRED_FILES=(
  run-info.md
  baseline.md
  hypotheses.md
  proposal.md
  validation.md
  outcome.md
)

for file in "${REQUIRED_FILES[@]}"; do
  [[ -f "$RUN_DIR/$file" ]] || fail "Missing required file: $RUN_DIR/$file"
done

RUN_INFO="$RUN_DIR/run-info.md"
BASELINE="$RUN_DIR/baseline.md"
HYPOTHESES="$RUN_DIR/hypotheses.md"
PROPOSAL="$RUN_DIR/proposal.md"
VALIDATION="$RUN_DIR/validation.md"
OUTCOME="$RUN_DIR/outcome.md"

require_line "$RUN_INFO" "# Run Info"
require_prefix "$RUN_INFO" "- Timestamp (UTC):"
require_prefix "$RUN_INFO" "- Mode:"
require_prefix "$RUN_INFO" "- Repo:"
require_prefix "$RUN_INFO" "- Objective:"
require_prefix "$RUN_INFO" "- Scope:"
require_prefix "$RUN_INFO" "- Validation Gate:"

require_line "$BASELINE" "# Baseline"
require_line "$BASELINE" "## Objective"
require_line "$BASELINE" "## Scope"
require_line "$BASELINE" "## Repo State"
require_line "$BASELINE" "## Reproduction"
require_line "$BASELINE" "## Metrics"
require_line "$BASELINE" "## Risks"
require_line "$BASELINE" "## Status"

require_line "$HYPOTHESES" "# Hypotheses"
require_line "$HYPOTHESES" "## Hypothesis 1"
require_line "$HYPOTHESES" "## Ranking"

require_line "$PROPOSAL" "# Proposal"
require_line "$PROPOSAL" "## Selected Hypothesis"
require_line "$PROPOSAL" "## Planned Changes"
require_line "$PROPOSAL" "## Files To Edit"
require_line "$PROPOSAL" "## Validation Gate"
require_line "$PROPOSAL" "## Rollback Plan"
require_line "$PROPOSAL" "## Approval Status"

require_line "$VALIDATION" "# Validation"
require_line "$VALIDATION" "## Commands Run"
require_line "$VALIDATION" "## Results"
require_line "$VALIDATION" "## Baseline vs New"
require_line "$VALIDATION" "## Pass/Fail"
require_line "$VALIDATION" "## Status"

require_line "$OUTCOME" "# Outcome"
require_line "$OUTCOME" "## Summary"
require_line "$OUTCOME" "## Evidence"
require_line "$OUTCOME" "## Residual Risk"
require_line "$OUTCOME" "## Next Iteration"
require_line "$OUTCOME" "## Status"

BASELINE_STATUS="$(extract_section_bullet "$BASELINE" "## Status")"
VALIDATION_STATUS="$(extract_section_bullet "$VALIDATION" "## Status")"
OUTCOME_STATUS="$(extract_section_bullet "$OUTCOME" "## Status")"
APPROVAL_STATUS="$(extract_section_bullet "$PROPOSAL" "## Approval Status")"

[[ -n "$BASELINE_STATUS" ]] || fail "Missing baseline status bullet in baseline.md"
[[ -n "$VALIDATION_STATUS" ]] || fail "Missing validation status bullet in validation.md"
[[ -n "$OUTCOME_STATUS" ]] || fail "Missing outcome status bullet in outcome.md"
[[ -n "$APPROVAL_STATUS" ]] || fail "Missing approval status bullet in proposal.md"

require_value_in_set "baseline status"   "$BASELINE_STATUS"   pass fail blocked inconclusive
require_value_in_set "validation status" "$VALIDATION_STATUS" pass fail blocked inconclusive
require_value_in_set "outcome status"    "$OUTCOME_STATUS"    pass fail blocked inconclusive
require_value_in_set "approval status"   "$APPROVAL_STATUS" \
  pending approved "approved and implemented" rejected blocked

if [[ "$REQUIRE_JSON" == "true" ]]; then
  [[ -f "$RUN_DIR/run-info.json" ]] || fail "Missing required JSON file: $RUN_DIR/run-info.json"
  [[ -f "$RUN_DIR/summary.json" ]]  || fail "Missing required JSON file: $RUN_DIR/summary.json"

  python3 - "$RUN_DIR" <<'PY' || fail "JSON validation failed"
import json
import sys
from pathlib import Path

run_dir = Path(sys.argv[1])

try:
    run_info = json.loads((run_dir / "run-info.json").read_text(encoding="utf-8"))
    summary  = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    raise SystemExit(f"Invalid JSON: {exc}")

required_run_info_keys = {
    "artifacts", "generated_at_utc", "git_branch", "git_commit",
    "mode", "objective", "repo", "scope", "timestamp_utc", "validation_gate",
}
required_summary_keys = {
    "approval_status", "baseline_status", "generated_at_utc", "mode",
    "next_iteration", "objective", "outcome_status", "run_dir", "scope",
    "selected_hypothesis", "timestamp_utc", "validation_status",
}

missing_run_info = sorted(required_run_info_keys - run_info.keys())
missing_summary  = sorted(required_summary_keys  - summary.keys())
if missing_run_info:
    raise SystemExit(f"run-info.json missing keys: {', '.join(missing_run_info)}")
if missing_summary:
    raise SystemExit(f"summary.json missing keys: {', '.join(missing_summary)}")

if summary["run_dir"] != str(run_dir):
    raise SystemExit("summary.json run_dir does not match requested run directory")
if run_info["timestamp_utc"] != summary["timestamp_utc"]:
    raise SystemExit("Timestamp mismatch between run-info.json and summary.json")
if run_info["mode"] != summary["mode"]:
    raise SystemExit("Mode mismatch between run-info.json and summary.json")
PY
fi

if [[ "$QUIET" != "true" ]]; then
  echo "Validation successful for $RUN_DIR"
fi
