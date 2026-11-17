#!/usr/bin/env bash
# =========================================================================
# ig-downloader-skill — Universal Installer
# Version: 2.2.0
#
# Installs the Instagram Downloader skill + Python package for any AI agent:
#   OpenCode, Claude Code, Codex CLI, Cursor, and more.
#
# Usage:
#   # From cloned repo (recommended)
#   ./install.sh
#   ./install.sh --agent all
#
#   # One-liner (auto-downloads repo)
#   curl -fsSL https://raw.githubusercontent.com/cripterhack/ig-downloader-skill/main/install.sh | bash
#
#   # Via npx (if skills.sh registry is enabled)
#   npx skills add cripterhack/ig-downloader-skill
# =========================================================================
set -euo pipefail

SKILL_NAME="instagram-downloader"
SKILL_VERSION="2.2.0"
REPO="cripterhack/ig-downloader-skill"
REPO_URL="https://github.com/${REPO}.git"
RAW_URL="https://raw.githubusercontent.com/${REPO}/main"

# ─── Colors ─────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
log()   { echo -e " ${GREEN}✔${NC} $1"; }
warn()  { echo -e " ${YELLOW}⚠${NC} $1"; }
error() { echo -e " ${RED}✘${NC} $1"; exit 1; }
info()  { echo -e " ${BLUE}ℹ${NC} $1"; }
header(){ echo -e "\n${CYAN}══${BOLD} $1 ${NC}"; }
line()  { echo -e "${CYAN}────────────────────────────────────────${NC}"; }

# ─── Usage ──────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: ./install.sh [OPTIONS]

Install the Instagram Downloader skill + Python package for AI coding agents.

Options:
  -a, --agent <agent>    Target agent (auto-detect | opencode | claude | codex | cursor | all)
  -g, --global           Install globally for current user (DEFAULT)
  -p, --project          Install in current project directory
  -d, --dir <path>       Custom install directory (overrides --global/--project)
  -h, --help             Show this help message

Examples:
  ./install.sh                    # Auto-detect agent, install globally
  ./install.sh --agent all        # Install for ALL supported agents
  ./install.sh --agent codex      # Install only for Codex CLI
  ./install.sh --project          # Install in current project only
EOF
    exit 0
}

# ─── Parse arguments ────────────────────────────────────────────
TARGET_AGENT="auto"
INSTALL_SCOPE="global"
CUSTOM_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--agent)  TARGET_AGENT="$2"; shift 2 ;;
        -g|--global) INSTALL_SCOPE="global"; shift ;;
        -p|--project) INSTALL_SCOPE="project"; shift ;;
        -d|--dir)    CUSTOM_DIR="$2"; shift 2 ;;
        -h|--help)   usage ;;
        *) error "Unknown option: $1. Use -h for help." ;;
    esac
done

# ─── Welcome ────────────────────────────────────────────────────
echo
echo -e "  ${BOLD}Instagram Downloader Skill v${SKILL_VERSION}${NC}"
echo -e "  ${BLUE}Universal Installer${NC}"
line

# ─── Step 0: Locate repo root ──────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT=""

# Check if we're inside the repo (script is there) or running standalone
if [[ -f "$SCRIPT_DIR/SKILL.md" ]] && [[ -f "$SCRIPT_DIR/instagram_downloader.py" ]]; then
    REPO_ROOT="$SCRIPT_DIR"
    info "Running from local repo: ${REPO_ROOT}"
else
    # Standalone mode — need to clone
    info "Running standalone — cloning repo..."
    TMP_DIR="$(mktemp -d)"
    trap "rm -rf '${TMP_DIR}'" EXIT
    git clone --depth 1 "$REPO_URL" "$TMP_DIR/repo" || error "Failed to clone repo"
    REPO_ROOT="$TMP_DIR/repo"
    log "Repo cloned to temporary directory"
fi

# ─── Step 1: Install Python package ────────────────────────────
install_python_package() {
    header "Step 1: Installing Python Package"

    # Detect pip
    local pip_cmd=""
    for cmd in pip3 pip; do
        if command -v "$cmd" &>/dev/null; then
            pip_cmd="$cmd"
            break
        fi
    done

    if [[ -z "$pip_cmd" ]]; then
        warn "Python pip not found. Install manually:"
        echo "  pip install instagrapi requests playwright"
        echo "  pip install git+${REPO_URL}"
        return
    fi

    info "Using: ${pip_cmd}"

    # Install dependencies
    info "Installing Python dependencies..."
    $pip_cmd install instagrapi requests playwright 2>/dev/null || \
        warn "Some dependencies failed. Try: ${pip_cmd} install instagrapi requests"

    # Install the package itself
    if [[ -f "$REPO_ROOT/pyproject.toml" ]]; then
        info "Installing package from local..."
        $pip_cmd install -e "$REPO_ROOT" 2>/dev/null && {
            log "Package installed from local source"
        } || {
            warn "Local install failed, trying from GitHub..."
            $pip_cmd install "git+${REPO_URL}" 2>/dev/null && {
                log "Package installed from GitHub"
            } || {
                warn "Package install failed. Try: ${pip_cmd} install git+${REPO_URL}"
            }
        }
    else
        $pip_cmd install "git+${REPO_URL}" 2>/dev/null && {
            log "Package installed from GitHub"
        } || {
            warn "Package install failed. Try: ${pip_cmd} install git+${REPO_URL}"
        }
    fi

    # Verify
    if command -v ig-downloader &>/dev/null; then
        ver="$($pip_cmd show ig-downloader-skill 2>/dev/null | grep Version || echo 'ok')"
        log "CLI available: ig-downloader (${ver})"
    else
        warn "CLI 'ig-downloader' not in PATH after install."
        warn "Try: python -m instagram_downloader --help"
    fi
}

