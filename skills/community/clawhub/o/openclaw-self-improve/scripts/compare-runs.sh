#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  compare-runs.sh --run-a <path> --run-b <path> [--json]

Side-by-side comparison of two OpenClaw self-improvement runs. Reads the
key fields from each run's run-info.md, baseline.md, proposal.md,
validation.md, and outcome.md, and prints a row-per-field table that
highlights where the two runs differ. Computes an aggregate verdict
("identical" / "diverged") so CI can branch on it.

Useful for:
  - Did the second iteration actually improve over the first?
  - Did two parallel branches reach the same outcome?
  - Did rerunning the same objective on a newer commit change anything?

Options:
  --run-a <path>   Path to the first run directory (required)
  --run-b <path>   Path to the second run directory (required)
  --json           Emit a JSON object instead of a text table
  -h, --help       Show this message

Exit codes:
  0  the two runs are identical on every compared field
  1  the two runs differ on at least one field
  2  bad arguments / run dir missing / required artifacts missing
USAGE
}

RUN_A=""
RUN_B=""
EMIT_JSON="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-a) RUN_A="${2:-}"; shift 2 ;;
    --run-b) RUN_B="${2:-}"; shift 2 ;;
    --json) EMIT_JSON="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$RUN_A" || -z "$RUN_B" ]]; then
  echo "Missing required --run-a and --run-b" >&2; usage >&2; exit 2
fi
if [[ ! -d "$RUN_A" ]]; then
  echo "Run directory does not exist: $RUN_A" >&2; exit 2
fi
if [[ ! -d "$RUN_B" ]]; then
  echo "Run directory does not exist: $RUN_B" >&2; exit 2
fi

REQUIRED_FILES=(run-info.md baseline.md proposal.md validation.md outcome.md)

for run in "$RUN_A" "$RUN_B"; do
  for f in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$run/$f" ]]; then
      echo "Required artifact missing: $run/$f" >&2
      exit 2
    fi
  done
done

# Extract a "- Key: value" line by exact-string prefix (handles parentheses
# in keys like "Timestamp (UTC)").
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

# First non-placeholder bullet under "## <heading>" in <file>.
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

# Read up to 5 informative lines under a section.
section_body() {
  local file="$1" heading="$2"
  awk -v h="$heading" '
    $0 == "## " h { in_section=1; next }
    /^## / && in_section { exit }
    in_section { print }
  ' "$file" | sed -E '/^_\(.*\)_$/d' | sed -E '/^[[:space:]]*$/d' | head -n 5
}

# Collect every field we want to compare for one run.
declare -A A_FIELDS B_FIELDS

read_run_into() {
  local prefix="$1" run="$2"
  local info="$run/run-info.md"
  local baseline="$run/baseline.md"
  local proposal="$run/proposal.md"
  local validation="$run/validation.md"
  local outcome="$run/outcome.md"

  eval "${prefix}_FIELDS[timestamp]=\"\$(field_from_run_info \"\$info\" \"Timestamp (UTC)\")\""
  eval "${prefix}_FIELDS[mode]=\"\$(field_from_run_info \"\$info\" \"Mode\")\""
  eval "${prefix}_FIELDS[repo]=\"\$(field_from_run_info \"\$info\" \"Repo\")\""
  eval "${prefix}_FIELDS[objective]=\"\$(field_from_run_info \"\$info\" \"Objective\")\""
  eval "${prefix}_FIELDS[scope]=\"\$(field_from_run_info \"\$info\" \"Scope\")\""
  eval "${prefix}_FIELDS[validation_gate]=\"\$(field_from_run_info \"\$info\" \"Validation Gate\")\""
  eval "${prefix}_FIELDS[git_commit]=\"\$(field_from_run_info \"\$info\" \"Git Commit\")\""
  eval "${prefix}_FIELDS[git_branch]=\"\$(field_from_run_info \"\$info\" \"Git Branch\")\""
  eval "${prefix}_FIELDS[baseline_status]=\"\$(first_status_under \"\$baseline\" \"Status\")\""
  eval "${prefix}_FIELDS[validation_status]=\"\$(first_status_under \"\$validation\" \"Status\")\""
  eval "${prefix}_FIELDS[outcome_status]=\"\$(first_status_under \"\$outcome\" \"Status\")\""
  eval "${prefix}_FIELDS[approval_status]=\"\$(first_status_under \"\$proposal\" \"Approval Status\")\""
  eval "${prefix}_FIELDS[selected_hypothesis]=\"\$(section_body \"\$proposal\" \"Selected Hypothesis\")\""
  eval "${prefix}_FIELDS[planned_changes]=\"\$(section_body \"\$proposal\" \"Planned Changes\")\""
}

read_run_into A "$RUN_A"
read_run_into B "$RUN_B"

# Stable field order. selected_hypothesis and planned_changes are last
# because their bodies can be multi-line.
FIELDS=(
  timestamp
  mode
  repo
  git_commit
  git_branch
  objective
  scope
  validation_gate
  approval_status
  baseline_status
  validation_status
  outcome_status
  selected_hypothesis
  planned_changes
)

