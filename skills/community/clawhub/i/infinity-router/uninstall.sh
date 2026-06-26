#!/usr/bin/env bash
# uninstall.sh — Infinity-Router uninstaller
#
# Removes:
#   - CLI symlinks from /usr/local/bin
#   - OpenClaw skill symlink from ~/.openclaw/workspace/skills/infinity-router
#   - The local .venv directory
#
# Does NOT remove:
#   - ~/.infinity-router/  (state, cache, rate-limit records)
#   - This project directory itself
#
# Usage:
#   chmod +x uninstall.sh && ./uninstall.sh

set -euo pipefail

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="/usr/local/bin"
SKILL_NAME="infinity-router"
COMMANDS=("infinity-router" "infinity-router-daemon" "infinity-router-watch")
OPENCLAW_SKILLS_DIR="$HOME/.openclaw/workspace/skills"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

info() { echo -e "${CYAN}▸ $*${RESET}"; }
ok()   { echo -e "${GREEN}✓ $*${RESET}"; }
warn() { echo -e "${YELLOW}! $*${RESET}"; }

echo ""
echo "  Infinity-Router — uninstaller"
echo "  ─────────────────────────────────"
echo ""

# ── Remove CLI symlinks ───────────────────────────────────────────────────────
info "Removing CLI symlinks from $BIN_DIR…"
for cmd in "${COMMANDS[@]}"; do
    dst="$BIN_DIR/$cmd"
    if [[ -L "$dst" ]]; then
        rm -f "$dst"
        ok "Removed $dst"
    else
        warn "$dst not found, skipping"
    fi
done

# ── Remove OpenClaw skill symlink ─────────────────────────────────────────────
SKILL_LINK="$OPENCLAW_SKILLS_DIR/$SKILL_NAME"
if [[ -L "$SKILL_LINK" ]]; then
    info "Removing OpenClaw skill symlink…"
    rm -f "$SKILL_LINK"
    ok "Removed $SKILL_LINK"
fi

# ── Remove venv ───────────────────────────────────────────────────────────────
info "Removing virtual environment…"
if [[ -d "$VENV_DIR" ]]; then
    rm -rf "$VENV_DIR"
    ok "Removed $VENV_DIR"
else
    warn "$VENV_DIR not found, skipping"
fi

echo ""
echo "  Uninstall complete."
echo ""
echo "  State files were left intact:"
echo "    ~/.infinity-router/    (cache, rate-limits, daemon state)"
echo "  Remove manually if needed:"
echo "    rm -rf ~/.infinity-router"
echo ""
