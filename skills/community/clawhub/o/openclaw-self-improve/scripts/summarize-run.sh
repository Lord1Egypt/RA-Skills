#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  summarize-run.sh --run-dir <path> [--json]

Prints a one-page status overview of a single self-improvement run by
extracting the most informative fields from run-info.md, baseline.md,
proposal.md, validation.md, and outcome.md. The output is the agent's
"at-a-glance" view; users do not have to open six files manually.

Options:
  --run-dir <path>   Path to the run directory (required)
  --json             Emit a JSON object instead of a text overview
  -h, --help         Show this message

Exit codes:
  0  summary printed
  1  bad arguments / run dir missing
  2  required artifacts are missing or unreadable
USAGE
}

RUN_DIR=""
EMIT_JSON="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir) RUN_DIR="${2:-}"; shift 2 ;;
    --json) EMIT_JSON="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$RUN_DIR" ]]; then
  echo "Missing required --run-dir <path>" >&2; usage >&2; exit 1
fi
if [[ ! -d "$RUN_DIR" ]]; then
  echo "Run directory does not exist: $RUN_DIR" >&2; exit 1
fi

INFO="$RUN_DIR/run-info.md"
BASELINE="$RUN_DIR/baseline.md"
PROPOSAL="$RUN_DIR/proposal.md"
VALIDATION="$RUN_DIR/validation.md"
OUTCOME="$RUN_DIR/outcome.md"

for f in "$INFO" "$BASELINE" "$PROPOSAL" "$VALIDATION" "$OUTCOME"; do
  if [[ ! -f "$f" ]]; then
    echo "Required artifact missing: $f" >&2
    exit 2
  fi
done

# Extract field by exact-string prefix match (no regex), so keys containing
# parentheses or other regex metacharacters (e.g. "Timestamp (UTC)") work.
field_from_run_info() {
  local file="$1" key="$2"
  local prefix="- $key: "
  awk -v p="$prefix" '
    index($0, p) == 1 {
      print substr($0, length(p) + 1)
      exit
    }
  ' "$file"
}

first_status_under() {
  local file="$1" heading="$2"
  awk -v h="$heading" '
    $0 == "## " h { in_section=1; next }
    /^## / && in_section { exit }
    in_section && /^[-*] / {
      sub(/^[-*][ \t]+/, "")
      if ($0 != "") { print; exit }
    }
  ' "$file"
}

# Extract the body of a section (skips placeholder italics like _( ... )_).
section_body() {
  local file="$1" heading="$2"
  awk -v h="$heading" '
    $0 == "## " h { in_section=1; next }
    /^## / && in_section { exit }
    in_section { print }
  ' "$file" | sed -E '/^_\(.*\)_$/d' | sed -E '/^[[:space:]]*$/d' | head -n 6
}

# JSON-escape one value (whole-string).
json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().rstrip("\n")), end="")'
}

ts="$(field_from_run_info "$INFO" "Timestamp (UTC)")"
mode="$(field_from_run_info "$INFO" "Mode")"
repo="$(field_from_run_info "$INFO" "Repo")"
objective="$(field_from_run_info "$INFO" "Objective")"
scope="$(field_from_run_info "$INFO" "Scope")"
gate="$(field_from_run_info "$INFO" "Validation Gate")"
git_commit="$(field_from_run_info "$INFO" "Git Commit")"
git_branch="$(field_from_run_info "$INFO" "Git Branch")"

baseline_status="$(first_status_under "$BASELINE" "Status")"
validation_status="$(first_status_under "$VALIDATION" "Status")"
outcome_status="$(first_status_under "$OUTCOME" "Status")"
approval_status="$(first_status_under "$PROPOSAL" "Approval Status")"

selected_hyp="$(section_body "$PROPOSAL" "Selected Hypothesis")"
planned_changes="$(section_body "$PROPOSAL" "Planned Changes")"
files_to_edit="$(section_body "$PROPOSAL" "Files To Edit")"
next_iteration="$(section_body "$OUTCOME" "Next Iteration")"

# Decide an overall verdict from the three status fields.
verdict="incomplete"
if [[ -n "$baseline_status" && -n "$validation_status" && -n "$outcome_status" ]]; then
  if [[ "$outcome_status" == "pass" && "$validation_status" == "pass" ]]; then
    verdict="success"
  elif [[ "$outcome_status" == "fail" || "$validation_status" == "fail" ]]; then
    verdict="regression"
  elif [[ "$outcome_status" == "blocked" || "$validation_status" == "blocked" ]]; then
    verdict="blocked"
  else
    verdict="inconclusive"
  fi
fi

if [[ "$EMIT_JSON" == "true" ]]; then
  python3 - "$RUN_DIR" "$ts" "$mode" "$repo" "$objective" "$scope" "$gate" \
    "$git_commit" "$git_branch" "$baseline_status" "$validation_status" \
    "$outcome_status" "$approval_status" "$selected_hyp" "$planned_changes" \
    "$files_to_edit" "$next_iteration" "$verdict" <<'PY'
import json, sys
keys = ["run_dir","timestamp","mode","repo","objective","scope","validation_gate",
        "git_commit","git_branch","baseline_status","validation_status",
        "outcome_status","approval_status","selected_hypothesis","planned_changes",
        "files_to_edit","next_iteration","verdict"]
vals = sys.argv[1:]
print(json.dumps(dict(zip(keys, vals)), indent=2, ensure_ascii=False))
PY
  exit 0
fi

cat <<EOF
=================================================================
OpenClaw Self-Improve Run Summary
=================================================================
Run Dir:        $RUN_DIR
Timestamp:      $ts
Mode:           $mode
Repo:           $repo
Git:            $git_commit ($git_branch)

Objective:      $objective
Scope:          $scope
Validation:     $gate

Statuses:
  Baseline      : ${baseline_status:--}
  Validation    : ${validation_status:--}
  Outcome       : ${outcome_status:--}
  Approval      : ${approval_status:--}
  Overall       : $verdict

Selected Hypothesis:
$(printf '%s\n' "${selected_hyp:-(none)}" | sed 's/^/  /')

Planned Changes:
$(printf '%s\n' "${planned_changes:-(none)}" | sed 's/^/  /')

Files To Edit:
$(printf '%s\n' "${files_to_edit:-(none)}" | sed 's/^/  /')

Next Iteration:
$(printf '%s\n' "${next_iteration:-(none)}" | sed 's/^/  /')
=================================================================
EOF
