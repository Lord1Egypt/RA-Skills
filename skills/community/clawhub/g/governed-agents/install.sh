#!/usr/bin/env bash
# DECLARES_WRITES: ~/.openclaw/workspace/.state/governed_agents/
# Governed Agents — Installer for OpenClaw
# Copies the governed_agents package into your OpenClaw workspace.
# No pip required — pure Python stdlib only.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="$WORKSPACE/.state"
TARGET="$STATE_DIR/governed_agents"

validate_workspace_path() {
    local resolved
    resolved="$(python3 -c "from pathlib import Path; print(Path('${STATE_DIR}').resolve())")"
    if [[ "$resolved" != "$HOME"* ]]; then
        echo "ERROR: workspace must resolve under \$HOME. Got: $resolved" >&2
        exit 1
    fi

    local workspace_root
    workspace_root="${STATE_DIR%/.state}"
    if [ -L "$workspace_root" ]; then
        echo "ERROR: workspace root must not be a symlink: $workspace_root" >&2
        exit 1
    fi

    local parent_dir
    parent_dir="$(dirname "$STATE_DIR")"
    if [ ! -d "$parent_dir" ]; then
        echo "ERROR: workspace parent missing: $parent_dir" >&2
        exit 1
    fi

    local owner
    owner="$(python3 -c "import os; print(os.stat('$parent_dir').st_uid)")"
    if [ "$owner" != "$(id -u)" ]; then
        echo "ERROR: workspace parent not owned by current user: $parent_dir" >&2
        exit 1
    fi
}

echo "🛡️  Installing governed-agents..."

validate_workspace_path
mkdir -p "$STATE_DIR"

if [ -d "$TARGET" ]; then
    echo "  Updating existing installation at $TARGET..."
    cp -r "$SCRIPT_DIR/governed_agents/." "$TARGET/"
else
    echo "  Installing to $TARGET..."
    cp -r "$SCRIPT_DIR/governed_agents" "$TARGET"
fi

echo ""
echo "  Running verification suite..."
GOVERNED_DB_PATH="$STATE_DIR/reputation.db" python3 "$TARGET/tests/test_verification.py"
echo ""
echo "✅ governed-agents installed at $TARGET"
echo "   Usage: from governed_agents.orchestrator import GovernedOrchestrator"
