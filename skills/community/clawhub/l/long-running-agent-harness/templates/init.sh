#!/bin/bash
# ============================================================
# Development Server Init Script
# ============================================================
# This script starts the development environment.
# Customize the commands below to match your project stack.
#
# Usage:
#   chmod +x init.sh
#   ./init.sh          # Start servers
#   ./init.sh stop     # Stop servers
#   ./init.sh restart  # Restart servers
# ============================================================

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# --- Configuration ---
# BACKEND_PORT=8000
# FRONTEND_PORT=3000
# PID_DIR="$PROJECT_DIR/.pids"

stop_servers() {
    echo "Stopping servers..."
    # kill $(cat "$PID_DIR/backend.pid" 2>/dev/null) 2>/dev/null || true
    # kill $(cat "$PID_DIR/frontend.pid" 2>/dev/null) 2>/dev/null || true
    # rm -rf "$PID_DIR"
    echo "Servers stopped."
}

start_servers() {
    echo "Starting development servers..."
    # mkdir -p "$PID_DIR"

    # --- Backend ---
    # echo "Starting backend..."
    # cd "$PROJECT_DIR/backend"
    # source venv/bin/activate
    # python -m uvicorn app.main:app --port $BACKEND_PORT &
    # echo $! > "$PID_DIR/backend.pid"

    # --- Frontend ---
    # echo "Starting frontend..."
    # cd "$PROJECT_DIR/frontend"
    # npm run dev -- --port $FRONTEND_PORT &
    # echo $! > "$PID_DIR/frontend.pid"

    # Wait for servers to be ready
    # echo "Waiting for servers to be ready..."
    # sleep 3

    echo "Development servers started."
    # echo "  Backend:  http://localhost:$BACKEND_PORT"
    # echo "  Frontend: http://localhost:$FRONTEND_PORT"
}

case "${1:-start}" in
    start)   start_servers ;;
    stop)    stop_servers ;;
    restart) stop_servers; sleep 1; start_servers ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
