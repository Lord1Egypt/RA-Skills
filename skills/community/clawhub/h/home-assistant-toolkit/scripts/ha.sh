#!/usr/bin/env bash
#
# ha.sh — REST/SSH Home Assistant CLI for OpenClaw
#
# Security:
#   - ENV vars: HA_URL, HA_TOKEN, HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_CONFIG_PATH
#   - Endpoints: HA_URL/api/* (REST), SSH to HA_HOST (CLI/file ops)
#   - File access: reads config files under HA_CONFIG_PATH on remote HA instance
#   - No data sent to external services; all traffic stays between local machine and user's HA
#
# Usage:
#   ha.sh info                         # Test connection, show HA version
#   ha.sh list [domain]                # List entities
#   ha.sh search <query>               # Search entities by name
#   ha.sh state <entity_id>            # Get entity state
#   ha.sh on <entity_id> [brightness]  # Turn on
#   ha.sh off <entity_id>              # Turn off
#   ha.sh toggle <entity_id>           # Toggle
#   ha.sh scene <scene_name>           # Activate scene
#   ha.sh script <script_name>         # Run script
#   ha.sh climate <entity_id> <temp>   # Set temperature
#   ha.sh call <domain> <service> <json> # Call any service
#   ha.sh logs [core|supervisor]       # View logs
#   ha.sh check                        # Validate configuration
#   ha.sh restart                      # Restart HA core
#   ha.sh addons                       # List addons
#   ha.sh config <file>                # Read config file
#   ha.sh edit <file>                  # Edit config file (show content)
#   ha.sh scan                         # Full integration scan
#
# Configuration:
#   HA_URL, HA_TOKEN (for REST API, preferred)
#   HA_HOST, HA_SSH_PORT, HA_SSH_USER  (for SSH file operations)
#   HA_CONFIG_PATH                     (default: /config)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

if [[ -z "$HA_URL" ]] && [[ -z "$HA_HOST" ]]; then
    echo -e "${RED}Error: Must set either HA_URL/HA_TOKEN or HA_HOST/HA_SSH_PORT/HA_SSH_USER.${NC}" >&2
    exit 1
fi

ha_cli() {
    # Quote each argument safely for remote shell execution
    local quoted_args=""
    local arg
    for arg in "$@"; do
        local safe
        safe=$(ssh_safe_quote "$arg")
        quoted_args="${quoted_args} '${safe}'"
    done
    ssh_cmd "ha${quoted_args}"
}

# Note: ha_api is now defined in common.sh

cmd_info() {
    echo "=== Home Assistant Connection ==="
    if [[ -n "$HA_URL" ]]; then
        echo "Mode: External REST API (${HA_URL})"
        local c
        c=$(ha_api GET "config" || echo "")
        if [[ -n "$c" ]]; then
            echo ""
            echo "=== HA Core Info ==="
            echo "$c" | jq '{version: .version, name: .location_name, uuid: .uuid}'
        else
            echo "❌ Cannot connect via REST API." >&2
            exit 1
        fi
    else
        echo "Host: ${HA_SSH_USER}@${HA_HOST}:${HA_SSH_PORT}"
        echo ""
        echo "=== HA Core Info ==="
        ha_cli "core info" 2>/dev/null || { echo "❌ Cannot connect."; exit 1; }
        echo ""
        echo "=== Supervisor Info ==="
        ha_cli "supervisor info" 2>/dev/null | head -10 || true
    fi
}

