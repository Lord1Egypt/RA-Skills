#!/usr/bin/env bash

HOST="http://$MOONRAKER_HOST:7125"

usage() {
    echo "Usage: moonraker.sh <command>"
    echo ""
    echo "Commands:"
    echo "  status   — show print state, progress, and temperatures"
    echo "  pause    — pause current print"
    echo "  resume   — resume paused print"
    echo "  cancel   — cancel current print"
    echo "  estop    — EMERGENCY STOP (requires firmware restart to recover)"
    echo "  files    — list gcode files on printer"
    exit 1
}

require_jq() {
    if ! command -v jq &>/dev/null; then
        echo "[warn] jq not found — raw JSON output will be shown"
        JQ_MISSING=1
    fi
}

jq_or_cat() {
    if [ "${JQ_MISSING:-0}" = "1" ]; then
        cat
    else
        jq "$@"
    fi
}

cmd_status() {
    RAW=$(curl -sf "${HOST}/printer/objects/query?print_stats&heater_bed&extruder&virtual_sdcard")
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not reach Moonraker at ${HOST}"
        exit 1
    fi

    if command -v jq &>/dev/null; then
        STATE=$(echo "$RAW" | jq -r '.result.status.print_stats.state // "unknown"')
        FILENAME=$(echo "$RAW" | jq -r '.result.status.print_stats.filename // "none"')
        PROGRESS=$(echo "$RAW" | jq -r '(.result.status.virtual_sdcard.progress // 0) * 100 | floor | tostring + "%"')
        HOTEND=$(echo "$RAW" | jq -r '.result.status.extruder.temperature // 0 | floor | tostring')
        HOTEND_TARGET=$(echo "$RAW" | jq -r '.result.status.extruder.target // 0 | floor | tostring')
        BED=$(echo "$RAW" | jq -r '.result.status.heater_bed.temperature // 0 | floor | tostring')
        BED_TARGET=$(echo "$RAW" | jq -r '.result.status.heater_bed.target // 0 | floor | tostring')

        echo "=== Printer Status ==="
        echo "State      : ${STATE}"
        echo "File       : ${FILENAME}"
        echo "Progress   : ${PROGRESS}"
        echo "Hotend     : ${HOTEND}°C / ${HOTEND_TARGET}°C (target)"
        echo "Bed        : ${BED}°C / ${BED_TARGET}°C (target)"
    else
        echo "$RAW"
    fi
}

cmd_pause() {
    echo "Pausing print..."
    curl -sf -X POST "${HOST}/printer/print/pause" | jq_or_cat .
}

cmd_resume() {
    echo "Resuming print..."
    curl -sf -X POST "${HOST}/printer/print/resume" | jq_or_cat .
}

cmd_cancel() {
    echo "Cancelling print..."
    curl -sf -X POST "${HOST}/printer/print/cancel" | jq_or_cat .
}

cmd_estop() {
    echo "⚠️  EMERGENCY STOP — all motion and heaters will halt immediately."
    echo "    Run 'curl -X POST ${HOST}/printer/firmware_restart' to recover."
    curl -sf -X POST "${HOST}/printer/emergency_stop" | jq_or_cat .
}

cmd_files() {
    RAW=$(curl -sf "${HOST}/server/files/list")
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not reach Moonraker at ${HOST}"
        exit 1
    fi

    if command -v jq &>/dev/null; then
        echo "=== GCode Files ==="
        echo "$RAW" | jq -r '.result[] | "\(.filename)  (\(.size / 1024 | floor) KB)"' 2>/dev/null \
            || echo "$RAW" | jq -r '.result[].filename'
    else
        echo "$RAW"
    fi
}

require_jq

case "${1:-}" in
    status) cmd_status ;;
    pause)  cmd_pause ;;
    resume) cmd_resume ;;
    cancel) cmd_cancel ;;
    estop)  cmd_estop ;;
    files)  cmd_files ;;
    *)      usage ;;
esac
