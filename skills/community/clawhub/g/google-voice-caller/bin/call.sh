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

DURATION=${DURATION:-60}

if [ -n "$TEXT" ]; then
    echo "正在生成带静默期的高清语音包..."
    TIMESTAMP=$(date +%s)
    GREET_WAV="/tmp/greet_$TIMESTAMP.wav"
    SILENCE_WAV="/tmp/silence_$TIMESTAMP.wav"
    FINAL_WAV="/tmp/call_final_$TIMESTAMP.wav"

    edge-tts --text "$TEXT" --write-media "/tmp/tts_$TIMESTAMP.mp3" > /dev/null
    ffmpeg -i "/tmp/tts_$TIMESTAMP.mp3" -ar 16000 -ac 1 "$GREET_WAV" -y > /dev/null 2>&1
    ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 600 "$SILENCE_WAV" -y > /dev/null 2>&1
    ffmpeg -i "$GREET_WAV" -i "$SILENCE_WAV" -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" "$FINAL_WAV" -y > /dev/null 2>&1
    
    AUDIO_PATH="$FINAL_WAV"
fi

RECORDING_WEB="/tmp/gv_recorded_incoming.webm"
RECORDING_MP3="/tmp/gv_call_$(date +%Y%m%d_%H%M%S).mp3"
rm -f "$RECORDING_WEB"

# 启动引擎
node "$SKILL_DIR/lib/engine.js" "$NUMBER" "$AUDIO_PATH" "$DURATION"

# 通话结束后，仅进行 MP3 转码
if [ -f "$RECORDING_WEB" ]; then
    echo "✅ 收到录音，正在转码..."
    ffmpeg -i "$RECORDING_WEB" -q:a 0 -map a "$RECORDING_MP3" -y > /dev/null 2>&1
    echo "FINISHED_FILE:$RECORDING_MP3"
fi
