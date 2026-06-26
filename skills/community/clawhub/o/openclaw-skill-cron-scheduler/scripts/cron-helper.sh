#!/bin/bash
#
# cron-helper.sh - Manage cron jobs on macOS/Linux
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="${HOME}/.cron-backups"
SCRIPT_NAME="$(basename "$0")"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

#######################################
# Utility Functions
#######################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

check_crontab() {
    if ! command -v crontab &> /dev/null; then
        log_error "crontab command not found. Please install cron."
        exit 1
    fi
}

get_os() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*) echo "linux" ;;
        *) echo "unknown" ;;
    esac
}

#######################################
# Feature 1: List all cron jobs
#######################################

list_jobs() {
    check_crontab
    
    local crontab_output
    crontab_output=$(crontab -l 2>/dev/null) || true
    
    if [[ -z "$crontab_output" ]]; then
        log_warn "No cron jobs found for user $(whoami)"
        return
    fi
    
    echo -e "${BLUE}=== Cron Jobs for $(whoami) ===${NC}"
    echo "$crontab_output" | nl -v 1
    log_success "Found $(echo "$crontab_output" | wc -l) job(s)"
}

#######################################
# Feature 2: Add a new cron job
#######################################

validate_cron_expression() {
    local cron_expr="$1"
    
    # Basic validation - check 5 fields
    local fields
    IFS=' ' read -ra fields <<< "$cron_expr"
    
    if [[ ${#fields[@]} -ne 5 ]]; then
        log_error "Invalid cron expression: expected 5 fields, got ${#fields[@]}"
        return 1
    fi
    
    # Validate each field (basic check)
    local minute="${fields[0]}"
    local hour="${fields[1]}"
    local day="${fields[2]}"
    local month="${fields[3]}"
    local weekday="${fields[4]}"
    
    # Check for valid ranges (simplified)
    if [[ ! "$minute" =~ ^(\*|[0-5]?[0-9](,[0-5]?[0-9])*|[0-5]?[0-9]-[0-5]?[0-9]|\*\/[0-5]?[0-9])$ ]]; then
        log_error "Invalid minute field: $minute"
        return 1
    fi
    
    return 0
}

add_job() {
    check_crontab
    
    local schedule="$1"
    local command="$2"
    
    if [[ -z "$schedule" || -z "$command" ]]; then
        log_error "Usage: $SCRIPT_NAME add '<schedule>' '<command>'"
        log_error "Example: $SCRIPT_NAME add '0 * * * *' '~/scripts/backup.sh'"
        exit 1
    fi
    
    if ! validate_cron_expression "$schedule"; then
        log_error "Invalid cron schedule expression"
        exit 1
    fi
    
    # Create temp file for safety
    local temp_file
    temp_file=$(mktemp)
    
    # Preserve existing crontab
    crontab -l 2>/dev/null >> "$temp_file" || true
    
    # Add new job
    echo "$schedule $command" >> "$temp_file"
    
    # Install new crontab
    crontab "$temp_file"
    rm -f "$temp_file"
    
    log_success "Added cron job: $schedule $command"
}

#######################################
# Feature 3: Remove cron jobs
#######################################

remove_job() {
    check_crontab
    
    local mode="$1"
    local value="$2"
    
    local temp_file
    temp_file=$(mktemp)
    
    # Get current crontab
    local current_crontab
    current_crontab=$(crontab -l 2>/dev/null) || true
    
    if [[ -z "$current_crontab" ]]; then
        log_error "No cron jobs to remove"
        rm -f "$temp_file"
        exit 1
    fi
    
    if [[ "$mode" == "line" ]]; then
        # Remove by line number
        echo "$current_crontab" | sed -n "H;1h;\$!d;x;s/^[0-9]*[ \t]*//;${value}d" > "$temp_file"
        log_success "Removed job at line $value"
    elif [[ "$mode" == "pattern" ]]; then
        # Remove by pattern
        echo "$current_crontab" | grep -v "$value" > "$temp_file"
        log_success "Removed jobs matching pattern: $value"
    else
        log_error "Invalid mode. Use 'line' or 'pattern'"
        rm -f "$temp_file"
        exit 1
    fi
    
    crontab "$temp_file"
    rm -f "$temp_file"
    log_success "Cron job(s) removed"
}

#######################################
# Feature 4: Edit crontab
#######################################

edit_crontab() {
    check_crontab
    crontab -e
    log_success "Crontab editor closed"
}

#######################################
# Feature 5: Show next run times
#######################################

show_next_runs() {
    check_crontab
    
    local crontab_output
    crontab_output=$(crontab -l 2>/dev/null) || true
    
    if [[ -z "$crontab_output" ]]; then
        log_warn "No cron jobs found"
        return
    fi
    
    echo -e "${BLUE}=== Next Run Times ===${NC}"
    
    # Try to use cronnext if available, otherwise show manual calculation
    if command -v cronnext &> /dev/null; then
        cronnext -u "$(whoami)"
        return
    fi
    
    # Fallback: basic next run calculation
    local line_num=1
    while IFS= read -r line; do
        # Skip empty lines and comments
        [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
        
        # Extract schedule (first 5 fields)
        local schedule
        schedule=$(echo "$line" | awk '{print $1,$2,$3,$4,$5}')
        
        echo -e "${GREEN}Job $line_num:${NC} $schedule"
        echo "  Command: $(echo "$line" | awk '{$1=$2=$3=$4=$5=""; print $0}' | xargs)"
        
        line_num=$((line_num + 1))
    done <<< "$crontab_output"
    
    log_info "Install 'cronnext' package for accurate next-run predictions"
}

#######################################
# Feature 6: Backup/Restore crontab
#######################################

backup_crontab() {
    check_crontab
    
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="${BACKUP_DIR}/crontab_${timestamp}.bak"
    
    local crontab_output
    crontab_output=$(crontab -l 2>/dev/null) || true
    
    if [[ -z "$crontab_output" ]]; then
        log_warn "No crontab to backup"
        return
    fi
    
    echo "$crontab_output" > "$backup_file"
    log_success "Backed up crontab to: $backup_file"
}

restore_crontab() {
    check_crontab
    
    local backup_file="$1"
    
    if [[ -z "$backup_file" ]]; then
        # List available backups
        echo -e "${BLUE}=== Available Backups ===${NC}"
        ls -la "$BACKUP_DIR"/crontab_*.bak 2>/dev/null || log_warn "No backups found"
        return
    fi
    
    if [[ ! -f "$backup_file" ]]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    # Show what will be restored
    echo -e "${YELLOW}=== Backup Content ===${NC}"
    cat "$backup_file"
    echo -e "${YELLOW}======================${NC}"
    
    read -p "Restore this crontab? (y/N) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        crontab "$backup_file"
        log_success "Crontab restored from: $backup_file"
    else
        log_info "Restore cancelled"
    fi
}

#######################################
# Feature 7: Enable/disable cron service
#######################################

manage_cron_service() {
    local action="$1"
    local os_type
    os_type=$(get_os)
    
    case "$os_type" in
        macos)
            case "$action" in
                start)
                    sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.cron.plist 2>/dev/null || \
                    log_error "Need sudo to start cron"
                    ;;
                stop)
                    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.cron.plist 2>/dev/null || \
                    log_error "Need sudo to stop cron"
                    ;;
                status)
                    if sudo launchctl list | grep -q com.apple.cron; then
                        log_success "Cron service is running"
                    else
                        log_warn "Cron service is not running"
                    fi
                    ;;
                *)
                    log_error "Unknown action: $action. Use start, stop, or status"
                    exit 1
                    ;;
            esac
            ;;
        linux)
            case "$action" in
                start)
                    sudo systemctl start cron 2>/dev/null || sudo systemctl start crond 2>/dev/null || \
                    log_error "Failed to start cron service"
                    ;;
                stop)
                    sudo systemctl stop cron 2>/dev/null || sudo systemctl stop crond 2>/dev/null || \
                    log_error "Failed to stop cron service"
                    ;;
                status)
                    if sudo systemctl is-active cron &>/dev/null || sudo systemctl is-active crond &>/dev/null; then
                        log_success "Cron service is running"
                    else
                        log_warn "Cron service is not running"
                    fi
                    ;;
                *)
                    log_error "Unknown action: $action. Use start, stop, or status"
                    exit 1
                    ;;
            esac
            ;;
        *)
            log_error "Unsupported OS: $os_type"
            exit 1
            ;;
    esac
}

