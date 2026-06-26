#!/usr/bin/env bash
set -euo pipefail
# load env if present
source "$(dirname "$0")/_env_loader.sh"

SESSION=${1:-debug}
DISPLAY_VAL=${2:-${VNC_DISPLAY:-:99}}
RES=${3:-${VNC_RESOLUTION:-1366x768}}
WORKDIR=/tmp/${SESSION}_vnc
LOG=${TMP_LOG_DIR:-/tmp}/x11vnc_${SESSION}.log
mkdir -p "$WORKDIR"
export DISPLAY="$DISPLAY_VAL"
# Launch Xvfb if not present
if ! pgrep -f "Xvfb $DISPLAY_VAL" >/dev/null 2>&1; then
  Xvfb "$DISPLAY_VAL" -screen 0 ${RES}x24 &> ""$LOG"" &
  echo "Xvfb started on $DISPLAY_VAL"
  sleep 1
fi
# Start fluxbox if available
if command -v fluxbox >/dev/null 2>&1; then
  if ! pgrep -f "fluxbox" >/dev/null 2>&1; then
    fluxbox &>> ""$LOG"" &
    sleep 0.5
  fi
fi
# Determine VNC implementation and passfile handling
VNC_PASS_FILE=${VNC_PASSFILE:-${WORKDIR}/vncpasswd}
VNC_IMPL=${VNC_IMPLEMENTATION:-auto}

echo "Using VNC implementation: $VNC_IMPL"
# If passfile already exists, prefer it
if [ -f "$VNC_PASS_FILE" ]; then
  echo "Using existing VNC passfile: $VNC_PASS_FILE"
else
  echo "Error: VNC_PASSFILE not found at $VNC_PASS_FILE" >&2
  echo "Please run './scripts/setup.sh --set-password' to generate it." >&2
  exit 1
fi

# Start x11vnc
if ! pgrep -f "x11vnc.*${DISPLAY_VAL}" >/dev/null 2>&1; then
  setsid x11vnc -display "$DISPLAY_VAL" -rfbauth "$VNC_PASS_FILE" -forever -shared -o ""$LOG"" &
  echo "x11vnc started (log: "$LOG")"
fi

# Report actual listening sockets for VNC (helpful when DISPLAY -> port mapping varies)
# Print complete info: process line, listening sockets, and inferred port
echo "--- VNC listener inspection ---"
# process info
pid=$(pgrep -f "x11vnc.*${DISPLAY_VAL}" | head -n1 || true)
if [ -n "$pid" ]; then
  ps -o pid,cmd -p "$pid" 2>/dev/null || true
else
  echo "(no x11vnc process found)"
fi
# list listening TCP sockets for x11vnc (if any)
ss -ltnp 2>/dev/null | grep -E ':(5900|5901|59[0-9]{2})\s' || true
# Try to extract the listening port for the x11vnc pid (prefer IPv4)
LISTEN_PORT=""
if [ -n "$pid" ]; then
  # search ss lines for this pid and extract the port number
  LISTEN_PORT=$(ss -ltnp 2>/dev/null | grep -F "pid=$pid" | sed -n 's/.*:\([0-9]\{4,5\}\) .*/\1/p' | head -n1 || true)
fi
# fallback: try to infer port from display number
DISPLAY_NUM=${DISPLAY_VAL#:}
if [ -z "$LISTEN_PORT" ] && [[ "$DISPLAY_NUM" =~ ^[0-9]+$ ]]; then
  INFER_PORT=$((5900 + DISPLAY_NUM))
  LISTEN_PORT="${INFER_PORT} (inferred)"
fi
if [ -n "$LISTEN_PORT" ]; then
  echo "VNC listening on port: $LISTEN_PORT"
else
  echo "VNC listening port: unknown"
fi

echo "--- end VNC listener inspection ---"

echo "VNC session $SESSION on display $DISPLAY_VAL started. VNC pass file: $VNC_PASS_FILE"

# Provide connection instructions if port is known
CLEAN_PORT=$(echo "$LISTEN_PORT" | grep -Eo '^[0-9]+' || echo "")
if [ -n "$CLEAN_PORT" ]; then
  echo ""
  echo "================================================================================"
  echo "To connect securely from your local machine, set up an SSH tunnel:"
  echo "  ssh -L ${CLEAN_PORT}:127.0.0.1:${CLEAN_PORT} user@$(hostname 2>/dev/null || echo 'server_address')"
  echo ""
  echo "Then connect your local VNC client (e.g. TigerVNC, RealVNC) to:"
  echo "  127.0.0.1:${CLEAN_PORT}"
  echo "================================================================================"
fi