#!/usr/bin/env bash
# MigrateSafe -- Main CLI entry point
# Usage: migratesafe.sh <command> [args...]
#
# Commands:
#   scan [file|dir]           One-shot migration safety scan (FREE: 3 files / PRO+: unlimited)
#   hooks install             Install pre-commit hooks (PRO+)
#   hooks uninstall           Remove MigrateSafe hooks (PRO+)
#   rollback-check [dir]      Verify rollback coverage (PRO+)
#   diff <file1> <file2>      Compare two schema files (PRO+)
#   history [dir]             Migration risk timeline (TEAM+)
#   report [dir]              Generate safety report (TEAM+)
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

log_info()    { echo -e "${BLUE}[MigrateSafe]${NC} $*"; }
log_success() { echo -e "${GREEN}[MigrateSafe]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[MigrateSafe]${NC} $*"; }
log_error()   { echo -e "${RED}[MigrateSafe]${NC} $*" >&2; }

# ─── Version / Help ─────────────────────────────────────────────────────────

show_version() {
  echo -e "${BOLD}MigrateSafe${NC} v${VERSION}"
  echo "  Database Migration Safety Checker"
  echo "  https://migratesafe.pages.dev"
}

show_help() {
  show_version
  echo ""
  echo -e "${BOLD}USAGE${NC}"
  echo "  migratesafe <command> [options]"
  echo ""
  echo -e "${BOLD}FREE COMMANDS${NC}"
  echo -e "  scan [file|dir]           ${DIM}[FREE]${NC}  Migration safety scan (up to 3 files)"
  echo ""
  echo -e "${BOLD}PRO COMMANDS${NC} (\$19/user/month)"
  echo -e "  scan [file|dir]           ${DIM}[PRO]${NC}   Unlimited migration scanning"
  echo -e "  hooks install             ${DIM}[PRO]${NC}   Install pre-commit hooks"
  echo -e "  hooks uninstall           ${DIM}[PRO]${NC}   Remove MigrateSafe hooks"
  echo -e "  rollback-check [dir]      ${DIM}[PRO]${NC}   Verify rollback coverage"
  echo -e "  diff <file1> <file2>      ${DIM}[PRO]${NC}   Compare two schema files"
  echo ""
  echo -e "${BOLD}TEAM COMMANDS${NC} (\$39/user/month)"
  echo -e "  history [dir]             ${DIM}[TEAM]${NC}  Migration risk timeline"
  echo -e "  report [dir]              ${DIM}[TEAM]${NC}  Generate compliance report"
  echo ""
  echo -e "${BOLD}OTHER${NC}"
  echo "  status                    Show license and config info"
  echo "  --help, -h, help          Show this help"
  echo "  --version, -v, version    Show version"
  echo ""
  echo -e "${BOLD}EXIT CODES${NC}"
  echo "  0   All migrations are safe"
  echo "  1   Dangerous operations detected"
  echo ""
  echo -e "Get a license at ${CYAN}https://migratesafe.pages.dev${NC}"
}

# ─── License ─────────────────────────────────────────────────────────────────

require_license() {
  local required_tier="${1:-pro}"
  source "$SCRIPT_DIR/license.sh"
  check_migratesafe_license "$required_tier"
}

get_current_tier() {
  source "$SCRIPT_DIR/license.sh"
  get_migratesafe_tier
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
    if grep -q "migratesafe" "$config" 2>/dev/null; then
      log_success "Hooks already configured."
      return 0
    fi

    # Append to existing config
    cat >> "$config" <<'HOOKS'

# --- MigrateSafe hooks -----------------------------------------
    migratesafe-migration-scan:
      glob: "*.{sql,rb,py,js,ts,xml}"
      run: |
        MIGRATESAFE_SKILL_DIR="${MIGRATESAFE_SKILL_DIR:-$HOME/.openclaw/skills/migratesafe}"
        if [[ -f "$MIGRATESAFE_SKILL_DIR/scripts/analyzer.sh" ]]; then
          source "$MIGRATESAFE_SKILL_DIR/scripts/patterns.sh"
          source "$MIGRATESAFE_SKILL_DIR/scripts/analyzer.sh"
          hook_migration_scan
        else
          echo "[MigrateSafe] Skill not found at $MIGRATESAFE_SKILL_DIR -- skipping"
        fi
      fail_text: |
        Destructive migration operations detected!
        Run 'migratesafe scan' to see details.
        Or 'git commit --no-verify' to skip (NOT recommended).
HOOKS
    echo -e "${GREEN}+${NC} Appended MigrateSafe hooks to existing lefthook.yml"
  else
    cp "$SKILL_DIR/config/lefthook.yml" "$config"
    echo -e "${GREEN}+${NC} Created lefthook.yml"
  fi

  (cd "$repo_root" && lefthook install)
  echo ""
  log_success "Hooks installed! Staged migration files will be scanned on every commit."
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
    if grep -q "migratesafe" "$config" 2>/dev/null; then
      local tmp
      tmp=$(mktemp)
      # Remove the MigrateSafe hook block
      awk '/# --- MigrateSafe hooks/{skip=1} /^[[:space:]]*[a-zA-Z]/ && skip && !/migratesafe/{skip=0} !skip' "$config" > "$tmp"
      mv "$tmp" "$config"
      echo -e "${GREEN}+${NC} Removed MigrateSafe hooks from lefthook.yml"
    else
      log_warn "No MigrateSafe hooks found in lefthook.yml"
    fi
  else
    log_warn "No lefthook.yml found in $repo_root"
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

  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  local max_files=3
  if [[ "$tier" == "pro" || "$tier" == "team" || "$tier" == "enterprise" ]]; then
    max_files=0  # 0 = unlimited
  fi

  log_info "Scanning for destructive migration operations in ${BOLD}$target${NC}"
  if [[ "$max_files" -gt 0 ]]; then
    echo -e "  ${DIM}Free tier: limited to $max_files files. Upgrade for unlimited scanning.${NC}"
  fi
  echo ""

  do_migration_scan "$target" "$max_files"
}

