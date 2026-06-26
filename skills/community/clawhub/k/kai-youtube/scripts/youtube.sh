#!/bin/bash
# Kai-YouTube: Watch YouTube videos by transcribing with Whisper
# Usage: ./youtube.sh <YouTube_URL> [--language <lang>]

set -e

URL="$1"
LANGUAGE="$2"
WORKSPACE="/home/kai/.openclaw/workspace/kai-yt-videos"

if [ -z "$URL" ]; then
    echo "Usage: $0 <YouTube_URL> [--language <lang>]"
    exit 1
fi

# Extract video ID - handle both formats:
# https://www.youtube.com/watch?v=VIDEO_ID
# https://youtu.be/VIDEO_ID
VIDEO_ID=$(echo "$URL" | sed -E 's/.*[?&]v=([^&]+).*/\1/; s/.*youtu\.be\/([^?]+).*/\1/')

if [ -z "$VIDEO_ID" ] || [ "$VIDEO_ID" == "$URL" ]; then
    echo "Error: Could not extract video ID from URL"
    exit 1
fi

AUDIO_OUTPUT="${WORKSPACE}/kai_yt_${VIDEO_ID}.mp3"
TRANSCRIPT_OUTPUT="${WORKSPACE}/kai_yt_${VIDEO_ID}.txt"

# Create workspace folder if it doesn't exist
mkdir -p "$WORKSPACE"

# Remove old files if they exist to force fresh download
rm -f "$AUDIO_OUTPUT" "$TRANSCRIPT_OUTPUT"

echo "📺 Downloading audio from: $URL (ID: $VIDEO_ID)"
echo "📁 Folder: $WORKSPACE"
yt-dlp --extract-audio --audio-format mp3 --output "$AUDIO_OUTPUT" "$URL"

echo ""
echo "🎙️ Transcribing with Whisper..."
echo "⏳ This may take several minutes for long videos..."
if [ -n "$LANGUAGE" ]; then
    whisper "$AUDIO_OUTPUT" --model base --language "$LANGUAGE" --output_format txt --output_dir "$WORKSPACE"
else
    whisper "$AUDIO_OUTPUT" --model base --output_format txt --output_dir "$WORKSPACE"
fi

echo ""
echo "📝 TRANSCRIPT:"
echo "=============="
cat "$TRANSCRIPT_OUTPUT"
echo "=============="
echo ""
echo "✅ DONE! Both files saved to: $WORKSPACE"
echo "   🎬 Audio:  kai_yt_${VIDEO_ID}.mp3"
echo "   📝 Trans: kai_yt_${VIDEO_ID}.txt"
echo ""
echo "   To read transcript later:"
echo "   cat $TRANSCRIPT_OUTPUT"