# Compute aggregate verdict.
diffs=()
for f in "${FIELDS[@]}"; do
  a="${A_FIELDS[$f]:-}"
  b="${B_FIELDS[$f]:-}"
  if [[ "$a" != "$b" ]]; then
    diffs+=("$f")
  fi
done

# Outcome-progression hint: if both runs have outcome_status set and they
# differ, classify the direction.
outcome_progression="n/a"
oa="${A_FIELDS[outcome_status]:-}"
ob="${B_FIELDS[outcome_status]:-}"
if [[ -n "$oa" && -n "$ob" ]]; then
  if [[ "$oa" == "$ob" ]]; then
    outcome_progression="same"
  elif [[ "$oa" == "pass" && "$ob" != "pass" ]]; then
    outcome_progression="regressed"
  elif [[ "$oa" != "pass" && "$ob" == "pass" ]]; then
    outcome_progression="improved"
  else
    outcome_progression="changed"
  fi
fi

verdict="identical"
if [[ ${#diffs[@]} -gt 0 ]]; then
  verdict="diverged"
fi

if [[ "$EMIT_JSON" == "true" ]]; then
  # Build a JSON object via python so we get correct escaping of multi-line
  # bodies and any embedded quotes.
  python3 - "$RUN_A" "$RUN_B" "$verdict" "$outcome_progression" \
    "${A_FIELDS[timestamp]:-}" "${A_FIELDS[mode]:-}" "${A_FIELDS[repo]:-}" \
    "${A_FIELDS[git_commit]:-}" "${A_FIELDS[git_branch]:-}" \
    "${A_FIELDS[objective]:-}" "${A_FIELDS[scope]:-}" "${A_FIELDS[validation_gate]:-}" \
    "${A_FIELDS[approval_status]:-}" "${A_FIELDS[baseline_status]:-}" \
    "${A_FIELDS[validation_status]:-}" "${A_FIELDS[outcome_status]:-}" \
    "${A_FIELDS[selected_hypothesis]:-}" "${A_FIELDS[planned_changes]:-}" \
    "${B_FIELDS[timestamp]:-}" "${B_FIELDS[mode]:-}" "${B_FIELDS[repo]:-}" \
    "${B_FIELDS[git_commit]:-}" "${B_FIELDS[git_branch]:-}" \
    "${B_FIELDS[objective]:-}" "${B_FIELDS[scope]:-}" "${B_FIELDS[validation_gate]:-}" \
    "${B_FIELDS[approval_status]:-}" "${B_FIELDS[baseline_status]:-}" \
    "${B_FIELDS[validation_status]:-}" "${B_FIELDS[outcome_status]:-}" \
    "${B_FIELDS[selected_hypothesis]:-}" "${B_FIELDS[planned_changes]:-}" \
    "${diffs[*]:-}" <<'PY'
import json, sys
keys = ["timestamp","mode","repo","git_commit","git_branch","objective",
        "scope","validation_gate","approval_status","baseline_status",
        "validation_status","outcome_status","selected_hypothesis",
        "planned_changes"]
argv = sys.argv[1:]
run_a, run_b, verdict, outcome_progression = argv[:4]
n = len(keys)
a_vals = argv[4:4+n]
b_vals = argv[4+n:4+2*n]
diffs = argv[4+2*n].split() if (4+2*n) < len(argv) else []
a_obj = dict(zip(keys, a_vals))
b_obj = dict(zip(keys, b_vals))
out = {
    "run_a": {"dir": run_a, **a_obj},
    "run_b": {"dir": run_b, **b_obj},
    "verdict": verdict,
    "outcome_progression": outcome_progression,
    "differing_fields": diffs,
}
print(json.dumps(out, indent=2, ensure_ascii=False))
PY
  if [[ "$verdict" == "identical" ]]; then exit 0; else exit 1; fi
fi

# Human-readable text output
echo "================================================================="
echo "OpenClaw Self-Improve Run Comparison"
echo "================================================================="
echo "Run A:  $RUN_A"
echo "Run B:  $RUN_B"
echo
printf '%-22s  %-32s  %-32s  diff\n' "field" "run A" "run B"
echo "-------------------------------------------------------------------------------------------------"

short() {
  local v="$1"
  # Collapse any internal newlines to spaces, then truncate to 32 chars
  v="${v//$'\n'/ }"
  if (( ${#v} > 32 )); then
    printf '%s...' "${v:0:29}"
  else
    printf '%s' "$v"
  fi
}

for f in "${FIELDS[@]}"; do
  a="${A_FIELDS[$f]:-}"
  b="${B_FIELDS[$f]:-}"
  marker=""
  if [[ "$a" != "$b" ]]; then
    marker="*"
  fi
  printf '%-22s  %-32s  %-32s  %s\n' "$f" "$(short "$a")" "$(short "$b")" "$marker"
done

echo
echo "Differing fields: ${#diffs[@]}"
if [[ ${#diffs[@]} -gt 0 ]]; then
  echo "  ${diffs[*]}"
fi
echo "Outcome progression: $outcome_progression"
echo "Verdict: $verdict"

if [[ "$verdict" == "identical" ]]; then
  exit 0
else
  exit 1
fi
