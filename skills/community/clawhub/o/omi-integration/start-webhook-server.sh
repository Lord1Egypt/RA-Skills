#!/bin/bash
# Start Omi webhook server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBHOOK_SERVER="$SCRIPT_DIR/webhook-server.py"
PID_FILE="$HOME/.config/omi/webhook-server.pid"

# Check if server is already running
if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "❌ Webhook server already running (PID: $OLD_PID)"
        echo "Stop it first: kill $OLD_PID"
        exit 1
    else
        # Stale PID file
        rm "$PID_FILE"
    fi
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Make webhook server executable
chmod +x "$WEBHOOK_SERVER"

# Optional: Set webhook secret for security
# export OMI_WEBHOOK_SECRET="your-secret-key-here"

# Optional: Change port (default: 8765)
# export OMI_WEBHOOK_PORT=8765

echo "🚀 Starting Omi webhook server..."

# Start in background
nohup python3 "$WEBHOOK_SERVER" > "$HOME/omi_recordings/.webhook-server.log" 2>&1 &
SERVER_PID=$!

# Save PID
mkdir -p "$(dirname "$PID_FILE")"
echo "$SERVER_PID" > "$PID_FILE"

sleep 2

# Check if still running
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo "✅ Webhook server started (PID: $SERVER_PID)"
    echo ""
    echo "📊 Status:"
    echo "  - Server running on port 8765"
    echo "  - Logs: tail -f ~/omi_recordings/.webhook-server.log"
    echo "  - PID file: $PID_FILE"
    echo ""
    echo "⚠️  Don't forget to run: ./setup-ngrok.sh"
    echo "   to expose your webhook to the internet!"
    echo ""
    echo "🛑 To stop: kill $SERVER_PID"
else
    echo "❌ Failed to start webhook server"
    echo "Check logs: cat ~/omi_recordings/.webhook-server.log"
    rm "$PID_FILE"
    exit 1
fi
