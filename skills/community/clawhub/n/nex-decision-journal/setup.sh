#!/usr/bin/env bash
# Nex Decision Journal - Setup Script
# Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Creates data dir, inits SQLite DB, verifies Python 3.

set -euo pipefail

SKILL_NAME="nex-decision-journal"
DATA_DIR="$HOME/.nex-decision-journal"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---------------------------------------------------------------------------
# Colors (if terminal supports them)
# ---------------------------------------------------------------------------
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    NC=''
fi

echo ""
echo "=========================================="
echo "  Nex Decision Journal - Setup"
echo "  By Nex AI (nex-ai.be)"
echo "=========================================="
echo ""

# ---------------------------------------------------------------------------
# Check Python 3
# ---------------------------------------------------------------------------
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PY_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1)
    if [ "$PY_VERSION" = "3" ]; then
        PYTHON="python"
    fi
fi

if [ -z "$PYTHON" ]; then
    echo -e "${RED}Error: Python 3 is required but not found.${NC}"
    echo "Install Python 3 and try again."
    exit 1
fi

PY_FULL_VERSION=$($PYTHON --version 2>&1)
echo -e "${GREEN}[OK]${NC} Found $PY_FULL_VERSION"

# ---------------------------------------------------------------------------
# Create data directory
# ---------------------------------------------------------------------------
if [ ! -d "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo -e "${GREEN}[OK]${NC} Created data directory: $DATA_DIR"
else
    echo -e "${GREEN}[OK]${NC} Data directory exists: $DATA_DIR"
fi

# Create exports subdirectory
if [ ! -d "$DATA_DIR/exports" ]; then
    mkdir -p "$DATA_DIR/exports"
    echo -e "${GREEN}[OK]${NC} Created exports directory: $DATA_DIR/exports"
fi

# Set permissions (non-Windows only)
if [[ "$(uname)" != MINGW* ]] && [[ "$(uname)" != MSYS* ]] && [[ "$(uname)" != CYGWIN* ]]; then
    chmod 700 "$DATA_DIR" 2>/dev/null || true
    chmod 700 "$DATA_DIR/exports" 2>/dev/null || true
fi

# ---------------------------------------------------------------------------
# Initialize database
# ---------------------------------------------------------------------------
echo ""
echo "Initializing database..."
cd "$SCRIPT_DIR"
$PYTHON -c "
import sys
sys.path.insert(0, '.')
from lib.storage import init_db
init_db()
print('Database initialized.')
"
echo -e "${GREEN}[OK]${NC} Database ready at $DATA_DIR/decisions.db"

# ---------------------------------------------------------------------------
# Verify CLI works
# ---------------------------------------------------------------------------
echo ""
echo "Verifying CLI..."
$PYTHON "$SCRIPT_DIR/nex-decision-journal.py" --help > /dev/null 2>&1
echo -e "${GREEN}[OK]${NC} CLI verified"

# ---------------------------------------------------------------------------
# Create convenience wrapper
# ---------------------------------------------------------------------------
WRAPPER_DIR="$HOME/.local/bin"
WRAPPER="$WRAPPER_DIR/nex-decision-journal"

if [ -d "$WRAPPER_DIR" ] || mkdir -p "$WRAPPER_DIR" 2>/dev/null; then
    cat > "$WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
exec $PYTHON "$SCRIPT_DIR/nex-decision-journal.py" "\$@"
WRAPPER_EOF
    chmod +x "$WRAPPER"
    echo -e "${GREEN}[OK]${NC} Created CLI wrapper at $WRAPPER"

    if [[ ":$PATH:" != *":$WRAPPER_DIR:"* ]]; then
        echo -e "${YELLOW}[NOTE]${NC} Add $WRAPPER_DIR to your PATH to use 'nex-decision-journal' directly:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
else
    echo -e "${YELLOW}[NOTE]${NC} Could not create CLI wrapper. Run directly with:"
    echo "  $PYTHON $SCRIPT_DIR/nex-decision-journal.py"
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "=========================================="
echo -e "  ${GREEN}Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  nex-decision-journal log \"My first decision\" --reasoning \"Because...\" --confidence 7 --follow-up 1m"
echo "  nex-decision-journal list"
echo "  nex-decision-journal pending"
echo ""
echo "Data stored at: $DATA_DIR"
echo "No telemetry. No tracking. Your decisions are yours."
echo ""
echo "[Decision Journal by Nex AI | nex-ai.be]"
