#!/usr/bin/env bash
# Multimedia Manager (Community Edition) — Quick Setup
#
# What this script does:
#   1. Checks Python 3.9+ and ffmpeg availability
#   2. Installs 3 Python packages: Flask, Pillow, PyYAML
#   3. Creates .env with a random access token (if not exists)
#   4. Creates ~/.image-vault directory for local storage
#   5. Initializes the SQLite database
#
# No network connections after package install. All data stays local.
# Usage: bash setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_VAULT="$HOME/.image-vault"

echo "=== Multimedia Manager Setup ==="
echo ""
echo "This will install Flask, Pillow, PyYAML and create local storage."
echo "No data leaves your machine. Press Ctrl+C to cancel."
echo ""

# 1. Check Python
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 not found. Please install Python 3.9+."
  exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python $PY_VERSION found"

# 2. Check ffmpeg (optional but recommended)
if command -v ffmpeg &>/dev/null; then
  echo "✓ ffmpeg found"
else
  echo "⚠ ffmpeg not found — video import will not work"
  echo "  Install: brew install ffmpeg (macOS) / apt install ffmpeg (Linux)"
fi

# 3. Install Python dependencies (3 packages only)
echo ""
echo "Installing Python dependencies (Flask, Pillow, PyYAML)..."
pip3 install -q Flask Pillow PyYAML 2>/dev/null || pip install -q Flask Pillow PyYAML
echo "✓ Dependencies installed"

# 4. Create .env if not exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
  TOKEN=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")
  cat > "$SCRIPT_DIR/.env" << EOF
# Multimedia Manager — Local Environment
IMAGE_VAULT_TOKEN=$TOKEN
# IMAGE_VAULT_DIR=$DEFAULT_VAULT
EOF
  echo "✓ Created .env with auto-generated token: $TOKEN"
  echo "  ⚠ Save this token — you'll need it to access the gallery"
else
  echo "✓ .env already exists"
fi

# 5. Create vault directory
VAULT_DIR=$(grep -E "^IMAGE_VAULT_DIR=" "$SCRIPT_DIR/.env" 2>/dev/null | cut -d= -f2 | sed "s|~|$HOME|")
VAULT_DIR="${VAULT_DIR:-$DEFAULT_VAULT}"

mkdir -p "$VAULT_DIR/originals" "$VAULT_DIR/thumbnails" "$VAULT_DIR/backups"
echo "✓ Vault directory ready: $VAULT_DIR"

# 6. Initialize database
cd "$SCRIPT_DIR/scripts"
python3 -c "from image_db import init_db; init_db(); print('✓ Database initialized')"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Start the gallery:"
echo "  python3 $SCRIPT_DIR/scripts/image_cli.py serve --port 9876"
echo ""
echo "Import images:"
echo "  python3 $SCRIPT_DIR/scripts/image_cli.py import /path/to/photos"
echo ""
echo "Open: http://localhost:9876"
