#!/bin/bash
# Voice to Text - Speech-to-Text using Whisper.cpp
# Converts audio files to text transcription
# Usage: voice-to-text <audio_file> [--model tiny|small|medium] [--language en|ne|hi] [--cache]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
CONFIG_FILE="$SCRIPT_DIR/../config/voices.yaml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MODEL=""
LANGUAGE=""
USE_CACHE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --language)
            LANGUAGE="$2"
            shift 2
            ;;
        --cache)
            USE_CACHE="--cache"
            shift
            ;;
        -h|--help)
            echo "Usage: voice-to-text <audio_file> [options]"
            echo ""
            echo "Options:"
            echo "  --model <tiny|small|medium>    Whisper model (default: tiny)"
            echo "  --language <en|ne|hi|...>      Language code (default: en)"
            echo "  --cache                        Enable caching"
            echo "  -h, --help                      Show this help"
            echo ""
            echo "Examples:"
            echo "  voice-to-text recording.wav"
            echo "  voice-to-text meeting.mp4 --model small --language en"
            echo "  voice-to-text voice-note.ogg --cache"
            exit 0
            ;;
        *)
            if [ -z "$AUDIO_FILE" ]; then
                AUDIO_FILE="$1"
            fi
            shift
            ;;
    esac
done

# Check audio file
if [ -z "$AUDIO_FILE" ] || [ ! -f "$AUDIO_FILE" ]; then
    echo -e "${RED}❌ Error: Audio file not found${NC}"
    echo ""
    echo "Usage: voice-to-text <audio_file>"
    echo "Try 'voice-to-text --help' for more information."
    exit 1
fi

# Check Python and dependencies
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python3 not found${NC}"
    exit 1
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    echo -e "${RED}❌ Error: PyYAML not installed${NC}"
    echo -e "${YELLOW}💡 Install with: pip3 install pyyaml${NC}"
    exit 1
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}❌ Error: FFmpeg not found${NC}"
    echo -e "${YELLOW}💡 Install with: sudo apt-get install -y ffmpeg${NC}"
    exit 1
fi

# Transcribe using Python wrapper
echo -e "${BLUE}📝 Transcribing audio...${NC}"

if [ -n "$MODEL" ] && [ -n "$LANGUAGE" ]; then
    python3 "$LIB_DIR/stt.py" "$AUDIO_FILE" "$MODEL" "$LANGUAGE" 2>&1
elif [ -n "$MODEL" ]; then
    python3 "$LIB_DIR/stt.py" "$AUDIO_FILE" "$MODEL" 2>&1
else
    python3 "$LIB_DIR/stt.py" "$AUDIO_FILE" 2>&1
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Transcription complete${NC}"
else
    echo -e "${RED}❌ Transcription failed${NC}"
    exit $EXIT_CODE
fi
