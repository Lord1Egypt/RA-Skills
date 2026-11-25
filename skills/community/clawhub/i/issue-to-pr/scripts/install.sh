#!/usr/bin/env bash

# SECURITY MANIFEST:
#   Environment variables accessed: ISSUE_TO_PR_SKILLS_DIR (optional), CLAUDE_CONFIG_DIR (optional)
#   External endpoints called: none
#   Local files read: SKILL.md, references/*, this script
#   Local files written: <skills dir>/issue-to-pr/{SKILL.md,references/*}

set -o errexit -o nounset -o pipefail

SKILL_NAME="issue-to-pr"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

info() { printf '[INFO]  %s\n' "$*"; }
success() { printf '[OK]    %s\n' "$*"; }
warn() { printf '[WARN]  %s\n' "$*"; }
error() { printf '[ERROR] %s\n' "$*" >&2; }

usage() {
  cat <<'EOF'
Usage: bash scripts/install.sh [OPTIONS]

Installs the issue-to-pr skill into a harness-specific skills directory.

Options:
  --target <dir>   Install into <dir>/issue-to-pr (highest priority)
  --project        Install into ./.claude/skills/issue-to-pr for this repository
  --list-targets   Print the directories this installer can detect
  --force          Overwrite an existing installation
  --uninstall      Remove <target>/issue-to-pr
  -h, --help       Show this help

Environment:
  ISSUE_TO_PR_SKILLS_DIR   Default parent directory for all targets
  CLAUDE_CONFIG_DIR        Used instead of ~/.claude when set

Detection order:
  1. --target
  2. ISSUE_TO_PR_SKILLS_DIR
  3. --project (./.claude/skills)
  4. ~/.claude/skills        (Claude Code and compatible harnesses)
  5. ~/.qoder/skills         (Qoder)
  6. ~/.config/agent/skills  (generic fallback)
EOF
}

detect_target() {
  if [ -n "${TARGET_OVERRIDE}" ]; then
    printf '%s\n' "${TARGET_OVERRIDE}"
    return 0
  fi
  if [ -n "${ISSUE_TO_PR_SKILLS_DIR:-}" ]; then
    printf '%s\n' "${ISSUE_TO_PR_SKILLS_DIR}"
    return 0
  fi
  if [ "${PROJECT_INSTALL}" = "true" ]; then
    printf '%s\n' "$(pwd)/.claude/skills"
    return 0
  fi
  if [ -n "${CLAUDE_CONFIG_DIR:-}" ] && [ -d "${CLAUDE_CONFIG_DIR}" ]; then
    printf '%s\n' "${CLAUDE_CONFIG_DIR}/skills"
    return 0
  fi
  if [ -d "${HOME}/.claude" ]; then
    printf '%s\n' "${HOME}/.claude/skills"
    return 0
  fi
  if [ -d "${HOME}/.qoder" ]; then
    printf '%s\n' "${HOME}/.qoder/skills"
    return 0
  fi
  printf '%s\n' "${HOME}/.config/agent/skills"
}

list_targets() {
  if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then
    printf 'claude (env): %s/skills\n' "${CLAUDE_CONFIG_DIR}"
  fi
  if [ -d "${HOME}/.claude" ]; then
    printf 'claude:      %s/skills\n' "${HOME}/.claude"
  fi
  if [ -d "${HOME}/.qoder" ]; then
    printf 'qoder:       %s/skills\n' "${HOME}/.qoder"
  fi
  printf 'generic:     %s/skills\n' "${HOME}/.config/agent"
}

install_skill() {
  local target_dir="$1"
  local destination="${target_dir}/${SKILL_NAME}"

  if [ ! -f "${REPO_ROOT}/SKILL.md" ]; then
    error "SKILL.md not found in ${REPO_ROOT}. Run this script from the repository."
    exit 1
  fi

  if [ -d "${destination}" ] && [ "${FORCE}" != "true" ]; then
    warn "${destination} already exists; use --force to overwrite."
    exit 0
  fi

  install -d "${destination}"
  cp "${REPO_ROOT}/SKILL.md" "${destination}/SKILL.md"

  if [ -d "${REPO_ROOT}/references" ]; then
    install -d "${destination}/references"
    cp -R "${REPO_ROOT}/references/." "${destination}/references/"
  fi

  success "Installed to ${destination}"
  info "Use it as: /fix-issue https://github.com/<owner>/<repo>/issues/<number>"
  info "Optional flags: --dry-run, --draft, --no-push, --non-interactive"
  if command -v gh >/dev/null 2>&1; then
    info "gh detected. If git push asks for credentials, run: gh auth setup-git"
  else
    warn "gh not found; the skill falls back to git plus the REST API with GH_TOKEN."
  fi
}

uninstall_skill() {
  local target_dir="$1"
  local destination="${target_dir}/${SKILL_NAME}"

  case "${destination}" in
    */"${SKILL_NAME}")
      if [ -d "${destination}" ]; then
        rm -rf "${destination}"
        success "Removed ${destination}"
      else
        warn "Nothing to remove at ${destination}"
      fi
      ;;
    *)
      error "Refusing to remove unexpected path: ${destination}"
      exit 1
      ;;
  esac
}

TARGET_OVERRIDE=""
PROJECT_INSTALL="false"
FORCE="false"
MODE="install"

while [ $# -gt 0 ]; do
  case "$1" in
    --target)
      [ $# -ge 2 ] || { error "--target requires a directory"; exit 1; }
      TARGET_OVERRIDE="$2"
      shift 2
      ;;
    --project)
      PROJECT_INSTALL="true"
      shift
      ;;
    --list-targets)
      list_targets
      exit 0
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    --uninstall)
      MODE="uninstall"
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      error "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

TARGET_DIR="$(detect_target)"
info "Target: ${TARGET_DIR}"

if [ "${MODE}" = "uninstall" ]; then
  uninstall_skill "${TARGET_DIR}"
else
  install_skill "${TARGET_DIR}"
fi