# ─── Rollback Check command ──────────────────────────────────────────────────

do_rollback_check() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  log_info "Checking rollback coverage in ${BOLD}$target${NC}"
  echo ""

  local -a migration_files=()
  find_migration_files "$target" migration_files

  if [[ ${#migration_files[@]} -eq 0 ]]; then
    log_success "No migration files found."
    return 0
  fi

  local total_files=0
  local has_rollback=0
  local missing_rollback=0
  local exit_code=0

  for file in "${migration_files[@]}"; do
    total_files=$((total_files + 1))
    local result
    result=$(check_rollback_exists "$file")
    if [[ "$result" == "found" ]]; then
      has_rollback=$((has_rollback + 1))
      echo -e "  ${GREEN}OK${NC}  $(basename "$file")"
    else
      missing_rollback=$((missing_rollback + 1))
      echo -e "  ${RED}MISSING${NC}  $(basename "$file") -- no rollback found"
      exit_code=1
    fi
  done

  echo ""
  local pct=0
  if [[ $total_files -gt 0 ]]; then
    pct=$(( (has_rollback * 100) / total_files ))
  fi

  echo -e "${BOLD}Rollback Coverage:${NC} ${pct}% ($has_rollback / $total_files)"
  if [[ $missing_rollback -gt 0 ]]; then
    echo -e "${YELLOW}$missing_rollback migration(s) missing rollback files.${NC}"
  else
    log_success "All migrations have rollback coverage."
  fi

  return $exit_code
}

# ─── Diff command ────────────────────────────────────────────────────────────

do_diff() {
  local file1="${1:-}"
  local file2="${2:-}"

  if [[ -z "$file1" || -z "$file2" ]]; then
    log_error "Usage: migratesafe diff <file1> <file2>"
    return 1
  fi

  if [[ ! -f "$file1" ]]; then
    log_error "File not found: $file1"
    return 1
  fi

  if [[ ! -f "$file2" ]]; then
    log_error "File not found: $file2"
    return 1
  fi

  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  log_info "Comparing schema files:"
  echo -e "  ${DIM}Old:${NC} $file1"
  echo -e "  ${DIM}New:${NC} $file2"
  echo ""

  do_schema_diff "$file1" "$file2"
}

# ─── History command ─────────────────────────────────────────────────────────

do_history() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  log_info "Building migration risk timeline for ${BOLD}$target${NC}"
  echo ""

  do_history_scan "$target"
}

# ─── Report command ──────────────────────────────────────────────────────────

do_report() {
  local target="${1:-.}"

  if [[ ! -e "$target" ]]; then
    log_error "Target not found: ${BOLD}$target${NC}"
    return 1
  fi

  source "$SCRIPT_DIR/patterns.sh"
  source "$SCRIPT_DIR/analyzer.sh"

  log_info "Generating migration safety report for ${BOLD}$target${NC}"
  echo ""

  generate_report "$target"
}

# ─── Status command ──────────────────────────────────────────────────────────

do_status() {
  show_version
  echo ""
  source "$SCRIPT_DIR/license.sh"
  show_migratesafe_status
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
          echo "  Usage: migratesafe hooks [install|uninstall]"
          exit 1
          ;;
      esac
      ;;

    rollback-check)
      require_license "pro"
      do_rollback_check "${1:-.}"
      ;;

    diff)
      require_license "pro"
      do_diff "${1:-}" "${2:-}"
      ;;

    history)
      require_license "team"
      do_history "${1:-.}"
      ;;

    report)
      require_license "team"
      do_report "${1:-.}"
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
