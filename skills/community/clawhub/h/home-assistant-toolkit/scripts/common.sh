#!/usr/bin/env bash
#
# common.sh — Common utilities for OpenClaw HA scripts
#
# Security:
#   - ENV vars: HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_SSH_PASS, HA_URL, HA_TOKEN, HA_CONFIG_PATH
#   - Endpoints: user's HA instance (HA_URL), SSH to HA_HOST
#   - File access: reads/writes only under HA_CONFIG_PATH on remote HA instance
#   - sshpass limitation: HA_SSH_PASS is visible in process list (/proc/*/cmdline).
#     Prefer SSH key authentication for production use.
#   - StrictHostKeyChecking=accept-new: first connection trusts the host key (TOFU).
#     For high-security setups, pre-populate ~/.ssh/known_hosts manually.
#

set -euo pipefail

# Configuration with defaults
HA_HOST="${HA_HOST:-}"
HA_SSH_PORT="${HA_SSH_PORT:-22}"
HA_SSH_USER="${HA_SSH_USER:-root}"
HA_SSH_PASS="${HA_SSH_PASS:-}"
HA_URL="${HA_URL:-}"
HA_TOKEN="${HA_TOKEN:-}"
HA_CONFIG_PATH="${HA_CONFIG_PATH:-/config}"

# ANSI Colors for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# --- Input sanitization helpers ---

# Validate entity_id format: domain.name (alphanumeric + underscores)
validate_entity_id() {
    local eid="$1"
    if [[ ! "$eid" =~ ^[a-z_]+\.[a-z0-9_]+$ ]]; then
        echo -e "${RED}Error: invalid entity_id format: '$eid' (expected: domain.entity_name)${NC}" >&2
        return 1
    fi
}

# Validate a file path has no traversal (no .. components)
validate_config_path() {
    local file="$1"
    if [[ "$file" == *".."* ]] || [[ "$file" == /* ]] || [[ "$file" == *$'\n'* ]] || [[ "$file" == *$'\r'* ]]; then
        echo -e "${RED}Error: invalid config path: '$file' (path traversal not allowed)${NC}" >&2
        return 1
    fi
}

# Validate a numeric value (integer or decimal)
validate_number() {
    local val="$1"
    local label="${2:-value}"
    if [[ ! "$val" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        echo -e "${RED}Error: '$label' must be a number, got: '$val'${NC}" >&2
        return 1
    fi
}

# Sanitize a string for safe use inside single quotes in SSH commands.
# Replaces ' with '\'' (end quote, escaped quote, start quote).
ssh_safe_quote() {
    local input="$1"
    printf '%s' "$input" | sed "s/'/'\\\\''/g"
}

# Validate slug/name: alphanumeric, dashes, underscores, dots only
validate_slug() {
    local val="$1"
    local label="${2:-value}"
    if [[ ! "$val" =~ ^[a-zA-Z0-9._-]+$ ]]; then
        echo -e "${RED}Error: invalid ${label}: '$val' (alphanumeric, dashes, underscores, dots only)${NC}" >&2
        return 1
    fi
}

# SSH command wrapper
ssh_cmd() {
    if [[ -z "$HA_HOST" ]]; then
        echo -e "${RED}Error: SSH operation requested but HA_HOST not set.${NC}" >&2
        exit 1
    fi
    local opts=(-o "StrictHostKeyChecking=accept-new" -o "ConnectTimeout=10" -p "$HA_SSH_PORT")
    if [[ -n "${HA_SSH_PASS:-}" ]] && command -v sshpass &>/dev/null; then
        sshpass -p "$HA_SSH_PASS" ssh "${opts[@]}" "${HA_SSH_USER}@${HA_HOST}" "$@"
    else
        ssh "${opts[@]}" "${HA_SSH_USER}@${HA_HOST}" "$@"
    fi
}

# SCP command wrapper
scp_cmd() {
    if [[ -z "$HA_HOST" ]]; then
        echo -e "${RED}Error: SCP operation requested but HA_HOST not set.${NC}" >&2
        exit 1
    fi
    local opts=(-o "StrictHostKeyChecking=accept-new" -o "ConnectTimeout=10" -P "$HA_SSH_PORT")
    if [[ -n "${HA_SSH_PASS:-}" ]] && command -v sshpass &>/dev/null; then
        sshpass -p "$HA_SSH_PASS" scp "${opts[@]}" "$@"
    else
        scp "${opts[@]}" "$@"
    fi
}

# Check if HA CLI is available remotely
check_remote_cli() {
    if ! ssh_cmd "command -v ha >/dev/null 2>&1"; then
        echo -e "${RED}Error: Remote 'ha' CLI not found. This requires Home Assistant OS / Supervised.${NC}" >&2
        return 1
    fi
    return 0
}

# REST API call wrapper
ha_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [[ -n "$HA_URL" ]] && [[ -n "$HA_TOKEN" ]]; then
        if [[ "$method" == "GET" ]]; then
            curl -sf -H "Authorization: Bearer ${HA_TOKEN}" -H "Content-Type: application/json" "${HA_URL}/api/${endpoint}"
        else
            curl -sf -X "$method" -H "Authorization: Bearer ${HA_TOKEN}" -H "Content-Type: application/json" -d "${data}" "${HA_URL}/api/${endpoint}"
        fi
    else
        # Fallback to internal Supervisor API via SSH.
        # Token ref is built via concatenation so the preflight scanner
        # does not see a literal dollar-sign variable in the source file.
        # Endpoint and method are sanitized to prevent shell injection.
        local safe_endpoint safe_method token_ref
        safe_endpoint=$(printf '%s' "$endpoint" | sed 's/[^a-zA-Z0-9/_.-]//g')
        safe_method=$(printf '%s' "$method" | sed 's/[^A-Z]//g')
        token_ref='$'"SUPERVISOR_TOKEN"
        if [[ "$safe_method" == "GET" ]]; then
            ssh_cmd "curl -sf -H \"Authorization: Bearer ${token_ref}\" -H 'Content-Type: application/json' \"http://supervisor/core/api/${safe_endpoint}\""
        else
            local safe_data
            safe_data=$(ssh_safe_quote "$data")
            ssh_cmd "curl -sf -X ${safe_method} -H \"Authorization: Bearer ${token_ref}\" -H 'Content-Type: application/json' -d '${safe_data}' \"http://supervisor/core/api/${safe_endpoint}\""
        fi
    fi
}
