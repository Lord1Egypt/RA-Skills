#!/usr/bin/env bash
# Nex PriceWatch - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-pricewatch"
BIN_DIR="$HOME/.local/bin"
SKILL_NAME="nex-pricewatch"

echo "============================================"
echo "  Nex PriceWatch - Setup"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="macos";;
    MINGW*|CYGWIN*|MSYS*) PLATFORM="windows";;
    *)       PLATFORM="unknown";;
esac
echo "Platform: $PLATFORM"
echo "Skill directory: $SKILL_DIR"
echo ""

# Step 1: Check Python
echo "[1/4] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "ERROR: Python 3 is required but not found." >&2
    echo "Install Python 3.8+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"
echo ""

# Step 2: Create data directory
echo "[2/4] Creating data directory..."
mkdir -p "$DATA_DIR"
mkdir -p "$DATA_DIR/snapshots"
echo "  Created: $DATA_DIR"
echo ""

# Step 3: Initialize database
echo "[3/4] Initializing database..."
$PYTHON -c "
import sys
sys.path.insert(0, '$SKILL_DIR')
from lib.storage import init_db
init_db()
print('  Database initialized')
"
echo ""

# Step 4: Create symlink to bin directory
echo "[4/4] Setting up command..."
mkdir -p "$BIN_DIR"

# Create wrapper script
WRAPPER_PATH="$BIN_DIR/$SKILL_NAME"
cat > "$WRAPPER_PATH" << 'EOF'
#!/bin/bash
SKILL_DIR="$(cd "$(dirname "$0")/../.local/share/clawhub-skills/nex-pricewatch" 2>/dev/null && pwd)" || \
SKILL_DIR="$(python3 -c 'import sys; sys.path.insert(0, "."); from pathlib import Path; print(Path(__file__).parent.parent.parent.parent / "lib")')" || \
SKILL_DIR="$(dirname "$0")/../src/nex-pricewatch"
python3 "$SKILL_DIR/nex-pricewatch.py" "$@"
EOF

chmod +x "$WRAPPER_PATH"
echo "  Command available as: $SKILL_NAME"
echo ""

echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Quick start:"
echo "  1. Add a target:"
echo "     nex-pricewatch add --name 'Competitor X' --url 'https://...' --selector '.price' --selector-type css"
echo ""
echo "  2. Check prices:"
echo "     nex-pricewatch check --alerts"
echo ""
echo "  3. View dashboard:"
echo "     nex-pricewatch dashboard"
echo ""
echo "  4. More commands:"
echo "     nex-pricewatch --help"
echo ""
echo "Data stored in: $DATA_DIR"
echo "Homepage: https://nex-ai.be"
echo ""
