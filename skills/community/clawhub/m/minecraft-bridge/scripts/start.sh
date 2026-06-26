#!/bin/bash
# minecraft-bridge startup helper

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BRIDGE_PORT="${MC_BRIDGE_PORT:-3001}"
PID_FILE="${XDG_RUNTIME_DIR:-/tmp}/minecraft-bridge-$(id -u).pid"

if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    echo "Bridge already running (PID=$PID, port $BRIDGE_PORT)"
    echo "  Check status: curl http://localhost:${BRIDGE_PORT}/status"
    echo "  Stop it: bash $(dirname "$0")/stop.sh"
    exit 0
  fi
fi

if ! node -e "require('mineflayer')" 2>/dev/null; then
  echo "Installing bridge dependencies..."
  cd "$SKILL_DIR" && npm install mineflayer mineflayer-pathfinder vec3 --silent
fi

echo "Starting Minecraft Bridge..."
echo "  Minecraft target: ${MC_HOST:-localhost}:${MC_PORT:-25565}"
echo "  API port: $BRIDGE_PORT"
echo ""

nohup node "$SKILL_DIR/bridge-server.js" > /tmp/minecraft-bridge.log 2>&1 &
echo $! > "$PID_FILE"

for i in $(seq 1 10); do
  sleep 1
  if curl -sf "http://localhost:${BRIDGE_PORT}/status" > /dev/null 2>&1; then
    echo "Bridge started successfully (PID=$(cat $PID_FILE))"
    echo "  Status: curl http://localhost:${BRIDGE_PORT}/status"
    echo "  Logs: tail -f /tmp/minecraft-bridge.log"
    exit 0
  fi
done

echo "Bridge startup timed out. Check logs: cat /tmp/minecraft-bridge.log"
exit 1
