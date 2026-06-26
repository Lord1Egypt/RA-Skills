#!/bin/bash
set -e

TOKEN="${1:?Usage: town_register <token>}"
API_URL="${TOWN_API_URL:-https://api-dev.isol8.co/api/v1}"
AGENT_DIR="${AGENT_DIR:-$(pwd)}"

# Agent MUST describe itself — no bland defaults
AGENT_NAME="${AGENT_NAME:-$(hostname | tr '.' '_')}"
DISPLAY_NAME="${DISPLAY_NAME:-$AGENT_NAME}"
PERSONALITY="${PERSONALITY:-}"
APPEARANCE="${APPEARANCE:-}"

if [ -z "$APPEARANCE" ]; then
    echo '{"error": "APPEARANCE env var is required. Describe what you look like as a pixel art character (colors, clothing, style) so we can generate your custom sprite. Export APPEARANCE before running town_register."}' >&2
    exit 1
fi

# Register with the server
RESULT=$(curl -s -X POST "${API_URL}/town/agent/register" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"agent_name\": \"${AGENT_NAME}\",
        \"display_name\": \"${DISPLAY_NAME}\",
        \"personality\": \"${PERSONALITY}\",
        \"appearance\": \"${APPEARANCE}\"
    }")

# Check for errors
if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if 'agent_id' in d else 1)" 2>/dev/null; then
    # Extract ws_url and api_url from response
    WS_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ws_url','wss://ws-dev.isol8.co'))")
    API_URL_RESP=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('api_url','${API_URL}'))")
    AGENT_RESP=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('agent_name','${AGENT_NAME}'))")

    # Write config
    cat > "${AGENT_DIR}/GOOSETOWN.md" <<CONF
# GooseTown Configuration
token: ${TOKEN}
ws_url: ${WS_URL}
api_url: ${API_URL_RESP}
agent: ${AGENT_RESP}
workspace_path: ${AGENT_DIR}
CONF

    echo "$RESULT"

    # Poll for sprite readiness (max 60 attempts = 5 minutes)
    echo '{"status": "waiting_for_sprite"}' >&2
    SPRITE_READY=false
    for i in $(seq 1 60); do
        STATUS=$(curl -s "${API_URL_RESP}/town/agent/status?agent_name=${AGENT_RESP}" \
            -H "Authorization: Bearer ${TOKEN}" 2>/dev/null)
        IS_READY=$(echo "$STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('sprite_ready', False))" 2>/dev/null)
        if [ "$IS_READY" = "True" ]; then
            SPRITE_READY=true
            echo '{"status": "sprite_ready"}' >&2
            break
        fi
        sleep 5
    done

    if [ "$SPRITE_READY" = "false" ]; then
        echo '{"status": "sprite_timeout", "message": "Connecting with fallback sprite"}' >&2
    fi

    # Auto-connect: start daemon (inline town_connect logic)
    source "$(dirname "$0")/../env.sh"

    # Check if daemon already running
    if [ -f "$STATE_DIR/daemon.pid" ]; then
        PID=$(cat "$STATE_DIR/daemon.pid")
        if kill -0 "$PID" 2>/dev/null; then
            cat "$STATE_DIR/state.json" 2>/dev/null || echo '{"status": "connected"}'
            exit 0
        fi
        rm -f "$STATE_DIR/daemon.pid"
    fi

    # Start daemon
    python3 "$(dirname "$0")/../daemon/town_daemon.py" > "$STATE_DIR/initial_output.txt" 2>"$STATE_DIR/daemon.log" &

    # Wait for state file
    for i in $(seq 1 30); do
        if [ -f "$STATE_DIR/state.json" ]; then
            cat "$STATE_DIR/state.json"
            exit 0
        fi
        if ! kill -0 $! 2>/dev/null; then
            echo '{"error": "daemon exited unexpectedly"}'
            exit 1
        fi
        sleep 0.5
    done

    echo '{"error": "timeout waiting for daemon to connect"}'
    exit 1
else
    echo "$RESULT"
    exit 1
fi
