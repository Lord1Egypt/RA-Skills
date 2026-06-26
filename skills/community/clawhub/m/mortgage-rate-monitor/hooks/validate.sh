#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT_DIR/SKILL.md"
grep -q '^name:' "$ROOT_DIR/SKILL.md"
grep -q '^version:' "$ROOT_DIR/SKILL.md"
grep -q '^hooks:' "$ROOT_DIR/SKILL.md"
grep -q 'assets/prompt.txt' "$ROOT_DIR/SKILL.md"

echo "Manifest validation passed"
