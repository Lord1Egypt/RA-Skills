#!/usr/bin/env bash
set -euo pipefail

PROMPT=""
MODEL=""
RATIO=""
SIZE=""
IMAGES="[]"

usage() {
  cat <<'EOF'
Usage: create.sh --prompt <text> [--model ID] [--ratio ID] [--size ID] [--images JSON array]

Examples:
  create.sh --prompt "White background product shot" --model abc --ratio def --size ghi
  create.sh --prompt "Match the style of [Image 1]" --images '["https://cdn.example.com/a.jpg"]'
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt) PROMPT="${2:-}"; shift 2 ;;
    --model) MODEL="${2:-}"; shift 2 ;;
    --ratio) RATIO="${2:-}"; shift 2 ;;
    --size) SIZE="${2:-}"; shift 2 ;;
    --images) IMAGES="${2:-[]}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

[[ -n "$PROMPT" ]] || usage

TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"

PAYLOAD=$(python3 -c '
import json, sys
prompt, model, ratio, size, images_raw = sys.argv[1:6]
body = {
    "prompt": prompt,
    "platform": 1,
    "terminal": 4,
    "language": "en",
}
if model:
    body["model"] = model
if ratio:
    body["ratio"] = ratio
if size:
    body["size"] = size
images = json.loads(images_raw)
if images:
    body["images"] = images
print(json.dumps(body, ensure_ascii=False))
' "$PROMPT" "$MODEL" "$RATIO" "$SIZE" "$IMAGES")

curl -s -X POST "https://www.clawec.com/api/aigc/ec_media/image/create" \
  -H "Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
