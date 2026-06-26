#!/usr/bin/env bash
# Nex Onboarding - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-onboarding"
VENV_DIR="$DATA_DIR/venv"
BIN_DIR="$HOME/.local/bin"

echo "============================================"
echo "  Nex Onboarding - Setup"
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
mkdir -p "$BIN_DIR"
echo "  Created: $DATA_DIR"
echo ""

# Step 3: Initialize database
echo "[3/5] Initializing database..."
cd "$SKILL_DIR"
$PYTHON << 'PYEOF'
from lib.storage import init_db
init_db()
print("  Database initialized")
PYEOF
echo ""

# Step 4: Create wrapper script
echo "[4/5] Creating command wrapper..."
WRAPPER="$BIN_DIR/nex-onboarding"
cat > "$WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
cd "$SKILL_DIR"
$PYTHON nex-onboarding.py "\$@"
WRAPPER_EOF
chmod +x "$WRAPPER"
echo "  Created: $WRAPPER"
echo ""

# Step 5: Verify installation
echo "[5/5] Verifying installation..."
$PYTHON "$SKILL_DIR/nex-onboarding.py" --help > /dev/null 2>&1 && echo "  CLI verified" || echo "  Warning: CLI verification failed"
echo ""

echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Quick Start:"
echo "  nex-onboarding start \"Bakkerij Peeters\" --tier starter --email \"info@bakkerijpeeters.be\""
echo "  nex-onboarding progress \"Bakkerij Peeters\""
echo "  nex-onboarding next \"Bakkerij Peeters\""
echo ""
echo "Make sure $BIN_DIR is in your PATH:"
echo "  export PATH=\"\$PATH:$BIN_DIR\""
echo ""
