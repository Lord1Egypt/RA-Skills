#!/bin/bash
# MOSI TTS - Text to Speech via curl + node (no Python needed)
set -e

usage() {
  echo "Usage: $0 --text TEXT [--voice-id ID] [--output PATH] [--api-key KEY]"
  exit 1
}

TEXT=""
VOICE_ID="2001257729754140672"
OUTPUT="${HOME}/.openclaw/workspace/tts_output.wav"
API_KEY="${MOSI_TTS_API_KEY}"

while [[ $# -gt 0 ]]; do
  case $1 in
    --text|-t)     TEXT="$2";     shift 2 ;;
    --voice-id|-v) VOICE_ID="$2"; shift 2 ;;
    --output|-o)   OUTPUT="$2";   shift 2 ;;
    --api-key|-k)  API_KEY="$2";  shift 2 ;;
    *) echo "Unknown: $1"; usage ;;
  esac
done

[[ -z "$TEXT" ]]    && echo "Error: --text required" && usage
[[ -z "$API_KEY" ]] && echo "Error: MOSI_TTS_API_KEY not set" && exit 1

# Build JSON payload via node stdin (handles escaping)
PAYLOAD=$(printf '%s' "$TEXT" | \
  env VOICE_ID="$VOICE_ID" node -e "
    let text = '';
    process.stdin.on('data', d => text += d);
    process.stdin.on('end', () => {
      process.stdout.write(JSON.stringify({
        model: 'moss-tts',
        text: text,
        voice_id: process.env.VOICE_ID,
        sampling_params: {
          max_new_tokens: 512,
          temperature: 1.7,
          top_p: 0.8,
          top_k: 25
        },
        meta_info: true
      }));
    });
  "
)

# Call API, pipe response to node for decoding
curl -sf -X POST "https://studio.mosi.cn/api/v1/audio/speech" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
| env OUT="$OUTPUT" node -e "
  const fs = require('fs');
  const outPath = process.env.OUT;
  let raw = '';
  process.stdin.on('data', d => raw += d);
  process.stdin.on('end', () => {
    let r;
    try { r = JSON.parse(raw); } catch(e) {
      console.error('Parse error:', raw.slice(0, 300));
      process.exit(1);
    }
    if (!r.audio_data) {
      console.error('API error:', JSON.stringify(r));
      process.exit(1);
    }
    fs.writeFileSync(outPath, Buffer.from(r.audio_data, 'base64'));
    console.log('Audio saved to: ' + outPath);
    if (r.duration_s) console.log('Duration: ' + r.duration_s + 's');
  });
"
