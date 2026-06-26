#!/usr/bin/env bash
# Nex SkillMon - Setup Script
# MIT-0 License - Copyright 2026 Nex AI
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-skillmon"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-skillmon"

echo "============================================"
echo "  Nex SkillMon - Setup"
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
echo "[1/5] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "ERROR: Python 3 is required but not found." >&2
    echo "Install Python 3.9+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"

# Step 2: Create data directory
echo "[2/5] Creating data directory..."
mkdir -p "$DATA_DIR/logs"
echo "  Directory: $DATA_DIR"

# Step 3: Initialize database
echo "[3/5] Initializing database..."
$PYTHON -c "
from lib.config import DB_PATH
from lib.storage import Storage

storage = Storage()
storage.init_db()
print('  Database initialized: $DATA_DIR/skillmon.db')
" 2>&1 || echo "  Database already initialized"

# Step 4: Create bin symlink
echo "[4/5] Creating command symlink..."
mkdir -p "$BIN_DIR"
SCRIPT_PATH="$SKILL_DIR/nex-skillmon.py"

if [ "$PLATFORM" = "windows" ]; then
    # Windows batch wrapper
    BAT_FILE="$BIN_DIR/nex-skillmon.bat"
    cat > "$BAT_FILE" << 'EOF'
@echo off
python "%~dp0..\..\.nex-skillmon\nex-skillmon.py" %*
EOF
    echo "  Created: $BAT_FILE"
else
    # Unix symlink
    LINK_PATH="$BIN_DIR/nex-skillmon"
    if [ -L "$LINK_PATH" ] || [ -e "$LINK_PATH" ]; then
        rm -f "$LINK_PATH"
    fi
    ln -s "$SCRIPT_PATH" "$LINK_PATH"
    chmod +x "$SCRIPT_PATH"
    echo "  Created: $LINK_PATH"
fi

# Step 5: Final instructions
echo "[5/5] Setup complete!"
echo ""
echo "Quick Start:"
echo "  1. Scan installed skills:"
echo "     nex-skillmon scan"
echo ""
echo "  2. View health dashboard:"
echo "     nex-skillmon health"
echo ""
echo "  3. Get cost overview:"
echo "     nex-skillmon cost"
echo ""
echo "  4. See all commands:"
echo "     nex-skillmon --help"
echo ""
echo "Data location: $DATA_DIR"
echo ""

if [ "$PLATFORM" != "windows" ] && ! echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "NOTE: Add $BIN_DIR to your PATH for easy access:"
    echo "  export PATH=\"\$PATH:$BIN_DIR\""
fi

echo ""
echo "[Nex SkillMon by Nex AI | nex-ai.be]"
