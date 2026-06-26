#!/usr/bin/env bash
# Nex Reports - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-reports"
BIN_DIR="$HOME/.local/bin"

echo "============================================"
echo "  Nex Reports - Setup"
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
echo ""

# Step 2: Create data directory
echo "[2/5] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
mkdir -p "$DATA_DIR/reports"
mkdir -p "$DATA_DIR/templates"
echo "  Data directory: $DATA_DIR"
echo ""

# Step 3: Create bin directory and symlink
echo "[3/5] Installing CLI symlink..."
mkdir -p "$BIN_DIR"

if [ "$PLATFORM" = "windows" ]; then
    # Windows batch wrapper
    cat > "$BIN_DIR/nex-reports.cmd" <<'EOF'
@echo off
python "%~dp0\..\..\..\mnt\ClawHub Skills - Nex AI Bible\nex-reports\nex-reports.py" %*
EOF
    echo "  Installed: $BIN_DIR/nex-reports.cmd"
else
    # Unix symlink
    ln -sf "$SKILL_DIR/nex-reports.py" "$BIN_DIR/nex-reports"
    chmod +x "$BIN_DIR/nex-reports"
    echo "  Installed: $BIN_DIR/nex-reports"
fi
echo ""

# Step 4: Initialize database
echo "[4/5] Initializing database..."
$PYTHON -c "
from lib.storage import get_db
db = get_db()
db.init_db()
print('  Database initialized successfully')
"
echo ""

# Step 5: Check for optional nex-* commands
echo "[5/5] Checking for nex-* tools..."
MISSING_TOOLS=()

for tool in nex-healthcheck nex-crm nex-expenses nex-deliverables nex-domains nex-vault; do
    if command -v "$tool" &>/dev/null; then
        echo "  ✓ Found: $tool"
    else
        echo "  ✗ Missing: $tool"
        MISSING_TOOLS+=("$tool")
    fi
done
echo ""

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "WARNING: Some optional nex-* tools are missing:"
    for tool in "${MISSING_TOOLS[@]}"; do
        echo "  - $tool"
    done
    echo ""
    echo "Install missing tools with: nex install <tool-name>"
    echo ""
fi

# Final message
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Quick start:"
echo "  nex-reports modules              # List available modules"
echo "  nex-reports create \"My Report\" \\"
echo "    --schedule \"0 9 * * 1\" \\"
echo "    --modules health,crm,deliverables"
echo ""
echo "Data directory: $DATA_DIR"
echo "Configure IMAP/Telegram via environment variables:"
echo "  IMAP_HOST, IMAP_USER, IMAP_PASS, IMAP_PORT"
echo "  TELEGRAM_TOKEN, TELEGRAM_CHAT_ID"
echo ""
