#!/bin/bash
# launch-chrome.sh — THE canonical way to start Chrome in the hermes container.
#
# Patched to use VPN Gate via host's SOCKS5 proxy instead of Mullvad.
# All traffic routes through the VPN tunnel on the host.
#
# This script is the ONLY correct way to launch Chrome. It ensures:
# - 1920x1080 resolution
# - VPN Gate tunnel via host's SOCKS5 proxy (host.docker.internal:1080)
# - CDP on 127.0.0.1:9222 (localhost only)
# - WebRTC leak protection
# - No automation detection flags
# - Persistent profile at <home>/hermes/.chrome-profile
#
# Usage:
#   <home>/hermes/launch-chrome.sh          — launch Chrome (kills existing first)
#   <home>/hermes/launch-chrome.sh status    — check if Chrome is healthy
#   <home>/hermes/launch-chrome.sh kill      — kill Chrome
#   <home>/hermes/launch-chrome.sh restart   — kill + relaunch

set -u

CHROME_BIN=$(command -v google-chrome-stable 2>/dev/null || command -v google-chrome 2>/dev/null)
PROFILE_DIR="<home>/hermes/.hermes/.chrome-profile"
CDP_PORT=9222
CDP_BIND="127.0.0.1"
# VPN Gate SOCKS5 proxy on the host (replaces Mullvad 172.18.0.1:1080)
PROXY="socks5://host.docker.internal:1080"
DISPLAY="${DISPLAY:-:99}"
LOG="<home>/hermes/chrome.log"

log() { echo "[launch-chrome] $*"; }

kill_chrome() {
    pkill -9 -f "google-chrome" 2>/dev/null || true
    pkill -9 -f "/opt/google/chrome/chrome" 2>/dev/null || true
    log "Chrome killed."
}

status_chrome() {
    if curl -sf "http://${CDP_BIND}:${CDP_PORT}/json/version" >/dev/null 2>&1; then
        local VER
        VER=$(curl -sf "http://${CDP_BIND}:${CDP_PORT}/json/version" | python3 -c "import sys,json; print(json.load(sys.stdin).get('Browser','unknown'))" 2>/dev/null)
        log "Chrome is UP — ${VER} — CDP at ${CDP_BIND}:${CDP_PORT}"
        return 0
    else
        log "Chrome is DOWN — CDP not responding on ${CDP_BIND}:${CDP_PORT}"
        return 1
    fi
}

launch_chrome() {
    if [ -z "${CHROME_BIN}" ]; then
        log "ERROR: google-chrome-stable not found!"
        return 1
    fi

    # Kill any existing Chrome
    kill_chrome
    sleep 1

    # Ensure profile directory exists
    mkdir -p "${PROFILE_DIR}"

    export DISPLAY

    log "Launching Chrome..."
    log "  Binary:     ${CHROME_BIN}"
    log "  Profile:    ${PROFILE_DIR}"
    log "  Proxy:      ${PROXY} (VPN Gate via host)"
    log "  CDP:        ${CDP_BIND}:${CDP_PORT}"
    log "  Resolution: 1920x1080"

    "${CHROME_BIN}" \
        --no-sandbox \
        --disable-gpu \
        --disable-dev-shm-usage \
        --no-first-run \
        --no-default-browser-check \
        --disable-infobars \
        --disable-blink-features=AutomationControlled \
        --enforce-webrtc-ip-permission-check \
        --webrtc-ip-handling-policy=disable_non_proxied_udp \
        --user-data-dir="${PROFILE_DIR}" \
        --remote-debugging-port="${CDP_PORT}" \
        --remote-debugging-address="${CDP_BIND}" \
        --window-size=1920,1080 \
        --proxy-server="${PROXY}" \
        about:blank \
        >"${LOG}" 2>&1 &

    # Wait for CDP
    for i in $(seq 1 30); do
        if curl -sf "http://${CDP_BIND}:${CDP_PORT}/json/version" >/dev/null 2>&1; then
            log "Chrome is UP and CDP ready."
            return 0
        fi
        sleep 0.5
    done

    log "WARNING: Chrome started but CDP not responding after 15s. Check ${LOG}"
    return 1
}

case "${1:-launch}" in
    launch|start) launch_chrome ;;
    kill|stop)    kill_chrome ;;
    restart)      launch_chrome ;;
    status|check) status_chrome ;;
    *) echo "Usage: $0 {launch|kill|restart|status}" >&2; exit 1 ;;
esac