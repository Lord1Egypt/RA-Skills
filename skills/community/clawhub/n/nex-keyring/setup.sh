#!/usr/bin/env bash
# Nex Keyring - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-keyring"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-keyring"

echo "============================================"
echo "  Nex Keyring - Setup"
echo "  Local API Key & Secret Rotation Tracker"
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
    echo "Install Python 3.8+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"

# Step 2: Create data directory
echo "[2/5] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 3: Initialize database
echo "[3/5] Initializing database..."
$PYTHON -c "
import sys
sys.path.insert(0, '$SKILL_DIR')
from lib.storage import Storage
from lib.config import DB_PATH
storage = Storage(DB_PATH)
print('  Database initialized successfully')
"

# Step 4: Create symlink to CLI tool
echo "[4/5] Installing CLI command..."
mkdir -p "$BIN_DIR"

# Create wrapper script
cat > "$BIN_DIR/$SERVICE_NAME" << 'WRAPPER'
#!/usr/bin/env bash
SKILL_DIR="$(dirname "$(cd "$(dirname "$0")/.." && pwd)")/mnt/ClawHub Skills - Nex AI Bible/nex-keyring"
exec python3 "$SKILL_DIR/nex-keyring.py" "$@"
WRAPPER

# Try to find the actual skill directory
if [ ! -d "$SKILL_DIR/lib" ]; then
    # Try alternative paths
    for alt_dir in \
        "$HOME/.nex-skills/nex-keyring" \
        "/opt/nex-skills/nex-keyring" \
        "./nex-keyring"; do
        if [ -d "$alt_dir/lib" ]; then
            SKILL_DIR="$alt_dir"
            break
        fi
    done
fi

# Update wrapper with correct path
cat > "$BIN_DIR/$SERVICE_NAME" << WRAPPER
#!/usr/bin/env bash
exec python3 "$SKILL_DIR/nex-keyring.py" "\$@"
WRAPPER

chmod +x "$BIN_DIR/$SERVICE_NAME"
echo "  Installed: $BIN_DIR/$SERVICE_NAME"

# Check if $BIN_DIR is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "  WARNING: $BIN_DIR is not in your PATH"
    echo "  Add this line to your shell profile (.bashrc, .zshrc, etc):"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Step 5: Check optional dependencies
echo "[5/5] Checking dependencies..."

# Check cryptography
if $PYTHON -c "import cryptography" 2>/dev/null; then
    echo "  cryptography: installed (Fernet encryption enabled)"
else
    echo "  cryptography: not installed (optional, recommended)"
    echo ""
    echo "  For stronger encryption, install it:"
    echo "    pip install cryptography"
    echo ""
fi

# Final summary
echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add ~/.local/bin to your PATH (if not already done)"
echo "  2. Run: nex-keyring config"
echo "  3. Try: nex-keyring help"
echo ""
echo "Quick example:"
echo "  nex-keyring add --name 'OpenAI Key' --service openai --env-var OPENAI_API_KEY"
echo "  nex-keyring list"
echo "  nex-keyring check"
echo ""
echo "Documentation: README.md"
echo "License: MIT-0"
echo "Author: Nex AI (nex-ai.be)"
echo ""
