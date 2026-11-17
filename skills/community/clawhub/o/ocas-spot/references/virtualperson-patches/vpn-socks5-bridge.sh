#!/bin/bash
# vpn-socks5-bridge.sh — SOCKS5 proxy that routes through VPN Gate (tun0)
#
# This replaces Mullvad's SOCKS5 proxy (172.18.0.1:1080) with a local
# SOCKS5 proxy that routes all traffic through the VPN Gate tun0 interface.
#
# Usage:
#   ./vpn-socks5-bridge.sh start    — start the SOCKS5 proxy
#   ./vpn-socks5-bridge.sh stop     — stop the SOCKS5 proxy
#   ./vpn-socks5-bridge.sh status   — check if proxy is running
#   ./vpn-socks5-bridge.sh restart  — restart the proxy

set -u

PROXY_PORT=1080
PROXY_BIND="127.0.0.1"
LOG="<fs-root>/vpn-socks5-bridge.log"
PIDFILE="<fs-root>/vpn-socks5-bridge.pid"

log() { echo "[vpn-socks5-bridge] $*"; }

check_tun0() {
    if ! ip addr show tun0 2>/dev/null | grep -q 'inet '; then
        log "ERROR: tun0 (VPN) is not active. Start VPN first:"
        log "  openvpn --config <vpn-config> --daemon"
        return 1
    fi
    return 0
}

start_proxy() {
    # Check if already running
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        log "Already running (PID $(cat "$PIDFILE"))"
        return 0
    fi

    # Check tun0 is up
    if ! check_tun0; then
        return 1
    fi

    # Check if microsocks is available
    if ! command -v microsocks &>/dev/null; then
        log "microsocks not found. Installing..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get update -qq && sudo apt-get install -y -qq microsocks 2>/dev/null
        fi
        # Fallback: build from source
        if ! command -v microsocks &>/dev/null; then
            log "Building microsocks from source..."
            TMPDIR=$(mktemp -d)
            git clone https://github.com/rofl0r/microsocks.git "$TMPDIR/microsocks" 2>/dev/null
            cd "$TMPDIR/microsocks" && make 2>/dev/null && sudo cp microsocks /usr/local/bin/
            rm -rf "$TMPDIR"
        fi
    fi

    if ! command -v microsocks &>/dev/null; then
        log "ERROR: microsocks could not be installed"
        return 1
    fi

    # Get tun0 IP for binding
    TUN0_IP=$(ip addr show tun0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)
    if [ -z "$TUN0_IP" ]; then
        log "ERROR: Could not determine tun0 IP"
        return 1
    fi

    log "Starting microsocks on ${PROXY_BIND}:${PROXY_PORT} (routing via tun0: ${TUN0_IP})"

    # Start microsocks bound to tun0 interface
    # This ensures all SOCKS5 traffic goes through the VPN tunnel
    microsocks -i "$TUN0_IP" -p "$PROXY_PORT" >"$LOG" 2>&1 &
    echo $! > "$PIDFILE"

    sleep 1

    if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        log "SOCKS5 proxy started (PID $(cat "$PIDFILE"))"
        log "  Listen:  ${PROXY_BIND}:${PROXY_PORT}"
        log "  Route:   via tun0 (${TUN0_IP})"
        return 0
    else
        log "ERROR: microsocks failed to start. Check $LOG"
        return 1
    fi
}

stop_proxy() {
    if [ -f "$PIDFILE" ]; then
        local PID
        PID=$(cat "$PIDFILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID" 2>/dev/null
            log "SOCKS5 proxy stopped (PID $PID)"
        else
            log "SOCKS5 proxy was not running (stale PID file)"
        fi
        rm -f "$PIDFILE"
    else
        log "No PID file found — proxy may not be running"
        # Try to kill any microsocks anyway
        pkill -f "microsocks" 2>/dev/null || true
    fi
}

status_proxy() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        log "SOCKS5 proxy is RUNNING (PID $(cat "$PIDFILE"))"
        log "  Listen: ${PROXY_BIND}:${PROXY_PORT}"
        if check_tun0 2>/dev/null; then
            log "  VPN:    tun0 is UP"
        else
            log "  VPN:    tun0 is DOWN — proxy will not route traffic"
        fi
        return 0
    else
        log "SOCKS5 proxy is NOT running"
        return 1
    fi
}

case "${1:-status}" in
    start)   start_proxy ;;
    stop)    stop_proxy ;;
    restart) stop_proxy; sleep 1; start_proxy ;;
    status)  status_proxy ;;
    *) echo "Usage: $0 {start|stop|restart|status}" >&2; exit 1 ;;
esac