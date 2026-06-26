#!/usr/bin/env bash
# InputShield -- Main CLI Dispatcher (Entry Point)
#
# Usage:
#   dispatcher.sh [command] [options]
#
# Commands:
#   scan [file|dir]           One-shot input validation scan
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove InputShield hooks (PRO+)
#   report [dir]              Generate markdown report (PRO+)
#   audit [dir]               Deep audit with all patterns (TEAM+)
#   patterns                  List all detection patterns
#   status                    Show license and config info
#
# Options:
#   --path <path>             Target file or directory (default: .)
#   --format <fmt>            Output format: text, json, html (default: text)
#   --tier <tier>             Override tier: free, pro, team, enterprise
#   --license-key <key>       License key (or set INPUTSHIELD_LICENSE_KEY)
#   --verbose                 Enable verbose output
#   --category <cat>          Filter by category: IV, DS, RD, PT, CI, XS
#   --help, -h                Show help
#   --version, -v             Show version

set -euo pipefail

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

log_info()    { echo -e "${BLUE}[InputShield]${NC} $*"; }
log_success() { echo -e "${GREEN}[InputShield]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[InputShield]${NC} $*"; }
log_error()   { echo -e "${RED}[InputShield]${NC} $*" >&2; }

# ---------------------------------------------------------------------------
# Version & Help
# ---------------------------------------------------------------------------

show_version() {
  echo -e "${BOLD}InputShield${NC} v${VERSION}"
  echo "  Input validation & sanitization scanner"
  echo "  https://inputshield.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  inputshield <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC} Input validation scan (30 patterns)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  hooks install             ${DIM}[PRO]${NC}  Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}  Remove InputShield hooks"
  echo -e "  report [dir]              ${DIM}[PRO]${NC}  Generate input validation report"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  audit [dir]               ${DIM}[TEAM]${NC} Deep audit (all 90 patterns)"
  echo ""
  echo -e "${BOLD}OPTIONS${NC}"
  echo "  --path <path>             Target file or directory (default: .)"
  echo "  --format <fmt>            Output format: text, json, html (default: text)"
  echo "  --tier <tier>             Override tier: free, pro, team, enterprise"
  echo "  --license-key <key>       License key (overrides env var)"
  echo "  --category <cat>          Filter: IV, DS, RD, PT, CI, XS"
  echo "  --verbose                 Enable verbose output"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  patterns                  List all detection patterns"
  echo "  status                    Show license and config info"
  echo "  --help, -h                Show this help"
  echo "  --version, -v             Show version"
  echo ""
  echo -e "${BOLD}CATEGORIES${NC}"
  echo "  IV  Input Validation       Missing length checks, type validation, allowlists"
  echo "  DS  Deserialization        Unsafe JSON.parse, pickle.loads, yaml.load, etc."
  echo "  RD  ReDoS                  Catastrophic backtracking, nested quantifiers"
  echo "  PT  Path Traversal         ../ injection, unsanitized file paths"
  echo "  CI  Command Injection      Shell exec, eval, subprocess, template injection"
  echo "  XS  XSS / Output          innerHTML, dangerouslySetInnerHTML, document.write"
  echo ""
  echo -e "Get a license at ${CYAN}https://inputshield.pages.dev${NC}"
}

# ---------------------------------------------------------------------------
# License Integration
# ---------------------------------------------------------------------------

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_inputshield_license "$required_tier"
}

# Resolve the effective tier from CLI args, env, or license key.
# Returns the tier string on stdout.
resolve_tier() {
  local cli_tier="${1:-}"
  local cli_key="${2:-}"

  # If a key was provided on CLI, set it as env var for license.sh
  if [[ -n "$cli_key" ]]; then
    export INPUTSHIELD_LICENSE_KEY="$cli_key"
  fi

  # If tier was explicitly set on CLI, use that (trust the user for local runs)
  if [[ -n "$cli_tier" ]]; then
    echo "$cli_tier"
    return 0
  fi

  # Otherwise detect from license
  source "$SCRIPT_DIR/license.sh"
  get_inputshield_tier
}

