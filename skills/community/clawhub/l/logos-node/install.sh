#!/usr/bin/env bash
# install.sh — Logos Node skill installer (no npm required)
# Usage: curl -fsSL https://raw.githubusercontent.com/citizenweb3/ai-integrations/logos-node/install.sh | bash
set -euo pipefail

REPO="citizenweb3/ai-integrations"
BRANCH="logos-node"
SKILL_NAME="logos-node"
TARBALL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.tar.gz"
TMP_DIR="$(mktemp -d)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[logos-node]${NC} $*"; }
warn()  { echo -e "${YELLOW}[logos-node]${NC} $*"; }

# Parse --global flag
GLOBAL=false
for arg in "$@"; do
  [[ "$arg" == "--global" || "$arg" == "-g" ]] && GLOBAL=true
done

info "Downloading skill from ${REPO}@${BRANCH}..."
curl -fsSL "$TARBALL" | tar -xz -C "$TMP_DIR" --strip-components=1
SKILL_SRC="${TMP_DIR}/skill"

# Agent detection
declare -A AGENTS
declare -A INSTALL_PATHS

detect_agents() {
  # Claude Code
  if [[ -d "${HOME}/.claude" || -d ".claude" ]]; then
    if $GLOBAL; then
      AGENTS[claude]="Claude Code"
      INSTALL_PATHS[claude]="${HOME}/.claude/skills/${SKILL_NAME}"
    else
      AGENTS[claude]="Claude Code"
      INSTALL_PATHS[claude]="${PWD}/.claude/skills/${SKILL_NAME}"
    fi
  fi

  # GitHub Copilot
  if [[ -d ".github/copilot" ]] || git remote -v 2>/dev/null | grep -q "github.com"; then
    if $GLOBAL; then
      AGENTS[copilot]="GitHub Copilot"
      INSTALL_PATHS[copilot]="${HOME}/.agents/skills/${SKILL_NAME}"
    else
      AGENTS[copilot]="GitHub Copilot"
      INSTALL_PATHS[copilot]="${PWD}/.agents/skills/${SKILL_NAME}"
    fi
  fi

  # Gemini CLI
  if [[ -d ".gemini" || -d "${HOME}/.gemini" || -n "${GEMINI_API_KEY:-}" ]]; then
    if $GLOBAL; then
      AGENTS[gemini]="Gemini CLI"
      INSTALL_PATHS[gemini]="${HOME}/.gemini/skills/${SKILL_NAME}"
    else
      AGENTS[gemini]="Gemini CLI"
      INSTALL_PATHS[gemini]="${PWD}/.gemini/skills/${SKILL_NAME}"
    fi
  fi

  # OpenAI Codex CLI
  if [[ -n "${OPENAI_API_KEY:-}" || -d ".codex" ]]; then
    if $GLOBAL; then
      AGENTS[codex]="OpenAI Codex CLI"
      INSTALL_PATHS[codex]="${HOME}/.agents/skills/${SKILL_NAME}"
    else
      AGENTS[codex]="OpenAI Codex CLI"
      INSTALL_PATHS[codex]="${PWD}/.agents/skills/${SKILL_NAME}"
    fi
  fi

  # opencode
  if [[ -d ".opencode" || -f "opencode.json" ]] || command -v opencode &>/dev/null; then
    if $GLOBAL; then
      AGENTS[opencode]="opencode"
      INSTALL_PATHS[opencode]="${HOME}/.config/opencode/skills/${SKILL_NAME}"
    else
      AGENTS[opencode]="opencode"
      INSTALL_PATHS[opencode]="${PWD}/.opencode/skills/${SKILL_NAME}"
    fi
  fi

  # OpenClaw (always global — personal assistant)
  if [[ -d "${HOME}/.openclaw" || -f "openclaw.json" ]] || command -v openclaw &>/dev/null; then
    AGENTS[openclaw]="OpenClaw"
    INSTALL_PATHS[openclaw]="${HOME}/.openclaw/skills/${SKILL_NAME}"
  fi
}

install_skill() {
  local agent="$1"
  local path="${INSTALL_PATHS[$agent]}"
  info "Installing for ${AGENTS[$agent]} → ${path}"
  mkdir -p "$path"
  cp -r "${SKILL_SRC}/." "$path/"
  info "✅ Done: ${path}"
}

detect_agents

if [[ ${#AGENTS[@]} -eq 0 ]]; then
  warn "No supported AI agents detected. Installing to ~/.agents/skills/${SKILL_NAME}"
  DEFAULT_PATH="${HOME}/.agents/skills/${SKILL_NAME}"
  mkdir -p "$DEFAULT_PATH"
  cp -r "${SKILL_SRC}/." "$DEFAULT_PATH/"
  info "✅ Installed to ${DEFAULT_PATH}"
else
  echo ""
  info "Detected agents:"
  for agent in "${!AGENTS[@]}"; do
    echo "  • ${AGENTS[$agent]} → ${INSTALL_PATHS[$agent]}"
  done
  echo ""

  for agent in "${!AGENTS[@]}"; do
    read -r -p "Install for ${AGENTS[$agent]}? [Y/n] " answer </dev/tty
    case "${answer,,}" in
      n|no) warn "Skipping ${AGENTS[$agent]}" ;;
      *)    install_skill "$agent" ;;
    esac
  done
fi

rm -rf "$TMP_DIR"

echo ""
info "Installation complete. To verify in your agent, run:"
echo "  /logos-node status"
echo ""
info "Available commands:"
echo "  /logos-node install   — fresh node setup"
echo "  /logos-node update    — breaking upgrade (wipe + re-init)"
echo "  /logos-node status    — check sync, peers, wallet balance"
