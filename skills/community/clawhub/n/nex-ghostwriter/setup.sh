#!/usr/bin/env bash
# Nex Ghostwriter - Setup Script
# Copyright 2026 Nex AI (Kevin Blancaflor)
# Creates data dir, inits SQLite DB, verifies Python 3.

set -euo pipefail

SKILL_NAME="nex-ghostwriter"
DATA_DIR="$HOME/.nex-ghostwriter"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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
echo "  Nex Ghostwriter - Setup"
echo "  By Nex AI (nex-ai.be)"
echo "=========================================="
echo ""

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
    echo -e "${RED}Error: Python 3 required but not found.${NC}"
    exit 1
fi

PY_FULL_VERSION=$($PYTHON --version 2>&1)
echo -e "${GREEN}[OK]${NC} Found $PY_FULL_VERSION"

for dir in "$DATA_DIR" "$DATA_DIR/exports" "$DATA_DIR/templates"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}[OK]${NC} Created: $dir"
    fi
done

if [[ "$(uname)" != MINGW* ]] && [[ "$(uname)" != MSYS* ]] && [[ "$(uname)" != CYGWIN* ]]; then
    chmod 700 "$DATA_DIR" 2>/dev/null || true
fi

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
echo -e "${GREEN}[OK]${NC} Database ready at $DATA_DIR/ghostwriter.db"

echo ""
echo "Verifying CLI..."
$PYTHON "$SCRIPT_DIR/nex-ghostwriter.py" --help > /dev/null 2>&1
echo -e "${GREEN}[OK]${NC} CLI verified"

WRAPPER_DIR="$HOME/.local/bin"
WRAPPER="$WRAPPER_DIR/nex-ghostwriter"

if [ -d "$WRAPPER_DIR" ] || mkdir -p "$WRAPPER_DIR" 2>/dev/null; then
    cat > "$WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
exec $PYTHON "$SCRIPT_DIR/nex-ghostwriter.py" "\$@"
WRAPPER_EOF
    chmod +x "$WRAPPER"
    echo -e "${GREEN}[OK]${NC} Created CLI wrapper at $WRAPPER"

    if [[ ":$PATH:" != *":$WRAPPER_DIR:"* ]]; then
        echo -e "${YELLOW}[NOTE]${NC} Add $WRAPPER_DIR to your PATH:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
else
    echo -e "${YELLOW}[NOTE]${NC} Run directly with:"
    echo "  $PYTHON $SCRIPT_DIR/nex-ghostwriter.py"
fi

echo ""
echo "=========================================="
echo -e "  ${GREEN}Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  nex-ghostwriter draft \"Client meeting\" --client \"Name\" --notes \"What was discussed\" --actions \"Item 1, Item 2\""
echo "  nex-ghostwriter list"
echo "  nex-ghostwriter drafts"
echo ""
echo "Data stored at: $DATA_DIR"
echo "No telemetry. No tracking. Your data is yours."
echo ""
echo "[Ghostwriter by Nex AI | nex-ai.be]"
