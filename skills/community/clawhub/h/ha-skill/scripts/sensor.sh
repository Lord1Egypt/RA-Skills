#!/bin/bash
# Query Home Assistant sensor values

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$HOME/.openclaw/credentials/homeassistant.json"

# Parse credentials
URL=$(jq -r '.url' "$CREDENTIALS_FILE")
TOKEN=$(jq -r '.token' "$CREDENTIALS_FILE")

COMMAND="${1:-help}"
ENTITY="${2:-}"

show_help() {
    echo "Usage: $0 <command> <entity> [format]"
    echo ""
    echo "Commands:"
    echo "  get <entity> [json]     Get sensor value"
    echo ""
    echo "Examples:"
    echo "  $0 get sensor.temperature_outside"
    echo "  $0 get sensor.humidity_living_room json"
}

get_sensor() {
    local entity="$1"
    local format="${2:-table}"

    RESPONSE=$(curl -s -X GET "${URL}/api/states/${entity}" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json")

    if [[ "$format" == "json" ]]; then
        echo "$RESPONSE" | jq '.'
    else
        FRIENDLY_NAME=$(echo "$RESPONSE" | jq -r '.attributes.friendly_name // .entity_id')
        VALUE=$(echo "$RESPONSE" | jq -r '.state')
        UNIT=$(echo "$RESPONSE" | jq -r '.attributes.unit_of_measurement // ""')

        echo "${FRIENDLY_NAME}: ${VALUE}${UNIT}"
    fi
}

case "$COMMAND" in
    get)
        [[ -z "$ENTITY" ]] && { show_help; exit 1; }
        get_sensor "$ENTITY" "$3"
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