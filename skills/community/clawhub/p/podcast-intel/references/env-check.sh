#!/bin/bash
# Environment variable discovery and validation for podcast-intel

echo "🔍 Environment Variable Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Required environment variables
echo "📌 Required Variables:"
echo ""

# OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY: NOT SET"
    echo "   Get one at: https://platform.openai.com/api-keys"
    echo "   Set with: export OPENAI_API_KEY='sk-...'"
else
    echo "✓ OPENAI_API_KEY: SET (${#OPENAI_API_KEY} chars)"
    echo "   Value is masked for security"
fi

echo ""
echo "🎛️  Optional Variables:"
echo ""

# OpenAI Base URL
if [ -z "$OPENAI_BASE_URL" ]; then
    echo "→ OPENAI_BASE_URL: NOT SET (using default: https://api.openai.com/v1)"
else
    echo "✓ OPENAI_BASE_URL: $OPENAI_BASE_URL"
fi

# Whisper Model
if [ -z "$WHISPER_MODEL" ]; then
    echo "→ WHISPER_MODEL: NOT SET (using default: whisper-1)"
else
    echo "✓ WHISPER_MODEL: $WHISPER_MODEL"
fi

# Local Whisper
if [ -z "$WHISPER_USE_LOCAL" ]; then
    echo "→ WHISPER_USE_LOCAL: NOT SET (using API, not local)"
else
    echo "✓ WHISPER_USE_LOCAL: $WHISPER_USE_LOCAL"
fi

echo ""
echo "🔧 System Dependencies:"
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ python3: $(python3 --version)"
else
    echo "❌ python3: NOT FOUND"
fi

# Check ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg: $(ffmpeg -version | head -n1)"
else
    echo "❌ ffmpeg: NOT FOUND (required for audio processing)"
fi

# Check curl
if command -v curl &> /dev/null; then
    echo "✓ curl: $(curl --version | head -n1)"
else
    echo "→ curl: NOT FOUND (optional, for HTTP requests)"
fi

echo ""
echo "📂 Directories:"
echo ""

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
CONFIG_DIR="$OPENCLAW_DIR/config"
CACHE_DIR="$OPENCLAW_DIR/cache/podcast-intel"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace/podcast-intel"
MEMORY_DIR="$OPENCLAW_DIR/memory/podcast-intel"

echo "Config: $CONFIG_DIR"
if [ -d "$CONFIG_DIR" ]; then
    echo "  ✓ Exists"
    if [ -f "$CONFIG_DIR/podcast-intel-feeds.yaml" ]; then
        echo "    - feeds.yaml ✓"
    else
        echo "    - feeds.yaml ❌ (missing)"
    fi
    if [ -f "$CONFIG_DIR/podcast-intel-interests.yaml" ]; then
        echo "    - interests.yaml ✓"
    else
        echo "    - interests.yaml ❌ (missing)"
    fi
else
    echo "  ❌ Does not exist"
fi

echo ""
echo "Cache: $CACHE_DIR"
if [ -d "$CACHE_DIR" ]; then
    echo "  ✓ Exists"
    size=$(du -sh "$CACHE_DIR" 2>/dev/null | cut -f1)
    echo "    Size: $size"
else
    echo "  → Does not exist (will create on first run)"
fi

echo ""
echo "Workspace: $WORKSPACE_DIR"
if [ -d "$WORKSPACE_DIR" ]; then
    echo "  ✓ Exists"
else
    echo "  → Does not exist (will create on first run)"
fi

echo ""
echo "Memory: $MEMORY_DIR"
if [ -d "$MEMORY_DIR" ]; then
    echo "  ✓ Exists"
    if [ -f "$WORKSPACE_DIR/diary.jsonl" ]; then
        lines=$(wc -l < "$WORKSPACE_DIR/diary.jsonl")
        echo "    Diary entries: $lines"
    fi
else
    echo "  → Does not exist (will create on first run)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Environment check complete"
