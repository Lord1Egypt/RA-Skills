#!/usr/bin/env bash
# First-run setup for luca-assistant skill.
# Installs the package via uv and initializes the database.
set -euo pipefail

# Ensure uv-installed binaries are on PATH
export PATH="$HOME/.local/bin:$PATH"

LUCA_DATA_DIR="${HOME}/.local/share/luca"
export DB_PATH="${LUCA_DATA_DIR}/luca.db"

echo "=== Luca Assistant Setup ==="

# 1. Install luca-assistant from PyPI
if command -v luca-mcp &>/dev/null; then
  echo "[ok] luca-assistant already installed"
else
  echo "[..] Installing luca-assistant from PyPI..."
  uv tool install luca-assistant
  echo "[ok] Installed"
fi

# 2. Create data directory and initialize the database
mkdir -p "${LUCA_DATA_DIR}"
echo "[..] Initializing database (downloading Offer Optimist card data)..."
luca init
echo "[ok] Database ready at ${DB_PATH}"

# 3. Verify installation
echo ""
echo "=== Verifying ==="
if luca-mcp --help &>/dev/null; then
  echo "[ok] luca-mcp is working"
else
  echo "[!!] luca-mcp not found — ensure ~/.local/bin is on PATH"
  exit 1
fi

echo ""
echo "=== Setup complete ==="
echo "The luca-mcp server is ready. Add it to your MCP config:"
echo ""
echo '  "luca-assistant": {'
echo '    "command": "luca-mcp",'
echo "    \"env\": { \"DB_PATH\": \"${DB_PATH}\" }"
echo '  }'
