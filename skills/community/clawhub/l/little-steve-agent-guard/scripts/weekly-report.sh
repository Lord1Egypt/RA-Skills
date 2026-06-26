#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AUDIT_LOG="$BASE_DIR/reports/audit-events.jsonl"
FAILURE_LOG="$BASE_DIR/reports/failure-dataset.json"
REPORTS_DIR="$BASE_DIR/reports"

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

cmd_generate(){
  require_jq
  local period="${1:-7}"  # days to look back, default 7

  if [[ ! -f "$AUDIT_LOG" ]]; then
    echo "NO_DATA: No audit events found"
    return
  fi

  local cutoff
  cutoff=$(date -u -v-"${period}d" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
           date -u -d "$period days ago" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
           echo "2000-01-01T00:00:00Z")

  local report
  report=$(jq -s --arg cutoff "$cutoff" '
    map(select(.timestamp >= $cutoff)) |
    {
      period_start: $cutoff,
      period_end: (now | strftime("%Y-%m-%dT%H:%M:%SZ")),
      total_events: length,
      by_risk: (group_by(.risk) | map({key: .[0].risk, value: length}) | from_entries),
      by_decision: (group_by(.decision) | map({key: .[0].decision, value: length}) | from_entries),
      by_outcome: (group_by(.outcome) | map({key: .[0].outcome, value: length}) | from_entries),
      by_skill: (group_by(.skill) | map({key: (.[0].skill // "unknown"), value: length}) | from_entries),
      blocked_actions: [.[] | select(.decision == "block") | {command, risk, reason, timestamp}],
      prompted_actions: [.[] | select(.decision == "prompt") | {command, risk, reason, timestamp}],
      failures: [.[] | select(.outcome == "failure") | {command, risk, reason, timestamp}],
      metrics: {
        block_rate: ((([.[] | select(.decision == "block")] | length) * 100.0 / (length + 0.001)) | round / 100),
        high_risk_rate: ((([.[] | select(.risk == "high" or .risk == "critical")] | length) * 100.0 / (length + 0.001)) | round / 100),
        failure_rate: ((([.[] | select(.outcome == "failure")] | length) * 100.0 / (length + 0.001)) | round / 100),
        secret_exposure_count: ([.[] | select(.reason != null) | select(.reason | test("secret|credential|token"; "i"))] | length)
      }
    }
  ' "$AUDIT_LOG")

  # Save report
  local ts
  ts=$(date -u +%Y%m%d-%H%M%S)
  local report_file="$REPORTS_DIR/weekly-report-$ts.json"
  echo "$report" > "$report_file"

  # Human-readable summary
  echo "═══════════════════════════════════════════"
  echo " Security Weekly Report"
  echo " Period: $(echo "$report" | jq -r '.period_start') → $(echo "$report" | jq -r '.period_end')"
  echo "═══════════════════════════════════════════"
  echo ""
  echo "Total events: $(echo "$report" | jq '.total_events')"
  echo ""
  echo "By Risk Level:"
  echo "$report" | jq -r '.by_risk | to_entries[] | "  \(.key): \(.value)"'
  echo ""
  echo "By Decision:"
  echo "$report" | jq -r '.by_decision | to_entries[] | "  \(.key): \(.value)"'
  echo ""
  echo "By Outcome:"
  echo "$report" | jq -r '.by_outcome | to_entries[] | "  \(.key): \(.value)"'
  echo ""
  echo "Metrics:"
  echo "  Block rate: $(echo "$report" | jq '.metrics.block_rate')%"
  echo "  High-risk rate: $(echo "$report" | jq '.metrics.high_risk_rate')%"
  echo "  Failure rate: $(echo "$report" | jq '.metrics.failure_rate')%"
  echo "  Secret exposure: $(echo "$report" | jq '.metrics.secret_exposure_count')"
  echo ""

  local blocked_count
  blocked_count=$(echo "$report" | jq '.blocked_actions | length')
  if [[ "$blocked_count" -gt 0 ]]; then
    echo "Blocked Actions ($blocked_count):"
    echo "$report" | jq -r '.blocked_actions[] | "  [\(.timestamp)] \(.command) — \(.reason)"'
    echo ""
  fi

  echo "Full report: $report_file"
}

main(){
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    generate) cmd_generate "$@" ;;
    *) echo "usage: weekly-report.sh generate [days]" >&2; exit 1 ;;
  esac
}

main "$@"
