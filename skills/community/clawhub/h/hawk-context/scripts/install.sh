#!/usr/bin/env bash
# install.sh — Auto-link hawk-compress command to ~/bin
# Run after: openclaw skills install ./context-compressor.skill

set -e

echo "[install] Context-Compressor — creating symlinks..."

mkdir -p "$HOME/bin"
if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo "[install] Adding ~/bin to PATH in ~/.bashrc..."
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$HOME/bin:$PATH"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ln -sf "$SCRIPT_DIR/hawk-compress" "$HOME/bin/hawk-compress"

echo "[install] Symlink created: ~/bin/hawk-compress"
echo "[install] Run: source ~/.bashrc && hawk-compress --help"
