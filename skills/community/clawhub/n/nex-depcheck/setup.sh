#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="Nex DepCheck"
SKILL_SLUG="nex-depcheck"
BRAND="Nex AI (nex-ai.be)"
BIN_DIR="$HOME/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  $SKILL_NAME - Setup"
echo "  By $BRAND"
echo "=========================================="
echo ""

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
    exit 1
fi

echo ""
echo "Verifying CLI..."
$PYTHON "$SCRIPT_DIR/$SKILL_SLUG.py" --help > /dev/null 2>&1
echo "[OK] CLI verified"

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
echo "  $SKILL_SLUG check /path/to/skill"
echo "  $SKILL_SLUG scan /path/to/skills"
echo "  $SKILL_SLUG stdlib pathlib"
echo ""
echo "No database. No telemetry. Pure scanner."
echo ""
echo "[$SKILL_NAME by $BRAND]"
