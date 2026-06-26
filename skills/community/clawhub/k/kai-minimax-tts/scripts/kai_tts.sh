#!/bin/bash
set -e
ACTION="$1"
WORKSPACE="${KAI_MINIMAX_WORKSPACE:-$HOME/.openclaw/workspace/kai-minimax}"
mkdir -p "$WORKSPACE"
if [ "$ACTION" = "--speak" ]; then
    TEXT="$2"
    LANG="${3:-en}"
    API_KEY="${MINIMAX_API_KEY}"
    if [ -z "$API_KEY" ]; then echo "Error: MINIMAX_API_KEY not set"; exit 1; fi
    VOICE_ID="moss_audio_a43c027d-10db-11f1-83e4-92355c742862"
    [ "$LANG" != "es" ] && VOICE_ID="moss_audio_2b525bea-10da-11f1-bd2a-3a1ec25b94c4"
    RESP=$(curl -s -X POST "https://api-uw.minimax.io/v1/t2a_v2" -H "Content-Type: application/json" -H "Authorization: Bearer ${API_KEY}" -d "{\"model\":\"speech-2.8-turbo\",\"text\":\"${TEXT}\",\"stream\":false,\"output_format\":\"hex\",\"voice_setting\":{\"voice_id\":\"${VOICE_ID}\",\"speed\":1},\"audio_setting\":{\"sample_rate\":32000}}")
    HEX=$(echo "$RESP" | grep -o '"audio":"[^"]*"' | cut -d'"' -f4)
    [ -n "$HEX" ] && echo "$HEX" | xxd -r -p > "${WORKSPACE}/Kai.mp3" && echo "Generated: ${WORKSPACE}/Kai.mp3" || echo "Error: $RESP"
elif [ "$ACTION" = "--transcribe" ]; then
    FILE="$2"
    whisper "$FILE" --model base --output_format txt --output_dir /tmp
    BASE=$(basename "$FILE" | sed 's/\.[^.]*$//')
    cp "/tmp/${BASE}.txt" "${WORKSPACE}/latest_from_blaze.txt" 2>/dev/null || true
    echo "Done"
fi
