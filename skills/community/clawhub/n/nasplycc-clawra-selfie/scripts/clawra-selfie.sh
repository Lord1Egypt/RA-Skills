#!/bin/bash
# clawra-selfie.sh
# Generate a Clawra selfie with Qwen-first routing and send it via OpenClaw.
#
# Usage:
#   ./clawra-selfie.sh "<user_context>" "<channel>" [mode] [caption]
#
# Environment variables required:
#   QWEN_API_KEY - DashScope API key (preferred) OR HF_TOKEN for fallback
#
# Optional env:
#   QWEN_API_KEY    - Alibaba DashScope API key for qwen-image-plus (preferred when set)
#   QWEN_IMAGE_MODEL - default: qwen-image-plus
#   ENABLE_GEMINI - set to 1 to enable Gemini image probe (default disabled)
#   GEMINI_API_KEY - Google Gemini API key for image generation probe/fallback
#   GEMINI_IMAGE_MODEL - default: gemini-2.5-flash-image
#   HF_IMAGE_MODEL  - default model id
#   HF_API_BASE     - default: https://api-inference.huggingface.co/models
#
# Note:
# - This script supports two request modes:
#   1) text-to-image fallback via standard HF model API
#   2) image-edit style via custom endpoint if the selected model supports binary image input + prompt
# - Because HF model compatibility varies, this script surfaces raw API errors clearly.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [ -z "${HF_TOKEN:-}" ] && [ -z "${QWEN_API_KEY:-}" ] && ! { [ "${ENABLE_GEMINI:-0}" = "1" ] && [ -n "${GEMINI_API_KEY:-}" ]; }; then
  log_error "Either QWEN_API_KEY or HF_TOKEN is required unless Gemini probe is explicitly enabled with GEMINI_API_KEY"
  echo "Set QWEN_API_KEY for DashScope qwen-image-plus, or HF_TOKEN for Hugging Face, or set ENABLE_GEMINI=1 with GEMINI_API_KEY"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  log_error "jq is required but not installed"
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  log_error "curl is required but not installed"
  exit 1
fi

PROMPT_CONTEXT="${1:-}"
CHANNEL="${2:-}"
MODE="${3:-auto}"
CAPTION="${4:-Raya 的自拍 ✨}"
MODEL="${HF_IMAGE_MODEL:-black-forest-labs/FLUX.1-schnell}"
QWEN_IMAGE_MODEL="${QWEN_IMAGE_MODEL:-qwen-image-plus}"
GEMINI_IMAGE_MODEL="${GEMINI_IMAGE_MODEL:-gemini-2.5-flash-image}"
HF_API_BASE="${HF_API_BASE:-https://router.huggingface.co/hf-inference/models}"
WORKDIR="$(mktemp -d)"
OUTPUT_DIR="${OUTPUT_DIR:-/home/Jaben/.openclaw/workspace-clawra-bot/generated}"

FACE_ANCHOR="18-year-old Chinese young woman, small oval face, soft facial lines, smooth midface, naturally defined but gentle jawline, small delicate chin, almond-shaped eyes, natural double eyelids, balanced eye distance, soft bright eyes, straight natural nose bridge, small refined nose tip, narrow to medium nose width, natural softly shaped lips, defined but not overly full lips, gentle flat eyebrows, black or dark brown medium-length hair, light natural makeup, clean bare-skin look, natural realistic facial proportions, delicate and understated East Asian features, height around 170cm, weight around 50kg, slim and well-proportioned figure, head-to-body ratio close to golden proportion in common beauty standards, relaxed and natural shoulder and neck lines, naturally visible but not overly bony collarbone, smooth waistline, long limbs, straight and natural leg lines, slender arms but not overly thin, coordinated overall body proportions, slight sporty and healthy feeling, not exaggerated athletic build and not excessively skinny, natural bust-waist-hip balance, natural transitions between body parts, overall light, slim, harmonious, and broadly attractive appearance"
NEGATIVE_ANCHOR="avoid heavy glam makeup, avoid overly mature celebrity face, avoid aggressive sexy expression, avoid exaggerated body proportions, avoid overly childish sweet look, avoid strong Western facial features, avoid influencer-style overediting, avoid heavy filters, avoid anime or illustration style, avoid overly sharp jawline, avoid overly pointed chin, avoid exaggerated lips, avoid dramatic nose shape, avoid thick heavy eyebrows, avoid exaggerated bust or hips, avoid extreme paper-thin body type, avoid obviously unrealistic head-to-body ratio, avoid overly muscular physique, avoid imbalanced body proportions"

