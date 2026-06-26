#!/usr/bin/env bash
# MemGuard -- Main CLI entry point
# Usage: memguard.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot resource leak scan (FREE, 5 file limit)
#   hook install              Install pre-commit hooks (FREE)
#   hook uninstall            Remove MemGuard hooks (FREE)
#   report [dir]              Generate resource health report (FREE)
#   watch [dir]               Continuous monitoring mode (PRO+)
#   ci [dir]                  CI/CD integration mode (PRO+)
#   team-report [dir]         Aggregate team metrics (TEAM+)
#   baseline [dir]            Establish resource issue baseline (TEAM+)
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

log_info()    { echo -e "${BLUE}[MemGuard]${NC} $*"; }
log_success() { echo -e "${GREEN}[MemGuard]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[MemGuard]${NC} $*"; }
log_error()   { echo -e "${RED}[MemGuard]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}MemGuard${NC} v${VERSION}"
  echo "  Memory leak & resource management scanner"
  echo "  https://memguard.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  memguard <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot resource leak scan (5 file limit)"
  echo -e "  hook install              ${DIM}[FREE]${NC} Install pre-commit hooks"
  echo -e "  hook uninstall            ${DIM}[FREE]${NC} Remove MemGuard hooks"
  echo -e "  report [dir]              ${DIM}[FREE]${NC} Generate resource health report"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  watch [dir]               ${DIM}[PRO]${NC}  Continuous monitoring mode"
  echo -e "  ci [dir]                  ${DIM}[PRO]${NC}  CI/CD integration mode"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  team-report [dir]         ${DIM}[TEAM]${NC} Aggregate team metrics"
  echo -e "  baseline [dir]            ${DIM}[TEAM]${NC} Establish resource issue baseline"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://memguard.pages.dev${NC}"
}

# --- License ----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_memguard_license "$required_tier"
}

# --- Hooks management -------------------------------------------------------

do_hooks_install() {
  if ! command -v lefthook &>/dev/null; then
    log_error "lefthook not installed."
    echo "  Install: brew install lefthook"
    echo "  Or: npm install -g lefthook"
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
    if grep -q "memguard" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- MemGuard hooks ----------------------------------------
    memguard-memory-scan:
      run: |
        MEMGUARD_SKILL_DIR="${MEMGUARD_SKILL_DIR:-$HOME/.openclaw/skills/memguard}"
        if [[ -f "$MEMGUARD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$MEMGUARD_SKILL_DIR/scripts/patterns.sh"
          source "$MEMGUARD_SKILL_DIR/scripts/analyzer.sh"
          hook_memory_scan
        else
          echo "[MemGuard] Skill not found at $MEMGUARD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Memory leak risks detected in staged files!
        Run 'memguard scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended MemGuard hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for resource leaks on every commit."
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
    if grep -q "memguard" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- MemGuard hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "memguard" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed MemGuard hooks"
    else
      log_warn "No MemGuard hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Pattern listing --------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- MemGuard Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(memguard_pattern_count) patterns across 6 categories${NC}"
  echo ""

  local cat_types=("FH" "EL" "CR" "UC" "RC" "TM")
  local cat_labels=("File Handles" "Event Listeners" "Circular References" "Unbounded Caches" "React Cleanup" "Timers & Streams")

  for i in "${!cat_types[@]}"; do
    local ctype="${cat_types[$i]}"
    local clabel="${cat_labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    memguard_list_patterns "$ctype" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}

# --- Command dispatch -------------------------------------------------------

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for resource leaks in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      do_memguard_scan "$target" 5
      ;;

    hook|hooks)
      local subcmd="${1:-}"
      case "$subcmd" in
        install)
          do_hooks_install
          ;;
        uninstall)
          do_hooks_uninstall
          ;;
        *)
          log_error "Unknown hook subcommand: $subcmd"
          echo "  Usage: memguard hook [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      local target="${1:-.}"
      log_info "Generating resource health report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_memguard_report "$target"
      ;;

    watch)
      require_license "pro"
      local target="${1:-.}"
      log_info "Starting watch mode on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      watch_mode "$target"
      ;;

    ci)
      require_license "pro"
      local target="${1:-.}"
      log_info "Running CI mode on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      ci_mode "$target"
      ;;

    team-report)
      require_license "team"
      local target="${1:-.}"
      log_info "Generating team report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      team_report "$target"
      ;;

    baseline)
      require_license "team"
      local target="${1:-.}"
      log_info "Creating resource baseline for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      baseline_mode "$target"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_memguard_status
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
