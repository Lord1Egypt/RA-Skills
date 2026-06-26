#!/usr/bin/env bash
# pdf-toolkit.sh — thin wrapper so the skill can be called as `pdf-toolkit <command> [args]`
# Usage: ./pdf-toolkit.sh <command> [args...]
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec uv run "$SKILL_DIR/src/main.py" "$@"
