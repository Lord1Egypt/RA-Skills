#!/usr/bin/env bash
#
# ha-monitor.sh — Monitor HA device health and status
#
# Security:
#   - ENV vars: HA_URL, HA_TOKEN, HA_HOST, HA_SSH_PORT, HA_SSH_USER
#   - Endpoints: HA_URL/api/states, HA_URL/api/config, HA_URL/api/error_log (REST, read-only)
#   - File access: none (read-only API queries)
#   - No data sent to external services
#
# Usage:
#   ha-monitor.sh status                  # Overview: online/offline/unavailable counts
#   ha-monitor.sh offline                 # List offline/unavailable devices
#   ha-monitor.sh battery [threshold]     # Low battery devices (default: <20%)
#   ha-monitor.sh stale [hours]           # Devices not updated in N hours (default: 24)
#   ha-monitor.sh errors                  # Recent error log entries
#   ha-monitor.sh health                  # Full health report

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

cmd_status() {
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then
        echo -e "${RED}Error: cannot fetch states from API.${NC}" >&2
        return 1
    fi
    local total online offline unavailable
    total=$(echo "$states" | jq 'length')
    unavailable=$(echo "$states" | jq '[.[] | select(.state == "unavailable")] | length')
    offline=$(echo "$states" | jq '[.[] | select(.state == "offline" or .state == "unknown")] | length')
    online=$((total - unavailable - offline))

    echo "=== HA Device Status ===" >&2
    echo "Total entities:  $total"
    echo -e "Online:          ${GREEN}$online${NC}"
    echo -e "Unavailable:     ${RED}$unavailable${NC}"
    echo -e "Offline/Unknown: ${YELLOW}$offline${NC}"
 
    if [[ "$unavailable" -gt 0 ]] || [[ "$offline" -gt 0 ]]; then
        echo ""
        echo -e "${YELLOW}⚠️ Issues detected. Run 'ha-monitor.sh offline' for details.${NC}"
    else
        echo ""
        echo -e "${GREEN}✅ All entities reporting normally.${NC}" >&2
    fi
}

cmd_offline() {
    echo "=== Unavailable / Offline Entities ===" >&2
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then echo -e "${RED}API error${NC}" >&2; return 1; fi
    echo "$states" | jq -r '.[] |
        select(.state == "unavailable" or .state == "offline" or .state == "unknown") |
        select(.entity_id | (
            startswith("sensor.") or startswith("switch.") or startswith("light.") or 
            startswith("binary_sensor.") or startswith("climate.") or startswith("cover.") or 
            startswith("lock.") or startswith("vacuum.") or startswith("media_player.") or
            startswith("camera.") or startswith("alarm_control_panel.") or startswith("fan.") or
            startswith("humidifier.") or startswith("water_heater.")
        )) |
        "\(.state)\t\(.entity_id)\t\(.attributes.friendly_name // "-")\t\(.last_changed // "-")"' | \
        sort | column -t -s $'\t'
}

cmd_battery() {
    local threshold="${1:-20}"
    echo "=== Low Battery Devices (< ${threshold}%) ===" >&2
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then echo -e "${RED}API error${NC}" >&2; return 1; fi
    echo "$states" | jq -r --argjson t "$threshold" '.[] |
        select(.entity_id | endswith("_battery") or endswith("_battery_level")) |
        select(.state != "unavailable" and .state != "unknown") |
        select((.state | tonumber? // 100) < $t) |
        "\(.state)%\t\(.entity_id)\t\(.attributes.friendly_name // "-")"' | \
        sort -n | column -t -s $'\t'
}

cmd_stale() {
    local hours="${1:-24}"
    local cutoff
    # Try GNU date, then BSD date, then Python as universal fallback (works on Windows)
    cutoff=$(date -u -d "$hours hours ago" +%Y-%m-%dT%H:%M:%S 2>/dev/null || \
             date -u -v-${hours}H +%Y-%m-%dT%H:%M:%S 2>/dev/null || \
             python3 -c "from datetime import datetime,timedelta;print((datetime.utcnow()-timedelta(hours=$hours)).strftime('%Y-%m-%dT%H:%M:%S'))" 2>/dev/null || echo "")

    if [[ -z "$cutoff" ]]; then
        echo "Error: cannot calculate cutoff time (install GNU date or python3)" >&2
        exit 1
    fi

    echo "=== Stale Entities (no update in ${hours}h) ==="
    local states
    states=$(ha_api GET "states" || echo "")
    if [[ -z "$states" ]]; then echo -e "${RED}API error${NC}" >&2; return 1; fi
    echo "$states" | jq -r --arg cutoff "$cutoff" '.[] |
        select(.last_changed < $cutoff) |
        select(.entity_id | (startswith("sensor.") or startswith("binary_sensor."))) |
        select(.state != "unavailable") |
        "\(.last_changed | split("T")[0])\t\(.entity_id)\t\(.state)\t\(.attributes.friendly_name // "-")"' | \
        sort | head -30 | column -t -s $'\t'
}

cmd_errors() {
    echo "=== Recent Errors (last 50 lines) ==="
    ha_api GET "error_log" | grep -iE "error|warning|exception|fail" || echo "No recent errors found."
}

cmd_health() {
    cmd_status
    echo ""
    cmd_offline
    echo ""
    cmd_battery 20
    echo ""
    echo "=== Core Connection ==="
    local config
    config=$(ha_api GET "config" || echo "")
    if [[ -n "$config" ]]; then
        echo "$config" | jq '{version: .version, name: .location_name}'
    else
        echo -e "${RED}Cannot fetch config.${NC}" >&2
    fi
}

case "${1:-help}" in
    status)   cmd_status ;;
    offline)  cmd_offline ;;
    battery)  cmd_battery "${2:-20}" ;;
    stale)    cmd_stale "${2:-24}" ;;
    errors)   cmd_errors ;;
    health)   cmd_health ;;
    *)
        echo "ha-monitor.sh — Monitor HA device health"
        echo ""
        echo "  status               Overview counts"
        echo "  offline              Unavailable/offline devices"
        echo "  battery [threshold]  Low battery (default <20%)"
        echo "  stale [hours]        Not updated in N hours"
        echo "  errors               Recent error log entries"
        echo "  health               Full health report"
        ;;
esac