# ---------------------------------------------------------------------------
# Hooks Management (Pro+)
# ---------------------------------------------------------------------------

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
    if grep -q "inputshield" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- InputShield hooks ----------------------------------------
    inputshield-check:
      run: |
        INPUTSHIELD_SKILL_DIR="${INPUTSHIELD_SKILL_DIR:-$HOME/.openclaw/skills/inputshield}"
        if [[ -f "$INPUTSHIELD_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$INPUTSHIELD_SKILL_DIR/scripts/patterns.sh"
          source "$INPUTSHIELD_SKILL_DIR/scripts/license.sh"
          source "$INPUTSHIELD_SKILL_DIR/scripts/analyzer.sh"
          hook_inputshield_check
        else
          echo "[InputShield] Skill not found at $INPUTSHIELD_SKILL_DIR -- skipping scan"
        fi
      fail_text: |
        Input validation issues detected in staged files!
        Run 'inputshield scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended InputShield hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged files will be scanned on every commit."
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
    if grep -q "inputshield" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      sed '/# --- InputShield hooks/,/fail_text:.*$/d' "$config" > "$tmp"
      grep -v "inputshield" "$tmp" > "$config" 2>/dev/null || mv "$tmp" "$config"
      rm -f "$tmp"
      echo -e "${GREEN}+${NC} Removed InputShield hooks"
    else
      log_warn "No InputShield hooks found"
    fi
  else
    log_warn "No lefthook.yml found"
  fi
}

# ---------------------------------------------------------------------------
# Validate Category Argument
# ---------------------------------------------------------------------------

validate_category() {
  local cat="$1"
  case "$cat" in
    IV|DS|RD|PT|CI|XS) return 0 ;;
    *)
      log_error "Invalid category: $cat"
      echo "  Valid categories: IV, DS, RD, PT, CI, XS"
      echo ""
      echo "  IV  Input Validation"
      echo "  DS  Deserialization"
      echo "  RD  ReDoS"
      echo "  PT  Path Traversal"
      echo "  CI  Command Injection"
      echo "  XS  XSS / Output"
      return 1
      ;;
  esac
}

# ---------------------------------------------------------------------------
# CLI Argument Parsing
# ---------------------------------------------------------------------------

main() {
  local cmd=""
  local target="."
  local format="text"
  local tier_override=""
  local license_key_cli=""
  local verbose=false
  local category_filter=""

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      scan|hooks|report|audit|patterns|status)
        cmd="$1"
        shift
        ;;
      install|uninstall)
        # Sub-command of hooks
        if [[ "$cmd" == "hooks" ]]; then
          cmd="hooks-$1"
        else
          cmd="$1"
        fi
        shift
        ;;
      --path)
        shift
        target="${1:-.}"
        shift
        ;;
      --format)
        shift
        format="${1:-text}"
        shift
        ;;
      --tier)
        shift
        tier_override="${1:-}"
        shift
        ;;
      --license-key)
        shift
        license_key_cli="${1:-}"
        shift
        ;;
      --verbose|-V)
        verbose=true
        shift
        ;;
      --category)
        shift
        category_filter="${1:-}"
        shift
        ;;
      --help|-h|help)
        show_help
        return 0
        ;;
      --version|-v)
        show_version
        return 0
        ;;
      -*)
        log_error "Unknown option: $1"
        echo ""
        show_help
        return 1
        ;;
      *)
        # Positional argument: treat as target path if no command yet
        if [[ -z "$cmd" ]]; then
          cmd="scan"
          target="$1"
        else
          target="$1"
        fi
        shift
        ;;
    esac
  done

  # Default command
  if [[ -z "$cmd" ]]; then
    show_help
    return 1
  fi

  # Source required modules
  source "$SCRIPT_DIR/license.sh"
  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  # Resolve effective tier
  local tier
  tier=$(resolve_tier "$tier_override" "$license_key_cli")

  # Get per-category pattern limit based on tier
  local per_category_limit
  per_category_limit=$(get_patterns_per_category "$tier")

  # Validate category filter if provided
  if [[ -n "$category_filter" ]]; then
    validate_category "$category_filter" || return 1
  fi

  # ---------------------------------------------------------------------------
  # Command Dispatch
  # ---------------------------------------------------------------------------

  case "$cmd" in
    scan)
      log_info "Scanning for input validation issues in ${BOLD}$target${NC}"
      do_inputshield_scan "$target" "$per_category_limit" "$format" "$category_filter" "$tier" "$verbose"
      ;;

    hooks-install)
      require_license "pro" || return 1
      do_hooks_install
      ;;

    hooks-uninstall)
      require_license "pro" || return 1
      do_hooks_uninstall
      ;;

    hooks)
      # If "hooks" was given without install/uninstall, show usage
      log_error "Missing sub-command."
      echo "  Usage: inputshield hooks [install|uninstall]"
      return 1
      ;;

    report)
      require_license "pro" || return 1
      log_info "Generating input validation report for ${BOLD}$target${NC}"
      generate_inputshield_report "$target" "$per_category_limit" "$category_filter"
      ;;

    audit)
      require_license "team" || return 1
      log_info "Running deep audit on ${BOLD}$target${NC}"
      do_inputshield_audit "$target" "$format" "$category_filter" "$verbose"
      ;;

    patterns)
      do_list_patterns "$per_category_limit"
      ;;

    status)
      show_version
      echo ""
      show_inputshield_status
      ;;

    *)
      log_error "Unknown command: $cmd"
      echo ""
      show_help
      return 1
      ;;
  esac
}

main "$@"
