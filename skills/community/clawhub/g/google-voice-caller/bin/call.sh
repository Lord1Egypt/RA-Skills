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

# 默认设置
DURATION=${DURATION:-60}

# 如果有文字，使用 Edge-TTS 生成特制的“开场即闭嘴”音频
if [ -n "$TEXT" ]; then
    echo "正在生成带静默期的高品质 AI 语音..."
    RAW_MP3="/tmp/gv_tts_$(date +%s).mp3"
    GREET_WAV="/tmp/gv_greet_$(date +%s).wav"
    SILENCE_WAV="/tmp/gv_silence_$(date +%s).wav"
    FINAL_WAV="/tmp/gv_call_final_$(date +%s).wav"

    # 1. 生成语音
    edge-tts --text "$TEXT" --write-media "$RAW_MP3" > /dev/null
    # 2. 转码为 16k mono
    ffmpeg -i "$RAW_MP3" -ar 16000 -ac 1 "$GREET_WAV" -y > /dev/null 2>&1
    # 3. 制作超长静音 (300秒) 以防止循环播放
    ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 300 "$SILENCE_WAV" -y > /dev/null 2>&1
    # 4. 拼接
    ffmpeg -i "concat:$GREET_WAV|$SILENCE_WAV" -c copy "$FINAL_WAV" -y > /dev/null 2>&1
    
    AUDIO_PATH="$FINAL_WAV"
fi

# 启动引擎
RECORDING_WEB="/tmp/gv_recorded_incoming.webm"
RECORDING_MP3="/tmp/gv_final_output.mp3"
rm -f "$RECORDING_WEB" "$RECORDING_MP3"

node "$SKILL_DIR/lib/engine.js" "$NUMBER" "$AUDIO_PATH" "$DURATION"

# 通话结束后，如果存在录音则处理
if [ -f "$RECORDING_WEB" ]; then
    echo "✅ 收到录音，正在后期处理..."
    ffmpeg -i "$RECORDING_WEB" -q:a 0 -map a "$RECORDING_MP3" -y > /dev/null 2>&1
    echo "正在尝试转写文字..."
    whisper "$RECORDING_MP3" --model base --language Chinese --output_format txt --output_dir /tmp/gv_trans 2>/dev/null
    
    echo "--- 通话反馈 ---"
    if [ -f "/tmp/gv_trans/gv_final_output.txt" ]; then
        cat "/tmp/gv_trans/gv_final_output.txt"
    else
        echo "(无法提取文字，可能录音过短或环境过于嘈杂)"
    fi
    echo "音频已存至: $RECORDING_MP3"
fi
