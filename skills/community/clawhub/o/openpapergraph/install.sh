#!/bin/bash
# OpenPaperGraph — One-line installer for Claude Code / OpenClaw
# Usage: bash install.sh [--global | --project | --check]
#
# --global   Install /opg skill globally (available in all Claude Code sessions)
# --project  Install /opg skill in the current project only
# --check    Verify installation status without making changes
# (no flag)  Interactive — asks which mode to use

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$SCRIPT_DIR/openpapergraph_cli.py"
SKILL_PATH="$SCRIPT_DIR/SKILL.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; }
info() { echo -e "  ${CYAN}→${NC} $1"; }

# ─── Check Prerequisites ──────────────────────────────────────────────

check_prerequisites() {
    echo ""
    echo "Checking prerequisites..."

    # Python 3.8+
    if command -v python3 &>/dev/null; then
        PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
        if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 8 ]; then
            ok "Python $PY_VER"
        else
            fail "Python $PY_VER (need 3.8+)"
            return 1
        fi
    else
        fail "Python 3 not found"
        return 1
    fi

    # Core dependencies
    local all_ok=true
    for pkg in httpx pymupdf scholarly; do
        if python3 -c "import $( [ "$pkg" = "pymupdf" ] && echo "fitz" || echo "$pkg" )" 2>/dev/null; then
            ok "$pkg installed"
        else
            fail "$pkg not installed"
            all_ok=false
        fi
    done

    # Optional: openai
    if python3 -c "import openai" 2>/dev/null; then
        ok "openai installed (LLM summaries enabled)"
    else
        warn "openai not installed (LLM summaries disabled, extractive mode only)"
    fi

    # CLI file exists
    if [ -f "$CLI_PATH" ]; then
        ok "CLI found: $CLI_PATH"
    else
        fail "CLI not found: $CLI_PATH"
        return 1
    fi

    # SKILL.md exists
    if [ -f "$SKILL_PATH" ]; then
        ok "SKILL.md found: $SKILL_PATH"
    else
        fail "SKILL.md not found: $SKILL_PATH"
        return 1
    fi

    # S2 API key
    if [ -n "${S2_API_KEY:-}" ]; then
        ok "S2_API_KEY set"
    else
        warn "S2_API_KEY not set (Semantic Scholar will be rate-limited)"
    fi

    # LLM API key (check common ones)
    local llm_found=false
    for key in OPENAI_API_KEY ANTHROPIC_API_KEY DEEPSEEK_API_KEY GEMINI_API_KEY DASHSCOPE_API_KEY ZHIPUAI_API_KEY MOONSHOT_API_KEY; do
        if [ -n "${!key:-}" ]; then
            ok "LLM key found: $key"
            llm_found=true
            break
        fi
    done
    if ! $llm_found; then
        warn "No LLM API key set (summary will use extractive mode)"
    fi

    if $all_ok; then
        return 0
    else
        return 1
    fi
}

# ─── Install Dependencies ─────────────────────────────────────────────

install_deps() {
    echo ""
    echo "Installing dependencies..."
    pip install httpx pymupdf scholarly && ok "Core dependencies installed" || { fail "pip install failed"; return 1; }
    echo ""
    info "Optional: run 'pip install openai' to enable LLM-powered summaries"
}

# ─── Install Skill (Global) ───────────────────────────────────────────

install_global() {
    echo ""
    echo "Installing /opg skill globally..."

    local target_dir="$HOME/.claude/commands/opg"
    mkdir -p "$target_dir"

    # Remove old installation (copy or broken symlink)
    if [ -e "$target_dir/SKILL.md" ] || [ -L "$target_dir/SKILL.md" ]; then
        rm -f "$target_dir/SKILL.md"
        info "Removed old installation"
    fi
    # Also remove legacy flat file if it exists
    if [ -e "$HOME/.claude/commands/opg.md" ] || [ -L "$HOME/.claude/commands/opg.md" ]; then
        rm -f "$HOME/.claude/commands/opg.md"
        info "Removed legacy opg.md"
    fi

    # Create symlink
    ln -sf "$SKILL_PATH" "$target_dir/SKILL.md"

    # Verify
    if [ -L "$target_dir/SKILL.md" ] && [ -f "$target_dir/SKILL.md" ]; then
        local resolved
        resolved=$(python3 -c "import os; print(os.path.dirname(os.path.realpath('$target_dir/SKILL.md')))")
        ok "Symlink created: $target_dir/SKILL.md"
        ok "SKILL_DIR resolves to: $resolved"
        if [ "$resolved" = "$SCRIPT_DIR" ]; then
            ok "Path resolution correct!"
        else
            warn "SKILL_DIR resolves to $resolved (expected $SCRIPT_DIR)"
        fi
    else
        fail "Symlink creation failed"
        return 1
    fi

    echo ""
    ok "Global install complete. Start a NEW Claude Code session and type /opg"
}

