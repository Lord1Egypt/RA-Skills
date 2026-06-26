#!/bin/bash
set -euo pipefail

# PixelDojo live model catalog helper

API_BASE="${PIXELDOJO_API_BASE:-https://pixeldojo.ai/api/v1}"
API_KEY="${PIXELDOJO_API_KEY:-}"

CURL_ARGS=(-sS "${API_BASE}/models")
if [[ -n "$API_KEY" ]]; then
  CURL_ARGS+=( -H "Authorization: Bearer ${API_KEY}" )
fi

RESPONSE=$(curl "${CURL_ARGS[@]}")

if ! echo "$RESPONSE" | jq -e '.models and (.models | type == "array")' >/dev/null 2>&1; then
  echo "Error: Unexpected response from PixelDojo model catalog" >&2
  echo "$RESPONSE" >&2
  exit 1
fi

echo "PixelDojo available models"
echo "========================="
echo ""
echo "Live catalog from ${API_BASE}/models"
echo ""

echo "Image models:"
echo "$RESPONSE" | jq -r '
  .models
  | map(select(.modality == "image"))
  | sort_by(.apiId)
  | .[]
  | "  " + (.apiId + "                              ")[0:30]
    + " - " + .name
    + (if (.capabilities | length) > 0 then " [" + (.capabilities | join(", ")) + "]" else "" end)
    + (if .creditCost.amount then " (" + (.creditCost.amount | tostring) + " credits)" else if .creditCost.default then " (" + (.creditCost.default | tostring) + " credits)" else "" end end)
'

echo ""
echo "Video models:"
echo "$RESPONSE" | jq -r '
  .models
  | map(select(.modality == "video"))
  | sort_by(.apiId)
  | .[]
  | "  " + (.apiId + "                              ")[0:30]
    + " - " + .name
    + (if (.capabilities | length) > 0 then " [" + (.capabilities | join(", ")) + "]" else "" end)
    + (if .creditCost.amount then " (" + (.creditCost.amount | tostring) + " credits)" else if .creditCost.default then " (" + (.creditCost.default | tostring) + " credits)" else "" end end)
'

echo ""
echo "Usage:"
echo "  bash ~/.openclaw/skills/pixeldojo/generate.sh image <prompt> <model> [options]"
echo "  bash ~/.openclaw/skills/pixeldojo/generate.sh video <prompt> <model> [options]"
echo ""
echo "Examples:"
echo "  bash ~/.openclaw/skills/pixeldojo/generate.sh image \"cyberpunk city\" flux-2-pro"
echo "  bash ~/.openclaw/skills/pixeldojo/generate.sh image \"product photo\" nano-banana-2 --aspect-ratio 16:9"
echo "  bash ~/.openclaw/skills/pixeldojo/generate.sh video \"ocean waves\" seedance-1.5 --duration 5"
