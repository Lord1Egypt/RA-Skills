#!/bin/bash
# install.sh — Set up or update the Ollama Task Orchestrator runner
# Run this after cloning or pulling the repo.
#
# Usage:
#   ./install.sh                        # installs to ~/worker/runner/
#   RUNNER_DIR=/custom/path ./install.sh  # installs to a custom path

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER_DIR="${RUNNER_DIR:-$HOME/worker/runner}"

echo "Ollama Task Orchestrator — installer"
echo "Runner target: $RUNNER_DIR"
echo ""

mkdir -p "$RUNNER_DIR"

cp "$SCRIPT_DIR/runner/run_task.sh" "$RUNNER_DIR/run_task.sh"
cp "$SCRIPT_DIR/runner/queue_status.sh" "$RUNNER_DIR/queue_status.sh"
chmod +x "$RUNNER_DIR/run_task.sh" "$RUNNER_DIR/queue_status.sh"

echo "✓ Installed runner scripts to $RUNNER_DIR"
echo ""
echo "Next steps:"
echo "  1. Set DEFAULT_PROJECT and OLLAMA_MODEL in your shell profile (~/.zshrc or ~/.bashrc)"
echo "  2. Test with: $RUNNER_DIR/run_task.sh ping"
echo "  3. Check Ollama: $RUNNER_DIR/queue_status.sh"
echo ""
echo "To update in future: git pull && ./install.sh"
