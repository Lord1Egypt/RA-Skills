#!/bin/bash
# Setup ngrok tunnel for Omi webhook endpoint

set -e

WEBHOOK_PORT=8765
CONFIG_DIR="$HOME/.config/omi"

echo "🔌 Setting up ngrok tunnel for Omi webhooks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not found!"
    echo ""
    echo "Please install ngrok:"
    echo "  1. Sign up at https://ngrok.com"
    echo "  2. Download and install: https://ngrok.com/download"
    echo "  3. Authenticate: ngrok config add-authtoken <your-token>"
    exit 1
fi

# Check for existing ngrok config
if [[ -f "$CONFIG_DIR/ngrok_url" ]]; then
    EXISTING_URL=$(cat "$CONFIG_DIR/ngrok_url")
    echo "📍 Existing ngrok URL found: $EXISTING_URL"
    echo ""
    read -p "Use existing URL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ Using existing URL: $EXISTING_URL"
        echo ""
        echo "Configure this URL in your Omi app:"
        echo "  Webhook URL: ${EXISTING_URL}/omi/webhook"
        exit 0
    fi
fi

echo ""
echo "Starting ngrok tunnel on port $WEBHOOK_PORT..."
echo "(This will run in the background)"
echo ""

# Start ngrok in background
ngrok http $WEBHOOK_PORT --log=stdout > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

# Get public URL from ngrok API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [[ -z "$NGROK_URL" ]] || [[ "$NGROK_URL" == "null" ]]; then
    echo "❌ Failed to get ngrok URL"
    echo "Check logs: tail -f /tmp/ngrok.log"
    exit 1
fi

# Save URL
mkdir -p "$CONFIG_DIR"
echo "$NGROK_URL" > "$CONFIG_DIR/ngrok_url"

echo "✅ ngrok tunnel established!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Public URL: $NGROK_URL"
echo "Webhook endpoint: ${NGROK_URL}/omi/webhook"
echo "Health check: ${NGROK_URL}/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Configure in Omi App:"
echo "  1. Open Omi app → Settings → Developer"
echo "  2. Create new webhook"
echo "  3. Webhook URL: ${NGROK_URL}/omi/webhook"
echo "  4. Select events: recording.created, transcript.updated"
echo ""
echo "🔍 Monitor webhook activity:"
echo "  - ngrok dashboard: http://localhost:4040"
echo "  - Logs: tail -f ~/omi_recordings/.webhook.log"
echo ""
echo "⚠️  Note: Free ngrok URLs expire when tunnel closes"
echo "    Restart this script to get a new URL"
echo ""
echo "ngrok PID: $NGROK_PID"
echo "To stop: kill $NGROK_PID"
