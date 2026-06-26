#!/bin/bash
# mosi_asr.sh - Speech to Text via MOSI Transcribe Diarize
# Model: moss-transcribe-diarize
# Endpoint: POST /api/v1/audio/transcriptions
# Supports: WAV, MP3, M4A, FLAC, OGG, OPUS, MP4, WebM, PCM, MOV (max 10MB)
set -e

usage() {
  cat <<EOF
Usage: $0 --file PATH [options]

Options:
  --file,     -f  PATH    Audio file to transcribe (required)
  --language, -l  LANG    Language hint, e.g. zh, en (optional)
  --api-key,  -k  KEY     Override MOSI_TTS_API_KEY env var
  --json,     -j          Output raw JSON (includes timestamps + speaker IDs)
  --max-tokens  INT       max_new_tokens for long audio (default: 4096)

Examples:
  # Transcribe a Feishu inbound voice file
  $0 --file "\$MediaPath"

  # Long audio (increase max tokens)
  $0 --file long_audio.wav --max-tokens 8192

  # Get raw JSON with timestamps and speaker labels
  $0 --file audio.opus --json
EOF
  exit 1
}

FILE=""
LANGUAGE=""
API_KEY="${MOSI_TTS_API_KEY}"
JSON_OUT=0
MAX_TOKENS=4096

while [ $# -gt 0 ]; do
  case $1 in
    --file|-f)       FILE="$2";       shift 2 ;;
    --language|-l)   LANGUAGE="$2";   shift 2 ;;
    --api-key|-k)    API_KEY="$2";    shift 2 ;;
    --json|-j)       JSON_OUT=1;      shift ;;
    --max-tokens)    MAX_TOKENS="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[ -z "$FILE" ]    && echo "Error: --file required" && usage
[ -z "$API_KEY" ] && echo "Error: MOSI_TTS_API_KEY not set" && exit 1
[ ! -f "$FILE" ]  && echo "Error: file not found: $FILE" && exit 1

# Build multipart form args
CURL_ARGS=(
  -sf
  -X POST
  "https://studio.mosi.cn/api/v1/audio/transcriptions"
  -H "Authorization: Bearer $API_KEY"
  -F "model=moss-transcribe-diarize"
  -F "file=@${FILE}"
  -F "sampling_params={\"max_new_tokens\":${MAX_TOKENS},\"temperature\":0}"
)
[ -n "$LANGUAGE" ] && CURL_ARGS+=(-F "language=${LANGUAGE}")

RESPONSE=$(curl "${CURL_ARGS[@]}")

if [ "$JSON_OUT" = "1" ]; then
  echo "$RESPONSE"
  exit 0
fi

# Extract full_text, print segments to stderr if multiple speakers
echo "$RESPONSE" | node -e "
  let d = '';
  process.stdin.on('data', c => d += c);
  process.stdin.on('end', () => {
    let r;
    try { r = JSON.parse(d); } catch(e) {
      process.stderr.write('Parse error: ' + d.slice(0,300) + '\n');
      process.exit(1);
    }
    if (r.code && r.error) {
      process.stderr.write('API error: ' + JSON.stringify(r) + '\n');
      process.exit(1);
    }
    const result = r.asr_transcription_result;
    if (!result) {
      process.stderr.write('Unexpected response: ' + JSON.stringify(r) + '\n');
      process.exit(1);
    }
    // Print full text to stdout
    console.log(result.full_text || '');
    // Print per-speaker segments to stderr for context
    const segs = result.segments || [];
    if (segs.length > 1) {
      const speakers = new Set(segs.map(s => s.speaker));
      if (speakers.size > 1) {
        process.stderr.write('Speakers detected:\n');
        segs.forEach(s =>
          process.stderr.write(
            '  [' + s.start_s + 's-' + s.end_s + 's] ' +
            (s.speaker || '') + ': ' + s.text + '\n'
          )
        );
      }
    }
  });
"
