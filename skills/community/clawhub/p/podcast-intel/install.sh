#!/bin/bash
# Installation script for podcast-intel OpenClaw skill

set -e

echo "🎧 Installing podcast-intel skill..."

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_ROOT="$SCRIPT_DIR"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found. Installing..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ Homebrew not found. Please install ffmpeg manually:"
            echo "   brew install ffmpeg"
            exit 1
        fi
    elif command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install -y ffmpeg
    else
        echo "❌ ffmpeg not found and cannot auto-install. Please install manually."
        exit 1
    fi
fi

echo "✓ ffmpeg found: $(ffmpeg -version | head -n1)"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r "$SKILL_ROOT/requirements.txt" --quiet

echo "✓ Dependencies installed"

# Create directories
echo ""
echo "📁 Creating directories..."

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
CONFIG_DIR="$OPENCLAW_DIR/config"
CACHE_DIR="$OPENCLAW_DIR/cache/podcast-intel"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace/podcast-intel"
MEMORY_DIR="$OPENCLAW_DIR/memory/podcast-intel"

mkdir -p "$CONFIG_DIR" "$CACHE_DIR" "$WORKSPACE_DIR" "$MEMORY_DIR"

echo "✓ Directories created"

# Copy config examples
echo ""
echo "⚙️  Setting up configuration..."

if [ ! -f "$CONFIG_DIR/podcast-intel-feeds.yaml" ]; then
    cp "$SKILL_ROOT/config/feeds.example.yaml" "$CONFIG_DIR/podcast-intel-feeds.yaml"
    echo "✓ Created feeds config: $CONFIG_DIR/podcast-intel-feeds.yaml"
else
    echo "→ Feeds config already exists"
fi

if [ ! -f "$CONFIG_DIR/podcast-intel-interests.yaml" ]; then
    cp "$SKILL_ROOT/config/interests.example.yaml" "$CONFIG_DIR/podcast-intel-interests.yaml"
    echo "✓ Created interests config: $CONFIG_DIR/podcast-intel-interests.yaml"
else
    echo "→ Interests config already exists"
fi

# Check environment variables
echo ""
echo "🔐 Checking environment..."

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   Set it with: export OPENAI_API_KEY='sk-...'"
else
    echo "✓ OPENAI_API_KEY is set"
fi

# Make scripts executable
echo ""
echo "🔨 Making scripts executable..."

chmod +x "$SKILL_ROOT/scripts/"*.py
echo "✓ Scripts are executable"

# Test basic functionality
echo ""
echo "🧪 Running smoke test..."

if python3 "$SKILL_ROOT/scripts/fetch_feeds.py" --help > /dev/null 2>&1; then
    echo "✓ Smoke test passed"
else
    echo "⚠️  Smoke test failed - check logs"
fi

# Print next steps
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Installation complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Configure your feeds:"
echo "   nano $CONFIG_DIR/podcast-intel-feeds.yaml"
echo ""
echo "2. Configure your interests:"
echo "   nano $CONFIG_DIR/podcast-intel-interests.yaml"
echo ""
echo "3. Set your OpenAI API key (if not already set):"
echo "   export OPENAI_API_KEY='sk-...'"
echo ""
echo "4. Try a test run:"
echo "   python3 $SKILL_ROOT/scripts/main.py --hours 24 --top 3"
echo ""
echo "5. See full usage:"
echo "   python3 $SKILL_ROOT/scripts/main.py --help"
echo ""
echo "📖 Documentation: $SKILL_ROOT/README.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
