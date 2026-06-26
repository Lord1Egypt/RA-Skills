#!/bin/bash
# MOSI Voice Generator - Generate voice from text + style description
# Model: moss-voice-generator
# Requires: curl, jq, base64
set -e

usage() {
  cat >&2 <<'EOF'
Usage: mosi_voice_generator.sh --text TEXT --instruction DESC [options]

Options:
  --text, -t          Text to synthesize (required)
  --instruction, -i   Voice style description (required)
                      e.g. "播音腔女声，专业、清晰、有亲和力"
  --output, -o        Output WAV path
                      (default: ~/.openclaw/workspace/voice_gen_output.wav)
  --temperature       Sampling temperature (default: 1.5)
  --top-p             Nucleus sampling threshold (default: 0.6)
  --top-k             Top-K sampling (default: 50)
  --api-key, -k       Override MOSI_TTS_API_KEY env var

Examples:
  mosi_voice_generator.sh \
    --text "各位观众朋友们大家好" \
    --instruction "播音腔女声，专业、清晰、有亲和力"

  mosi_voice_generator.sh \
    --text "晚安，好梦" \
    --instruction "一个温柔的男声，轻柔舒缓"
EOF
  exit 2
}

TEXT=""
INSTRUCTION=""
OUTPUT="${HOME}/.openclaw/workspace/voice_gen_output.wav"
TEMPERATURE="1.5"
TOP_P="0.6"
TOP_K="50"
API_KEY="${MOSI_TTS_API_KEY}"

while [ $# -gt 0 ]; do
  case $1 in
    --text|-t)        TEXT="$2";        shift 2 ;;
    --instruction|-i) INSTRUCTION="$2"; shift 2 ;;
    --output|-o)      OUTPUT="$2";      shift 2 ;;
    --temperature)    TEMPERATURE="$2"; shift 2 ;;
    --top-p)          TOP_P="$2";       shift 2 ;;
    --top-k)          TOP_K="$2";       shift 2 ;;
    --api-key|-k)     API_KEY="$2";     shift 2 ;;
    -h|--help)        usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

[ -z "$TEXT" ]        && echo "Error: --text required" >&2 && usage
[ -z "$INSTRUCTION" ] && echo "Error: --instruction required" >&2 && usage
[ -z "$API_KEY" ]     && echo "Error: MOSI_TTS_API_KEY not set" >&2 && exit 1

# Build JSON payload with jq
PAYLOAD=$(jq -n \
  --arg text        "$TEXT" \
  --arg instruction "$INSTRUCTION" \
  --argjson temp    "$TEMPERATURE" \
  --argjson top_p   "$TOP_P" \
  --argjson top_k   "$TOP_K" \
  '{
    model: "moss-voice-generator",
    text: $text,
    instruction: $instruction,
    sampling_params: {
      temperature: $temp,
      top_p: $top_p,
      top_k: $top_k
    }
  }')

echo "Generating voice..." >&2

RESPONSE=$(curl -sf -X POST \
  "https://studio.mosi.cn/api/v1/audio/speech" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Extract audio_data and decode
AUDIO_B64=$(echo "$RESPONSE" | jq -r '.audio_data // empty')

if [ -z "$AUDIO_B64" ]; then
  echo "API error: $(echo "$RESPONSE" | jq -r '.message // .')" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
echo "$AUDIO_B64" | base64 -d > "$OUTPUT"
echo "Audio saved to: $OUTPUT" >&2
