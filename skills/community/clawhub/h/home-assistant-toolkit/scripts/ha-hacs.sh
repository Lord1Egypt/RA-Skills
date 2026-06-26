#!/usr/bin/env bash
#
# ha-hacs.sh — HACS custom component management via SSH
#
# Security:
#   - ENV vars: HA_URL, HA_TOKEN, HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_CONFIG_PATH
#   - Endpoints: HA_URL/api/states, HA_URL/api/error_log (REST), SSH to HA_HOST (file listing)
#   - File access: reads custom_components/ and .storage/hacs.repositories on remote HA
#   - No data sent to external services
#
# Usage:
#   ha-hacs.sh list                    # List installed HACS integrations
#   ha-hacs.sh updates                 # Check for available updates
#   ha-hacs.sh installed               # Show installed with versions
#   ha-hacs.sh repos                   # List HACS repositories
#   ha-hacs.sh logs                    # HACS-related logs

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Note: ha_api is now defined in common.sh

cmd_list() {
    echo "=== HACS Custom Components ===" >&2
    ssh_cmd "ls -1 ${HA_CONFIG_PATH}/custom_components/ 2>/dev/null" || echo "No custom components found."
}

cmd_installed() {
    echo "=== Installed Custom Components (with versions) ===" >&2
    ssh_cmd 'for d in '"${HA_CONFIG_PATH}"'/custom_components/*/; do
        name=$(basename "$d")
        manifest="$d/manifest.json"
        if [ -f "$manifest" ]; then
            version=$(cat "$manifest" | python3 -c "import sys,json; print(json.load(sys.stdin).get(\"version\",\"?\"))" 2>/dev/null || echo "?")
            domain=$(cat "$manifest" | python3 -c "import sys,json; print(json.load(sys.stdin).get(\"domain\",\"?\"))" 2>/dev/null || echo "?")
            echo "$name  v$version  ($domain)"
        else
            echo "$name  (no manifest)"
        fi
    done' 2>/dev/null | column -t
}

cmd_updates() {
    echo "=== HACS Update Status ===" >&2
    # Fetch all states and filter for update.* entities where state is 'on'
    local updates
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then echo -e "${RED}API error${NC}" >&2; return 1; fi
    updates=$(echo "$states" | jq -r '.[] |
        select(.entity_id | startswith("update.")) | 
        select(.state == "on") | 
        "\(.entity_id)\t\(.attributes.installed_version // "?") -> \(.attributes.latest_version // "?")\t\(.attributes.friendly_name // "-")"')
    
    if [[ -n "$updates" ]]; then
        echo -e "${updates}" | column -t -s $'\t'
    else
        echo "✅ All HACS components are up to date."
    fi
}

cmd_repos() {
    echo "=== HACS Repositories (from filesystem) ===" >&2
    ssh_cmd 'if [ -f '"${HA_CONFIG_PATH}"'/.storage/hacs.repositories ]; then
        cat '"${HA_CONFIG_PATH}"'/.storage/hacs.repositories | python3 -c "
import sys, json
data = json.load(sys.stdin)
repos = data.get(\"data\", {}).get(\"repositories\", data.get(\"repositories\", []))
if isinstance(repos, dict):
    repos = list(repos.values())
for r in repos[:50]:
    if isinstance(r, dict):
        name = r.get(\"full_name\", r.get(\"name\", \"?\"))
        cat = r.get(\"category\", \"?\")
        installed = r.get(\"installed\", False)
        if installed:
            print(f\"{name}  [{cat}]  installed\")
" 2>/dev/null
    else
        echo "HACS storage file not found."
    fi'
}

cmd_logs() {
    echo "=== HACS-related Logs ==="
    ha_api GET "error_log" | grep -i "hacs\|custom_components" || echo "No HACS logs found recently."
}

case "${1:-help}" in
    list)       cmd_list ;;
    installed)  cmd_installed ;;
    updates)    cmd_updates ;;
    repos)      cmd_repos ;;
    logs)       cmd_logs ;;
    *)
        echo "ha-hacs.sh — HACS management"
        echo ""
        echo "  list          Custom components directories"
        echo "  installed     Components with versions"
        echo "  updates       Pending updates"
        echo "  repos         HACS repositories"
        echo "  logs          HACS-related logs"
        ;;
esac
