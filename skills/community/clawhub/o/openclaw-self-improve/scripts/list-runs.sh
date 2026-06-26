#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  list-runs.sh --repo <path> [options]

Lists all OpenClaw self-improvement runs under <repo>/.openclaw-self-improve/
in chronological order (newest first). For each run prints the timestamp,
mode, baseline status, validation status, outcome status, and the first
line of the objective.

Options:
  --repo <path>             Repository path to scan (required)
  --filter-mode <mode>      Only list runs with this mode
                            (audit-only|proposal-only|approved-implementation)
  --filter-status <status>  Only list runs whose outcome.md status matches
                            (pass|fail|blocked|inconclusive)
  --limit <N>               Show only the most recent N runs (default: all)
  --json                    Emit a JSON array instead of a text table
  -h, --help                Show this message

Exit codes:
  0  at least one matching run was listed
  1  bad arguments / repo not found
  3  no matching runs found (useful for scripts)
USAGE
}

REPO=""
FILTER_MODE=""
FILTER_STATUS=""
LIMIT=""
EMIT_JSON="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    --filter-mode) FILTER_MODE="${2:-}"; shift 2 ;;
    --filter-status) FILTER_STATUS="${2:-}"; shift 2 ;;
    --limit) LIMIT="${2:-}"; shift 2 ;;
    --json) EMIT_JSON="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$REPO" ]]; then
  echo "Missing required --repo <path>" >&2; usage >&2; exit 1
fi
if [[ ! -d "$REPO" ]]; then
  echo "Repository path does not exist: $REPO" >&2; exit 1
fi

if [[ -n "$LIMIT" && ! "$LIMIT" =~ ^[0-9]+$ ]]; then
  echo "Invalid --limit: must be a non-negative integer" >&2; exit 1
fi

case "${FILTER_MODE:-}" in
  ""|audit-only|proposal-only|approved-implementation) ;;
  *) echo "Invalid --filter-mode: $FILTER_MODE" >&2; exit 1 ;;
esac

case "${FILTER_STATUS:-}" in
  ""|pass|fail|blocked|inconclusive) ;;
  *) echo "Invalid --filter-status: $FILTER_STATUS" >&2; exit 1 ;;
esac

REPO_ABS="$(cd "$REPO" && pwd)"
ROOT="$REPO_ABS/.openclaw-self-improve"

if [[ ! -d "$ROOT" ]]; then
  if [[ "$EMIT_JSON" == "true" ]]; then
    echo "[]"
  else
    echo "No runs found: $ROOT does not exist." >&2
  fi
  exit 3
fi

# Read first non-empty bullet under "## <heading>" in <file>.
first_status_under() {
  local file="$1" heading="$2"
  [[ -f "$file" ]] || { echo ""; return; }
  awk -v h="$heading" '
    $0 == "## " h { in_section=1; next }
    /^## / && in_section { exit }
    in_section && /^[-*] / {
      sub(/^[-*][ \t]+/, "")
      if ($0 != "") { print; exit }
    }
  ' "$file"
}

# Read field "Foo: bar" from a run-info.md file.
field_from_run_info() {
  local file="$1" key="$2"
  [[ -f "$file" ]] || { echo ""; return; }
  awk -v k="$key" '
    $0 ~ "^- " k ":" {
      sub("^- " k ":[ \t]*", "")
      print; exit
    }
  ' "$file"
}

# JSON-escape a single value (basic: quotes, backslashes, control chars).
json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")'
}

shopt -s nullglob
runs=("$ROOT"/*/)
shopt -u nullglob

if [[ ${#runs[@]} -eq 0 ]]; then
  if [[ "$EMIT_JSON" == "true" ]]; then echo "[]"; else echo "No runs found in $ROOT." >&2; fi
  exit 3
fi

# Sort newest-first by directory name (timestamps are sortable).
IFS=$'\n' sorted=($(printf '%s\n' "${runs[@]}" | sort -r))
unset IFS

matched=()
for run in "${sorted[@]}"; do
  run="${run%/}"
  ts="$(basename "$run")"
  info="$run/run-info.md"
  baseline="$run/baseline.md"
  validation="$run/validation.md"
  outcome="$run/outcome.md"
  proposal="$run/proposal.md"

  mode="$(field_from_run_info "$info" "Mode")"
  objective="$(field_from_run_info "$info" "Objective")"

  bs="$(first_status_under "$baseline" "Status")"
  vs="$(first_status_under "$validation" "Status")"
  os="$(first_status_under "$outcome" "Status")"
  approval="$(first_status_under "$proposal" "Approval Status")"

  if [[ -n "$FILTER_MODE" && "$mode" != "$FILTER_MODE" ]]; then continue; fi
  if [[ -n "$FILTER_STATUS" && "$os" != "$FILTER_STATUS" ]]; then continue; fi

  matched+=("$ts|$mode|$bs|$vs|$os|$approval|$objective")
  if [[ -n "$LIMIT" && ${#matched[@]} -ge $LIMIT ]]; then break; fi
done

if [[ ${#matched[@]} -eq 0 ]]; then
  if [[ "$EMIT_JSON" == "true" ]]; then echo "[]"; else echo "No matching runs." >&2; fi
  exit 3
fi

if [[ "$EMIT_JSON" == "true" ]]; then
  printf '['
  first=1
  for row in "${matched[@]}"; do
    IFS='|' read -r ts mode bs vs os approval objective <<<"$row"
    [[ $first -eq 1 ]] && first=0 || printf ','
    printf '\n  {'
    printf '"timestamp":%s,' "$(printf '%s' "$ts" | json_escape)"
    printf '"mode":%s,' "$(printf '%s' "$mode" | json_escape)"
    printf '"baseline_status":%s,' "$(printf '%s' "$bs" | json_escape)"
    printf '"validation_status":%s,' "$(printf '%s' "$vs" | json_escape)"
    printf '"outcome_status":%s,' "$(printf '%s' "$os" | json_escape)"
    printf '"approval_status":%s,' "$(printf '%s' "$approval" | json_escape)"
    printf '"objective":%s' "$(printf '%s' "$objective" | json_escape)"
    printf '}'
  done
  printf '\n]\n'
else
  printf '%-17s  %-22s  %-12s  %-12s  %-12s  %s\n' "TIMESTAMP" "MODE" "BASELINE" "VALIDATION" "OUTCOME" "OBJECTIVE"
  for row in "${matched[@]}"; do
    IFS='|' read -r ts mode bs vs os approval objective <<<"$row"
    obj_short="${objective:0:60}"
    [[ ${#objective} -gt 60 ]] && obj_short="${obj_short}..."
    printf '%-17s  %-22s  %-12s  %-12s  %-12s  %s\n' "$ts" "${mode:--}" "${bs:--}" "${vs:--}" "${os:--}" "$obj_short"
  done
  echo
  echo "Total: ${#matched[@]}"
fi
