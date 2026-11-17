#!/usr/bin/env bash
set -euo pipefail

SINCE="7 days ago"
UNTIL="now"
AUTHOR=""
FORMAT="text"
REPO="."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since) SINCE="$2"; shift 2 ;;
    --until) UNTIL="$2"; shift 2 ;;
    --author) AUTHOR="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --repo) REPO="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

cd "$REPO"

# Build git log args
GIT_ARGS=(log "--since=${SINCE}" "--until=${UNTIL}" "--format=%h|%an|%ad|%s" "--date=short")
if [[ -n "$AUTHOR" ]]; then
  GIT_ARGS+=("--author=${AUTHOR}")
fi

# Fetch commits
mapfile -t COMMITS < <(git "${GIT_ARGS[@]}" 2>/dev/null || true)

TOTAL=${#COMMITS[@]}

# Count by conventional commit type
declare -A TYPE_COUNT
for line in "${COMMITS[@]}"; do
  msg="${line#*|*|*|}"
  type="other"
  if [[ "$msg" =~ ^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)(\(.+\))?: ]]; then
    type="${BASH_REMATCH[1]}"
  fi
  TYPE_COUNT["$type"]=$(( ${TYPE_COUNT["$type"]:-0} + 1 ))
done

if [[ "$FORMAT" == "json" ]]; then
  echo "{"
  echo "  \"since\": \"$SINCE\","
  echo "  \"until\": \"$UNTIL\","
  echo "  \"totalCommits\": $TOTAL,"
  echo "  \"byType\": {"
  first=true
  for t in "${!TYPE_COUNT[@]}"; do
    $first && first=false || echo ","
    echo -n "    \"$t\": ${TYPE_COUNT[$t]}"
  done
  echo ""
  echo "  },"
  echo "  \"commits\": ["
  for i in "${!COMMITS[@]}"; do
    line="${COMMITS[$i]}"
    IFS='|' read -r hash author date msg <<< "$line"
    type="other"
    if [[ "$msg" =~ ^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)(\(.+\))?: ]]; then
      type="${BASH_REMATCH[1]}"
    fi
    comma=","
    [[ $i -eq $(( ${#COMMITS[@]} - 1 )) ]] && comma=""
    cat <<EOF
    { "hash": "$hash", "author": "$author", "date": "$date", "message": "$msg", "type": "$type" }$comma
EOF
  done
  echo "  ]"
  echo "}"
else
  echo "## Commit Summary: ${SINCE} → ${UNTIL}"
  echo "Total commits: ${TOTAL}"
  echo ""
  echo "### By type"
  for t in "${!TYPE_COUNT[@]}"; do
    echo "- ${t}: ${TYPE_COUNT[$t]}"
  done
  echo ""
  echo "### Recent commits"
  for line in "${COMMITS[@]}"; do
    IFS='|' read -r hash author date msg <<< "$line"
    echo "- ${hash} ${msg}"
  done
fi
