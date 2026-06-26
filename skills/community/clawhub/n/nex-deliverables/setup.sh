#!/usr/bin/env bash
# Nex Deliverables - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-deliverables"
BIN_DIR="$HOME/.local/bin"

echo "============================================"
echo "  Nex Deliverables - Setup"
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
    echo "Install Python 3.9+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"

# Step 2: Create data directory
echo "[2/4] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 3: Initialize database
echo "[3/4] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" "$PYTHON" -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/deliverables.db')
"

# Step 4: Make CLI executable and create symlink
echo "[4/4] Setting up CLI tool..."
chmod +x "$SKILL_DIR/nex-deliverables.py"

mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-deliverables" << 'WRAPPER'
#!/usr/bin/env bash
exec python3 "SKILL_DIR_PLACEHOLDER/nex-deliverables.py" "$@"
WRAPPER

# Replace placeholder with actual path
sed -i.bak "s|SKILL_DIR_PLACEHOLDER|$SKILL_DIR|g" "$BIN_DIR/nex-deliverables"
rm -f "$BIN_DIR/nex-deliverables.bak"
chmod +x "$BIN_DIR/nex-deliverables"
echo "  CLI installed to $BIN_DIR/nex-deliverables"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "============================================"
echo "  Nex Deliverables installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. View all deliverables:"
echo "     nex-deliverables list"
echo ""
echo "  2. Add a client:"
echo "     nex-deliverables client add --name 'Your Client' --email 'contact@client.com'"
echo ""
echo "  3. Add a deliverable:"
echo "     nex-deliverables add --client 'Your Client' --title 'Homepage redesign' --type website --deadline 2026-05-01"
echo ""
echo "  4. Check workload:"
echo "     nex-deliverables workload"
echo ""
