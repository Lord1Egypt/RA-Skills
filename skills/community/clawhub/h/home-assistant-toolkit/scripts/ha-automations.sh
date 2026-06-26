#!/usr/bin/env bash
#
# ha-automations.sh — Create, edit, list, delete HA automations
#
# Security:
#   - ENV vars: HA_URL, HA_TOKEN, HA_HOST, HA_SSH_PORT, HA_SSH_USER, HA_CONFIG_PATH
#   - Endpoints: HA_URL/api/* (REST), SSH to HA_HOST (file ops)
#   - File access: reads/writes automations.yaml under HA_CONFIG_PATH on remote HA
#   - Creates timestamped backups before any write operation
#   - No data sent to external services
#
# Usage:
#   ha-automations.sh list                          # List all automations
#   ha-automations.sh show <automation_id>           # Show automation YAML
#   ha-automations.sh create <file.yaml>             # Append automation from file
#   ha-automations.sh create-inline '<yaml>'         # Append automation from string
#   ha-automations.sh enable <entity_id>             # Enable automation
#   ha-automations.sh disable <entity_id>            # Disable automation
#   ha-automations.sh trigger <entity_id>            # Trigger automation manually
#   ha-automations.sh reload                         # Reload automations from YAML
#   ha-automations.sh validate                       # Check config validity
#   ha-automations.sh backup                         # Backup automations.yaml before edit

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Main logic

cmd_list() {
    echo "=== Automations ==="
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then echo -e "${RED}Error: cannot fetch states.${NC}" >&2; return 1; fi
    echo "$states" | jq -r '.[] | select(.entity_id | startswith("automation.")) | .entity_id' | sort
    echo ""
    echo "Tip: to see YAML, use 'ha-automations.sh show <id>'"
}

cmd_show() {
    local input_id="$1"
    local search_id="$input_id"

    # If it looks like an entity_id (starts with automation.), resolve its internal ID
    if [[ "$input_id" == automation.* ]]; then
        echo "Resolving entity $input_id..." >&2
        local resolved_id
        resolved_id=$(ha_api GET "states/$input_id" 2>/dev/null | jq -r '.attributes.id // empty' 2>/dev/null || echo "")
        if [[ -n "$resolved_id" ]] && [[ "$resolved_id" != "null" ]]; then
            echo "Resolved ID: $resolved_id" >&2
            search_id="$resolved_id"
        fi
    fi

    # Get the YAML content and extract precisely one automation block locally
    # to avoid SSH escaping issues with complex awk scripts.
    # automations.yaml format: "- id: '12345'" starts a block at column 0,
    # continuation lines are indented with 2+ spaces.
    ssh_cmd "cat ${HA_CONFIG_PATH}/automations.yaml" | awk -v id="${search_id}" '
        /^- / {
            if (found) { printf "%s", block; printed = 1; exit }
            block = $0 "\n"
            in_block = 1
            if ($0 ~ "id:.*" id) found = 1
            next
        }
        in_block && /^  / {
            block = block $0 "\n"
            if ($0 ~ "id:.*" id) found = 1
            next
        }
        in_block && /^[^ ]/ {
            if (found) { printf "%s", block; printed = 1; exit }
            in_block = 0
        }
        END { if (found && !printed) printf "%s", block }
    '
}

cmd_create() {
    local yaml_file="$1"
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    echo "Backing up automations.yaml..." >&2
    ssh_cmd "cp ${HA_CONFIG_PATH}/automations.yaml ${HA_CONFIG_PATH}/automations.yaml.bak.${ts}"
    echo "Appending automation..." >&2
    ssh_cmd "cat >> ${HA_CONFIG_PATH}/automations.yaml" < "$yaml_file"
    
    echo "Validating..." >&2
    if ha_api POST "config/core/check_config" | jq -e '.result == "valid"' >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Config valid. Reloading...${NC}" >&2
        ha_api POST "services/automation/reload" "{}" >/dev/null
        echo -e "${GREEN}✅ Automations reloaded.${NC}" >&2
    else
        echo -e "${RED}❌ Config invalid! Restoring backup...${NC}" >&2
        # Use a single remote command to find and restore the latest backup
        ssh_cmd "bash -c 'latest=\$(ls -t ${HA_CONFIG_PATH}/automations.yaml.bak.* | head -1); if [ -n \"\$latest\" ]; then cp \"\$latest\" ${HA_CONFIG_PATH}/automations.yaml; echo \"Restored from \$latest\"; else echo \"No backup found!\"; fi'"
        exit 1
    fi
}

