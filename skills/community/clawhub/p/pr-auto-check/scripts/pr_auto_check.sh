#!/usr/bin/env bash
# pr_auto_check.sh — Automated PR review + health check pipeline
# Usage: bash pr_auto_check.sh [--pr <number>] [--repo <owner/repo>] [--json]
set -euo pipefail

PR_NUMBER=""
REPO=""
JSON_OUTPUT=false
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pr)    PR_NUMBER="$2"; shift 2 ;;
    --repo)  REPO="$2"; shift 2 ;;
    --json)  JSON_OUTPUT=true; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# --- Resolve PR number ---
if [[ -z "$PR_NUMBER" ]]; then
  PR_NUMBER=$(gh pr status --json number --jq '.currentBranch.number' 2>/dev/null || true)
  if [[ -z "$PR_NUMBER" ]]; then
    echo "ERROR: Cannot determine PR number. Use --pr <number>" >&2; exit 1
  fi
fi

REPO_FLAG=""
[[ -n "$REPO" ]] && REPO_FLAG="--repo $REPO"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RESULT_FILE=$(mktemp /tmp/pr-auto-check.XXXXXX.json)

# --- Step 1: CI/CD Status ---
echo "==> Checking CI/CD status for PR #$PR_NUMBER ..."
CI_JSON=$(gh pr view "$PR_NUMBER" $REPO_FLAG --json statusCheckRollup --jq '.statusCheckRollup')
CI_PASS=true
CI_SUMMARY=""
if echo "$CI_JSON" | jq -e '.[] | select(.status=="completed" and .conclusion!="success")' >/dev/null 2>&1; then
  CI_PASS=false
  CI_SUMMARY=$(echo "$CI_JSON" | jq -r '[.[] | select(.status=="completed" and .conclusion!="success") | "\(.name): \(.conclusion)"] | join(", ")')
else
  CI_SUMMARY="All checks passed"
fi

# --- Step 2: Diff summary ---
echo "==> Gathering PR diff ..."
DIFF_STATS=$(gh pr diff "$PR_NUMBER" $REPO_FLAG --stat 2>/dev/null | tail -1 || echo "N/A")
CHANGED_FILES=$(gh pr diff "$PR_NUMBER" $REPO_FLAG --name-only 2>/dev/null | head -50 || echo "N/A")

# --- Step 3: Health check ---
echo "==> Running health check ..."
HEALTH_SCRIPT="$SKILL_DIR/../healthcheck/healthcheck.sh"
HEALTH_JSON="{}"
if [[ -x "$HEALTH_SCRIPT" ]]; then
  HEALTH_JSON=$("$HEALTH_SCRIPT" --json 2>/dev/null || echo '{"max_severity":2,"checks":{}}')
else
  # Fallback: try installed healthcheck skill
  HC=$(find ~/.openclaw/skills/healthcheck -name healthcheck.sh -type f 2>/dev/null | head -1)
  if [[ -n "$HC" ]]; then
    HEALTH_JSON=$(bash "$HC" --json 2>/dev/null || echo '{"max_severity":2,"checks":{}}')
  else
    HEALTH_JSON='{"max_severity":-1,"checks":{},"note":"healthcheck script not found"}'
  fi
fi
HEALTH_MAX=$(echo "$HEALTH_JSON" | jq '.max_severity // -1')
HEALTH_SUMMARY=$(echo "$HEALTH_JSON" | jq -r '.checks | to_entries | map("\(.key): \(.value.status)") | join(", ")' 2>/dev/null || echo "N/A")

# --- Step 4: Build result ---
cat > "$RESULT_FILE" <<ENDJSON
{
  "timestamp": "$TIMESTAMP",
  "pr": $PR_NUMBER,
  "ci": {
    "pass": $CI_PASS,
    "summary": "$CI_SUMMARY"
  },
  "diff_stats": $(echo "$DIFF_STATS" | jq -R .),
  "changed_files": $(echo "$CHANGED_FILES" | jq -Rs 'split("\n") | map(select(length>0))'),
  "health": {
    "max_severity": $HEALTH_MAX,
    "summary": "$HEALTH_SUMMARY",
    "raw": $HEALTH_JSON
  }
}
ENDJSON

if $JSON_OUTPUT; then
  cat "$RESULT_FILE"
else
  echo ""
  echo "=== PR Auto-Check Report — $TIMESTAMP ==="
  echo "  PR:        #$PR_NUMBER"
  echo "  CI/CD:     $( $CI_PASS && echo '✅ PASS' || echo '❌ FAIL' ) — $CI_SUMMARY"
  echo "  Diff:      $DIFF_STATS"
  echo "  Health:    $( [[ $HEALTH_MAX -eq 0 ]] && echo '✅ OK' || ([[ $HEALTH_MAX -eq 1 ]] && echo '⚠️ WARN' || echo '❌ CRITICAL')) — $HEALTH_SUMMARY"
  echo ""
fi

echo "$RESULT_FILE"
