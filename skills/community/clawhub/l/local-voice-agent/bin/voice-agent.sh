#!/bin/bash
# Voice Agent - Complete Voice Pipeline
# Records audio, transcribes with Whisper, processes with OpenClaw AI, and speaks response
# Usage: voice-agent [options] [<text_or_file>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
CONFIG_FILE="$SCRIPT_DIR/../config/voices.yaml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
INTERACTIVE=false
NO_VOICE=false
AUDIO_FILE=""
TEXT_INPUT=""
DURATION=5
WAKE_WORD=""
RECORDING_DIR="/tmp/voice-agent"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        --no-voice)
            NO_VOICE=true
            shift
            ;;
        -f|--file)
            AUDIO_FILE="$2"
            shift 2
            ;;
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --wake-word)
            WAKE_WORD="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: voice-agent [options] [<text_or_file>]"
            echo ""
            echo "Options:"
            echo "  -i, --interactive              Interactive conversation mode"
            echo "  -f, --file <audio_file>        Process audio file instead of recording"
            echo "  --duration <seconds>           Recording duration (default: 5)"
            echo "  --no-voice                     Text-only mode (no TTS)"
            echo "  --wake-word <word>             Enable wake word detection"
            echo "  -h, --help                      Show this help"
            echo ""
            echo "Examples:"
            echo "  voice-agent \"What time is it?\""
            echo "  voice-agent --interactive"
            echo "  voice-agent --file recording.wav"
            echo "  voice-agent \"Hello\" --no-voice"
            echo "  voice-agent --duration 10"
            exit 0
            ;;
        *)
            if [ -z "$TEXT_INPUT" ]; then
                TEXT_INPUT="$1"
            fi
            shift
            ;;
    esac
done

# Setup
mkdir -p "$RECORDING_DIR"

# Check dependencies
check_dependencies() {
    local missing=0

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 not found${NC}"
        missing=1
    fi

    if ! python3 -c "import yaml; import requests" 2>/dev/null; then
        echo -e "${RED}❌ Python dependencies missing${NC}"
        echo -e "${YELLOW}💡 Install: pip3 install pyyaml requests${NC}"
        missing=1
    fi

    if ! command -v ffmpeg &> /dev/null; then
        echo -e "${RED}❌ FFmpeg not found${NC}"
        echo -e "${YELLOW}💡 Install: sudo apt-get install -y ffmpeg${NC}"
        missing=1
    fi

    # Check Whisper.cpp
    WHISPER_DIR=$(grep "whisper_dir:" "$CONFIG_FILE" | sed 's/.*: *//;s/["'\'']//g')
    if [ -z "$WHISPER_DIR" ]; then
        WHISPER_DIR="$HOME/.local/whisper.cpp"
    fi
    WHISPER_DIR=$(eval echo "$WHISPER_DIR")

    if [ ! -d "$WHISPER_DIR" ]; then
        echo -e "${RED}❌ Whisper.cpp not found at $WHISPER_DIR${NC}"
        echo -e "${YELLOW}💡 Install: git clone https://github.com/ggerganov/whisper.cpp ~/.local/whisper.cpp${NC}"
        echo -e "${YELLOW}   Then: cd ~/.local/whisper.cpp && make -j4${NC}"
        missing=1
    fi

    # Check TTS server
    TTS_URL=$(grep "url:" "$CONFIG_FILE" | head -1 | sed 's/.*: *//;s/["'\'']//g')
    if [ -z "$TTS_URL" ]; then
        TTS_URL="http://localhost:5000"
    fi

    if ! curl -s --max-time 2 "$TTS_URL/v1/voices" > /dev/null 2>&1; then
        echo -e "${RED}❌ Cannot connect to TTS server at $TTS_URL${NC}"
        echo -e "${YELLOW}💡 Start Pocket-TTS: python3 -m app.main --host 0.0.0.0 --port 5000${NC}"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        exit 1
    fi
}

# Process text through OpenClaw
process_with_ai() {
    local text="$1"
    local session_key=""

    # Get session key from config
    SESSION_KEY=$(grep "session_key:" "$CONFIG_FILE" | sed 's/.*: *//;s/["'\'']//g')
    if [ -n "$SESSION_KEY" ]; then
        session_key="$SESSION_KEY"
    fi

    # Call OpenClaw AI (placeholder - implement actual OpenClaw integration)
    echo "Response to: $text"
    echo "This is a placeholder. Integrate with OpenClaw AI here."
}

