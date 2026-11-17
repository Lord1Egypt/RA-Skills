#!/usr/bin/env bash
set -euo pipefail

PROMPT=""
MODEL=""
RATIO=""
SIZE=""
IMAGES="[]"
TARGET_PLATFORM=""
REGION=""
SCENE="cover"

usage() {
  cat <<'EOF'
Usage: create.sh --target-platform <code> [options]

Required:
  --target-platform CODE   Platform code from platform_options

Optional:
  --prompt TEXT            Prompt (at least prompt or --images required)
  --scene SCENE            cover | cover_other | detail (default cover)
  --region CODE            Market code
  --model ID --ratio ID --size ID
  --images JSON            Reference URL array
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
    --target-platform) TARGET_PLATFORM="${2:-}"; shift 2 ;;
    --region) REGION="${2:-}"; shift 2 ;;
    --scene) SCENE="${2:-cover}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

[[ -n "$TARGET_PLATFORM" ]] || usage

TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"

PAYLOAD=$(python3 -c '
import json, sys
prompt, model, ratio, size, images_raw, target_platform, region, scene = sys.argv[1:9]
body = {
    "target_platform": target_platform,
    "image_scene": scene or "cover",
    "platform": 1,
    "terminal": 4,
    "language": "en",
}
if prompt:
    body["prompt"] = prompt
if model:
    body["model"] = model
if ratio:
    body["ratio"] = ratio
if size:
    body["size"] = size
if region:
    body["region"] = region
images = json.loads(images_raw)
if images:
    body["images"] = images
if not body.get("prompt") and not body.get("images"):
    raise SystemExit("Error: --prompt and --images cannot both be empty")
print(json.dumps(body, ensure_ascii=False))
' "$PROMPT" "$MODEL" "$RATIO" "$SIZE" "$IMAGES" "$TARGET_PLATFORM" "$REGION" "$SCENE")

curl -s -X POST "https://www.clawec.com/api/aigc/ec_media/image/create" \
  -H "Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
