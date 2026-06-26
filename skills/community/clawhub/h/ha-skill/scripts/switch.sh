#!/bin/bash
# Control Home Assistant switch entities

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$HOME/.openclaw/credentials/homeassistant.json"

# Parse credentials
URL=$(jq -r '.url' "$CREDENTIALS_FILE")
TOKEN=$(jq -r '.token' "$CREDENTIALS_FILE")

COMMAND="${1:-help}"
ENTITY="${2:-}"

show_help() {
    echo "Usage: $0 <command> <entity>"
    echo ""
    echo "Commands:"
    echo "  on <entity>         Turn on"
    echo "  off <entity>        Turn off"
    echo "  toggle <entity>     Toggle"
    echo "  status <entity>     Get current state"
    echo ""
    echo "Examples:"
    echo "  $0 on switch.bedroom_fan"
    echo "  $0 toggle switch.kitchen_light"
}

call_service() {
    local domain="$1"
    local service="$2"
    local entity="$3"

    curl -s -X POST "${URL}/api/services/${domain}/${service}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"entity_id\": \"${entity}\"}" | jq -e '.[0]' > /dev/null 2>&1
}

switch_on() {
    local entity="$1"
    if call_service "switch" "turn_on" "$entity"; then
        echo "✓ ${entity} turned on"
    else
        echo "✗ Failed to turn on ${entity}"
    fi
}

switch_off() {
    local entity="$1"
    if call_service "switch" "turn_off" "$entity"; then
        echo "✓ ${entity} turned off"
    else
        echo "✗ Failed to turn off ${entity}"
    fi
}

switch_toggle() {
    local entity="$1"
    if call_service "switch" "toggle" "$entity"; then
        echo "✓ ${entity} toggled"
    else
        echo "✗ Failed to toggle ${entity}"
    fi
}

get_status() {
    local entity="$1"

    RESPONSE=$(curl -s -X GET "${URL}/api/states/${entity}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")

    FRIENDLY_NAME=$(echo "$RESPONSE" | jq -r '.attributes.friendly_name // .entity_id')
    STATE=$(echo "$RESPONSE" | jq -r '.state')

    echo "${FRIENDLY_NAME}: ${STATE}"
}

case "$COMMAND" in
    on)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        switch_on "$ENTITY"
        ;;
    off)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        switch_off "$ENTITY"
        ;;
    toggle)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        switch_toggle "$ENTITY"
        ;;
    status)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        get_status "$ENTITY"
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