#!/usr/bin/env bash
set -euo pipefail

BASE_URL="" BASE_TYPE="1" BG_URL="" PROMPT="" FACE_PROMPT="" NUM="1" ASPECT="1:1"

usage() {
  cat <<'EOF'
Usage: create.sh --base-url URL [options]

Required:
  --base-url URL           Source image URL

Optional:
  --base-type N            1 = real person (default), 2 = mannequin
  --bg-url URL             Background reference URL
  --prompt TEXT            Model look prompt
  --face-prompt TEXT       Face prompt
  --num N                  Output count (default 1)
  --aspect RATIO           e.g. 1:1, 9:16, or 比例不变
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url) BASE_URL="${2:-}"; shift 2 ;;
    --base-type) BASE_TYPE="${2:-1}"; shift 2 ;;
    --bg-url) BG_URL="${2:-}"; shift 2 ;;
    --prompt) PROMPT="${2:-}"; shift 2 ;;
    --face-prompt) FACE_PROMPT="${2:-}"; shift 2 ;;
    --num) NUM="${2:-1}"; shift 2 ;;
    --aspect) ASPECT="${2:-1:1}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

[[ -n "$BASE_URL" ]] || usage

TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"

ARGS=(
  --data-urlencode "base_image_url=${BASE_URL}"
  --data-urlencode "base_image_type=${BASE_TYPE}"
  --data-urlencode "num=${NUM}"
  --data-urlencode "aspect_radio=${ASPECT}"
  --data-urlencode "platform=1"
  --data-urlencode "terminal=4"
  --data-urlencode "language=en"
)
[[ -n "$BG_URL" ]] && ARGS+=(--data-urlencode "bg_image_url=${BG_URL}")
[[ -n "$PROMPT" ]] && ARGS+=(--data-urlencode "prompt=${PROMPT}")
[[ -n "$FACE_PROMPT" ]] && ARGS+=(--data-urlencode "face_prompt=${FACE_PROMPT}")

curl -s -G "https://www.clawec.com/api/aigc/image/virtual_model_create" \
  -H "Token: $TOKEN" \
  "${ARGS[@]}"
