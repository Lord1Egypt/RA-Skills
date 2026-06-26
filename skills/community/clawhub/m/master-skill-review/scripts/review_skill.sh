#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: review_skill.sh <skill-dir-or-skill-md>"
  exit 1
fi

if [[ -d "$TARGET" ]]; then
  SKILL_MD="$TARGET/SKILL.md"
  ROOT="$TARGET"
elif [[ -f "$TARGET" ]]; then
  SKILL_MD="$TARGET"
  ROOT="$(dirname "$TARGET")"
else
  echo "Target not found: $TARGET"
  exit 2
fi

if [[ ! -f "$SKILL_MD" ]]; then
  echo "SKILL.md not found: $SKILL_MD"
  exit 3
fi

echo "== Target =="
echo "$ROOT"

echo
echo "== File sizes =="
wc -l "$SKILL_MD" || true
find "$ROOT" -maxdepth 2 -type f | sort | xargs -r wc -l || true

echo
echo "== Scripts =="
find "$ROOT/scripts" -maxdepth 2 -type f 2>/dev/null | sort || echo "No scripts"

echo
echo "== References =="
find "$ROOT/references" -maxdepth 2 -type f 2>/dev/null | sort || echo "No references"

echo
echo "== Heuristic warnings =="
LINES=$(wc -l < "$SKILL_MD")
if [[ "$LINES" -gt 80 ]]; then
  echo "WARN: SKILL.md is long ($LINES lines); consider compressing."
fi
if ! find "$ROOT/scripts" -maxdepth 1 -type f 2>/dev/null | grep -q .; then
  echo "WARN: No scripts found; check if mechanical steps can be scripted."
fi
if grep -qi 'checklist\|流程\|步骤' "$SKILL_MD"; then
  echo "INFO: Review whether listed steps should move to scripts/references."
fi

echo
echo "Review scaffold complete."
