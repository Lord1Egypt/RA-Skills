#!/bin/bash
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
export NODE_PATH="$SKILL_DIR/node_modules:$NODE_PATH"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --number) NUMBER="$2"; shift ;;
        --text) TEXT="$2"; shift ;;
        --audio) AUDIO_PATH="$2"; shift ;;
        --duration) DURATION="$2"; shift ;;
    esac
    shift
done

if [ -n "$TEXT" ]; then
    AUDIO_PATH="/tmp/gv_dynamic_$RANDOM.wav"
    openclaw tts "$TEXT" > /dev/null
    LATEST_MP3=$(ls -t /tmp/openclaw/tts-*/voice-*.mp3 | head -n 1)
    ffmpeg -i "$LATEST_MP3" -ar 44100 -ac 1 "$AUDIO_PATH" -y > /dev/null 2>&1
fi

# 执行引擎
node "$SKILL_DIR/lib/engine.js" "$NUMBER" "$AUDIO_PATH" "$DURATION"
