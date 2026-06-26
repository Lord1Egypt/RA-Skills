#!/usr/bin/env bash
# Setup script for OpenClaw 飞书语音聊天 - 完全离线版
# Creates virtual environment and installs dependencies for Whisper ASR and Qwen3-TTS
#
# Usage:
#   cd /root/.openclaw/skills/openclaw-feishu-voice-free
#   bash setup.sh
#   # or
#   ./setup.sh

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Skill directory is the parent of setup.sh
SKILL_DIR="$SCRIPT_DIR"
VENV_DIR="$SKILL_DIR/venv"

echo "🔧 OpenClaw 飞书语音聊天 - 完全离线版 Setup"
echo "=============================================="
echo

# Check Python version
PYTHON_CMD=""
for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | grep -oP '\d+\.\d+')
        MAJOR=$(echo "$VERSION" | cut -d. -f1)
        MINOR=$(echo "$VERSION" | cut -d. -f2)
        
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ] && [ "$MINOR" -le 12 ]; then
            PYTHON_CMD="$cmd"
            echo "✓ Found suitable Python: $cmd ($VERSION)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.10-3.12 required (onnxruntime compatibility)"
    echo "   Current python3: $(python3 --version 2>&1)"
    exit 1
fi

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment already exists at: $VENV_DIR"
    read -p "Remove and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_DIR"
    else
        echo "Keeping existing venv. Run with --force to override."
        exit 0
    fi
fi

echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv "$VENV_DIR"

# Activate and install
echo "📥 Installing dependencies..."
source "$VENV_DIR/bin/activate"

# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install core dependencies
echo "   Installing core dependencies..."
pip install torch transformers accelerate soundfile requests

# Install qwen-tts (this may take several minutes)
echo "   Installing qwen-tts (this may take several minutes)..."
pip install qwen-tts

# Install additional dependencies for audio processing
echo "   Installing audio processing dependencies..."
pip install pydub

# Install whisper dependencies (for ASR server)
echo "   Installing Whisper dependencies..."
pip install openai-whisper 2>/dev/null || echo "   (whisper optional, using transformers instead)"

echo
echo "✅ Setup complete!"
echo
echo "Virtual environment created at:"
echo "  $VENV_DIR"
echo
echo "📋 Next steps:"
echo
echo "1. Download models (if not already done):"
echo "   - Whisper ASR: openai/whisper-large-v3-turbo"
echo "   - Qwen3-TTS: Qwen/Qwen3-TTS-12Hz-1.7B-Base"
echo "   See README.md for detailed download instructions"
echo
echo "2. Configure OpenClaw:"
echo "   Edit /root/.openclaw/openclaw.json"
echo "   - Add Whisper ASR config in tools.media.audio"
echo "   - Add Qwen3-TTS config in messages.tts"
echo "   See README.md for configuration details"
echo
echo "3. Start the Whisper ASR server (port 8001):"
echo "   source venv/bin/activate"
echo "   nohup python scripts/server/whisper-server.py --port 8001 > /tmp/whisper-server.log 2>&1 &"
echo
echo "4. Start the Qwen3-TTS server (port 8000, OpenAI compatible API):"
echo "   nohup python scripts/server/tts-base-server-openai.py --port 8000 --clone voice_embedings/huopo_kexin.pt > /tmp/tts-server.log 2>&1 &"
echo "   Note: If you don't have a voice file yet, omit --clone parameter to use default voice"
echo
echo "5. Restart OpenClaw:"
echo "   openclaw gateway restart"
echo
echo "📚 For more information, see README.md"
echo
