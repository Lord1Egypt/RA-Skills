#!/usr/bin/env bash

# ASR CLI Wrapper powered by SkillBoss API Hub
# STT endpoint: https://api.heybossai.com/v1/pilot

API_BASE="https://api.heybossai.com/v1"

# 1. Check for API Key
if [ -z "$SKILLBOSS_API_KEY" ]; then
    echo "Error: SKILLBOSS_API_KEY environment variable is not set."
    echo "--------------------------------------------------------"
    echo "To use this skill, you need a SkillBoss API key."
    echo "1. Sign up at: https://heybossai.com"
    echo "2. Copy your key."
    echo "3. Run: export SKILLBOSS_API_KEY='your_key_here'"
    echo "--------------------------------------------------------"
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    transcribe)
        URL=""
        FILE=""
        LANGUAGE=""

        while [[ "$#" -gt 0 ]]; do
            case $1 in
                --url) URL="$2"; shift ;;
                --file) FILE="$2"; shift ;;
                --language) LANGUAGE="$2"; shift ;;
                --speakers|--words|--labels|--stream|--private|--confidence|--format|--webhook|--segment-duration)
                    shift ;;
                *) echo "Unknown parameter: $1"; exit 1 ;;
            esac
            shift
        done

        TMPFILE=$(mktemp /tmp/asr_audio_XXXXXX)
        TMPREQ=$(mktemp /tmp/asr_req_XXXXXX.json)

        if [ -n "$URL" ]; then
            FILENAME=$(basename "$URL" | cut -d'?' -f1)
            curl -sL "$URL" -o "$TMPFILE"
        elif [ -n "$FILE" ]; then
            FILENAME=$(basename "$FILE")
            cp "$FILE" "$TMPFILE"
        else
            echo "Usage: asr transcribe --url <url> OR --file <path>"
            rm -f "$TMPFILE" "$TMPREQ"
            exit 1
        fi

        AUDIO_B64=$(base64 "$TMPFILE" | tr -d '\n')
        rm -f "$TMPFILE"

        cat > "$TMPREQ" <<EOF
{
  "type": "stt",
  "inputs": {
    "audio_data": "$AUDIO_B64",
    "filename": "$FILENAME",
    "language": "$LANGUAGE"
  },
  "prefer": "balanced"
}
EOF

        curl -s -X POST "$API_BASE/pilot" \
            -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
            -H "Content-Type: application/json" \
            -d @"$TMPREQ"

        rm -f "$TMPREQ"
        ;;

    status)
        echo "Note: SkillBoss API Hub STT is synchronous — no job tracking needed."
        echo "Transcription results are returned immediately from the transcribe command."
        ;;

    help|*)
        echo "ASR Skill powered by SkillBoss API Hub"
        echo "Usage:"
        echo "  asr transcribe --url <url> [--language <code>]"
        echo "  asr transcribe --file <path> [--language <code>]"
        echo ""
        echo "  Options:"
        echo "    --language <code>      Set language (e.g., 'en', 'fr')"
        echo ""
        echo "Response: JSON with transcription text at .result.text"
        ;;
esac
