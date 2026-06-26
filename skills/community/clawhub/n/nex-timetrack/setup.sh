#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="Nex Timetrack"
SKILL_SLUG="nex-timetrack"
BRAND="Nex AI (nex-ai.be)"
DATA_DIR="$HOME/.nex-timetrack"
BIN_DIR="$HOME/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  $SKILL_NAME - Setup"
echo "  By $BRAND"
echo "=========================================="
echo ""

# --- Python check ---
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+\.\d+')
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            PYTHON="$cmd"
            echo "[OK] Found Python $version"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] Python 3.8+ required but not found."
    echo "Install Python: https://www.python.org/downloads/"
    exit 1
fi

# --- Data directories ---
mkdir -p "$DATA_DIR"
echo "[OK] Created: $DATA_DIR"
mkdir -p "$DATA_DIR/exports"
echo "[OK] Created: $DATA_DIR/exports"

# --- Permissions (non-Windows) ---
if [[ "$(uname)" != MINGW* ]] && [[ "$(uname)" != MSYS* ]]; then
    chmod 700 "$DATA_DIR" 2>/dev/null || true
fi

# --- Database init ---
echo ""
echo "Initializing database..."
$PYTHON -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from lib.storage import init_db
init_db()
print('Database initialized.')
"
echo "[OK] Database ready at $DATA_DIR/timetrack.db"

# --- CLI verification ---
echo ""
echo "Verifying CLI..."
$PYTHON "$SCRIPT_DIR/$SKILL_SLUG.py" --help > /dev/null 2>&1
echo "[OK] CLI verified"

# --- Wrapper script ---
mkdir -p "$BIN_DIR"
WRAPPER="$BIN_DIR/$SKILL_SLUG"

cat > "$WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
exec $PYTHON "$SCRIPT_DIR/$SKILL_SLUG.py" "\$@"
WRAPPER_EOF

chmod +x "$WRAPPER"
echo "[OK] Created CLI wrapper at $WRAPPER"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "[NOTE] Add $BIN_DIR to your PATH:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "=========================================="
echo "  Setup complete!"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  $SKILL_SLUG start \"Working on homepage\" --client \"Client Name\""
echo "  $SKILL_SLUG stop"
echo "  $SKILL_SLUG log \"Design work\" 2h --client \"Client Name\""
echo "  $SKILL_SLUG summary --client \"Client Name\""
echo ""
echo "Data stored at: $DATA_DIR"
echo "No telemetry. No tracking. Your data is yours."
echo ""
echo "[$SKILL_NAME by $BRAND]"
