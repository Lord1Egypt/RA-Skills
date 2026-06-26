#!/usr/bin/env bash
# stock-watcher-scheduler.sh — Stock Watcher Pro Scheduling Automation
#
# Sets up scheduled briefings and filing checks via OpenClaw heartbeat
# or external scheduling (cron, Trigger.dev).
#
# Usage:
#   bash scripts/stock-watcher-scheduler.sh setup     — Configure scheduling
#   bash scripts/stock-watcher-scheduler.sh status     — Check current schedule
#   bash scripts/stock-watcher-scheduler.sh run-check  — Run a manual filing check now
#   bash scripts/stock-watcher-scheduler.sh briefing [pre-market|mid-day|post-market]
#
# Requirements:
#   - OpenClaw agent with exec, web_search, web_fetch tools
#   - config/watchlist-config.json must exist
#   - data/portfolio.json must exist with at least one holding

set -euo pipefail

# --- Path Resolution ---
# Workspace root is passed as $1, or detected from script location.
# If scripts/ is at workspace root (copied during setup), go up 1 level.
# If still inside the skill package, go up to find the workspace root.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -n "${1:-}" ] && [ -d "$1" ] && [ "$1" != "setup" ] && [ "$1" != "status" ] && [ "$1" != "run-check" ] && [ "$1" != "briefing" ]; then
  CANDIDATE_WORKSPACE="$(cd "$1" && pwd)"
    # Skill directory detection (stay within skill boundary)
    WORKSPACE_DIR="$CANDIDATE_WORKSPACE"
  else
    echo "[ERROR] Invalid workspace directory: $1" >&2
    # Skill directory detection (stay within skill boundary)
    exit 1
  fi
    # Skill directory detection (stay within skill boundary)
  WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    # Skill directory detection (stay within skill boundary)
  # Inside skill package: skills/stock-watcher-pro/scripts/
  WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
else
  WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
fi
CONFIG_FILE="$WORKSPACE_DIR/config/watchlist-config.json"
PORTFOLIO_FILE="$WORKSPACE_DIR/data/portfolio.json"
HEARTBEAT_FILE="$WORKSPACE_DIR/HEARTBEAT.md"

