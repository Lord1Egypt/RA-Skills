#!/bin/bash
# Kai Realtime Voice - MiniMax WebSocket Streaming
set -e

ACTION="$1"
WORKSPACE="${KAI_MINIMAX_WORKSPACE:-$HOME/.openclaw/workspace/kai-minimax}"
API_KEY="${MINIMAX_API_KEY}"

if [ -z "$API_KEY" ]; then
    echo "Error: MINIMAX_API_KEY not set"
    exit 1
fi

case "$ACTION" in
    --test)
        echo "Testing MiniMax WebSocket connection..."
        # Test basic connectivity to API
        RESP=$(curl -s -o /dev/null -w "%{http_code}" "https://api.minimax.io/v1/t2a_v2" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json" \
            -d '{"model":"speech-02-turbo","text":"test","stream":false,"output_format":"mp3"}')
        if [ "$RESP" = "200" ] || [ "$RESP" = "400" ]; then
            echo "API connection OK (code: $RESP)"
        else
            echo "API connection failed (code: $RESP)"
            exit 1
        fi
        ;;
    --stream)
        TEXT="$2"
        VOICE_ID="${KAI_ENGLISH_VOICE_ID:-moss_audio_2b525bea-10da-11f1-bd2a-3a1ec25b94c4}"
        
        if [ -z "$TEXT" ]; then
            echo "Usage: $0 --stream \"text\""
            exit 1
        fi
        
        echo "Streaming text: $TEXT"
        
        # For real streaming, would use WebSocket here
        # For now, fallback to REST API
        RESP=$(curl -s -X POST "https://api.minimax.io/v1/t2a_v2" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json" \
            -d "{\"model\":\"speech-02-turbo\",\"text\":\"$TEXT\",\"stream\":false,\"output_format\":\"hex\",\"voice_setting\":{\"voice_id\":\"$VOICE_ID\",\"speed\":1},\"audio_setting\":{\"sample_rate\":32000}}")
        
        HEX=$(echo "$RESP" | grep -o '"audio":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$HEX" ]; then
            mkdir -p "$WORKSPACE"
            echo "$HEX" | xxd -r -p > "${WORKSPACE}/realtime_test.mp3"
            echo "Saved: ${WORKSPACE}/realtime_test.mp3"
        else
            echo "Error: $RESP"
            exit 1
        fi
        ;;
    *)
        echo "Kai Realtime Voice"
        echo ""
        echo "Usage:"
        echo "  $0 --test          Test API connection"
        echo "  $0 --stream \"text\"  Stream text to audio"
        ;;
esac
