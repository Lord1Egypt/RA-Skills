#!/bin/bash
# MOSI Multi-Speaker Dialogue (moss-ttsd) via curl + node
# Endpoint: POST /api/v1/audio/speech (same as TTS)
# Text format: [S1] line\n[S2] line\n[S1] ...
# Supports up to 5 speakers: voice_id / voice_id2 / voice_id3 / voice_id4 / voice_id5
set -e

usage() {
  cat <<EOF
Usage: $0 --text TEXT --voice1 ID [--voice2 ID] ... [options]

Options:
  --text,    -t  TEXT   Dialogue text with [S1][S2]... tags (required)
                        e.g. "[S1] 你好！\n[S2] 你好，很高兴认识你。"
  --voice1   -1  ID     Voice ID for S1 (required)
  --voice2   -2  ID     Voice ID for S2
  --voice3   -3  ID     Voice ID for S3
  --voice4   -4  ID     Voice ID for S4
  --voice5   -5  ID     Voice ID for S5
  --output,  -o  PATH   Output WAV path
                        (default: ~/.openclaw/workspace/dialogue.wav)
  --api-key, -k  KEY    Override MOSI_TTS_API_KEY env var
  --duration -d  SECS   Expected total duration in seconds (optional)

Example (2 speakers):
  $0 \\
    --text "[S1] 你好！\n[S2] 你好，很高兴认识你。\n[S1] 今天天气真好。" \\
    --voice1 2001257729754140672 \\
    --voice2 2001931510222950400
EOF
  exit 1
}

TEXT=""
VOICE1=""
VOICE2=""
VOICE3=""
VOICE4=""
VOICE5=""
OUTPUT="${HOME}/.openclaw/workspace/dialogue.wav"
API_KEY="${MOSI_TTS_API_KEY}"
DURATION=""

while [ $# -gt 0 ]; do
  case $1 in
    --text|-t)     TEXT="$2";     shift 2 ;;
    --voice1|-1)   VOICE1="$2";   shift 2 ;;
    --voice2|-2)   VOICE2="$2";   shift 2 ;;
    --voice3|-3)   VOICE3="$2";   shift 2 ;;
    --voice4|-4)   VOICE4="$2";   shift 2 ;;
    --voice5|-5)   VOICE5="$2";   shift 2 ;;
    --output|-o)   OUTPUT="$2";   shift 2 ;;
    --api-key|-k)  API_KEY="$2";  shift 2 ;;
    --duration|-d) DURATION="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[ -z "$TEXT" ]   && echo "Error: --text required" && usage
[ -z "$VOICE1" ] && echo "Error: --voice1 required" && usage
[ -z "$API_KEY" ] && echo "Error: MOSI_TTS_API_KEY not set" && exit 1

PAYLOAD=$(printf '%s' "$TEXT" | \
  env \
    VOICE1="$VOICE1" VOICE2="$VOICE2" \
    VOICE3="$VOICE3" VOICE4="$VOICE4" \
    VOICE5="$VOICE5" DURATION="$DURATION" \
  node -e "
    let text = '';
    process.stdin.on('data', d => text += d);
    process.stdin.on('end', () => {
      const p = {
        model: 'moss-ttsd',
        text: text,
        voice_id: process.env.VOICE1
      };
      if (process.env.VOICE2) p.voice_id2 = process.env.VOICE2;
      if (process.env.VOICE3) p.voice_id3 = process.env.VOICE3;
      if (process.env.VOICE4) p.voice_id4 = process.env.VOICE4;
      if (process.env.VOICE5) p.voice_id5 = process.env.VOICE5;
      if (process.env.DURATION)
        p.expected_duration_sec = parseFloat(process.env.DURATION);
      process.stdout.write(JSON.stringify(p));
    });
  "
)

echo "Generating dialogue..."

curl -sf -X POST \
  "https://studio.mosi.cn/api/v1/audio/speech" \
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
    console.log('Dialogue saved to: ' + outPath);
    if (r.duration_s) console.log('Duration: ' + r.duration_s + 's');
  });
"
