#!/usr/bin/env bash
#
# ha-dashboard.sh — Generate and manage HA dashboard configurations
#
# Security:
#   - ENV vars: HA_URL, HA_TOKEN, HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_CONFIG_PATH
#   - Endpoints: SSH to HA_HOST (file ops)
#   - File access: reads/writes .storage/lovelace* and ui-lovelace.yaml on remote HA
#   - Creates timestamped backups before any write operation
#   - No data sent to external services
#
# Usage:
#   ha-dashboard.sh list                     # List existing dashboards
#   ha-dashboard.sh show <dashboard>          # Show dashboard YAML
#   ha-dashboard.sh entities <domain>         # List entities for card creation
#   ha-dashboard.sh generate-view <area>      # Generate a view for an area
#   ha-dashboard.sh apply <file.yaml>         # Upload dashboard config
#   ha-dashboard.sh backup                    # Backup current dashboards

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Note: ha_api is now defined in common.sh

cmd_list() {
    echo "=== Dashboards ==="
    echo "Checking ${HA_CONFIG_PATH}/.storage/ for dashboard configs..."
    ssh_cmd "ls -1 ${HA_CONFIG_PATH}/.storage/lovelace* 2>/dev/null" || echo "No custom dashboards found."
    echo ""
    echo "Default dashboard:"
    ssh_cmd "ls -la ${HA_CONFIG_PATH}/ui-lovelace.yaml 2>/dev/null" || echo "  Using auto-generated (no ui-lovelace.yaml)"
}

cmd_show() {
    local dashboard="${1:-}"
    if [[ -z "$dashboard" ]] || [[ "$dashboard" == "default" ]]; then
        echo "=== Default Dashboard ==="
        ssh_cmd "cat ${HA_CONFIG_PATH}/.storage/lovelace 2>/dev/null" | \
            python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin).get('data',{}).get('config',{}), indent=2))" 2>/dev/null || \
            ssh_cmd "cat ${HA_CONFIG_PATH}/ui-lovelace.yaml 2>/dev/null" || \
            echo "No dashboard config found."
    else
        echo "=== Dashboard: $dashboard ==="
        ssh_cmd "cat ${HA_CONFIG_PATH}/.storage/lovelace.${dashboard} 2>/dev/null" | \
            python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin).get('data',{}).get('config',{}), indent=2))" 2>/dev/null || \
            echo "Dashboard '$dashboard' not found."
    fi
}

cmd_entities() {
    local domain="${1:-light}"
    case "$domain" in
        lights) domain="light" ;;
        switches) domain="switch" ;;
        sensors) domain="sensor" ;;
        covers) domain="cover" ;;
        climates) domain="climate" ;;
        cameras) domain="camera" ;;
    esac
    echo "=== ${domain}.* entities ==="
    # Rely on ha.sh list or direct api call. Wait, ha.sh doesnt output friendly name in list, 
    # but we can use ha.sh search ".*" and filter. Or just use ha_api equivalent directly.
    # We will use `$SCRIPT_DIR/ha.sh list $domain` as closest match. 
    # Since we dropped direct `ha_api` from here, we will use internal `search` with blank if possible.
    # Let's bypass to `ha.sh state` ? ha.sh `list` is easier.
    "$SCRIPT_DIR/ha.sh" list "$domain"
}

