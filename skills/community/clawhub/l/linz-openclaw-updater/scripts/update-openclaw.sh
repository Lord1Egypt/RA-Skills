#!/bin/bash
#
# OpenClaw Auto-Updater Script
# Automatically checks for and installs OpenClaw updates
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LOG_FILE="${OPENCLAW_UPDATE_LOG:-$HOME/.openclaw/logs/auto-update.log}"
LOCK_FILE="/tmp/openclaw-updater.lock"
BACKUP_DIR="$HOME/.openclaw/backups"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$BACKUP_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if already running
check_lock() {
    if [ -f "$LOCK_FILE" ]; then
        pid=$(cat "$LOCK_FILE" 2>/dev/null)
        if ps -p "$pid" > /dev/null 2>&1; then
            log "${YELLOW}Updater already running (PID: $pid)${NC}"
            exit 0
        else
            rm -f "$LOCK_FILE"
        fi
    fi
    echo $$ > "$LOCK_FILE"
}

# Cleanup on exit
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

# Get current version
get_current_version() {
    if command -v openclaw &> /dev/null; then
        openclaw --version 2>/dev/null | head -1 || echo "unknown"
    else
        echo "not_installed"
    fi
}

# Get latest version from npm
get_latest_version() {
    npm view @openclaw/core version 2>/dev/null || npm view openclaw version 2>/dev/null || echo ""
}

# Check Node.js version
check_node_version() {
    local required_version="22.16.0"
    local current_version
    current_version=$(node --version 2>/dev/null | sed 's/v//' || echo "0.0.0")

    if [ "$(printf '%s\n' "$required_version" "$current_version" | sort -V | head -n1)" != "$required_version" ]; then
        log "${YELLOW}Warning: Node.js $current_version detected. OpenClaw requires >= $required_version${NC}"
        return 1
    fi
    return 0
}

# Create backup before update
create_backup() {
    local backup_name="openclaw-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    local backup_path="$BACKUP_DIR/$backup_name"

    log "${BLUE}Creating backup: $backup_name${NC}"

    # Backup config and data
    tar -czf "$backup_path" \
        -C "$HOME" \
        .openclaw/config \
        .openclaw/workspace \
        2>/dev/null || true

    # Keep only last 5 backups
    ls -t "$BACKUP_DIR"/openclaw-backup-*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true

    echo "$backup_path"
}

# Perform the update
perform_update() {
    local current_version=$1
    local latest_version=$2

    log "${BLUE}Starting update from $current_version to $latest_version...${NC}"

    # Create backup
    local backup_path
    backup_path=$(create_backup)
    log "${GREEN}Backup created: $backup_path${NC}"

    # Update OpenClaw
    log "${BLUE}Installing update...${NC}"

    if ! npm install -g @openclaw/core@latest 2>&1 | tee -a "$LOG_FILE"; then
        # Try alternative package name
        if ! npm install -g openclaw@latest 2>&1 | tee -a "$LOG_FILE"; then
            log "${RED}Update failed! Check $LOG_FILE for details.${NC}"
            return 1
        fi
    fi

    # Verify installation
    local new_version
    new_version=$(get_current_version)

    if [ "$new_version" != "$current_version" ]; then
        log "${GREEN}✓ Successfully updated to $new_version${NC}"
        return 0
    else
        log "${YELLOW}Version unchanged after update. May already be at latest version.${NC}"
        return 0
    fi
}

# Send notification (if configured)
send_notification() {
    local message="$1"
    local priority="${2:-normal}"

    # Try various notification methods
    if command -v notify &> /dev/null; then
        notify "$message" 2>/dev/null || true
    fi

    # Log to file either way
    log "$message"
}

# Main update logic
main() {
    local force_update=false
    local dry_run=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force)
                force_update=true
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [--force] [--dry-run]"
                echo ""
                echo "Options:"
                echo "  --force     Force update even if versions match"
                echo "  --dry-run   Check for updates but don't install"
                exit 0
                ;;
            *)
                shift
                ;;
        esac
    done

    log "${BLUE}=== OpenClaw Auto-Updater ===${NC}"
    log "Checking for updates..."

    # Check lock
    check_lock

    # Check Node.js version
    if ! check_node_version; then
        log "${RED}Node.js version check failed. Update may not work properly.${NC}"
    fi

    # Get versions
    local current_version
    local latest_version

    current_version=$(get_current_version)
    latest_version=$(get_latest_version)

    log "Current version: $current_version"
    log "Latest version: $latest_version"

    # Check if update is needed
    if [ "$current_version" = "$latest_version" ] && [ "$force_update" = false ]; then
        log "${GREEN}Already up to date!${NC}"
        exit 0
    fi

    if [ -z "$latest_version" ]; then
        log "${RED}Could not determine latest version. Check network connection.${NC}"
        exit 1
    fi

    # Dry run mode
    if [ "$dry_run" = true ]; then
        log "${YELLOW}Dry run mode - would update to $latest_version${NC}"
        exit 0
    fi

    # Perform update
    if perform_update "$current_version" "$latest_version"; then
        send_notification "OpenClaw updated successfully to $latest_version" "normal"
        exit 0
    else
        send_notification "OpenClaw update failed! Check logs at $LOG_FILE" "high"
        exit 1
    fi
}

# Run main function
main "$@"