mkdir -p "$OUTPUT_DIR"
trap 'rm -rf "$WORKDIR"' EXIT

if [ -z "$PROMPT_CONTEXT" ] || [ -z "$CHANNEL" ]; then
  echo "Usage: $0 <user_context> <channel> [mode] [caption]"
  echo "Modes: mirror, direct, auto (default)"
  exit 1
fi

OFFICIAL_FACE=""
for candidate in \
  "/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-current.png" \
  "/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-current.jpg" \
  "/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-current.jpeg" \
  "/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-v1.png" \
  "/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-v1.jpg" \
  "/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-v1.jpeg"; do
  if [ -f "$candidate" ]; then
    OFFICIAL_FACE="$candidate"
    break
  fi
done

if [ "$MODE" = "auto" ]; then
  if echo "$PROMPT_CONTEXT" | grep -qiE "outfit|wearing|clothes|dress|suit|fashion|full-body|mirror|穿|衣服|穿搭|全身|镜子"; then
    MODE="mirror"
  elif echo "$PROMPT_CONTEXT" | grep -qiE "cafe|restaurant|beach|park|city|close-up|portrait|face|eyes|smile|咖啡|海边|公园|城市|特写|脸|表情|状态"; then
    MODE="direct"
  else
    MODE="direct"
  fi
fi

# Prompt-first route reality: even with Qwen-first routing, soft identity anchoring is more reliable than pretending this is true image-editing on shared public backends.
# So default to a strong persona prompt that preserves the current Raya persona.
if [ "$MODE" = "direct" ]; then
  FINAL_PROMPT="realistic close-up phone selfie of Raya, ${FACE_ANCHOR}, soft real-life lighting, direct eye contact, calm authentic expression, in ${PROMPT_CONTEXT}, candid smartphone photo, detailed skin, photorealistic, ${NEGATIVE_ANCHOR}"
else
  FINAL_PROMPT="realistic full-body or mirror-area photo of Raya, ${FACE_ANCHOR}, wearing simple tasteful outfits with light commuter style, urban and elegant but natural, half or full body framing, natural relaxed pose, in ${PROMPT_CONTEXT}, candid real-life photo, photorealistic, ${NEGATIVE_ANCHOR}"
fi

if [ -n "$OFFICIAL_FACE" ]; then
  FINAL_PROMPT="${FINAL_PROMPT}, matching Raya's established official face reference as closely as possible, preserving her stable identity: natural clean beauty, soft bright eyes, gentle facial lines, consistent hairstyle and hair color, stable youthful Chinese features, consistent visual identity"
  log_info "Official face reference found: $OFFICIAL_FACE"
else
  log_warn "No official face reference file found; using prompt-only identity fallback."
fi

log_info "Mode: $MODE"
log_info "Preferred backend: ${QWEN_IMAGE_MODEL} (Qwen), fallback HF model: $MODEL"
log_warn "Hugging Face free mode may not preserve identity as well as reference-image editing backends."

