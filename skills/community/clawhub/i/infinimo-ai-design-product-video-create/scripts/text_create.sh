#!/usr/bin/env bash
set -euo pipefail
PROMPT="" MODEL="" LANG="English" LENGTH="10"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt) PROMPT="${2:-}"; shift 2 ;;
    --model) MODEL="${2:-}"; shift 2 ;;
    --lang) LANG="${2:-}"; shift 2 ;;
    --length) LENGTH="${2:-10}"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done
[[ -n "$PROMPT" && -n "$MODEL" ]] || {
  echo "Usage: text_create.sh --prompt TEXT --model ID [--lang English] [--length 10]" >&2; exit 1; }
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"
PAYLOAD=$(python3 -c 'import json,sys; print(json.dumps({"prompt":sys.argv[1],"model":sys.argv[2],"target_language":sys.argv[3],"video_length":int(sys.argv[4]),"platform":1,"terminal":4,"language":"en"},ensure_ascii=False))' "$PROMPT" "$MODEL" "$LANG" "$LENGTH")
curl -s -X POST "https://www.clawec.com/api/aigc/ec_product_video/text_create" \
  -H "Token: $TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD"