cmd_updates() {
    echo "=== Comprehensive Update Check ===" >&2
    
    # 1. Fetch all states once for efficiency
    local entities
    entities=$(ha_api GET "states" || echo "")
    
    # Check Core & OS via entities (available in 2024+)
    echo -n "Core Update: " >&2
    local core_update
    core_update=$(echo "$entities" | jq -r '.[] | select(.entity_id == "update.home_assistant_core_update")' || echo "")
    if [[ $(echo "$core_update" | jq -r '.state') == "on" ]]; then
        echo -e "${YELLOW}Update available ($(echo "$core_update" | jq -r '.attributes.installed_version') -> $(echo "$core_update" | jq -r '.attributes.latest_version'))${NC}"
    else
        echo -e "${GREEN}Up to date.${NC}"
    fi

    echo -n "OS Update:   " >&2
    local os_update
    os_update=$(echo "$entities" | jq -r '.[] | select(.entity_id == "update.home_assistant_operating_system_update")' || echo "")
    if [[ $(echo "$os_update" | jq -r '.state') == "on" ]]; then
        echo -e "${YELLOW}Update available ($(echo "$os_update" | jq -r '.attributes.installed_version') -> $(echo "$os_update" | jq -r '.attributes.latest_version'))${NC}"
    else
        echo -e "${GREEN}Up to date.${NC}"
    fi

    # 2. Check Add-ons (Supervisor path)
    echo "" >&2
    echo "=== Add-on Updates (Supervisor) ===" >&2
    if [[ -n "$HA_HOST" ]]; then
        local raw_addons
        local sv_token_ref='$'"SUPERVISOR_TOKEN"
        raw_addons=$(ssh_cmd "curl -sf -H \"Authorization: Bearer ${sv_token_ref}\" http://supervisor/addons" 2>/dev/null || echo "")
        if [[ -n "$raw_addons" ]]; then
            local addon_updates
            addon_updates=$(echo "$raw_addons" | jq -r '.data.addons[] | select(.update_available == true) | "* \(.name) (\(.version) -> \(.available_version))"')
            if [[ -n "$addon_updates" ]]; then
                echo -e "${YELLOW}${addon_updates}${NC}"
            else
                echo -e "${GREEN}All add-ons up to date.${NC}"
            fi
        else
            echo "Skipped (Supervisor API error)" >&2
        fi
    else
        echo "Skipped (SSH/Host info not set)" >&2
    fi

    # 3. Check HACS & Other Custom Components (Entity path)
    echo "" >&2
    echo "=== Community & Custom Updates (HACS/Entities) ===" >&2
    if [[ -n "$entities" ]]; then
        local custom_updates
        custom_updates=$(echo "$entities" | jq -r '.[] | 
            select(.entity_id | startswith("update.")) | 
            select(.state == "on") | 
            select(.entity_id != "update.home_assistant_core_update" and .entity_id != "update.home_assistant_operating_system_update") |
            "* \(.attributes.friendly_name // .entity_id) (\(.attributes.installed_version // "?") -> \(.attributes.latest_version // "?"))"')
        
        if [[ -n "$custom_updates" ]]; then
            echo -e "${YELLOW}${custom_updates}${NC}"
        else
            echo -e "${GREEN}All custom components up to date.${NC}"
        fi
    else
        echo "Skipped (REST API connection failed)" >&2
    fi
}

cmd_list() {
    local domain="${1:-all}"
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then
        echo -e "${RED}Error: cannot fetch entity list from API.${NC}" >&2
        return 1
    fi

    if [[ "$domain" == "all" ]]; then
        echo "$states" | jq -r '.[].entity_id' | sort
    else
        case "$domain" in
            lights) domain="light" ;;
            switches) domain="switch" ;;
            sensors) domain="sensor" ;;
            covers) domain="cover" ;;
            automations) domain="automation" ;;
        esac
        echo "$states" | jq -r --arg d "$domain" \
            '.[] | select(.entity_id | startswith($d + ".")) | .entity_id' | sort
    fi
}

cmd_search() {
    local query="$1"
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then
        echo -e "${RED}Error: cannot fetch states from API.${NC}" >&2
        return 1
    fi
    echo "$states" | jq -r --arg q "$query" \
        '.[] | select(
            (.entity_id | ascii_downcase | contains($q | ascii_downcase)) or
            (.attributes.friendly_name // "" | ascii_downcase | contains($q | ascii_downcase))
        ) | "\(.entity_id)\t\(.attributes.friendly_name // "-")\t\(.state)"' | \
        column -t -s $'\t'
}

cmd_state() {
    validate_entity_id "$1"
    local result
    result=$(ha_api GET "states/$1" || echo "")
    if [[ -z "$result" ]]; then
        echo -e "${RED}Error: entity '$1' not found or API unreachable.${NC}" >&2
        return 1
    fi
    echo "$result" | jq -r '.state'
}

