#!/usr/bin/env bash
set -euo pipefail

ID=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --id) ID="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "Usage: $0 --id INC-1234"
  exit 1
fi

OUT="docs/incidents/${ID}/evidence"
mkdir -p "$OUT"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short > "$OUT/git-status.txt" || true
  git log --oneline -n 30 > "$OUT/git-log.txt" || true
  git diff --stat > "$OUT/diff-stat.txt" || true
  git diff --name-only > "$OUT/changed-files.txt" || true
fi

( env | grep -E '^(NODE_ENV|ENV|APP_ENV|CI|GITHUB_)' || true ) > "$OUT/env-safe.txt"

echo "Evidence captured at $OUT"