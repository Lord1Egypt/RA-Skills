#!/bin/bash
# Text to Voice - Text-to-Speech using Pocket-TTS
# Converts text to speech audio file
# Usage: text-to-voice <text> [output_file] [--voice <voice_id>] [--format wav|mp3]

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
VOICE=""
FORMAT=""
OUTPUT_FILE=""

# Parse arguments
TEXT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --voice)
            VOICE="$2"
            shift 2
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: text-to-voice <text> [output_file] [options]"
            echo ""
            echo "Options:"
            echo "  --voice <voice_id>             Voice to use (default: alba)"
            echo "  --format <wav|mp3>             Output format (default: wav)"
            echo "  -o, --output <file>            Output file path"
            echo "  -h, --help                      Show this help"
            echo ""
            echo "Examples:"
            echo "  text-to-voice \"Hello world!\""
            echo "  text-to-voice \"Namaste!\" greeting.wav"
            echo "  text-to-voice \"Hi there\" --voice \"peter voice\" --format mp3"
            echo "  text-to-voice \"Hello\" -o output.wav"
            exit 0
            ;;
        *)
            if [ -z "$TEXT" ]; then
                TEXT="$1"
            elif [ -z "$OUTPUT_FILE" ]; then
                OUTPUT_FILE="$1"
            fi
            shift
            ;;
    esac
done

# Check text
if [ -z "$TEXT" ]; then
    echo -e "${RED}❌ Error: No text provided${NC}"
    echo ""
    echo "Usage: text-to-voice <text> [output_file]"
    echo "Try 'text-to-voice --help' for more information."
    exit 1
fi

# Generate output filename if not provided
if [ -z "$OUTPUT_FILE" ]; then
    # Create temp file
    OUTPUT_FILE=$(mktemp --suffix=.wav 2>/dev/null || tempfile -s .wav 2>/dev/null || echo "/tmp/output_$(date +%s).wav")
fi

# Check Python and dependencies
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python3 not found${NC}"
    exit 1
fi

if ! python3 -c "import yaml; import requests" 2>/dev/null; then
    echo -e "${RED}❌ Error: Dependencies not installed${NC}"
    echo -e "${YELLOW}💡 Install with: pip3 install pyyaml requests${NC}"
    exit 1
fi

# Check TTS server
TTS_URL=$(grep "url:" "$CONFIG_FILE" | head -1 | sed 's/.*: *//;s/["'\'']//g')
if [ -z "$TTS_URL" ]; then
    TTS_URL="http://localhost:5000"
fi

echo -e "${BLUE}🔊 Generating speech...${NC}"
echo -e "${BLUE}   Text: $TEXT${NC}"

# Generate speech using Python wrapper
if [ -n "$VOICE" ] && [ -n "$FORMAT" ]; then
    python3 "$LIB_DIR/tts.py" "$TEXT" "$VOICE" "$OUTPUT_FILE" 2>&1
elif [ -n "$VOICE" ]; then
    python3 "$LIB_DIR/tts.py" "$TEXT" "$VOICE" "$OUTPUT_FILE" 2>&1
elif [ -n "$FORMAT" ]; then
    python3 "$LIB_DIR/tts.py" "$TEXT" "" "$OUTPUT_FILE" 2>&1
else
    python3 "$LIB_DIR/tts.py" "$TEXT" "" "$OUTPUT_FILE" 2>&1
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Audio generated: $OUTPUT_FILE${NC}"

    # Try to play the audio
    if command -v ffplay &> /dev/null; then
        echo -e "${BLUE}🎵 Playing audio...${NC}"
        ffplay -nodisp -autoexit "$OUTPUT_FILE" 2>/dev/null || true
    elif command -v paplay &> /dev/null; then
        paplay "$OUTPUT_FILE" 2>/dev/null || true
    fi
else
    echo -e "${RED}❌ TTS generation failed${NC}"
    exit $EXIT_CODE
fi
