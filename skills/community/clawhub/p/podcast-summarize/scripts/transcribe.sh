#!/bin/bash
# Podcast Transcript Helper
# Usage: ./transcribe.sh <audio_file> [output_format]

AUDIO_FILE="$1"
OUTPUT_FORMAT="${2:-txt}"

if [ -z "$AUDIO_FILE" ]; then
    echo "Usage: $0 <audio_file> [output_format]"
    exit 1
fi

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: File not found: $AUDIO_FILE"
    exit 1
fi

# Get duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)
echo "Audio duration: $DURATION seconds"

# For now, output instructions for using Whisper
# TODO: Integrate actual Whisper transcription
echo ""
echo "To transcribe this file, run:"
echo "  whisper \"$AUDIO_FILE\" --language auto"
echo ""
echo "Or use OpenAI API:"
echo "  openai audio transcriptions.create --file \"$AUDIO_FILE\" --model whisper-1"
