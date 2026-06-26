#!/bin/bash
# Control Home Assistant climate entities

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$HOME/.openclaw/credentials/homeassistant.json"

# Parse credentials
URL=$(jq -r '.url' "$CREDENTIALS_FILE")
TOKEN=$(jq -r '.token' "$CREDENTIALS_FILE")

COMMAND="${1:-help}"
ENTITY="${2:-}"
VALUE="${3:-}"
MODE="${4:-}"

show_help() {
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  set <entity> <temp> [mode]  Set temperature (mode: cool/heat/auto, auto-detects if omitted)"
    echo "  mode <entity> <mode>        Set HVAC mode (cool/heat/auto/off)"
    echo "  status <entity> [json]     Get current state"
    echo ""
    echo "Examples:"
    echo "  $0 set climate.living_room 73 cool"
    echo "  $0 set climate.living_room 73        # Auto-detects cool/heat"
    echo "  $0 mode climate.living_room off"
    echo "  $0 status climate.living_room"
}

get_current_temp() {
    local entity="$1"
    curl -s -X GET "${URL}/api/states/${entity}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" | jq -r '.attributes.current_temperature // "unknown"'
}

get_current_mode() {
    local entity="$1"
    curl -s -X GET "${URL}/api/states/${entity}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" | jq -r '.state'
}

set_temperature() {
    local entity="$1"
    local temp="$2"
    local mode="$3"

    # Get current temp if mode not specified
    if [[ -z "$mode" ]]; then
        CURRENT=$(get_current_temp "$entity")
        if [[ "$CURRENT" != "unknown" && -n "$CURRENT" ]]; then
            # If target is lower than current, use cool; if higher, use heat
            if (( $(echo "$temp < $CURRENT" | bc -l) )); then
                mode="cool"
            else
                mode="heat"
            fi
        else
            mode="cool"  # Default to cool
        fi
    fi

    echo "Setting ${entity} to ${temp}°F (${mode} mode)..."

    # Set temperature and mode
    PAYLOAD=$(jq -n \
        --arg entity "$entity" \
        --argjson temp "$temp" \
        --arg mode "$mode" \
        '{"entity_id": $entity, "temperature": $temp, "hvac_mode": $mode}')

    RESPONSE=$(curl -s -X POST "${URL}/api/services/climate/set_temperature" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD")

    if echo "$RESPONSE" | jq -e '.[0]' > /dev/null 2>&1; then
        echo "✓ Temperature set to ${temp}°F, mode: ${mode}"
    else
        echo "✗ Failed to set temperature"
        echo "$RESPONSE" | jq -r '.error // .message // "Unknown error"'
    fi
}

set_mode() {
    local entity="$1"
    local mode="$2"

    echo "Setting ${entity} to ${mode} mode..."

    PAYLOAD=$(jq -n \
        --arg entity "$entity" \
        --arg mode "$mode" \
        '{"entity_id": $entity, "hvac_mode": $mode}')

    RESPONSE=$(curl -s -X POST "${URL}/api/services/climate/set_hvac_mode" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD")

    if echo "$RESPONSE" | jq -e '.[0]' > /dev/null 2>&1; then
        echo "✓ Mode set to ${mode}"
    else
        echo "✗ Failed to set mode"
        echo "$RESPONSE" | jq -r '.error // .message // "Unknown error"'
    fi
}

get_status() {
    local entity="$1"
    local format="${2:-table}"

    RESPONSE=$(curl -s -X GET "${URL}/api/states/${entity}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")

    if [[ "$format" == "json" ]]; then
        echo "$RESPONSE" | jq '.'
    else
        FRIENDLY_NAME=$(echo "$RESPONSE" | jq -r '.attributes.friendly_name // .entity_id')
        CURRENT=$(echo "$RESPONSE" | jq -r '.attributes.current_temperature // "N/A"')
        TARGET=$(echo "$RESPONSE" | jq -r '.attributes.temperature // .attributes.target_temp_high // "N/A"')
        MODE=$(echo "$RESPONSE" | jq -r '.state')
        UNIT=$(echo "$RESPONSE" | jq -r '.attributes.temperature_unit // "°F"')
        HUMIDITY=$(echo "$RESPONSE" | jq -r '.attributes.current_humidity // "N/A"')

        echo "┌─────────────────────────────────────────┐"
        echo "│ ${FRIENDLY_NAME}"
        echo "├─────────────────────────────────────────┤"
        echo "│ Mode:      ${MODE}"
        echo "│ Current:   ${CURRENT}${UNIT}"
        echo "│ Target:    ${TARGET}${UNIT}"
        [[ "$HUMIDITY" != "N/A" ]] && echo "│ Humidity:  ${HUMIDITY}%"
        echo "└─────────────────────────────────────────┘"
    fi
}

case "$COMMAND" in
    set)
        [[ -z "$ENTITY" || -z "$VALUE" ]] && { show_help; exit 1; }
        set_temperature "$ENTITY" "$VALUE" "$MODE"
        ;;
    mode)
        [[ -z "$ENTITY" || -z "$VALUE" ]] && { show_help; exit 1; }
        set_mode "$ENTITY" "$VALUE"
        ;;
    status)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        get_status "$ENTITY" "$VALUE"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac