#!/usr/bin/env bash
# run_audit.sh — Parse logs/security-audit.log and print a structured report
#
# Usage:
#   ./run_audit.sh [days]
#
# Arguments:
#   days   How many past days to include (default: 7)
#
# Output: Markdown-formatted audit report to stdout

set -euo pipefail

DAYS="${1:-7}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SCRIPT_DIR}/../../.."
LOG_FILE="${WORKSPACE}/logs/security-audit.log"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "## Security Audit Report"
  echo "**No log file found.** No events have been recorded yet."
  exit 0
fi

# Cutoff timestamp
if date -v -"${DAYS}"d +%s &>/dev/null 2>&1; then
  CUTOFF_EPOCH=$(date -v -"${DAYS}"d +%s)
else
  CUTOFF_EPOCH=$(date -d "${DAYS} days ago" +%s)
fi

CRITICAL_LINES=()
WARN_LINES=()
INFO_COUNT=0
TOTAL=0

while IFS= read -r line; do
  [[ -z "$line" ]] && continue

  ts=$(echo "$line"       | grep -o '"ts":"[^"]*"'       | cut -d'"' -f4)
  level=$(echo "$line"    | grep -o '"level":"[^"]*"'    | cut -d'"' -f4)
  category=$(echo "$line" | grep -o '"category":"[^"]*"' | cut -d'"' -f4)
  summary=$(echo "$line"  | grep -o '"summary":"[^"]*"'  | cut -d'"' -f4)
  action=$(echo "$line"   | grep -o '"action":"[^"]*"'   | cut -d'"' -f4)

  if date -j -f "%Y-%m-%dT%H:%M:%S" "${ts%+*}" +%s &>/dev/null 2>&1; then
    entry_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${ts%+*}" +%s 2>/dev/null || echo 0)
  else
    entry_epoch=$(date -d "${ts%+*}" +%s 2>/dev/null || echo 0)
  fi

  [[ "$entry_epoch" -lt "$CUTOFF_EPOCH" ]] && continue

  TOTAL=$((TOTAL + 1))

  case "$level" in
    CRITICAL) CRITICAL_LINES+=("- [$ts] $category: $summary — $action") ;;
    WARN)     WARN_LINES+=("- [$ts] $category: $summary — $action") ;;
    INFO)     INFO_COUNT=$((INFO_COUNT + 1)) ;;
  esac
done < "$LOG_FILE"

WARN_COUNT="${#WARN_LINES[@]}"
CRITICAL_COUNT="${#CRITICAL_LINES[@]}"

TODAY=$(date +"%Y-%m-%d")
if date -v -"${DAYS}"d +%Y-%m-%d &>/dev/null 2>&1; then
  START_DATE=$(date -v -"${DAYS}"d +"%Y-%m-%d")
else
  START_DATE=$(date -d "${DAYS} days ago" +"%Y-%m-%d")
fi

echo "## Security Audit Report"
echo "**Period**: ${START_DATE} → ${TODAY}"
echo "**Total Events**: ${TOTAL} (${INFO_COUNT} INFO, ${WARN_COUNT} WARN, ${CRITICAL_COUNT} CRITICAL)"
echo ""

if [[ "${CRITICAL_COUNT}" -gt 0 ]]; then
  echo "### ⛔ CRITICAL"
  for l in "${CRITICAL_LINES[@]}"; do echo "$l"; done
  echo ""
fi

if [[ "${WARN_COUNT}" -gt 0 ]]; then
  echo "### ⚠️ WARN"
  for l in "${WARN_LINES[@]}"; do echo "$l"; done
  echo ""
fi

if [[ "${CRITICAL_COUNT}" -eq 0 && "${WARN_COUNT}" -eq 0 ]]; then
  echo "### ✅ No threats detected"
  echo "All ${TOTAL} events were routine INFO-level operations."
else
  echo "### Summary"
  [[ "${CRITICAL_COUNT}" -gt 0 ]] && echo "⚠️ **${CRITICAL_COUNT} CRITICAL event(s)** — review immediately."
  [[ "${WARN_COUNT}" -gt 0 ]]     && echo "- ${WARN_COUNT} WARN event(s) flagged — review for unexpected patterns."
fi
