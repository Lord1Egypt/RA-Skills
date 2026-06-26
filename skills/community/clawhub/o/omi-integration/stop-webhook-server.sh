#!/bin/bash
# Stop Omi webhook server

PID_FILE="$HOME/.config/omi/webhook-server.pid"

if [[ ! -f "$PID_FILE" ]]; then
    echo "❌ No PID file found. Server not running?"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 Stopping webhook server (PID: $PID)..."
    kill "$PID"
    rm "$PID_FILE"
    echo "✅ Webhook server stopped"
else
    echo "⚠️  Process $PID not found (already stopped?)"
    rm "$PID_FILE"
fi

# Also check for ngrok
NGROK_PID=$(pgrep ngrok || true)
if [[ -n "$NGROK_PID" ]]; then
    echo ""
    read -p "Also stop ngrok tunnel (PID: $NGROK_PID)? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill "$NGROK_PID"
        echo "✅ ngrok stopped"
    fi
fi
