#!/usr/bin/env bash
# LicenseGuard -- Main CLI entry point
# Usage: licenseguard.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot license compliance scan (FREE)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove LicenseGuard hooks (PRO+)
#   report [dir]              Generate compliance report (PRO+)
#   matrix [dir]              License compatibility matrix (PRO+)
#   policy [dir]              Enforce approved license list (TEAM+)
#   sbom [dir]                Generate SBOM (TEAM+)
#   status                    Show license and config info

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[LicenseGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[LicenseGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[LicenseGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[LicenseGuard]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}LicenseGuard${NC} v${VERSION}"
  echo "  Open source license compliance scanner"
  echo "  https://licenseguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  licenseguard <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} License compliance scan (5 file limit)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  scan [file|dir]           ${DIM}[PRO]${NC}  Unlimited scanning"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove LicenseGuard hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}  Full compliance report"
  echo -e "  matrix [dir]              ${DIM}[PRO]${NC}  License compatibility matrix"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  policy [dir]              ${DIM}[TEAM]${NC} Enforce approved license list"
  echo -e "  sbom [dir]                ${DIM}[TEAM]${NC} Generate SBOM"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://licenseguard.pages.dev${NC}"
}

# --- License ----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_licenseguard_license "$required_tier"
}

# --- Check tier without failing (for free-tier gating) ----------------------

get_current_tier() {
  source "$SCRIPT_DIR/license.sh"
  get_licenseguard_tier
}

# --- Hooks management -------------------------------------------------------

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    return 1
  fi

  if ! git rev-parse --git-dir &>/dev/null 2>&1; then
    log_error "Not inside a git repository."
    return 1
  fi

  local repo_root
  repo_root=$(git rev-parse --show-toplevel)

  log_info "Installing hooks in ${BOLD}$repo_root${NC}"

  local config="$repo_root/lefthook.yml"

  if [[ -f "$config" ]]; then
    if grep -q "licenseguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- LicenseGuard hooks ------------------------------------
    licenseguard-license-scan:
      run: |
        LICENSEGUARD_SKILL_DIR="${LICENSEGUARD_SKILL_DIR:-$HOME/.openclaw/skills/licenseguard}"
        if [[ -f "$LICENSEGUARD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$LICENSEGUARD_SKILL_DIR/scripts/analyzer.sh"
          hook_license_scan
        else
          echo "[LicenseGuard] Skill not found at $LICENSEGUARD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Copyleft or problematic licenses detected in staged dependency files!
        Run 'licenseguard scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended LicenseGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Dependency manifests will be scanned for license issues on every commit."
}

do_hooks_uninstall() {
  if ! git rev-parse --git-dir &>/dev/null 2>&1; then
    log_error "Not inside a git repository."
    return 1
  fi

  local repo_root
  repo_root=$(git rev-parse --show-toplevel)
  local config="$repo_root/lefthook.yml"

  if [[ -f "$config" ]]; then
    if grep -q "licenseguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- LicenseGuard hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "licenseguard" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed LicenseGuard hooks"
    else
      log_warn "No LicenseGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Command dispatch -------------------------------------------------------

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for license issues in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/analyzer.sh"
      do_license_scan "$target"
      ;;

    hooks)
      require_license "pro"
      local subcmd="${1:-}"
      case "$subcmd" in
        install)
          do_hooks_install
          ;;
        uninstall)
          do_hooks_uninstall
          ;;
        *)
          log_error "Unknown hooks subcommand: $subcmd"
          echo "  Usage: licenseguard hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      local target="${1:-.}"
      log_info "Generating compliance report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_report "$target"
      ;;

    matrix)
      require_license "pro"
      local target="${1:-.}"
      log_info "Generating license compatibility matrix for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_matrix "$target"
      ;;

    policy)
      require_license "team"
      local target="${1:-.}"
      log_info "Running policy enforcement in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/analyzer.sh"
      enforce_policy "$target"
      ;;

    sbom)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating SBOM for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_sbom "$target"
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_licenseguard_status
      ;;

    --help|-h|help)
      show_help
      ;;

    --version|-v)
      show_version
      ;;

    "")
      show_help
      exit 1
      ;;

    *)
      log_error "Unknown command: $cmd"
      echo ""
      show_help
      exit 1
      ;;
  esac
}

main "$@"
