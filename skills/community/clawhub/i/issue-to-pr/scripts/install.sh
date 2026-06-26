#!/usr/bin/env bash

# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called: https://github.com (git clone only)
#   Local files read: SKILL.md, scripts/*
#   Local files written: ~/.qoder/skills/issue-to-pr/

set -o errexit -o nounset -o pipefail

# ============================================================
# issue-to-pr Skill — Installer / Uninstaller
# ============================================================

SKILL_NAME="issue-to-pr"
INSTALL_DIR="${HOME}/.qoder/skills/${SKILL_NAME}"
SKILL_FILE="SKILL.md"

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()    { printf "${BLUE}[INFO]${NC}  %s\n" "$*"; }
success() { printf "${GREEN}[OK]${NC}    %s\n" "$*"; }
warn()    { printf "${YELLOW}[WARN]${NC}  %s\n" "$*"; }
error()   { printf "${RED}[ERROR]${NC} %s\n" "$*" >&2; }

# ------------------------------------------------------------
# Resolve the directory where this script lives
# ------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ------------------------------------------------------------
# Uninstall
# ------------------------------------------------------------
uninstall() {
    info "Uninstalling ${SKILL_NAME}..."

    if [ -d "${INSTALL_DIR}" ]; then
        rm -rf "${INSTALL_DIR}"
        success "Removed ${INSTALL_DIR}"
    else
        warn "Nothing to uninstall — ${INSTALL_DIR} does not exist."
    fi

    success "Uninstall complete."
    exit 0
}

# ------------------------------------------------------------
# Install
# ------------------------------------------------------------
install() {
    info "Installing ${SKILL_NAME}..."

    # Check dependencies
    if ! command -v git &>/dev/null; then
        error "git is not installed. Please install git first."
        exit 1
    fi

    if command -v gh &>/dev/null; then
        info "GitHub CLI (gh) detected — full functionality available."
    else
        warn "GitHub CLI (gh) not found. The skill will use fallback methods."
        warn "For the best experience, install gh: https://cli.github.com"
    fi

    # Verify source file exists
    if [ ! -f "${REPO_ROOT}/${SKILL_FILE}" ]; then
        error "Cannot find ${SKILL_FILE} in ${REPO_ROOT}."
        error "Please run this script from the repository root or the scripts/ directory."
        exit 1
    fi

    # Create target directory
    mkdir -p "${INSTALL_DIR}"
    info "Target directory: ${INSTALL_DIR}"

    # Copy skill file
    cp "${REPO_ROOT}/${SKILL_FILE}" "${INSTALL_DIR}/${SKILL_FILE}"
    success "Copied ${SKILL_FILE} to ${INSTALL_DIR}/"

    # Verify installation
    if [ -f "${INSTALL_DIR}/${SKILL_FILE}" ]; then
        success "Installation complete!"
        echo ""
        info "The skill is now available at: ${INSTALL_DIR}/${SKILL_FILE}"
        info "You can use it in Qoder, Cursor, or Claude Code by typing:"
        echo ""
        echo "    /fix-issue https://github.com/owner/repo/issues/123"
        echo ""
    else
        error "Installation verification failed. Please try manual installation."
        exit 1
    fi
}

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
case "${1:-}" in
    --uninstall | -u)
        uninstall
        ;;
    --help | -h)
        echo "Usage: $(basename "$0") [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  (none)          Install the ${SKILL_NAME} skill"
        echo "  --uninstall, -u Remove the ${SKILL_NAME} skill"
        echo "  --help, -h      Show this help message"
        ;;
    *)
        install
        ;;
esac