QWEN_OK=0
if [ -n "${QWEN_API_KEY:-}" ]; then
  QWEN_REQ_JSON="$WORKDIR/qwen-request.json"
  QWEN_RESP_JSON="$WORKDIR/qwen-response.json"
  QWEN_RESULT_JSON="$WORKDIR/qwen-result.json"
  jq -n --arg model "$QWEN_IMAGE_MODEL" --arg prompt "$FINAL_PROMPT" '{model:$model,input:{prompt:$prompt},parameters:{size:"1024*1024"}}' > "$QWEN_REQ_JSON"
  log_info "Trying Qwen image model: $QWEN_IMAGE_MODEL"
  QWEN_HTTP_CODE=$(curl -sS \
    -o "$QWEN_RESP_JSON" \
    -w '%{http_code}' \
    -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis" \
    -H "Authorization: Bearer $QWEN_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-Async: enable" \
    --data-binary "@$QWEN_REQ_JSON" || true)

  if [ "${QWEN_HTTP_CODE:-0}" -lt 400 ]; then
    QWEN_TASK_ID=$(jq -r '.output.task_id // empty' "$QWEN_RESP_JSON" 2>/dev/null || true)
    if [ -n "$QWEN_TASK_ID" ]; then
      for _ in $(seq 1 20); do
        sleep 3
        QWEN_RESULT_HTTP_CODE=$(curl -sS \
          -o "$QWEN_RESULT_JSON" \
          -w '%{http_code}' \
          -X GET "https://dashscope.aliyuncs.com/api/v1/tasks/${QWEN_TASK_ID}" \
          -H "Authorization: Bearer $QWEN_API_KEY" || true)
        [ "${QWEN_RESULT_HTTP_CODE:-0}" -ge 400 ] && continue
        QWEN_TASK_STATUS=$(jq -r '.output.task_status // empty' "$QWEN_RESULT_JSON" 2>/dev/null || true)
        if [ "$QWEN_TASK_STATUS" = "SUCCEEDED" ]; then
          QWEN_IMAGE_URL=$(jq -r '.output.results[0].url // empty' "$QWEN_RESULT_JSON" 2>/dev/null || true)
          if [ -n "$QWEN_IMAGE_URL" ]; then
            FINAL_PATH="$OUTPUT_DIR/clawra-selfie.png"
            curl -sS -L "$QWEN_IMAGE_URL" -o "$FINAL_PATH"
            QWEN_OK=1
            MODEL="$QWEN_IMAGE_MODEL"
            log_info "Qwen image generation succeeded"
            break
          fi
        elif [ "$QWEN_TASK_STATUS" = "FAILED" ] || [ "$QWEN_TASK_STATUS" = "CANCELED" ]; then
          break
        fi
      done
    fi
  fi

  if [ "$QWEN_OK" -ne 1 ]; then
    log_warn "Qwen image generation unavailable or incomplete; falling back to Gemini/Hugging Face"
    if [ -s "$QWEN_RESP_JSON" ]; then
      echo "--- Qwen submit response (truncated) ---"
      head -c 1200 "$QWEN_RESP_JSON" || true
      echo ""
      echo "--- end ---"
    fi
    if [ -s "$QWEN_RESULT_JSON" ]; then
      echo "--- Qwen task response (truncated) ---"
      head -c 1200 "$QWEN_RESULT_JSON" || true
      echo ""
      echo "--- end ---"
    fi
  fi
fi

GEMINI_TRIED=0
GEMINI_OK=0
if [ "$QWEN_OK" -ne 1 ] && [ "${ENABLE_GEMINI:-0}" = "1" ] && [ -n "${GEMINI_API_KEY:-}" ]; then
  GEMINI_TRIED=1
  GEMINI_RESP_JSON="$WORKDIR/gemini-response.json"
  GEMINI_IMAGE_B64="$WORKDIR/gemini-image.b64"
  GEMINI_TEXT_ERR="$WORKDIR/gemini-text.txt"
  GEMINI_PAYLOAD="$WORKDIR/gemini-payload.json"
  jq -n --arg text "$FINAL_PROMPT" '{contents:[{parts:[{text:$text}]}], generationConfig:{responseModalities:["TEXT","IMAGE"]}}' > "$GEMINI_PAYLOAD"
  log_info "Trying Gemini image model: $GEMINI_IMAGE_MODEL"
  GEMINI_HTTP_CODE=$(curl -sS \
    -o "$GEMINI_RESP_JSON" \
    -w '%{http_code}' \
    -X POST "https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_IMAGE_MODEL}:generateContent?key=${GEMINI_API_KEY}" \
    -H "Content-Type: application/json" \
    --data-binary "@$GEMINI_PAYLOAD" || true)

  if [ "${GEMINI_HTTP_CODE:-0}" -lt 400 ] && jq -e -r '.. | .inlineData? // empty | select(.mimeType | startswith("image/")) | .data' "$GEMINI_RESP_JSON" > "$GEMINI_IMAGE_B64" 2>/dev/null; then
    GEMINI_MIME=$(jq -r '.. | .inlineData? // empty | select(.mimeType | startswith("image/")) | .mimeType' "$GEMINI_RESP_JSON" | head -n1)
    case "$GEMINI_MIME" in
      image/png) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.png" ;;
      image/jpeg|image/jpg) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.jpg" ;;
      image/webp) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.webp" ;;
      *) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.png" ;;
    esac
    base64 -d "$GEMINI_IMAGE_B64" > "$FINAL_PATH"
    GEMINI_OK=1
    MODEL="$GEMINI_IMAGE_MODEL"
    log_info "Gemini image generation succeeded"
  else
    log_warn "Gemini image generation unavailable or quota-limited; falling back to Hugging Face"
    if [ -s "$GEMINI_RESP_JSON" ]; then
      echo "--- Gemini response (truncated) ---"
      head -c 1200 "$GEMINI_RESP_JSON" || true
      echo ""
      echo "--- end ---"
    fi
  fi