# Interactive mode
interactive_mode() {
    echo -e "${PURPLE}╔════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  🎤 Voice Agent - Interactive Mode    ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}💡 Say 'quit', 'exit', or 'stop' to end conversation${NC}"
    echo -e "${YELLOW}💡 Or press Ctrl+C to exit${NC}"
    echo ""

    while true; do
        # Record audio
        RECORDING_FILE="$RECORDING_DIR/recording_$(date +%s).wav"
        echo -e "${CYAN}[User]${NC}"
        echo -e "${BLUE}🎤 Recording for $DURATION seconds... (speak now)${NC}"

        ffmpeg -f dshow -i audio="Microphone" -t "$DURATION" -y "$RECORDING_FILE" 2>/dev/null || \
        ffmpeg -f alsa -i default -t "$DURATION" -y "$RECORDING_FILE" 2>/dev/null

        if [ ! -f "$RECORDING_FILE" ]; then
            echo -e "${RED}❌ Failed to record audio${NC}"
            continue
        fi

        # Transcribe
        echo -e "${BLUE}📝 Transcribing...${NC}"
        TRANSCRIPTION=$(python3 "$LIB_DIR/stt.py" "$RECORDING_FILE" 2>&1)

        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Transcription failed: $TRANSCRIPTION${NC}"
            rm -f "$RECORDING_FILE"
            continue
        fi

        echo -e "${CYAN}Text:${NC} $TRANSCRIPTION"

        # Check for exit commands
        if [[ "$TRANSCRIPTION" =~ ^(quit|exit|stop|goodbye)$ ]]; then
            echo -e "${GREEN}👋 Goodbye!${NC}"
            rm -f "$RECORDING_FILE"
            break
        fi

        # Process with AI
        echo -e "${CYAN}[AI]${NC}"
        echo -e "${BLUE}🧠 Processing...${NC}"

        RESPONSE_TEXT=$(process_with_ai "$TRANSCRIPTION")

        if [ "$NO_VOICE" = false ]; then
            # Generate speech
            echo -e "${BLUE}🔊 Speaking...${NC}"
            RESPONSE_AUDIO=$(mktemp --suffix=.wav)
            python3 "$LIB_DIR/tts.py" "$RESPONSE_TEXT" "" "$RESPONSE_AUDIO" 2>&1

            if [ $? -eq 0 ]; then
                ffplay -nodisp -autoexit "$RESPONSE_AUDIO" 2>/dev/null || \
                paplay "$RESPONSE_AUDIO" 2>/dev/null || true
                rm -f "$RESPONSE_AUDIO"
            else
                echo -e "${YELLOW}⚠️  TTS failed, showing text:${NC}"
                echo "$RESPONSE_TEXT"
            fi
        else
            echo -e "${CYAN}Response:${NC} $RESPONSE_TEXT"
        fi

        # Cleanup
        rm -f "$RECORDING_FILE"
        echo ""
    done
}

# Process single command
process_command() {
    local input="$1"

    # Check if input is a file
    if [ -f "$input" ]; then
        AUDIO_FILE="$input"
    fi

    if [ -n "$AUDIO_FILE" ]; then
        # Process audio file
        echo -e "${BLUE}📝 Transcribing audio file: $AUDIO_FILE${NC}"
        TRANSCRIPTION=$(python3 "$LIB_DIR/stt.py" "$AUDIO_FILE" 2>&1)

        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Transcription failed: $TRANSCRIPTION${NC}"
            exit 1
        fi

        echo -e "${GREEN}Transcription:${NC}"
        echo "$TRANSCRIPTION"
        input="$TRANSCRIPTION"
    fi

    # Process text
    echo -e "${BLUE}🧠 Processing with AI...${NC}"
    RESPONSE_TEXT=$(process_with_ai "$input")

    if [ "$NO_VOICE" = false ]; then
        echo -e "${BLUE}🔊 Generating speech...${NC}"
        RESPONSE_AUDIO=$(mktemp --suffix=.wav)
        python3 "$LIB_DIR/tts.py" "$RESPONSE_TEXT" "" "$RESPONSE_AUDIO" 2>&1

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Response:${NC}"
            ffplay -nodisp -autoexit "$RESPONSE_AUDIO" 2>/dev/null || \
            paplay "$RESPONSE_AUDIO" 2>/dev/null || \
            echo "$RESPONSE_TEXT"
            rm -f "$RESPONSE_AUDIO"
        else
            echo -e "${YELLOW}⚠️  TTS failed:${NC}"
            echo "$RESPONSE_TEXT"
        fi
    else
        echo -e "${GREEN}✅ Response:${NC}"
        echo "$RESPONSE_TEXT"
    fi
}

# Main execution
main() {
    # Show banner
    echo -e "${PURPLE}╔════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  🎤 Voice Agent                       ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}"
    echo ""

    # Check dependencies
    check_dependencies

    # Handle modes
    if [ "$INTERACTIVE" = true ]; then
        interactive_mode
    elif [ -n "$TEXT_INPUT" ]; then
        process_command "$TEXT_INPUT"
    elif [ -n "$AUDIO_FILE" ]; then
        process_command "$AUDIO_FILE"
    else
        echo -e "${YELLOW}💡 Usage:${NC}"
        echo "  voice-agent \"What time is it?\""
        echo "  voice-agent --interactive"
        echo "  voice-agent --file recording.wav"
        echo ""
        echo "Try 'voice-agent --help' for more options."
    fi
}

main "$@"