cmd_on() {
    local entity="$1"
    validate_entity_id "$entity"
    local brightness="${2:-}"
    local domain="${entity%%.*}"
    local data="{\"entity_id\": \"$entity\"}"
    if [[ -n "$brightness" ]] && [[ "$domain" == "light" ]]; then
        validate_number "$brightness" "brightness"
        data="{\"entity_id\": \"$entity\", \"brightness\": $brightness}"
    fi
    ha_api POST "services/${domain}/turn_on" "$data" > /dev/null
    echo "✅ $entity → on"
}

cmd_off() {
    local entity="$1"
    validate_entity_id "$entity"
    local domain="${entity%%.*}"
    ha_api POST "services/${domain}/turn_off" "{\"entity_id\": \"$entity\"}" > /dev/null
    echo "✅ $entity → off"
}

cmd_toggle() {
    local entity="$1"
    validate_entity_id "$entity"
    local domain="${entity%%.*}"
    ha_api POST "services/${domain}/toggle" "{\"entity_id\": \"$entity\"}" > /dev/null
    echo "✅ $entity → toggled"
}

cmd_scene() {
    local scene="$1"
    [[ "$scene" != scene.* ]] && scene="scene.$scene"
    validate_entity_id "$scene"
    ha_api POST "services/scene/turn_on" "{\"entity_id\": \"$scene\"}" > /dev/null
    echo "✅ $scene → activated"
}

cmd_script() {
    local script="$1"
    [[ "$script" != script.* ]] && script="script.$script"
    validate_entity_id "$script"
    ha_api POST "services/script/turn_on" "{\"entity_id\": \"$script\"}" > /dev/null
    echo "✅ $script → started"
}

cmd_climate() {
    validate_entity_id "$1"
    validate_number "$2" "temperature"
    ha_api POST "services/climate/set_temperature" \
        "{\"entity_id\": \"$1\", \"temperature\": $2}" > /dev/null
    echo "✅ $1 → ${2}°"
}

cmd_call() {
    local data="$3"
    if [[ -z "$data" ]]; then data='{}'; fi
    local result
    result=$(ha_api POST "services/${1}/${2}" "$data" || echo "")
    if [[ -n "$result" ]]; then
        echo "$result" | jq '.'
    fi
}

cmd_logs() {
    local target="${1:-core}"
    if [[ -n "$HA_URL" ]]; then
        ha_api GET "error_log" 2>/dev/null | tail -50 || echo "No logs available."
    else
        ha_cli "${target} logs" 2>/dev/null | tail -50
    fi
}

cmd_check() {
    echo "Validating configuration..." >&2
    if [[ -n "$HA_URL" ]]; then
        ha_api POST "config/core/check_config"
    else
        # Force JSON output even in CLI mode for parsing consistency
        ha_cli "core check --format json"
    fi
}

cmd_restart() {
    echo "Restarting Home Assistant Core..." >&2
    if [[ -n "$HA_URL" ]]; then
        ha_api POST "services/homeassistant/restart" > /dev/null
        echo -e "${GREEN}✅ Restart initiated.${NC}" >&2
    else
        ha_cli "core restart"
    fi
}

cmd_addons() {
    if [[ -n "$HA_URL" ]]; then
        # Try SSH fallback if available
        if [[ -n "$HA_HOST" ]]; then
            echo -e "${YELLOW}REST API: Addons not directly supported. Attempting SSH/Supervisor API fallback...${NC}" >&2
            local raw sv_token_ref='$'"SUPERVISOR_TOKEN"
            raw=$(ssh_cmd "curl -sf -H \"Authorization: Bearer ${sv_token_ref}\" -H \"Content-Type: application/json\" http://supervisor/addons")
            if [[ -n "$raw" ]]; then
                echo "$raw" | jq -r '.data.addons[] | "* \(.name) (\(.version)) [\(.state)]"' | sort
            else
                echo -e "${RED}Error: Failed to fetch addons via SSH fallback.${NC}" >&2
            fi
        else
            echo -e "${RED}Error: Addons list is not supported via REST API (requires Supervisor/SSH).${NC}" >&2
        fi
    else
        ha_cli "addons list" 2>/dev/null
    fi
}