#######################################
# Feature 8: Common templates
#######################################

show_templates() {
    echo -e "${BLUE}=== Cron Job Templates ===${NC}"
    echo ""
    echo "1. Daily backup at 2am"
    echo "   0 2 * * * ~/scripts/backup.sh"
    echo ""
    echo "2. Weekly cleanup (Sunday at 3am)"
    echo "   0 3 * * 0 ~/scripts/cleanup.sh"
    echo ""
    echo "3. Monthly report (1st of month at 9am)"
    echo "   0 9 1 * * ~/scripts/monthly-report.sh"
    echo ""
    echo "4. Hourly sync"
    echo "   0 * * * * ~/scripts/sync.sh"
    echo ""
    echo "5. Every 5 minutes"
    echo "   */5 * * * * ~/scripts/monitor.sh"
    echo ""
    echo "6. Every day at noon"
    echo "   0 12 * * * ~/scripts/daily-task.sh"
    echo ""
    echo "7. Weekdays at 5pm"
    echo "   0 17 * * 1-5 ~/scripts/after-work.sh"
    echo ""
    echo "Use: $SCRIPT_NAME add '<schedule>' '<command>'"
}

#######################################
# Usage / Help
#######################################

usage() {
    echo "cron-helper.sh - Cron Job Manager"
    echo ""
    echo "Usage: $SCRIPT_NAME <command> [options]"
    echo ""
    echo "Commands:"
    echo "  list, l                    List all cron jobs"
    echo "  add <schedule> <command>   Add a new cron job"
    echo "  remove <line#>             Remove job by line number"
    echo "  removep <pattern>          Remove jobs matching pattern"
    echo "  edit, e                    Edit crontab in editor"
    echo "  next, n                    Show next run times"
    echo "  backup                      Backup current crontab"
    echo "  restore [file]             Restore from backup (list if no file)"
    echo "  service <start|stop|status> Manage cron service"
    echo "  templates, t               Show common cron templates"
    echo "  help, h                    Show this help"
    echo ""
    echo "Examples:"
    echo "  $SCRIPT_NAME list"
    echo "  $SCRIPT_NAME add '0 2 * * *' '~/scripts/backup.sh'"
    echo "  $SCRIPT_NAME remove 3"
    echo "  $SCRIPT_NAME removep 'backup'"
    echo "  $SCRIPT_NAME service status"
    echo ""
    echo "Cron Schedule Format:"
    echo "  ┌──────────── minute (0 - 59)"
    echo "  │ ┌────────── hour (0 - 23)"
    echo "  │ │ ┌──────── day of month (1 - 31)"
    echo "  │ │ │ ┌------ month (1 - 12)"
    echo "  │ │ │ │ ┌---- day of week (0 - 6, Sunday=0)"
    echo "  * * * * *"
}

#######################################
# Main
#######################################

main() {
    local command="${1:-}"
    
    case "$command" in
        list|l)
            list_jobs
            ;;
        add)
            add_job "$2" "$3"
            ;;
        remove|rm)
            remove_job "line" "${2:-}"
            ;;
        removep|rmp)
            remove_job "pattern" "${2:-}"
            ;;
        edit|e)
            edit_crontab
            ;;
        next|n)
            show_next_runs
            ;;
        backup|b)
            backup_crontab
            ;;
        restore|r)
            restore_crontab "${2:-}"
            ;;
        service|s)
            manage_cron_service "${2:-}"
            ;;
        templates|t)
            show_templates
            ;;
        help|h|"")
            usage
            ;;
        *)
            log_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Run main with all arguments
main "$@"