cmd_create_inline() {
    local yaml_content="$1"
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    echo "Backing up automations.yaml..." >&2
    ssh_cmd "cp ${HA_CONFIG_PATH}/automations.yaml ${HA_CONFIG_PATH}/automations.yaml.bak.${ts}"
    echo "Appending automation..." >&2
    echo "$yaml_content" | ssh_cmd "cat >> ${HA_CONFIG_PATH}/automations.yaml"
    
    echo "Validating..." >&2
    if ha_api POST "config/core/check_config" | jq -e '.result == "valid"' >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Config valid. Reloading...${NC}" >&2
        ha_api POST "services/automation/reload" "{}" >/dev/null
        echo -e "${GREEN}✅ Automations reloaded.${NC}" >&2
    else
        echo -e "${RED}❌ Config invalid! Check YAML syntax. Restoring...${NC}" >&2
        ssh_cmd "bash -c 'latest=\$(ls -t ${HA_CONFIG_PATH}/automations.yaml.bak.* | head -1); if [ -n \"\$latest\" ]; then cp \"\$latest\" ${HA_CONFIG_PATH}/automations.yaml; echo \"Restored from \$latest\"; else echo \"No backup found!\"; fi'"
        exit 1
    fi
}

cmd_enable() {
    validate_entity_id "$1"
    ha_api POST "services/automation/turn_on" "{\"entity_id\": \"$1\"}" >/dev/null
    echo -e "${GREEN}✅ $1 enabled${NC}" >&2
}

cmd_disable() {
    validate_entity_id "$1"
    ha_api POST "services/automation/turn_off" "{\"entity_id\": \"$1\"}" >/dev/null
    echo -e "${GREEN}✅ $1 disabled${NC}" >&2
}

cmd_trigger() {
    validate_entity_id "$1"
    ha_api POST "services/automation/trigger" "{\"entity_id\": \"$1\"}" >/dev/null
    echo -e "${GREEN}✅ $1 triggered${NC}" >&2
}

cmd_reload() {
    ha_api POST "services/automation/reload" "{}" >/dev/null
    echo -e "${GREEN}✅ Automations reloaded.${NC}" >&2
}

cmd_validate() {
    ha_api POST "config/core/check_config"
}

cmd_backup() {
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    ssh_cmd "cp ${HA_CONFIG_PATH}/automations.yaml ${HA_CONFIG_PATH}/automations.yaml.bak.${ts}"
    echo "✅ Backup: ${HA_CONFIG_PATH}/automations.yaml.bak.${ts}"
}

case "${1:-help}" in
    list)           cmd_list ;;
    show)           cmd_show "${2:?automation_id required}" ;;
    create)         cmd_create "${2:?yaml file required}" ;;
    create-inline)  cmd_create_inline "${2:?yaml string required}" ;;
    enable)         cmd_enable "${2:?entity_id required}" ;;
    disable)        cmd_disable "${2:?entity_id required}" ;;
    trigger)        cmd_trigger "${2:?entity_id required}" ;;
    reload)         cmd_reload ;;
    validate)       cmd_validate ;;
    backup)         cmd_backup ;;
    *)
        echo "ha-automations.sh — Manage HA automations"
        echo ""
        echo "  list                        List all automations"
        echo "  show <id>                   Show automation YAML"
        echo "  create <file.yaml>          Add automation from file"
        echo "  create-inline '<yaml>'      Add automation inline"
        echo "  enable <entity_id>          Enable"
        echo "  disable <entity_id>         Disable"
        echo "  trigger <entity_id>         Trigger manually"
        echo "  reload                      Reload from YAML"
        echo "  validate                    Check config"
        echo "  backup                      Backup automations.yaml"
        ;;
esac
