# ClawLink Setup — Install dependencies for the ClawLink agent mesh
# Usage: bash setup.sh [server|client|both]

set -e

MODE="${1:-both}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════╗"
echo "║          🔗 ClawLink Setup                   ║"
echo "╠══════════════════════════════════════════════╣"
echo "║  Mode: $MODE                                 "
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not found."
    exit 1
fi

# Install dependencies into user site-packages to avoid system changes
echo "[1/3] Installing dependencies (user install)..."
pip install --user aiohttp requests || {
    echo "  User install failed. Trying venv approach:"
    echo "  Run: python3 -m venv ~/.clawlink/venv && source ~/.clawlink/venv/bin/activate"
    exit 1
}

# Optional: mDNS support for zero-config LAN discovery
echo "[2/3] Installing mDNS support (optional — for LAN auto-discovery)..."
pip install --user zeroconf 2>/dev/null || echo "  (mDNS skipped — manual --relay URL required for LAN, HTTP still works)"

echo "[3/3] Setup complete!"
echo ""

if [ "$MODE" = "server" ] || [ "$MODE" = "both" ]; then
    echo "Start the relay server with:"
    echo "  python3 $SCRIPT_DIR/server.py --token YOUR_SHARED_SECRET"
    echo ""
    echo "Options:"
    echo "  --port 9077           Custom port (default: 9077)"
    echo "  --host 127.0.0.1      Bind to localhost only (default; safest)"
    echo "  --host 0.0.0.0        Bind to all interfaces (LAN access)"
    echo "  --token SECRET        Shared auth token (required for multi-machine)"
    echo "  --no-mdns             Disable LAN broadcast"
    echo ""
fi

if [ "$MODE" = "client" ] || [ "$MODE" = "both" ]; then
    echo "Connect an agent with:"
    echo "  python3 $SCRIPT_DIR/client.py --relay http://HOST:9077 --token YOUR_SHARED_SECRET register --name 'my-agent' --caps 'code,search'"
    echo ""
    echo "Or scan for relays on your LAN:"
    echo "  python3 $SCRIPT_DIR/client.py scan"
    echo ""
fi

if [ "$MODE" = "both" ]; then
    echo "Quick start (run in separate terminals):"
    echo "  Terminal 1:  python3 $SCRIPT_DIR/server.py --token mysecret"
    echo "  Terminal 2:  python3 $SCRIPT_DIR/client.py --token mysecret register --name agent-a --caps 'code,search'"
    echo "  Terminal 3:  python3 $SCRIPT_DIR/client.py --token mysecret register --name agent-b --caps 'write,review'"
    echo ""
    echo "Then delegate a task:"
    echo "  python3 $SCRIPT_DIR/client.py --token mysecret delegate --to <agent-b-id> --task 'Review my code'"
fi
