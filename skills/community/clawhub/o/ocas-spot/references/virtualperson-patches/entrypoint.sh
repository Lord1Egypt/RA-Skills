#!/bin/bash
# entrypoint.sh — starts virtual display stack then hands off to hermes gateway
#
# Patched to use VPN Gate via host's SOCKS5 proxy instead of Mullvad.
#
# Display stack:
#   Xvfb :99       virtual framebuffer (1920x1080 24-bit)
#   Chrome          Google Chrome on :99, CDP on 127.0.0.1:9222, VPN Gate proxy
#   x11vnc          VNC server mirroring :99, port 5900
#   websockify      noVNC websocket proxy, port 6080
#
# Chrome profile persists at <home>/hermes/.hermes/.chrome-profile (on named volume).
# Cookies, sessions, localStorage all survive container restarts.

set -u

DISPLAY_NUM=99
DISPLAY=":${DISPLAY_NUM}"
VNC_PORT=5900
NOVNC_PORT=6080
CDP_PORT=9222
CHROME_PROFILE="<home>/hermes/.hermes/.chrome-profile"

log() { echo "[entrypoint] $*"; }

# ── 0. Clean up stale X lock (left by a previous container restart) ───────────
rm -f "/tmp/.X${DISPLAY_NUM}-lock" "/tmp/.X11-unix/X${DISPLAY_NUM}" 2>/dev/null || true

# ── 1. Xvfb ──────────────────────────────────────────────────────────────────
log "Starting Xvfb on display ${DISPLAY}..."
Xvfb "${DISPLAY}" -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!

for i in $(seq 1 20); do
    [ -e "/tmp/.X${DISPLAY_NUM}-lock" ] && break
    sleep 0.5
done

if [ -e "/tmp/.X${DISPLAY_NUM}-lock" ]; then
    log "Xvfb up on display ${DISPLAY} (pid ${XVFB_PID})"
else
    log "WARNING: Xvfb did not start cleanly — display may be unavailable"
fi

export DISPLAY

# ── 2. Google Chrome (headed, CDP + VPN Gate proxy) ───────────────────────────
# Uses launch-chrome.sh as the single source of truth for Chrome flags.
# The proxy points to the host's SOCKS5 bridge which routes through VPN Gate.
if [ -x <home>/hermes/launch-chrome.sh ]; then
    <home>/hermes/launch-chrome.sh launch
else
    log "WARNING: launch-chrome.sh not found, launching Chrome directly"
    CHROME_BIN=$(command -v google-chrome-stable 2>/dev/null || command -v google-chrome 2>/dev/null || true)
    if [ -n "${CHROME_BIN}" ]; then
        mkdir -p "${CHROME_PROFILE}"
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
            --user-data-dir="${CHROME_PROFILE}" \
            --remote-debugging-port="${CDP_PORT}" \
            --remote-debugging-address=127.0.0.1 \
            --window-size=1920,1080 \
            --proxy-server=socks5://host.docker.internal:1080 \
            about:blank \
            >"${HOME}/chrome.log" 2>&1 &
    fi
fi

# Wait for CDP to become available (max 15s)
CDP_READY=0
for i in $(seq 1 30); do
    if curl -sf "http://127.0.0.1:${CDP_PORT}/json/version" >/dev/null 2>&1; then
        CDP_READY=1
        break
    fi
    sleep 0.5
done

if [ "${CDP_READY}" -eq 1 ]; then
    log "Chrome up on CDP 127.0.0.1:${CDP_PORT}"
    export BROWSER_CDP_URL="http://127.0.0.1:${CDP_PORT}"
else
    log "WARNING: Chrome CDP not available — browser_tool will manage its own Chromium"
fi

# ── 3. Chrome watchdog ───────────────────────────────────────────────────────
# Restarts Chrome if it crashes. Checks every 30s. Runs in background.
(
    sleep 30  # initial grace period
    while true; do
        if ! curl -sf "http://127.0.0.1:${CDP_PORT}/json/version" >/dev/null 2>&1; then
            log "WATCHDOG: Chrome CDP down — restarting Chrome..."
            pkill -9 -f "google-chrome" 2>/dev/null || true
            sleep 2
            if [ -x <home>/hermes/launch-chrome.sh ]; then
                <home>/hermes/launch-chrome.sh launch
            fi
        fi
        sleep 30
    done
) &
log "Chrome watchdog started"

# ── 4. x11vnc ────────────────────────────────────────────────────────────────
log "Starting x11vnc on port ${VNC_PORT}..."
x11vnc \
    -display "${DISPLAY}" \
    -nopw \
    -rfbport "${VNC_PORT}" \
    -forever \
    -shared \
    -bg \
    -quiet \
    -logfile "${HOME}/x11vnc.log" \
    2>/dev/null || log "WARNING: x11vnc failed to start"

log "x11vnc started (see ~/x11vnc.log)"

# ── 5. noVNC / websockify ─────────────────────────────────────────────────────
NOVNC_WEB=""
for p in /usr/share/novnc /usr/share/novnc/web /opt/novnc; do
    if [ -f "${p}/vnc.html" ] || [ -f "${p}/vnc_lite.html" ]; then
        NOVNC_WEB="${p}"
        break
    fi
done

if [ -n "${NOVNC_WEB}" ]; then
    log "Starting noVNC websockify on port ${NOVNC_PORT} (web root: ${NOVNC_WEB})"
    websockify --web "${NOVNC_WEB}" "${NOVNC_PORT}" "127.0.0.1:${VNC_PORT}" \
        >"${HOME}/websockify.log" 2>&1 &
else
    log "noVNC web root not found — starting raw websockify proxy"
    websockify "${NOVNC_PORT}" "127.0.0.1:${VNC_PORT}" \
        >"${HOME}/websockify.log" 2>&1 &
fi
log "websockify/noVNC started on port ${NOVNC_PORT}"

# ── 6. Hand off to hermes gateway ─────────────────────────────────────────────
log "Display stack ready. Starting hermes gateway..."
exec hermes gateway run