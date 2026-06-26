#!/usr/bin/env bash
set -euo pipefail

# Kling Omni-Video: submit → poll → download
# Requires: HSAI_API_KEY env var, curl, python3

BASE_URL="${HSAI_BASE_URL:-https://api-aigw.corp.hongsong.club}"
KLING_API_PATH="/kling-video/v1/videos/omni-video"
MODEL="kling-v3-omni"
PROMPT=""
OUTPUT=""
ASPECT_RATIO=""
DURATION="5"
MODE="pro"
SOUND="off"
IMAGE=""
IMAGE_TYPE=""
IMAGE2=""
IMAGE2_TYPE=""
VIDEO=""
VIDEO_REFER_TYPE="base"
VIDEO_KEEP_SOUND="no"
POLL_INTERVAL=10
TIMEOUT=900

usage() {
  cat <<EOF
Usage: $0 --prompt <text> [options]

Options:
  --prompt <text>              Video description (required)
  --model <name>               Model: kling-video-o1 (default), kling-v3-omni
  --output <path>              Output file path
  --aspect-ratio <ratio>       16:9, 9:16, 1:1 (required for text-to-video)
  --duration <sec>             3-15 seconds (default: 5)
  --mode <mode>                pro (default) or std
  --sound <on|off>             Generate sound (default: off)
  --image <url>                Reference image URL or Base64
  --image-type <type>          first_frame or end_frame
  --image2 <url>               Second reference image URL
  --image2-type <type>         first_frame or end_frame
  --video <url>                Reference video URL (MP4/MOV)
  --video-refer-type <type>    base (edit) or feature (reference)
  --video-keep-sound <yes|no>  Keep original video sound
  --poll-interval <sec>        Poll interval (default: 10)
  --timeout <sec>              Max wait time (default: 900)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)            PROMPT="$2"; shift 2 ;;
    --model)             MODEL="$2"; shift 2 ;;
    --output)            OUTPUT="$2"; shift 2 ;;
    --aspect-ratio)      ASPECT_RATIO="$2"; shift 2 ;;
    --duration)          DURATION="$2"; shift 2 ;;
    --mode)              MODE="$2"; shift 2 ;;
    --sound)             SOUND="$2"; shift 2 ;;
    --image)             IMAGE="$2"; shift 2 ;;
    --image-type)        IMAGE_TYPE="$2"; shift 2 ;;
    --image2)            IMAGE2="$2"; shift 2 ;;
    --image2-type)       IMAGE2_TYPE="$2"; shift 2 ;;
    --video)             VIDEO="$2"; shift 2 ;;
    --video-refer-type)  VIDEO_REFER_TYPE="$2"; shift 2 ;;
    --video-keep-sound)  VIDEO_KEEP_SOUND="$2"; shift 2 ;;
    --poll-interval)     POLL_INTERVAL="$2"; shift 2 ;;
    --timeout)           TIMEOUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$PROMPT" ]]; then
  echo "Error: --prompt is required"
  usage
fi

if [[ -z "${HSAI_API_KEY:-}" ]]; then
  echo "Error: HSAI_API_KEY environment variable is not set"
  exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "Error: python3 is required but not installed"
  exit 1
fi

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="./kling_video_$(date +%Y%m%d_%H%M%S).mp4"
fi

API_KEY=$(printf '%s' "$HSAI_API_KEY")
AUTH="Authorization: Bearer $API_KEY"

# --- Build JSON body ---
build_json() {
  python3 - "$MODEL" "$PROMPT" "$ASPECT_RATIO" "$DURATION" "$MODE" "$SOUND" \
    "$IMAGE" "$IMAGE_TYPE" "$IMAGE2" "$IMAGE2_TYPE" \
    "$VIDEO" "$VIDEO_REFER_TYPE" "$VIDEO_KEEP_SOUND" <<'PYEOF'
import json, sys

args = sys.argv[1:]
model, prompt, aspect_ratio, duration, mode, sound = args[0:6]
image, image_type, image2, image2_type = args[6:10]
video, video_refer_type, video_keep_sound = args[10:13]

body = {
    "model_name": model,
    "prompt": prompt,
    "mode": mode,
    "duration": duration,
}

if sound:
    body["sound"] = sound

if aspect_ratio:
    body["aspect_ratio"] = aspect_ratio

# Image list
image_list = []
if image:
    img = {"image_url": image}
    if image_type:
        img["type"] = image_type
    image_list.append(img)
if image2:
    img2 = {"image_url": image2}
    if image2_type:
        img2["type"] = image2_type
    image_list.append(img2)
if image_list:
    body["image_list"] = image_list

# Video list
if video:
    vid = {"video_url": video, "refer_type": video_refer_type}
    if video_keep_sound:
        vid["keep_original_sound"] = video_keep_sound
    body["video_list"] = [vid]

print(json.dumps(body, ensure_ascii=False))
PYEOF
}

JSON_BODY=$(build_json)

# --- Step 1: Submit generation task ---
echo "Submitting Kling Omni-Video task..."
echo "  Model:   $MODEL"
echo "  Mode:    $MODE"
echo "  Prompt:  $PROMPT"
[[ -n "$ASPECT_RATIO" ]] && echo "  Ratio:   $ASPECT_RATIO"
echo "  Duration: ${DURATION}s"
[[ -n "$IMAGE" ]] && echo "  Image:   $IMAGE"
[[ -n "$VIDEO" ]] && echo "  Video:   $VIDEO ($VIDEO_REFER_TYPE)"

