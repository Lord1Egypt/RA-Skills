#!/bin/bash
# MOSI Voice Generator - Generate voice from text + natural language description
# Model: moss-voice-generator
set -e

usage() {
  cat >&2 <<'EOF'
Usage:
  mosi_voice_generator.sh --text "要生成的文字" --instruction "声音描述"
  mosi_voice_generator.sh -t "文字" -i "一个温柔的女声" -o output.wav

Options:
  --text, -t       要转换成语音的文字 (必填)
  --instruction, -i 声音风格描述，例如：一个温柔的女声 (必填)
  --output, -o     输出文件路径 (默认: ~/.openclaw/workspace/voice_gen_output.wav)
  --temperature    采样温度 (默认: 1.5)
  --top-p          核采样阈值 (默认: 0.6)
  --top-k          Top-K 采样 (默认: 50)
  --meta-info      返回性能指标 (默认: false)
  --api-key, -k    API Key (默认: 从 MOSI_TTS_API_KEY 环境变量读取)

Examples:
  # 播音腔女声
  mosi_voice_generator.sh -t "各位观众朋友们大家好" -i "播音腔女声，专业、清晰、有亲和力"

  # 温柔男声
  mosi_voice_generator.sh -t "晚安，好梦" -i "一个温柔的男声，轻柔舒缓"

  # 有活力的年轻女声
  mosi_voice_generator.sh -t "欢迎来到我们的节目" -i "年轻有活力的女声，热情开朗"
EOF
  exit 2
}

TEXT=""
INSTRUCTION=""
OUTPUT="${HOME}/.openclaw/workspace/voice_gen_output.wav"
TEMPERATURE="1.5"
TOP_P="0.6"
TOP_K="50"
META_INFO="false"
API_KEY="${MOSI_TTS_API_KEY}"

while [[ $# -gt 0 ]]; do
  case $1 in
    --text|-t)        TEXT="$2";        shift 2 ;;
    --instruction|-i) INSTRUCTION="$2"; shift 2 ;;
    --output|-o)      OUTPUT="$2";      shift 2 ;;
    --temperature)    TEMPERATURE="$2"; shift 2 ;;
    --top-p)          TOP_P="$2";       shift 2 ;;
    --top-k)          TOP_K="$2";       shift 2 ;;
    --meta-info)      META_INFO="true"; shift ;;
    --api-key|-k)     API_KEY="$2";     shift 2 ;;
    -h|--help)        usage ;;
    *) echo "Unknown: $1" >&2; usage ;;
  esac
done

[[ -z "$TEXT" ]]        && echo "Error: --text required" >&2 && usage
[[ -z "$INSTRUCTION" ]] && echo "Error: --instruction required" >&2 && usage
[[ -z "$API_KEY" ]]     && echo "Error: MOSI_TTS_API_KEY not set" >&2 && exit 1

# Build JSON payload via node (handles escaping)
PAYLOAD=$(printf '%s\n%s' "$TEXT" "$INSTRUCTION" | \
  env TEMP="$TEMPERATURE" TOP_P="$TOP_P" TOP_K="$TOP_K" META="$META_INFO" node -e "
    let input = '';
    process.stdin.on('data', d => input += d);
    process.stdin.on('end', () => {
      const [text, instruction] = input.split('\n');
      process.stdout.write(JSON.stringify({
        model: 'moss-voice-generator',
        text: text,
        instruction: instruction,
        sampling_params: {
          temperature: parseFloat(process.env.TEMP),
          top_p: parseFloat(process.env.TOP_P),
          top_k: parseInt(process.env.TOP_K, 10)
        },
        meta_info: process.env.META === 'true'
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
    if (r.meta_info) {
      if (r.meta_info.e2e_latency_sec) console.log('Latency: ' + r.meta_info.e2e_latency_sec + 's');
    }
    if (r.usage && r.usage.credit_cost) console.log('Cost: ' + r.usage.credit_cost + ' credits');
  });
"