# ─── Install Skill (Project) ──────────────────────────────────────────

install_project() {
    echo ""
    echo "Installing /opg skill in current project..."

    local target_dir="$SCRIPT_DIR/.claude/commands/opg"
    mkdir -p "$target_dir"

    # Create symlink (relative for portability within repo)
    ln -sf "../../../SKILL.md" "$target_dir/SKILL.md"

    if [ -L "$target_dir/SKILL.md" ] && [ -f "$target_dir/SKILL.md" ]; then
        ok "Symlink created: $target_dir/SKILL.md -> ../../../SKILL.md"
        ok "Project-level /opg skill installed"
    else
        fail "Symlink creation failed"
        return 1
    fi

    echo ""
    ok "Project install complete. Start a NEW Claude Code session from this directory"
}

# ─── Check Installation Status ─────────────────────────────────────────

check_status() {
    echo ""
    echo "=== OpenPaperGraph Installation Status ==="

    check_prerequisites

    echo ""
    echo "Skill registration:"

    # Global
    if [ -L "$HOME/.claude/commands/opg/SKILL.md" ]; then
        local target
        target=$(readlink "$HOME/.claude/commands/opg/SKILL.md" 2>/dev/null || true)
        ok "Global: ~/.claude/commands/opg/SKILL.md -> $target"
    elif [ -f "$HOME/.claude/commands/opg/SKILL.md" ]; then
        warn "Global: ~/.claude/commands/opg/SKILL.md exists but is a COPY (should be symlink)"
    elif [ -f "$HOME/.claude/commands/opg.md" ]; then
        warn "Global: ~/.claude/commands/opg.md exists (legacy flat file, should be opg/SKILL.md symlink)"
    else
        info "Global: not installed"
    fi

    # Project
    if [ -L "$SCRIPT_DIR/.claude/commands/opg/SKILL.md" ]; then
        ok "Project: .claude/commands/opg/SKILL.md (symlinked)"
    elif [ -f "$SCRIPT_DIR/.claude/commands/opg/SKILL.md" ]; then
        warn "Project: .claude/commands/opg/SKILL.md exists but is a COPY"
    else
        info "Project: not installed"
    fi

    echo ""
    echo "Quick test:"
    if python3 "$CLI_PATH" conferences --quiet 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  CLI works: {len(d)} conferences found')" 2>/dev/null; then
        ok "CLI is functional"
    else
        fail "CLI test failed"
    fi

    echo ""
}

# ─── Main ──────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   OpenPaperGraph Installer               ║"
echo "║   Academic Literature Discovery CLI       ║"
echo "╚══════════════════════════════════════════╝"

case "${1:-}" in
    --global)
        install_deps
        install_global
        ;;
    --project)
        install_deps
        install_project
        ;;
    --check)
        check_status
        ;;
    *)
        echo ""
        echo "Usage:"
        echo "  bash install.sh --global    Install globally (recommended)"
        echo "  bash install.sh --project   Install for this project only"
        echo "  bash install.sh --check     Check installation status"
        echo ""
        echo "What would you like to do?"
        echo "  1) Global install (available in all Claude Code sessions)"
        echo "  2) Project install (only in this directory)"
        echo "  3) Check status"
        echo ""
        read -rp "Choose [1/2/3]: " choice
        case "$choice" in
            1) install_deps; install_global ;;
            2) install_deps; install_project ;;
            3) check_status ;;
            *) echo "Invalid choice"; exit 1 ;;
        esac
        ;;
esac

echo ""