fi

if [ "$QWEN_OK" -ne 1 ] && [ "$GEMINI_OK" -ne 1 ]; then
  if [ -z "${HF_TOKEN:-}" ]; then
    log_error "Qwen/Gemini failed and HF_TOKEN is not set for fallback"
    exit 1
  fi

  PAYLOAD_PATH="$WORKDIR/payload.json"
  jq -n --arg inputs "$FINAL_PROMPT" '{inputs: $inputs}' > "$PAYLOAD_PATH"

  RESP_HEADERS="$WORKDIR/headers.txt"
  IMAGE_PATH="$WORKDIR/output.bin"
  HF_HTTP_CODE=$(curl -sS \
    -D "$RESP_HEADERS" \
    -o "$IMAGE_PATH" \
    -w '%{http_code}' \
    -X POST "$HF_API_BASE/${HF_IMAGE_MODEL:-black-forest-labs/FLUX.1-schnell}" \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H "Content-Type: application/json" \
    --data-binary "@$PAYLOAD_PATH")

  CONTENT_TYPE=$(grep -i '^content-type:' "$RESP_HEADERS" | tail -n1 | sed 's/^[^:]*:[[:space:]]*//I' | tr -d '\r')

  if [ "$HF_HTTP_CODE" -ge 400 ]; then
    log_error "HF request failed (HTTP $HF_HTTP_CODE)"
    cat "$IMAGE_PATH"
    exit 1
  fi

  case "$CONTENT_TYPE" in
    image/png*) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.png" ; mv "$IMAGE_PATH" "$FINAL_PATH" ;;
    image/jpeg*|image/jpg*) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.jpg" ; mv "$IMAGE_PATH" "$FINAL_PATH" ;;
    image/webp*) FINAL_PATH="$OUTPUT_DIR/clawra-selfie.webp" ; mv "$IMAGE_PATH" "$FINAL_PATH" ;;
    application/json*|text/plain*)
      log_error "HF returned non-image response"
      cat "$IMAGE_PATH"
      exit 1
      ;;
    *)
      log_error "Unexpected content type: ${CONTENT_TYPE:-unknown}"
      cat "$IMAGE_PATH" | head -c 500 || true
      exit 1
      ;;
  esac

  MODEL="${HF_IMAGE_MODEL:-black-forest-labs/FLUX.1-schnell}"
fi

log_info "Sending image to channel: $CHANNEL"
log_info "Image saved at: $FINAL_PATH"

if [ "${NO_SEND:-0}" = "1" ]; then
  echo ""
  echo "--- Result ---"
  jq -n --arg channel "$CHANNEL" --arg mode "$MODE" --arg prompt "$FINAL_PROMPT" --arg model "$MODEL" --arg file_path "$FINAL_PATH" '{success:true, channel:$channel, mode:$mode, prompt:$prompt, model:$model, file_path:$file_path}'
  exit 0
fi

if command -v openclaw >/dev/null 2>&1; then
  openclaw message send \
    --action send \
    --channel "$CHANNEL" \
    --target "$CHANNEL" \
    --message "$CAPTION" \
    --file "$FINAL_PATH"
else
  log_error "openclaw CLI not found"
  exit 1
fi

log_info "Done!"
echo ""
echo "--- Result ---"
jq -n --arg channel "$CHANNEL" --arg mode "$MODE" --arg prompt "$FINAL_PROMPT" --arg model "$MODEL" '{success:true, channel:$channel, mode:$mode, prompt:$prompt, model:$model}'
