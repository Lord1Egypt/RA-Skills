#!/usr/bin/env bash
set -euo pipefail
MODEL="" RATIO="" SIZE="" LENGTH="" PROMPT="."
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="${2:-}"; shift 2 ;;
    --ratio) RATIO="${2:-}"; shift 2 ;;
    --size) SIZE="${2:-}"; shift 2 ;;
    --length) LENGTH="${2:-}"; shift 2 ;;
    --prompt) PROMPT="${2:-.}"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done
[[ -n "$MODEL" && -n "$RATIO" && -n "$SIZE" ]] || {
  echo "Usage: point_calculate.sh --model ID --ratio ID --size ID [--length N]" >&2; exit 1; }
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"
PAYLOAD=$(python3 -c 'import json,sys; md,r,s,l,p=sys.argv[1:6]; b={"create_mode":1,"model":md,"ratio":r,"size":s,"prompt":p,"platform":1,"terminal":4,"language":"en"};
ln=l.strip();
if ln: b["length"]=int(ln); print(json.dumps(b))' "$MODEL" "$RATIO" "$SIZE" "$LENGTH" "$PROMPT")
curl -s -X POST "https://www.clawec.com/api/aigc/ec_media/video/point_calculate" \
  -H "Token: $TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD"
