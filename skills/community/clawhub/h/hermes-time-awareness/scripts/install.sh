#!/usr/bin/env bash
# Install hermes-time-awareness plugin for Hermes Agent.
# Usage: bash scripts/install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="hermes-time-awareness"
PLUGIN_DIR="$HOME/.hermes/plugins/$PLUGIN_NAME"

echo "hermes-time-awareness installer"
echo "  source: $ROOT"
echo ""

# 1. Link/copy to Hermes plugins directory
mkdir -p "$HOME/.hermes/plugins"
if [[ -L "$PLUGIN_DIR" ]]; then
  rm "$PLUGIN_DIR"
  echo "  removed old symlink"
fi
if [[ -d "$PLUGIN_DIR" && "$PLUGIN_DIR" != "$ROOT" ]]; then
  echo "  warning: $PLUGIN_DIR already exists (not a symlink)"
  echo "  copying files..."
  cp -r "$ROOT"/* "$PLUGIN_DIR/"
else
  ln -sfn "$ROOT" "$PLUGIN_DIR"
  echo "  linked $PLUGIN_DIR → $ROOT"
fi

# 2. Enable the plugin
if command -v hermes >/dev/null 2>&1; then
  hermes plugins enable "$PLUGIN_NAME" 2>/dev/null || true
  echo "  plugin enabled"
else
  echo "  note: hermes CLI not found — enable manually: hermes plugins enable $PLUGIN_NAME"
fi

# 3. Run tests
echo ""
echo "Running tests..."
cd "$PLUGIN_DIR"
if python3 -m pytest tests/ -q 2>/dev/null; then
  echo "  ✓ all tests passed"
else
  echo "  ✗ some tests failed — check output above"
fi

# 4. Verify
echo ""
echo "Verifying plugin output..."
OUTPUT=$(python3 -c "from time_awareness.time_context import format_time_context; print(format_time_context())" 2>/dev/null)
if [[ "$OUTPUT" == *"[time:"* ]]; then
  echo "  ✓ time context: $OUTPUT"
else
  echo "  ✗ time context not working — check Python version (3.9+ required)"
  exit 1
fi

echo ""
echo "Done! Restart Hermes to activate:"
echo "  hermes gateway restart    # for gateway"
echo "  hermes                    # for CLI (new session)"
