#!/usr/bin/env bash
#
# ha-backup.sh — HA backup management via SSH
#
# Security:
#   - ENV vars: HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_SSH_PASS
#   - Endpoints: SSH to HA_HOST (ha CLI commands)
#   - File access: reads/writes /backup/* on remote HA, downloads to local path via SCP
#   - No data sent to external services
#
# Usage:
#   ha-backup.sh list                     # List existing backups
#   ha-backup.sh create [name]            # Create full backup
#   ha-backup.sh create-partial [name]    # Backup config only (no addons)
#   ha-backup.sh info <slug>              # Backup details
#   ha-backup.sh restore <slug>           # Restore from backup (⚠️ dangerous)
#   ha-backup.sh remove <slug>            # Delete a backup
#   ha-backup.sh download <slug> <local>  # Download backup to local machine

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

check_cli() {
    if ! ssh_cmd "command -v ha >/dev/null 2>&1"; then
        echo "❌ Backup commands require the 'ha' CLI, which is only available on Home Assistant OS / Supervised." >&2
        exit 1
    fi
}

cmd_list() {
    check_cli
    echo "=== HA Backups ===" >&2
    ssh_cmd "ha backups list" 2>/dev/null
}

cmd_create() {
    check_cli
    local name="${1:-openclaw-backup-$(date +%Y%m%d)}"
    validate_slug "$name" "backup name"
    echo "Creating full backup: $name ..." >&2
    local safe_name
    safe_name=$(ssh_safe_quote "$name")
    ssh_cmd "ha backups new --name '${safe_name}'" 2>/dev/null
    echo -e "${GREEN}✅ Backup '$name' created.${NC}" >&2
    echo "" >&2
    cmd_list
}

cmd_create_partial() {
    check_cli
    local name="${1:-config-backup-$(date +%Y%m%d)}"
    validate_slug "$name" "backup name"
    echo "Creating partial backup (config only): $name ..." >&2
    local safe_name
    safe_name=$(ssh_safe_quote "$name")
    ssh_cmd "ha backups new --name '${safe_name}' --homeassistant" 2>/dev/null
    echo -e "${GREEN}✅ Partial backup '$name' created.${NC}" >&2
}

cmd_info() {
    check_cli
    local slug="$1"
    validate_slug "$slug" "backup slug"
    local safe_slug
    safe_slug=$(ssh_safe_quote "$slug")
    ssh_cmd "ha backups info '${safe_slug}'" 2>/dev/null
}

cmd_restore() {
    check_cli
    local slug="$1"
    validate_slug "$slug" "backup slug"
    echo -e "${YELLOW}⚠️  WARNING: Restoring backup will restart Home Assistant!${NC}" >&2
    echo "    Backup: $slug" >&2
    echo "" >&2
    # Confirmation is handled at the agent/user interface level.
    # To prevent hanging in non-interactive environments, we proceed directly.
    echo "Restoring..."
    local safe_slug
    safe_slug=$(ssh_safe_quote "$slug")
    ssh_cmd "ha backups restore '${safe_slug}'" 2>/dev/null
    echo -e "${GREEN}✅ Restore initiated. HA will restart.${NC}"
}

cmd_remove() {
    check_cli
    local slug="$1"
    validate_slug "$slug" "backup slug"
    local safe_slug
    safe_slug=$(ssh_safe_quote "$slug")
    ssh_cmd "ha backups remove '${safe_slug}'" 2>/dev/null
    echo "✅ Backup $slug removed."
}

cmd_download() {
    check_cli
    local slug="$1"
    local local_path="${2:-.}"
    local remote_path="/backup/${slug}.tar"
    echo "Downloading backup $slug..."
    scp_cmd "${HA_SSH_USER}@${HA_HOST}:${remote_path}" "${local_path}/"
    echo "✅ Downloaded to ${local_path}/${slug}.tar"
}

case "${1:-help}" in
    list)           cmd_list ;;
    create)         cmd_create "${2:-}" ;;
    create-partial) cmd_create_partial "${2:-}" ;;
    info)           cmd_info "${2:?slug required}" ;;
    restore)        cmd_restore "${2:?slug required}" ;;
    remove)         cmd_remove "${2:?slug required}" ;;
    download)       cmd_download "${2:?slug required}" "${3:-.}" ;;
    *)
        echo "ha-backup.sh — Manage HA backups"
        echo ""
        echo "  list                      List backups"
        echo "  create [name]             Full backup"
        echo "  create-partial [name]     Config-only backup"
        echo "  info <slug>               Backup details"
        echo "  restore <slug>            Restore (⚠️ restarts HA)"
        echo "  remove <slug>             Delete backup"
        echo "  download <slug> [path]    Download to local machine"
        ;;
esac
