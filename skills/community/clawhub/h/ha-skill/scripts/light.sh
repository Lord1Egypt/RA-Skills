#!/bin/bash
# Control Home Assistant light entities

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$HOME/.openclaw/credentials/homeassistant.json"

# Parse credentials
URL=$(jq -r '.url' "$CREDENTIALS_FILE")
TOKEN=$(jq -r '.token' "$CREDENTIALS_FILE")

COMMAND="${1:-help}"
ENTITY="${2:-}"
VALUE="${3:-}"

show_help() {
    echo "Usage: $0 <command> <entity> [args]"
    echo ""
    echo "Commands:"
    echo "  on <entity>                     Turn on"
    echo "  off <entity>                    Turn off"
    echo "  toggle <entity>                 Toggle"
    echo "  brightness <entity> <0-255>     Set brightness"
    echo "  color <entity> <r> <g> <b>      Set RGB color"
    echo "  status <entity> [json]          Get current state"
    echo ""
    echo "Examples:"
    echo "  $0 on light.living_room"
    echo "  $0 brightness light.living_room 128"
    echo "  $0 color light.living_room 255 0 0"
}

call_service() {
    local domain="$1"
    local service="$2"
    local entity="$3"
    local data="$4"

    PAYLOAD="{\"entity_id\": \"${entity}\""
    [[ -n "$data" ]] && PAYLOAD=$(echo "$PAYLOAD" | sed "s/}$/, $data}/")
    PAYLOAD="$PAYLOAD"

    curl -s -X POST "${URL}/api/services/${domain}/${service}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" | jq -e '.[0]' > /dev/null 2>&1
}

light_on() {
    local entity="$1"
    if call_service "light" "turn_on" "$entity"; then
        echo "✓ ${entity} turned on"
    else
        echo "✗ Failed to turn on ${entity}"
    fi
}

light_off() {
    local entity="$1"
    if call_service "light" "turn_off" "$entity"; then
        echo "✓ ${entity} turned off"
    else
        echo "✗ Failed to turn off ${entity}"
    fi
}

light_toggle() {
    local entity="$1"
    if call_service "light" "toggle" "$entity"; then
        echo "✓ ${entity} toggled"
    else
        echo "✗ Failed to toggle ${entity}"
    fi
}

set_brightness() {
    local entity="$1"
    local brightness="$2"

    if [[ "$brightness" -lt 0 || "$brightness" -gt 255 ]]; then
        echo "✗ Brightness must be 0-255"
        exit 1
    fi

    PAYLOAD="{\"entity_id\": \"${entity}\", \"brightness\": ${brightness}}"

    RESPONSE=$(curl -s -X POST "${URL}/api/services/light/turn_on" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD")

    if echo "$RESPONSE" | jq -e '.[0]' > /dev/null 2>&1; then
        echo "✓ ${entity} brightness set to ${brightness}"
    else
        echo "✗ Failed to set brightness"
    fi
}

set_color() {
    local entity="$1"
    local r="$2"
    local g="$3"
    local b="$4"

    PAYLOAD="{\"entity_id\": \"${entity}\", \"rgb_color\": [${r}, ${g}, ${b}]}"

    RESPONSE=$(curl -s -X POST "${URL}/api/services/light/turn_on" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD")

    if echo "$RESPONSE" | jq -e '.[0]' > /dev/null 2>&1; then
        echo "✓ ${entity} color set to RGB(${r}, ${g}, ${b})"
    else
        echo "✗ Failed to set color"
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
        STATE=$(echo "$RESPONSE" | jq -r '.state')
        BRIGHTNESS=$(echo "$RESPONSE" | jq -r '.attributes.brightness // "N/A"')
        COLOR=$(echo "$RESPONSE" | jq -r '.attributes.rgb_color // empty')

        echo "┌─────────────────────────────────────────┐"
        echo "│ ${FRIENDLY_NAME}"
        echo "├─────────────────────────────────────────┤"
        echo "│ State:     ${STATE}"
        [[ "$BRIGHTNESS" != "N/A" ]] && echo "│ Brightness: ${BRIGHTNESS}/255"
        [[ -n "$COLOR" ]] && echo "│ RGB:       ${COLOR}"
        echo "└─────────────────────────────────────────┘"
    fi
}

case "$COMMAND" in
    on)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        light_on "$ENTITY"
        ;;
    off)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        light_off "$ENTITY"
        ;;
    toggle)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        light_toggle "$ENTITY"
        ;;
    brightness)
        [[ -z "$ENTITY" || -z "$VALUE" ]] && { show_help; exit 1; }
        set_brightness "$ENTITY" "$VALUE"
        ;;
    color)
        [[ -z "$ENTITY" || -z "$VALUE" || -z "$4" || -z "$5" ]] && { show_help; exit 1; }
        set_color "$ENTITY" "$VALUE" "$4" "$5"
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