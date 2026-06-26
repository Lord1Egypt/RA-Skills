#!/usr/bin/env bash
set -euo pipefail

# Replay Verifier: test candidate rules against historical audit events
# Compares block/allow decisions with and without the candidate rule.

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AUDIT_LOG="$BASE_DIR/reports/audit-events.jsonl"
CANDIDATES_DIR="$BASE_DIR/rules/candidates"

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

cmd_test(){
  require_jq
  local rule_name=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --rule) [[ $# -ge 2 ]] || { echo "error: missing --rule" >&2; exit 1; }; rule_name="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$rule_name" ]] || { echo "error: --rule required" >&2; exit 1; }

  local rule_file="$CANDIDATES_DIR/${rule_name}.rule"
  [[ -f "$rule_file" ]] || { echo "error: candidate rule not found: $rule_name" >&2; exit 1; }

  if [[ ! -f "$AUDIT_LOG" ]]; then
    echo "NO_DATA: No audit events to replay"
    return
  fi

  local pattern level
  pattern=$(head -1 "$rule_file")
  level=$(sed -n '2p' "$rule_file")

  local total matches would_change
  total=$(wc -l < "$AUDIT_LOG" | tr -d ' ')

  # Find events where the rule pattern matches the command/input
  matches=$(jq -s --arg pat "$pattern" '[.[] | select(
    (.command // "" | test($pat; "i")) or
    (.input // "" | test($pat; "i"))
  )] | length' "$AUDIT_LOG")

  # Of those matches, how many were previously allowed but would now be blocked/prompted?
  would_change=$(jq -s --arg pat "$pattern" --arg lvl "$level" '[.[] | select(
    ((.command // "" | test($pat; "i")) or (.input // "" | test($pat; "i"))) and
    (.decision == "allow") and
    (
      ($lvl == "critical") or
      ($lvl == "high" and (.risk == "low" or .risk == "medium"))
    )
  )] | length' "$AUDIT_LOG")

  # Events that were blocked but rule would not have blocked (false positive check)
  local false_positives
  false_positives=$(jq -s --arg pat "$pattern" '[.[] | select(
    (.decision == "block") and
    ((.command // "" | test($pat; "i")) or (.input // "" | test($pat; "i"))) and
    (.outcome == "success" or .outcome == "approved")
  )] | length' "$AUDIT_LOG")

  echo "═══════════════════════════════════════════"
  echo " Replay Verification: $rule_name"
  echo "═══════════════════════════════════════════"
  echo ""
  echo "Rule: pattern=$pattern  level=$level"
  echo ""
  echo "Results against $total historical events:"
  echo "  Matched events: $matches"
  echo "  Would change decision: $would_change"
  echo "  Potential false positives: $false_positives"
  echo ""

  if [[ "$would_change" -gt 0 && "$false_positives" -eq 0 ]]; then
    echo "Recommendation: PROMOTE (benefit with no false positives)"
  elif [[ "$would_change" -gt 0 && "$false_positives" -gt 0 ]]; then
    echo "Recommendation: REVIEW (benefit exists but has false positives)"
  elif [[ "$matches" -eq 0 ]]; then
    echo "Recommendation: INSUFFICIENT DATA (no matching events)"
  else
    echo "Recommendation: SKIP (no benefit over current rules)"
  fi
}

# Test all candidate rules
cmd_test_all(){
  require_jq
  if [[ -z "$(ls -A "$CANDIDATES_DIR" 2>/dev/null)" ]]; then
    echo "No candidate rules to test"
    return
  fi

  for f in "$CANDIDATES_DIR"/*.rule; do
    [[ -f "$f" ]] || continue
    local name
    name=$(basename "$f" .rule)
    cmd_test --rule "$name"
    echo ""
  done
}

main(){
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    test)     cmd_test "$@" ;;
    test-all) cmd_test_all ;;
    *) echo "usage: replay-verify.sh {test|test-all} [--rule <name>]" >&2; exit 1 ;;
  esac
}

main "$@"