CREATE_RESP=$(curl -s -w "\n%{http_code}" \
  -X POST "${BASE_URL}${KLING_API_PATH}" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "$JSON_BODY")

HTTP_CODE=$(echo "$CREATE_RESP" | tail -1)
RESP_BODY=$(echo "$CREATE_RESP" | sed '$d')

# json_get <json> <dotpath> — extract value via python
json_get() {
  local json="$1" keys="$2"
  python3 -c "
import json, sys
data = json.loads(sys.argv[1])
for k in sys.argv[2].split('.'):
    if isinstance(data, dict):
        data = data.get(k)
    else:
        data = None
    if data is None:
        break
if data is not None:
    print(data)
" "$json" "$keys" 2>/dev/null || true
}

CODE=$(json_get "$RESP_BODY" "code")
if [[ "$CODE" != "0" ]]; then
  MSG=$(json_get "$RESP_BODY" "message")
  echo "Error: Task submission failed (HTTP $HTTP_CODE, code=$CODE)"
  echo "  Message: $MSG"
  echo "  Response: $RESP_BODY"
  exit 1
fi

TASK_ID=$(json_get "$RESP_BODY" "data.task_id")
if [[ -z "$TASK_ID" ]]; then
  echo "Error: No task_id in response"
  echo "$RESP_BODY"
  exit 1
fi

echo "Task submitted. Task ID: $TASK_ID"

# --- Step 2: Poll for completion ---
echo "Polling task status (interval: ${POLL_INTERVAL}s, timeout: ${TIMEOUT}s)..."

ELAPSED=0
while true; do
  POLL_RESP=$(curl -s -w "\n%{http_code}" \
    -X GET "${BASE_URL}${KLING_API_PATH}/${TASK_ID}?model_name=${MODEL}" \
    -H "$AUTH" \
    -H "Content-Type: application/json")

  P_CODE=$(echo "$POLL_RESP" | tail -1)
  P_BODY=$(echo "$POLL_RESP" | sed '$d')

  if [[ "$P_CODE" -lt 200 || "$P_CODE" -ge 300 ]]; then
    echo "Warning: Poll returned HTTP $P_CODE, retrying..."
    sleep "$POLL_INTERVAL"
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
    if [[ "$ELAPSED" -ge "$TIMEOUT" ]]; then
      echo "Error: Timeout after ${TIMEOUT}s"
      exit 1
    fi
    continue
  fi

  API_CODE=$(json_get "$P_BODY" "code")
  if [[ "$API_CODE" != "0" ]]; then
    echo "Warning: API returned code=$API_CODE, retrying..."
    sleep "$POLL_INTERVAL"
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
    if [[ "$ELAPSED" -ge "$TIMEOUT" ]]; then
      echo "Error: Timeout after ${TIMEOUT}s"
      exit 1
    fi
    continue
  fi

  STATUS=$(json_get "$P_BODY" "data.task_status")

  case "$STATUS" in
    succeed)
      echo "Video generation completed!"
      # Extract video URL from task_result.videos[0].url
      VIDEO_URL=$(python3 -c "
import json, sys
data = json.loads(sys.argv[1])
videos = data.get('data', {}).get('task_result', {}).get('videos', [])
if videos:
    print(videos[0].get('url', ''))
" "$P_BODY" 2>/dev/null || true)
      VIDEO_DURATION=$(python3 -c "
import json, sys
data = json.loads(sys.argv[1])
videos = data.get('data', {}).get('task_result', {}).get('videos', [])
if videos:
    print(videos[0].get('duration', ''))
" "$P_BODY" 2>/dev/null || true)
      echo "  Video duration: ${VIDEO_DURATION}s"
      break
      ;;
    failed)
      FAIL_MSG=$(json_get "$P_BODY" "data.task_status_msg")
      echo "Error: Video generation failed"
      echo "  Reason: $FAIL_MSG"
      exit 1
      ;;
    submitted|processing)
      echo "  Status: $STATUS (elapsed: ${ELAPSED}s)"
      ;;
    *)
      echo "  Status: $STATUS (elapsed: ${ELAPSED}s)"
      ;;
  esac

  sleep "$POLL_INTERVAL"
  ELAPSED=$((ELAPSED + POLL_INTERVAL))

  if [[ "$ELAPSED" -ge "$TIMEOUT" ]]; then
    echo "Error: Timeout after ${TIMEOUT}s (last status: $STATUS)"
    exit 1
  fi
done

# --- Step 3: Download video ---
if [[ -z "${VIDEO_URL:-}" ]]; then
  echo "Error: No video URL in response"
  echo "$P_BODY"
  exit 1
fi

echo "Video URL: $VIDEO_URL"
echo "Downloading video to $OUTPUT ..."

DL_CODE=$(curl -s -o "$OUTPUT" -w "%{http_code}" -L "$VIDEO_URL")

if [[ "$DL_CODE" -lt 200 || "$DL_CODE" -ge 300 ]]; then
  echo "Error: Download failed (HTTP $DL_CODE)"
  rm -f "$OUTPUT"
  exit 1
fi

ABS_PATH=$(cd "$(dirname "$OUTPUT")" && echo "$(pwd)/$(basename "$OUTPUT")")
FILE_SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')
echo "Done! Video saved to: $ABS_PATH (${FILE_SIZE} bytes)"
