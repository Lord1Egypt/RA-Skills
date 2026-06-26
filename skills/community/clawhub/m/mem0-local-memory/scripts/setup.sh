#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "=== mem0-local setup ==="

# Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python venv..."
    python3 -m venv "$VENV_DIR"
fi

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" -q

# Create chroma_db dir
mkdir -p "$SCRIPT_DIR/chroma_db"

echo ""
echo "=== Setup complete ==="
echo "To start: $VENV_DIR/bin/python3 $SCRIPT_DIR/mem0_server.py"
echo "Health check: curl http://127.0.0.1:8300/api/health"