# ─── Step 2: Install agent skill files ─────────────────────────
install_agent_skill() {
    local agent="$1"
    local scope="$2"
    local base_dir=""

    if [[ -n "$CUSTOM_DIR" ]]; then
        base_dir="$CUSTOM_DIR"
    elif [[ "$scope" == "project" ]]; then
        base_dir="$(pwd)/.${agent}"
    else
        case "$agent" in
            opencode) base_dir="${HOME}/.config/opencode" ;;
            claude)   base_dir="${HOME}/.claude" ;;
            codex)    base_dir="${HOME}/.codex" ;;
            cursor)   base_dir="${HOME}/.cursor" ;;
            agents)   base_dir="${HOME}/.agents" ;;
            *) warn "Unknown agent: ${agent}"; return 1 ;;
        esac
    fi

    local skill_dir="${base_dir}/skills/${SKILL_NAME}"
    mkdir -p "$skill_dir"

    # Copy skill files
    local copied=0
    for f in SKILL.md AGENTS.md README.md; do
        if [[ -f "$REPO_ROOT/$f" ]]; then
            cp "$REPO_ROOT/$f" "$skill_dir/$f" 2>/dev/null && ((copied++))
        fi
    done

    if [[ $copied -gt 0 ]]; then
        log "Installed ${copied} file(s) → ${skill_dir}"
    else
        warn "No skill files found at ${REPO_ROOT}"
        return 1
    fi
}

detect_agents() {
    local detected=()
    command -v opencode &>/dev/null && detected+=("opencode")
    command -v claude   &>/dev/null && detected+=("claude")
    command -v codex    &>/dev/null && detected+=("codex")
    command -v cursor   &>/dev/null && detected+=("cursor")
    # Always install .agents/ for forward-compat
    detected+=("agents")
    echo "${detected[@]}"
}

install_agent_skills() {
    header "Step 2: Installing Agent Skills"

    local agents=()
    case "$TARGET_AGENT" in
        auto)
            IFS=' ' read -ra agents <<< "$(detect_agents)"
            if [[ ${#agents[@]} -eq 0 ]] || [[ ${#agents[@]} -eq 1 && "${agents[0]}" == "agents" ]]; then
                warn "No AI agent detected. Installing for all supported agents."
                agents=(opencode claude codex cursor agents)
            else
                info "Detected agents: ${agents[*]}"
            fi
            ;;
        all)  agents=(opencode claude codex cursor agents) ;;
        opencode|claude|codex|cursor) agents=("$TARGET_AGENT" agents) ;;
        *)    error "Unknown agent: ${TARGET_AGENT}. Supported: auto, all, opencode, claude, codex, cursor" ;;
    esac

    local success=0
    for agent in "${agents[@]}"; do
        install_agent_skill "$agent" "$INSTALL_SCOPE" && ((success++))
    done

    echo
    log "Skills installed for ${success}/${#agents[@]} agent(s)"
}

# ─── Step 3: Verify ─────────────────────────────────────────────
verify_installation() {
    header "Step 3: Verification"

    local ok=0; local total=0

    # Check SKILL.md
    ((total++))
    local skill_paths=()
    if [[ -n "$CUSTOM_DIR" ]]; then
        skill_paths+=("$CUSTOM_DIR/skills/${SKILL_NAME}/SKILL.md")
    elif [[ "$INSTALL_SCOPE" == "project" ]]; then
        skill_paths+=("$(pwd)/.opencode/skills/${SKILL_NAME}/SKILL.md")
        skill_paths+=("$(pwd)/.claude/skills/${SKILL_NAME}/SKILL.md")
    else
        skill_paths+=("${HOME}/.config/opencode/skills/${SKILL_NAME}/SKILL.md")
        skill_paths+=("${HOME}/.claude/skills/${SKILL_NAME}/SKILL.md")
        skill_paths+=("${HOME}/.codex/skills/${SKILL_NAME}/SKILL.md")
        skill_paths+=("${HOME}/.cursor/skills/${SKILL_NAME}/SKILL.md")
        skill_paths+=("${HOME}/.agents/skills/${SKILL_NAME}/SKILL.md")
    fi

    for p in "${skill_paths[@]}"; do
        if [[ -f "$p" ]]; then
            log "SKILL.md found: ${p}"
            ((ok++))
        fi
    done

    # Check CLI
    ((total++))
    if command -v ig-downloader &>/dev/null; then
        log "CLI 'ig-downloader' available"
        ((ok++))
    else
        warn "CLI 'ig-downloader' not in PATH. Try: python -m instagram_downloader --help"
    fi

    echo
    if [[ $ok -gt 0 ]]; then
        log "${ok}/${total} checks passed"
    else
        warn "No checks passed — something went wrong"
    fi
}

# ─── Post-install instructions ──────────────────────────────────
show_instructions() {
    header "Installation Complete 🎉"

    cat <<EOF
${BOLD}Instagram Downloader Skill v${SKILL_VERSION}${NC} is ready.

${BOLD}Quick start:${NC}
  1. Set up Instagram access:
     ig-downloader --setup

  2. Download a profile:
     ig-downloader -u username -o ./downloads

${BOLD}Learn more:${NC}
  ig-downloader --help
  https://github.com/${REPO}

${BOLD}Skill auto-discovery:${NC}
  The SKILL.md has been placed in your agent's skills directory.
  Your AI agent will discover it automatically in new sessions.

  To use the skill, ask your agent:
  "Download instagram posts from username"
EOF
    line
}

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
main() {
    install_python_package
    install_agent_skills
    verify_installation
    show_instructions
}

main
