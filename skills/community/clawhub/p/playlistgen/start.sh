#!/bin/bash
# Start PlaylistGen music server

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load environment
if [ -f .env ]; then
    set -a; source .env; set +a
else
    echo "Warning: .env not found. Using defaults or existing environment."
fi

# Use venv if present
PYTHON=python3
if [ -f venv/bin/python3 ]; then
    PYTHON=venv/bin/python3
fi

# Kill any existing instance on the port
PORT="${PORT:-5678}"
fuser -k "${PORT}/tcp" 2>/dev/null || true
sleep 1

echo "Starting PlaylistGen on port ${PORT}..."
nohup "$PYTHON" playlist_server.py >> playlist_server.log 2>&1 &
echo "PID $! — log: $SCRIPT_DIR/playlist_server.log"
sleep 2
lsof -i :"$PORT" | grep LISTEN && echo "Server is up." || echo "Server did not start — check playlist_server.log"
