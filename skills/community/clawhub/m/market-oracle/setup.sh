#!/usr/bin/env bash
# Market Oracle — Setup Script
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"

echo "📊 Market Oracle — Installing dependencies..."

# Check Python3
if ! command -v python3 &>/dev/null; then
    echo "❌ python3 not found. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Install dependencies
if [ -f "$TOOLS_DIR/requirements.txt" ]; then
    echo "📦 Installing Python packages..."
    python3 -m pip install -r "$TOOLS_DIR/requirements.txt" --quiet
    echo "✅ Dependencies installed."
else
    echo "⚠️  requirements.txt not found, skipping pip install."
fi

# Make scripts executable
chmod +x "$TOOLS_DIR"/*.py 2>/dev/null || true

echo ""
echo "✅ Market Oracle setup complete!"
echo ""
echo "Quick test:"
echo "  python3 $TOOLS_DIR/market_data.py --assets gold,btc,oil --period 1d"
echo "  python3 $TOOLS_DIR/news_fetch.py --query '黄金 原油'"
echo "  python3 $TOOLS_DIR/event_analyze.py --event '美联储宣布降息25个基点'"