cmd_generate_view() {
    local area="$1"
    echo "Generating view for area: $area"
    echo "Fetching entities..."

    # In refactored mode, getting states requires going through ha.sh search.
    # Since ha.sh doesn't export ha_api, we can't fetch all raw JSON easily from here.
    # We will use `ha.sh search` which outputs TSV: entity_id, friendly_name, state
    local entities
    entities=$("$SCRIPT_DIR/ha.sh" search "$area" 2>/dev/null | awk '{print $1}' || echo "")

    if [[ -z "$entities" ]]; then
        echo "No entities found matching area '$area'."
        echo "Tip: entities are matched by friendly_name. Check your entity names."
        return 1
    fi

    echo ""
    echo "# Generated view for: $area"
    echo "# Copy this into your dashboard YAML or use as reference"
    echo ""
    echo "title: ${area^}"
    echo "path: $(echo "$area" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
    echo "cards:"

    local lights switches sensors climates others
    lights=$(echo "$entities" | grep "^light\." || true)
    switches=$(echo "$entities" | grep "^switch\." || true)
    sensors=$(echo "$entities" | grep "^sensor\.\|^binary_sensor\." || true)
    climates=$(echo "$entities" | grep "^climate\." || true)
    others=$(echo "$entities" | grep -v "^light\.\|^switch\.\|^sensor\.\|^binary_sensor\.\|^climate\." || true)

    if [[ -n "$lights" ]]; then
        echo "  - type: entities"
        echo "    title: Lights"
        echo "    entities:"
        echo "$lights" | while read -r e; do echo "      - entity: $e"; done
    fi

    if [[ -n "$switches" ]]; then
        echo "  - type: entities"
        echo "    title: Switches"
        echo "    entities:"
        echo "$switches" | while read -r e; do echo "      - entity: $e"; done
    fi

    if [[ -n "$climates" ]]; then
        echo "  - type: thermostat"
        echo "    entity: $(echo "$climates" | head -1)"
    fi

    if [[ -n "$sensors" ]]; then
        echo "  - type: entities"
        echo "    title: Sensors"
        echo "    entities:"
        echo "$sensors" | while read -r e; do echo "      - entity: $e"; done
    fi

    if [[ -n "$others" ]]; then
        echo "  - type: entities"
        echo "    title: Other"
        echo "    entities:"
        echo "$others" | while read -r e; do echo "      - entity: $e"; done
    fi
}

cmd_apply() {
    local yaml_file="$1"
    echo -e "${YELLOW}⚠️  WARNING: This will upload a dashboard config to HA.${NC}"
    echo "    File: $yaml_file"
    echo ""
    
    # Check for .storage/lovelace which indicates UI-managed mode
    if ssh_cmd "[ -f ${HA_CONFIG_PATH}/.storage/lovelace ]"; then
        echo -e "${RED}⚠️  CRITICAL NOTICE: Found .storage/lovelace.${NC}"
        echo -e "${YELLOW}Home Assistant is currently in UI-managed mode.${NC}"
        echo -e "${YELLOW}Applying changes to ui-lovelace.yaml will have NO EFFECT unless:${NC}"
        echo "1. You have 'mode: yaml' set in your configuration.yaml under 'lovelace:'"
        echo "2. You or the user manually switch the dashboard to YAML mode in the UI."
        echo ""
        echo "Use 'ha-dashboard.sh backup' before proceeding if you are unsure."
        echo ""
    fi

    echo "Backing up current dashboard..."
    ssh_cmd "cp ${HA_CONFIG_PATH}/ui-lovelace.yaml ${HA_CONFIG_PATH}/ui-lovelace.yaml.bak.\$(date +%Y%m%d_%H%M%S) 2>/dev/null" || true
    
    echo "Uploading to ui-lovelace.yaml..."
    cat "$yaml_file" | ssh_cmd "cat > ${HA_CONFIG_PATH}/ui-lovelace.yaml"
    echo -e "${GREEN}✅ Dashboard uploaded. Refresh browser and ensure YAML mode is enabled to see changes.${NC}"
}

cmd_backup() {
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    ssh_cmd "cp ${HA_CONFIG_PATH}/.storage/lovelace ${HA_CONFIG_PATH}/.storage/lovelace.bak.${ts} 2>/dev/null" || true
    ssh_cmd "cp ${HA_CONFIG_PATH}/ui-lovelace.yaml ${HA_CONFIG_PATH}/ui-lovelace.yaml.bak.${ts} 2>/dev/null" || true
    echo "✅ Dashboard backup created (${ts})"
}

case "${1:-help}" in
    list)           cmd_list ;;
    show)           cmd_show "${2:-default}" ;;
    entities)       cmd_entities "${2:-light}" ;;
    generate-view)  cmd_generate_view "${2:?area name required}" ;;
    apply)          cmd_apply "${2:?yaml file required}" ;;
    backup)         cmd_backup ;;
    *)
        echo "ha-dashboard.sh — Dashboard management"
        echo ""
        echo "  list                      List dashboards"
        echo "  show [name]               Show dashboard config"
        echo "  entities <domain>         List entities for cards"
        echo "  generate-view <area>      Generate view YAML for area"
        echo "  apply <file.yaml>         Upload dashboard config"
        echo "  backup                    Backup dashboards"
        ;;
esac
