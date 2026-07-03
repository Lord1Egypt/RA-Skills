#!/usr/bin/env bash
# Build ACP-to-OpenAI Bridge as a single executable.
#
# Usage:
#   ./build.sh          # build for current platform
#   ./build.sh clean    # remove build artifacts
#
# Output: dist/acp-bridge

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "${1:-}" = "clean" ]; then
    echo "Cleaning build artifacts..."
    rm -rf build/ dist/ __pycache__/ *.egg-info/
    echo "Done."
    exit 0
fi

# Create/activate venv if not already in one
if [ -z "${VIRTUAL_ENV:-}" ]; then
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Ensure dependencies are installed
echo "Installing dependencies..."
pip install -r requirements.txt -q

echo "Building acp-bridge executable..."
pyinstaller acp_bridge.spec --clean --noconfirm

BINARY="dist/acp-bridge"
if [ -f "$BINARY" ]; then
    SIZE=$(du -h "$BINARY" | cut -f1)
    echo ""
    echo "Build successful!"
    echo "  Binary: $BINARY ($SIZE)"
    echo ""
    echo "Usage:"
    echo "  $BINARY --help"
    echo "  $BINARY --port 18788 --cwd /your/project"
else
    echo "Build failed — binary not found at $BINARY"
    exit 1
fi
