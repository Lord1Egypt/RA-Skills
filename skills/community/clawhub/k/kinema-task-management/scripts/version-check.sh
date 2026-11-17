#!/bin/bash
# Validate root SKILL.md, Claude/Codex manifests, optional package metadata, and latest git tag.
# Usage: ./scripts/version-check.sh [expected-version] [project-dir]

set -euo pipefail

EXPECTED_VER="${1:-}"
PROJECT_DIR="${2:-.}"
cd "$PROJECT_DIR"

SKILL_VER=$(grep '^version:' SKILL.md | head -1 | sed 's/version: *//' | tr -d '[:space:]')

read_json_version() {
  local path="$1"
  if [ ! -f "$path" ]; then
    return 0
  fi
  if command -v python3 &>/dev/null; then
    python3 -c "import json; print(json.load(open('$path', encoding='utf-8-sig'))['version'])" 2>/dev/null || true
  elif command -v python &>/dev/null; then
    python -c "import json; print(json.load(open('$path', encoding='utf-8-sig'))['version'])" 2>/dev/null || true
  elif command -v node &>/dev/null; then
    node -e "console.log(require('./$path').version)" 2>/dev/null || true
  else
    grep '"version"' "$path" | head -1 | sed 's/.*"version": *"\([^"]*\)".*/\1/'
  fi
}

CLAUDE_PLUGIN_VER=$(read_json_version .claude-plugin/plugin.json)
CODEX_PLUGIN_VER=$(read_json_version .codex-plugin/plugin.json)
TAG_VER=$(git tag -l 'v*' --sort=-version:refname 2>/dev/null | head -1 | sed 's/^v//')
BASE_VER="${EXPECTED_VER:-$SKILL_VER}"
ALL_MATCH=true

check_match() {
  local label="$1"
  local value="$2"
  if [ -z "$value" ]; then
    echo "  ❌ $label: (未找到)"
    ALL_MATCH=false
  elif [ "$value" = "$BASE_VER" ]; then
    echo "  ✅ $label: $value"
  else
    echo "  ❌ $label: $value (期望: $BASE_VER)"
    ALL_MATCH=false
  fi
}

echo "=== Version Check ==="
echo ""
check_match "SKILL.md" "$SKILL_VER"
check_match "Claude plugin.json" "$CLAUDE_PLUGIN_VER"
check_match "Codex plugin.json" "$CODEX_PLUGIN_VER"
check_match "Latest tag" "$TAG_VER"
echo ""

if [ "$ALL_MATCH" = true ]; then
  echo "✅ All versions match: $BASE_VER"
  exit 0
fi

echo "❌ Version mismatch detected"
exit 1
