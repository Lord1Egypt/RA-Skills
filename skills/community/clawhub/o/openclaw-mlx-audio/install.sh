#!/bin/bash
# OpenClaw mlx-audio Plugin - Dependency Installer
# Does NOT use brew tap, only uv for mlx-audio installation

set -e

echo "🔧 Installing OpenClaw mlx-audio dependencies..."

# Check for required tools
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ Missing: $1"
        return 1
    fi
    echo "✅ Found: $1"
    return 0
}

# Install ffmpeg if missing
if ! check_command ffmpeg; then
    echo "📦 Installing ffmpeg..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y ffmpeg
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y ffmpeg
    else
        echo "⚠️  Please install ffmpeg manually"
        exit 1
    fi
fi

# Install uv if missing
if ! check_command uv; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install mlx-audio via uv tool
echo "📦 Installing mlx-audio..."
uv tool install --force mlx-audio --prerelease=allow

# Verify installation
echo ""
echo "🔍 Verifying installation..."
check_command ffmpeg
check_command uv
check_command mlx_audio.tts.generate
check_command mlx_audio.stt.generate

echo ""
echo "✅ Installation complete!"
echo ""
echo "📚 Next steps:"
echo "1. Build the plugin: cd /path/to/openclaw-mlx-audio && bun install && bun run build"
echo "2. Copy to extensions: cp -r /path/to/openclaw-mlx-audio ~/.openclaw/extensions/"
echo "3. Add to openclaw.json plugins.allow and plugins.entries"
echo "4. Restart OpenClaw Gateway"