# --- Color Output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# --- Validation ---
validate_setup() {
    local errors=0

    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "Config file not found: $CONFIG_FILE"
        log_error "Run SETUP-PROMPT.md first to initialize configuration."
        errors=$((errors + 1))
    fi

    if [ ! -f "$PORTFOLIO_FILE" ]; then
        log_error "Portfolio file not found: $PORTFOLIO_FILE"
        log_error "Run SETUP-PROMPT.md first, then add at least one holding."
        errors=$((errors + 1))
    fi

    if [ $errors -gt 0 ]; then
        log_error "Validation failed with $errors error(s). Fix the above issues and retry."
        exit 1
    fi

    # Check if portfolio has holdings
    local holding_count
    holding_count=$(PORTFOLIO_FILE="$PORTFOLIO_FILE" python3 -c "
import json, os, sys
try:
    with open(os.environ['PORTFOLIO_FILE']) as f:
        data = json.load(f)
    print(len(data.get('holdings', [])))
except Exception as e:
    print(0, file=sys.stderr)
    print(0)
" 2>/dev/null || echo "0")

    if [ "$holding_count" = "0" ]; then
        log_warn "Portfolio has no holdings. Add tickers before scheduling briefings."
        log_warn "Example: Tell your agent 'Add AAPL — 50 shares at \$178.50'"
    else
        log_info "Portfolio validated: $holding_count holding(s) found."
    fi
}

# --- Read Config Values ---
read_config() {
    CONFIG_FILE="$CONFIG_FILE" python3 -c "
import json, os, sys
try:
    with open(os.environ['CONFIG_FILE']) as f:
        data = json.load(f)
    # Extract schedule info
    sched = data.get('briefing_schedule', {})
    tz = data.get('timezone', 'America/New_York')
    print(f'Timezone: {tz}')
    for btype in ['pre_market', 'mid_day', 'post_market']:
        b = sched.get(btype, {})
        enabled = b.get('enabled', False)
        time_val = b.get('time', 'N/A')
        status = 'ENABLED' if enabled else 'DISABLED'
        print(f'{btype}: {time_val} [{status}]')
    weekly = sched.get('weekly_wrap', {})
    w_enabled = weekly.get('enabled', False)
    w_day = weekly.get('day', 'friday')
    w_status = 'ENABLED' if w_enabled else 'DISABLED'
    print(f'weekly_wrap: {w_day} [{w_status}]')
    edgar = data.get('edgar_settings', {})
    interval = edgar.get('check_interval_hours', 2)
    print(f'edgar_check_interval: {interval}h')
except Exception as e:
    print(f'Error reading config: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1
}

# --- Setup Heartbeat Integration ---
setup_heartbeat() {
    log_info "Configuring heartbeat integration for Stock Watcher Pro..."

    # Create or update HEARTBEAT.md with stock watcher checks
    local heartbeat_entry="## Stock Watcher Pro Checks
- [ ] Check EDGAR for new filings (every 2h during market hours: 9:30 AM - 4:00 PM ET, Mon-Fri)
- [ ] Generate pre-market briefing (6:00 AM local, weekdays)
- [ ] Generate mid-day briefing (12:30 PM ET, weekdays)
- [ ] Generate post-market briefing (4:30 PM ET, weekdays)
- [ ] Source health check (Sundays)
- [ ] Weekly wrap (Friday post-market)"

    if [ -f "$HEARTBEAT_FILE" ]; then
        # Check if stock watcher section already exists
        if grep -q "Stock Watcher Pro Checks" "$HEARTBEAT_FILE" 2>/dev/null; then
            log_info "Stock Watcher Pro already in HEARTBEAT.md. Skipping."
        else
            echo "" >> "$HEARTBEAT_FILE"
            echo "$heartbeat_entry" >> "$HEARTBEAT_FILE"
            log_info "Added Stock Watcher Pro checks to existing HEARTBEAT.md"
        fi
    else
        echo "# Heartbeat Checklist" > "$HEARTBEAT_FILE"
        echo "" >> "$HEARTBEAT_FILE"
        echo "$heartbeat_entry" >> "$HEARTBEAT_FILE"
        log_info "Created HEARTBEAT.md with Stock Watcher Pro checks."
    fi

    chmod 600 "$HEARTBEAT_FILE" 2>/dev/null || true

    log_info "Heartbeat integration configured."
    log_info "Your agent will check for filing updates and generate briefings on the configured schedule."
}

# --- Manual Filing Check ---
run_filing_check() {
    log_info "Running manual EDGAR filing check..."
    validate_setup

    # Extract tickers from portfolio
    local tickers
    tickers=$(PORTFOLIO_FILE="$PORTFOLIO_FILE" python3 -c "
import json
import os
import re
with open(os.environ['PORTFOLIO_FILE']) as f:
    data = json.load(f)
pat = re.compile(r'^[A-Z][A-Z0-9.-]{0,9}$')
tickers = []
for h in data.get('holdings', []):
    t = str(h.get('ticker', '')).strip().upper()
    if pat.match(t):
        tickers.append(t)
print(' '.join(tickers))
" 2>/dev/null)

    if [ -z "$tickers" ]; then
        log_warn "No tickers in portfolio. Add holdings first."
        exit 0
    fi

    log_info "Checking filings for: $tickers"
    log_info "Delegating to agent for EDGAR API queries..."
    echo ""
    echo "Tell your agent: 'Check EDGAR for new filings for my portfolio tickers.'"
    echo "The agent will use web_fetch to query SEC EDGAR and summarize any new filings."
}

# --- Status ---
show_status() {
    echo "========================================="
    echo "  Stock Watcher Pro — Schedule Status"
    echo "========================================="
    echo ""

    validate_setup
    echo ""
    read_config
    echo ""

    if [ -f "$HEARTBEAT_FILE" ] && grep -q "Stock Watcher Pro" "$HEARTBEAT_FILE" 2>/dev/null; then
        log_info "Heartbeat integration: ACTIVE"
    else
        log_warn "Heartbeat integration: NOT CONFIGURED"
        log_warn "Run 'bash scripts/stock-watcher-scheduler.sh setup' to configure."
    fi

    echo ""
    echo "========================================="
}

# --- Main ---
case "${1:-help}" in
    setup)
        validate_setup
        setup_heartbeat
        echo ""
        log_info "Setup complete! Your agent will now run Stock Watcher Pro on schedule."
        ;;
    status)
        show_status
        ;;
    run-check)
        run_filing_check
        ;;
    briefing)
        briefing_type="${2:-pre-market}"
        case "$briefing_type" in
            pre-market|mid-day|post-market)
                ;;
            *)
                log_error "Invalid briefing type: $briefing_type"
                log_error "Use one of: pre-market, mid-day, post-market"
                exit 1
                ;;
        esac
        log_info "Requesting $briefing_type briefing..."
        echo "Tell your agent: 'Generate my $briefing_type briefing now.'"
        ;;
    help|*)
        echo "Stock Watcher Pro Scheduler"
        echo ""
        echo "Usage: bash scripts/stock-watcher-scheduler.sh <command>"
        echo ""
        echo "Commands:"
        echo "  setup       — Configure scheduled briefings and filing checks"
        echo "  status      — Show current schedule configuration"
        echo "  run-check   — Trigger a manual EDGAR filing check"
        echo "  briefing    — Request a briefing (pre-market|mid-day|post-market)"
        echo "  help        — Show this help message"
        ;;
esac
