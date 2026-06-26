#!/usr/bin/env bash
# Nex Voice - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-voice"
BIN_DIR="$HOME/.local/bin"

echo "============================================"
echo "  Nex Voice - Setup"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="macos";;
    MINGW*|CYGWIN*|MSYS*) PLATFORM="windows";;
    *)       PLATFORM="unknown";;
esac
echo "Platform: $PLATFORM"
echo "Skill directory: $SKILL_DIR"
echo ""

# Step 1: Check Python
echo "[1/5] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "ERROR: Python 3 is required but not found." >&2
    echo "Install Python 3.9+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"
echo ""

# Step 2: Check Whisper
echo "[2/5] Checking Whisper..."
if command -v whisper &>/dev/null; then
    WHISPER_VERSION=$(whisper --version 2>&1 || echo "unknown")
    echo "  Found: $WHISPER_VERSION"
else
    echo "  WARNING: whisper CLI not found"
    echo "  Install with: pip install openai-whisper"
    echo "  Or faster alternative: pip install faster-whisper"
    echo ""
fi

# Step 3: Check FFmpeg
echo "[3/5] Checking FFmpeg..."
if command -v ffmpeg &>/dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -1)
    echo "  Found: $FFMPEG_VERSION"
else
    echo "  WARNING: ffmpeg not found"
    echo "  Install with:"
    case "$PLATFORM" in
        linux)
            echo "    Ubuntu/Debian: sudo apt-get install ffmpeg"
            echo "    Fedora: sudo dnf install ffmpeg"
            echo "    Arch: sudo pacman -S ffmpeg"
            ;;
        macos)
            echo "    Homebrew: brew install ffmpeg"
            ;;
        windows)
            echo "    Scoop: scoop install ffmpeg"
            echo "    Chocolatey: choco install ffmpeg"
            ;;
    esac
    echo ""
fi

# Step 4: Create data directory
echo "[4/5] Creating data directory..."
mkdir -p "$DATA_DIR"
mkdir -p "$DATA_DIR/recordings"
mkdir -p "$DATA_DIR/exports"
echo "  Created: $DATA_DIR"
echo ""

# Step 5: Initialize database
echo "[5/5] Initializing database..."
"$PYTHON" "$SKILL_DIR/lib/storage.py" --init
echo "  Database initialized"
echo ""

echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Data directory: $DATA_DIR"
echo ""
echo "To transcribe your first voice note:"
echo "  nex-voice transcribe /path/to/audio.ogg"
echo ""
echo "To list all recordings:"
echo "  nex-voice list"
echo ""
echo "To view statistics:"
echo "  nex-voice stats"
echo ""
