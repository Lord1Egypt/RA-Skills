#!/usr/bin/env bash
# I18nCheck -- Main CLI entry point
# Usage: i18ncheck.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot i18n scan (FREE, 5 file limit)
#   hook install              Install pre-commit hooks (FREE)
#   hook uninstall            Remove I18nCheck hooks (FREE)
#   report [dir]              Generate i18n readiness report (FREE)
#   watch [dir]               Continuous monitoring (PRO+)
#   ci [dir]                  CI integration with exit codes (PRO+)
#   team-report [dir]         Aggregate team i18n metrics (TEAM+)
#   baseline [dir]            Baseline known i18n issues (TEAM+)
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

log_info()    { echo -e "${BLUE}[I18nCheck]${NC} $*"; }
log_success() { echo -e "${GREEN}[I18nCheck]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[I18nCheck]${NC} $*"; }
log_error()   { echo -e "${RED}[I18nCheck]${NC} $*" >&2; }

show_version() {
  echo -e "${BOLD}I18nCheck${NC} v${VERSION}"
  echo "  Internationalization & localization readiness scanner"
  echo "  https://i18ncheck.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  i18ncheck <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} One-shot i18n scan (5 file limit)"
  echo -e "  hook install              ${DIM}[FREE]${NC} Install pre-commit hooks"
  echo -e "  hook uninstall            ${DIM}[FREE]${NC} Remove I18nCheck hooks"
  echo -e "  report [dir]              ${DIM}[FREE]${NC} Generate i18n readiness report"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  watch [dir]               ${DIM}[PRO]${NC}  Continuous monitoring"
  echo -e "  ci [dir]                  ${DIM}[PRO]${NC}  CI integration with exit codes"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  team-report [dir]         ${DIM}[TEAM]${NC} Aggregate team i18n metrics"
  echo -e "  baseline [dir]            ${DIM}[TEAM]${NC} Baseline known i18n issues"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  patterns                  List all detection patterns"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "Get a license at ${CYAN}https://i18ncheck.pages.dev${NC}"
}

# --- License ----------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_i18ncheck_license "$required_tier"
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
    if grep -q "i18ncheck" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- I18nCheck hooks ----------------------------------------
    i18ncheck-i18n-scan:
      run: |
        I18NCHECK_SKILL_DIR="${I18NCHECK_SKILL_DIR:-$HOME/.openclaw/skills/i18ncheck}"
        if [[ -f "$I18NCHECK_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$I18NCHECK_SKILL_DIR/scripts/patterns.sh"
          source "$I18NCHECK_SKILL_DIR/scripts/analyzer.sh"
          hook_i18n_scan
        else
          echo "[I18nCheck] Skill not found at $I18NCHECK_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Internationalization issues detected in staged files!
        Run 'i18ncheck scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended I18nCheck hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned for i18n issues on every commit."
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
    if grep -q "i18ncheck" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- I18nCheck hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "i18ncheck" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed I18nCheck hooks"
    else
      log_warn "No I18nCheck hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# --- Pattern listing --------------------------------------------------------

do_list_patterns() {
  source "$SCRIPT_DIR/patterns.sh"

  echo -e "${BOLD}--- I18nCheck Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(i18ncheck_pattern_count) patterns across 6 categories${NC}"
  echo ""

  local cat_types=("HS" "TK" "DF" "RL" "SC" "EN")
  local cat_labels=("Hardcoded Strings" "Translation Keys" "Date & Number Formatting" "RTL & Layout" "String Concatenation" "Encoding & Locale")

  for i in "${!cat_types[@]}"; do
    local ctype="${cat_types[$i]}"
    local clabel="${cat_labels[$i]}"
    echo -e "${CYAN}${BOLD}$clabel:${NC}"
    i18ncheck_list_patterns "$ctype" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}

# --- Team report (TEAM) -----------------------------------------------------

do_team_report() {
  local target="${1:-.}"
  log_info "Generating team i18n report for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"
  team_report "$target"
}

# --- Baseline management (TEAM) --------------------------------------------

do_baseline() {
  local target="${1:-.}"
  log_info "Creating i18n baseline for ${BOLD}$target${NC}"
  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"
  baseline_mode "$target"
}

# --- Command dispatch -------------------------------------------------------

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    scan)
      local target="${1:-.}"
      log_info "Scanning for i18n issues in ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      do_i18ncheck_scan "$target" 5
      ;;

    hook)
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
          echo "  Usage: i18ncheck hook [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    report)
      local target="${1:-.}"
      log_info "Generating i18n readiness report for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      generate_report "$target"
      ;;

    watch)
      require_license "pro"
      local target="${1:-.}"
      log_info "Starting watch mode for ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      watch_mode "$target"
      ;;

    ci)
      require_license "pro"
      local target="${1:-.}"
      log_info "Running CI mode scan on ${BOLD}$target${NC}"
      source "$SCRIPT_DIR/patterns.sh"
      source "$SCRIPT_DIR/analyzer.sh"
      ci_mode "$target"
      ;;

    team-report)
      require_license "team"
      do_team_report "${1:-.}"
      ;;

    baseline)
      require_license "team"
      do_baseline "${1:-.}"
      ;;

    patterns)
      do_list_patterns
      ;;

    status)
      show_version
      echo ""
      source "$SCRIPT_DIR/license.sh"
      show_i18ncheck_status
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
