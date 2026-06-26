#!/bin/bash
# MOSI Multi-Speaker Dialogue (moss-ttsd)
# Endpoint: POST /api/v1/audio/speech, model: moss-ttsd
# Supports 1~5 speakers via --speakers array
# Text format: [S1]text[S2]text (no space after tag, uppercase)
# Requires: curl, jq, base64
set -e

usage() {
  cat >&2 <<'EOF'
Usage: mosi_dialogue.sh --text TEXT --speakers ID1[,ID2,...] [options]

Options:
  --text,        -t  TEXT   Dialogue text with [S1]~[S5] tags (required)
                            e.g. "[S1]你好！[S2]你好，很高兴认识你。[S1]我也是！"
                            Rules: uppercase tags, no space after tag
  --speakers,    -s  IDs    Comma-separated voice IDs, 1~5 (required)
                            Order matches [S1]~[S5] in text
  --output,      -o  PATH   Output WAV path
                            (default: ~/.openclaw/workspace/dialogue.wav)
  --model,       -m  MODEL  Model name (default: moss-ttsd)
                            Snapshot: moss-ttsd-20260320
  --max-tokens       INT    Max new tokens (default: 20000, max: 40960)
  --temperature      FLOAT  Sampling temperature (default: 1.1)
  --top-p            FLOAT  Nucleus sampling (default: 0.9)
  --top-k            INT    Top-K sampling (default: 50)
  --rep-penalty      FLOAT  Repetition penalty (default: 1.1)
  --audio-penalty    FLOAT  Audio presence penalty (default: 1.5)
  --meta-info               Return performance metrics
  --api-key,     -k  KEY    Override MOSI_TTS_API_KEY env var

Examples:
  # 2-speaker dialogue
  mosi_dialogue.sh \
    --text "[S1]你好，今天天气真好。[S2]是的，很适合出去走走。" \
    --speakers "2001257729754140672,2002941772480647168"

  # 3-speaker dialogue
  mosi_dialogue.sh \
    --text "[S1]你好！[S2]你好！[S3]大家好！" \
    --speakers "ID_A,ID_B,ID_C" \
    --output ~/my_dialogue.wav
EOF
  exit 1
}

TEXT=""
SPEAKERS=""
OUTPUT="${HOME}/.openclaw/workspace/dialogue.wav"
MODEL="moss-ttsd"
API_KEY="${MOSI_TTS_API_KEY}"
MAX_TOKENS="20000"
TEMPERATURE="1.1"
TOP_P="0.9"
TOP_K="50"
REP_PENALTY="1.1"
AUDIO_PENALTY="1.5"
META_INFO="false"

while [ $# -gt 0 ]; do
  case $1 in
    --text|-t)          TEXT="$2";         shift 2 ;;
    --speakers|-s)      SPEAKERS="$2";     shift 2 ;;
    --output|-o)        OUTPUT="$2";       shift 2 ;;
    --model|-m)         MODEL="$2";        shift 2 ;;
    --api-key|-k)       API_KEY="$2";      shift 2 ;;
    --max-tokens)       MAX_TOKENS="$2";   shift 2 ;;
    --temperature)      TEMPERATURE="$2";  shift 2 ;;
    --top-p)            TOP_P="$2";        shift 2 ;;
    --top-k)            TOP_K="$2";        shift 2 ;;
    --rep-penalty)      REP_PENALTY="$2";  shift 2 ;;
    --audio-penalty)    AUDIO_PENALTY="$2";shift 2 ;;
    --meta-info)        META_INFO="true";  shift ;;
    -h|--help)          usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

[ -z "$TEXT" ]     && echo "Error: --text required" >&2 && usage
[ -z "$SPEAKERS" ] && echo "Error: --speakers required" >&2 && usage
[ -z "$API_KEY" ]  && echo "Error: MOSI_TTS_API_KEY not set" >&2 && exit 1

# Convert comma-separated speakers to JSON array
SPEAKERS_JSON=$(echo "$SPEAKERS" | \
  tr ',' '\n' | \
  jq -R . | \
  jq -sc .)

# Build JSON payload with jq
PAYLOAD=$(jq -n \
  --arg  model       "$MODEL" \
  --arg  text        "$TEXT" \
  --argjson speakers "$SPEAKERS_JSON" \
  --argjson meta     "$META_INFO" \
  --argjson maxtok   "$MAX_TOKENS" \
  --argjson temp     "$TEMPERATURE" \
  --argjson top_p    "$TOP_P" \
  --argjson top_k    "$TOP_K" \
  --argjson rep      "$REP_PENALTY" \
  --argjson aud      "$AUDIO_PENALTY" \
  '{
    model: $model,
    text: $text,
    speakers: $speakers,
    meta_info: $meta,
    sampling_params: {
      max_new_tokens: $maxtok,
      temperature: $temp,
      top_p: $top_p,
      top_k: $top_k,
      repetition_penalty: $rep,
      audio_presence_penalty: $aud
    }
  }')

echo "Generating dialogue (${#SPEAKERS_JSON} speakers)..." >&2

RESPONSE=$(curl -sf -X POST \
  "https://studio.mosi.cn/api/v1/audio/speech" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 1800 \
  -d "$PAYLOAD")

# Check for warnings
WARNINGS=$(echo "$RESPONSE" | jq -r '.warnings[]?.message // empty' 2>/dev/null)
[ -n "$WARNINGS" ] && echo "Warning: $WARNINGS" >&2

# Extract and decode audio
AUDIO_B64=$(echo "$RESPONSE" | jq -r '.audio_data // empty')

if [ -z "$AUDIO_B64" ]; then
  echo "API error: $(echo "$RESPONSE" | jq -r '.error // .message // .')" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
echo "$AUDIO_B64" | base64 -d > "$OUTPUT"
echo "Dialogue saved to: $OUTPUT" >&2

# Print meta_info if requested
if [ "$META_INFO" = "true" ]; then
  echo "$RESPONSE" | \
    jq -r '.meta_info | "latency: \(.latency_ms)ms | tokens: \(.total_tokens)"' \
    2>/dev/null >&2 || true
fi
