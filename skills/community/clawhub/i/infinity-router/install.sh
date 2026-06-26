#!/usr/bin/env bash
# install.sh — Infinity-Router installer
#
# What it does:
#   1. Creates a Python venv inside this project directory
#   2. Installs the package into the venv
#   3. Symlinks CLI commands to /usr/local/bin  (global access)
#   4. If OpenClaw is installed, registers the skill in
#      ~/.openclaw/workspace/skills/infinity-router  (symlink → this dir)
#
# Usage:
#   chmod +x install.sh && ./install.sh
#
# Uninstall:
#   ./uninstall.sh

set -euo pipefail

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="/usr/local/bin"
SKILL_NAME="infinity-router"
COMMANDS=("infinity-router" "infinity-router-daemon" "infinity-router-watch")
OPENCLAW_SKILLS_DIR="$HOME/.openclaw/workspace/skills"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RESET='\033[0m'

info()  { echo -e "${CYAN}▸ $*${RESET}"; }
ok()    { echo -e "${GREEN}✓ $*${RESET}"; }
warn()  { echo -e "${YELLOW}! $*${RESET}"; }
fail()  { echo -e "${RED}✗ $*${RESET}"; exit 1; }

echo ""
echo "  Infinity-Router — installer"
echo "  ────────────────────────────────"
echo ""

# ── 1. Check Python 3.10+ ─────────────────────────────────────────────────────
info "Checking Python 3.10+…"
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || fail "Python not found")
PY_MAJOR=$("$PYTHON" -c "import sys; print(sys.version_info.major)")
PY_MINOR=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")
PY_VERSION="$PY_MAJOR.$PY_MINOR"

if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 10 ]]; then
    fail "Python 3.10+ required, found $PY_VERSION"
fi
ok "Python $PY_VERSION"

# ── 2. Create venv ────────────────────────────────────────────────────────────
info "Creating virtual environment at $VENV_DIR…"
"$PYTHON" -m venv "$VENV_DIR"
ok "Virtual environment created"

# ── 3. Install package ────────────────────────────────────────────────────────
info "Installing infinity-router into venv…"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -e "$INSTALL_DIR"
ok "Package installed"

# ── 4. Symlink CLI commands to /usr/local/bin ─────────────────────────────────
info "Linking commands to $BIN_DIR…"
for cmd in "${COMMANDS[@]}"; do
    src="$VENV_DIR/bin/$cmd"
    dst="$BIN_DIR/$cmd"

    [[ -f "$src" ]] || fail "Binary not found after install: $src"

    # Remove existing link/file
    [[ -e "$dst" || -L "$dst" ]] && rm -f "$dst"

    ln -s "$src" "$dst"
    ok "Linked $cmd → $dst"
done

# ── 5. Register with OpenClaw (if installed) ──────────────────────────────────
echo ""
if [[ -d "$HOME/.openclaw" ]]; then
    info "OpenClaw detected — registering skill…"

    mkdir -p "$OPENCLAW_SKILLS_DIR"
    SKILL_PATH="$OPENCLAW_SKILLS_DIR/$SKILL_NAME"

    # Remove existing entry (could be a stale symlink or old directory)
    if [[ -L "$SKILL_PATH" ]]; then
        rm -f "$SKILL_PATH"
    elif [[ -d "$SKILL_PATH" ]]; then
        warn "$SKILL_PATH already exists as a directory — leaving it untouched"
        SKILL_PATH=""
    fi

    if [[ -n "$SKILL_PATH" ]]; then
        ln -s "$INSTALL_DIR" "$SKILL_PATH"
        ok "Skill registered at $SKILL_PATH → $INSTALL_DIR"
    fi
else
    warn "OpenClaw not found — skipping skill registration"
    warn "If you install OpenClaw later, re-run this script."
fi

# ── 6. Verify ─────────────────────────────────────────────────────────────────
echo ""
info "Verifying…"
for cmd in "${COMMANDS[@]}"; do
    if command -v "$cmd" &>/dev/null; then
        ok "$cmd is available"
    else
        warn "$cmd not in PATH — you may need: export PATH=\"$BIN_DIR:\$PATH\""
    fi
done

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "  Installation complete."
echo ""
echo "  Next steps:"
echo "    export OPENROUTER_API_KEY='sk-or-v1-...'   # get free key: openrouter.ai/keys"
echo "    infinity-router pick                        # configure best free model"
if [[ -d "$HOME/.openclaw" ]]; then
echo "    openclaw gateway restart                    # apply config to OpenClaw"
fi
echo ""
