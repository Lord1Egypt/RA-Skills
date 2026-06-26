#!/usr/bin/env bash
# Sync root skill files → nested .agents/skills/memoclaw/ copies
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NESTED="$REPO_ROOT/.agents/skills/memoclaw"

cp "$REPO_ROOT/SKILL.md" "$NESTED/SKILL.md"
cp "$REPO_ROOT/examples.md" "$NESTED/examples.md"
cp "$REPO_ROOT/api-reference.md" "$NESTED/api-reference.md"

echo "✅ Nested skill files synced from root."
