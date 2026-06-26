#!/usr/bin/env bash
# PerfGuard -- Main CLI entry point
# Usage: perfguard.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot performance scan (FREE: 5 files / PRO+: unlimited)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove PerfGuard hooks (PRO+)
#   report [dir]              Generate performance audit report (PRO+)
#   hotspots [dir]            Identify performance hot paths (PRO+)
#   budget [dir]              Check against performance budgets (TEAM+)
#   trend [dir]               Performance trend over git history (TEAM+)
#   status                    Show license and config info
#   help / --help / -h        Show this help
#   version / --version / -v  Show version

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# ─── Colors ──────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[PerfGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[PerfGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[PerfGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[PerfGuard]${NC} $*" >&2; }

# ─── Version / Help ─────────────────────────────────────────────────────────

show_version() {
  echo -e "${BOLD}PerfGuard${NC} v${VERSION}"
  echo "  Performance Anti-Pattern Scanner"
  echo "  https://perfguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  perfguard <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC}  Performance scan (up to 5 files)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  scan [file|dir]           ${DIM}[PRO]${NC}   Unlimited scanning + full checks"
  echo -e "  hooks install             ${DIM}[PRO]${NC}   Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}   Remove PerfGuard hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}   Generate performance audit report"
  echo -e "  hotspots [dir]            ${DIM}[PRO]${NC}   Identify performance hot paths"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  budget [dir]              ${DIM}[TEAM]${NC}  Check against performance budgets"
  echo -e "  trend [dir]               ${DIM}[TEAM]${NC}  Performance trend over git history"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  --help, -h, help          Show this help"
  echo "  --version, -v, version    Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://perfguard.pages.dev${NC}"
}

# ─── License ─────────────────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_perfguard_license "$required_tier"
}

get_current_tier() {
  source "$SCRIPT_DIR/license.sh"
  get_perfguard_tier
}

# ─── Hooks management ────────────────────────────────────────────────────────

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    echo "  Or:      npm install -g @arkweid/lefthook"
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
    if grep -q "perfguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- PerfGuard hooks ------------------------------------------
    perfguard-perf-scan:
      glob: "*.{js,ts,jsx,tsx,py,rb,java}"
      run: |
        PERFGUARD_SKILL_DIR="${PERFGUARD_SKILL_DIR:-$HOME/.openclaw/skills/perfguard}"
        if [[ -f "$PERFGUARD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$PERFGUARD_SKILL_DIR/scripts/patterns.sh"
          source "$PERFGUARD_SKILL_DIR/scripts/analyzer.sh"
          hook_perf_scan
        else
          echo "[PerfGuard] Skill not found at $PERFGUARD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Performance anti-patterns detected in staged files!
        Run 'perfguard scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended PerfGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for performance anti-patterns on every commit."
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
    if grep -q "perfguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      # Remove the PerfGuard hook block
      awk '/# --- PerfGuard hooks/{skip=1} /^[[:space:]]*[a-zA-Z]/ && skip && !/perfguard/{skip=0} !skip' "$config" > "$tmp"
      mv "$tmp" "$config"
      echo -e "${GREEN}+${NC} Removed PerfGuard hooks"
    else
      log_warn "No PerfGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ─── Scan command ─────────────────────────────────────────────────────────────

do_scan() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  # Determine tier for file limits
  local tier="free"
  tier=$(get_current_tier 2>/dev/null) || tier="free"

  source "$SCRIPT_DIR/analyzer.sh"

  local max_files=5
  if [[ "$tier" == "pro" || "$tier" == "team" || "$tier" == "enterprise" ]]; then
    max_files=0  # 0 = unlimited
  fi

  log_info "Scanning for performance anti-patterns in ${BOLD}$target${NC}"
  do_perf_scan "$target" "$max_files"
}

# ─── Report command ──────────────────────────────────────────────────────────

do_report() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Generating performance audit report for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/analyzer.sh"
  generate_report "$target"
}

# ─── Hotspots command ───────────────────────────────────────────────────────

do_hotspots() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Identifying performance hotspots in ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/analyzer.sh"
  find_hotspots "$target"
}

# ─── Budget command ─────────────────────────────────────────────────────────

do_budget() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Checking performance budgets for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/analyzer.sh"
  check_budget "$target"
}

# ─── Trend command ──────────────────────────────────────────────────────────

do_trend() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  log_info "Analyzing performance trend for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/analyzer.sh"
  show_trend "$target"
}

# ─── Status command ──────────────────────────────────────────────────────────

do_status() {
  show_version
  echo ""
  source "$SCRIPT_DIR/license.sh"
  show_perfguard_status
}

# ─── Command dispatch ────────────────────────────────────────────────────────

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      do_scan "${1:-.}"
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
          echo "  Usage: perfguard hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      require_license "pro"
      do_report "${1:-.}"
      ;;

    hotspots)
      require_license "pro"
      do_hotspots "${1:-.}"
      ;;

    budget)
      require_license "team"
      do_budget "${1:-.}"
      ;;

    trend)
      require_license "team"
      do_trend "${1:-.}"
      ;;

    status)
      do_status
      ;;

    --help|-h|help)
      show_help
      ;;

    --version|-v|version)
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
