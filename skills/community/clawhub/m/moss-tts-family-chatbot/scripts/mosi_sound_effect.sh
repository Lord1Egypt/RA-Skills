#!/bin/bash
# MOSI Sound Effect Generation via curl + node
set -e

usage() {
  cat <<EOF
Usage: $0 --prompt TEXT [options]

Options:
  --prompt,    -p  TEXT   Sound description (required)
  --duration,  -d  SECS   Duration in seconds (default: 5)
  --output,    -o  PATH   Output WAV path
                          (default: ~/.openclaw/workspace/sound_effect.wav)
  --api-key,   -k  KEY    Override MOSI_TTS_API_KEY env var
  --variations -n  INT    Number of variations (default: 1)
EOF
  exit 1
}

PROMPT=""
DURATION=5
OUTPUT="${HOME}/.openclaw/workspace/sound_effect.wav"
API_KEY="${MOSI_TTS_API_KEY}"
VARIATIONS=1

while [[ $# -gt 0 ]]; do
  case $1 in
    --prompt|-p)     PROMPT="$2";     shift 2 ;;
    --duration|-d)   DURATION="$2";   shift 2 ;;
    --output|-o)     OUTPUT="$2";     shift 2 ;;
    --api-key|-k)    API_KEY="$2";    shift 2 ;;
    --variations|-n) VARIATIONS="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[[ -z "$PROMPT" ]]   && echo "Error: --prompt required" && usage
[[ -z "$API_KEY" ]]  && echo "Error: MOSI_TTS_API_KEY not set" && exit 1

PAYLOAD=$(printf '%s' "$PROMPT" | \
  env DURATION="$DURATION" VARIATIONS="$VARIATIONS" node -e "
    let prompt = '';
    process.stdin.on('data', d => prompt += d);
    process.stdin.on('end', () => {
      process.stdout.write(JSON.stringify({
        model: 'moss-sound-effect',
        prompt: prompt,
        duration_sec: parseFloat(process.env.DURATION),
        num_variations: parseInt(process.env.VARIATIONS)
      }));
    });
  "
)

echo "Generating sound effect: ${PROMPT:0:60}..."

curl -sf -X POST \
  "https://studio.mosi.cn/api/v1/audio/sound-effect" \
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
    const audio = r.audio_data || (r.data && r.data.audio_data);
    if (!audio) {
      console.error('API error:', JSON.stringify(r));
      process.exit(1);
    }
    fs.writeFileSync(outPath, Buffer.from(audio, 'base64'));
    console.log('Sound effect saved to: ' + outPath);
    if (r.duration_s) console.log('Duration: ' + r.duration_s + 's');
  });
"