cmd_config() {
    local file="${1:-configuration.yaml}"
    validate_config_path "$file"
    ssh_cmd "cat '${HA_CONFIG_PATH}/${file}'"
}

cmd_edit() {
    local file="${1:-configuration.yaml}"
    validate_config_path "$file"
    echo "=== ${HA_CONFIG_PATH}/${file} ==="
    ssh_cmd "cat '${HA_CONFIG_PATH}/${file}'"
    echo ""
    echo "(To edit: ssh -p ${HA_SSH_PORT} ${HA_SSH_USER}@${HA_HOST} nano '${HA_CONFIG_PATH}/${file}')"
}

cmd_scan() {
    echo "Scanning HA integrations (using scan_integrations.py)..." >&2
    if [[ -n "$HA_URL" ]] || [[ -n "$HA_HOST" ]]; then
        # scan_integrations.py reads HA_URL/HA_TOKEN/HA_HOST from env vars
        python3 "$SCRIPT_DIR/scan_integrations.py"
    else
        echo -e "${RED}Error: Set HA_URL/HA_TOKEN or HA_HOST for scanning.${NC}" >&2
        return 1
    fi
}

cmd_get() {
    local endpoint="$1"
    ha_api GET "$endpoint"
}

# Main
case "${1:-help}" in
    info)     cmd_info ;;
    get)      cmd_get "${2:?Usage: ha.sh get <endpoint>}" ;;
    list)     cmd_list "${2:-all}" ;;
    search)   cmd_search "${2:?Usage: ha.sh search <query>}" ;;
    state)    cmd_state "${2:?Usage: ha.sh state <entity_id>}" ;;
    on)       cmd_on "${2:?Usage: ha.sh on <entity_id>}" "${3:-}" ;;
    off)      cmd_off "${2:?Usage: ha.sh off <entity_id>}" ;;
    toggle)   cmd_toggle "${2:?Usage: ha.sh toggle <entity_id>}" ;;
    scene)    cmd_scene "${2:?Usage: ha.sh scene <name>}" ;;
    script)   cmd_script "${2:?Usage: ha.sh script <name>}" ;;
    climate)  cmd_climate "${2:?entity_id}" "${3:?temp}" ;;
    call)     cmd_call "${2:?domain}" "${3:?service}" "${4:-}" ;;
    updates)  cmd_updates ;;
    logs)     cmd_logs "${2:-core}" ;;
    check)    cmd_check ;;
    restart)  cmd_restart ;;
    addons)   cmd_addons ;;
    config)   cmd_config "${2:-configuration.yaml}" ;;
    edit)     cmd_edit "${2:-configuration.yaml}" ;;
    scan)     cmd_scan ;;
    *)
        cat << 'USAGE'
ha.sh — REST/SSH Home Assistant CLI for OpenClaw

Device Control (Uses REST API if HA_URL is set):
  ha.sh on <entity_id> [brightness]   Turn on
  ha.sh off <entity_id>               Turn off
  ha.sh toggle <entity_id>            Toggle
  ha.sh scene <name>                  Activate scene
  ha.sh script <name>                 Run script
  ha.sh climate <entity_id> <temp>    Set temperature
  ha.sh call <domain> <svc> [json]    Call any service

Queries:
  ha.sh list [domain]                 List entities
  ha.sh search <query>                Search by name
  ha.sh state <entity_id>             Get state value
  ha.sh get <endpoint>                Raw GET API endpoint

System:
  ha.sh info                          Connection + version info
  ha.sh updates                       Check all updates (Core, OS, Addons, HACS)
  ha.sh logs [core|supervisor]        View logs
  ha.sh check                         Validate config
  ha.sh restart                       Restart HA Core
  ha.sh addons                        List addons
  ha.sh config [file]                 Read config file (Uses SSH)
  ha.sh scan                          Scan integrations

Config via ENV Vars:
  HA_URL, HA_TOKEN, HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_CONFIG_PATH
USAGE
        ;;
esac
