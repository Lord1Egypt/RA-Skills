#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
. "${SCRIPT_DIR}/common.sh"

IDEA=""
LANGUAGE=""
NUM_PAGES=""
REFERENCES=()
REFERENCE_CONTENT=""
ASPECT_RATIO=""
RESOLUTION=""
GENERATION_POLL_MAX_ATTEMPTS="${GOAI_PPT_GENERATE_POLL_MAX_ATTEMPTS:-60}"
EXPORT_POLL_MAX_ATTEMPTS="${GOAI_PPT_EXPORT_POLL_MAX_ATTEMPTS:-120}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/generate_ppt.sh --idea "..." [options]

Options:
  --idea TEXT                Required PPT idea/prompt.
  --language TEXT            Optional language (default: zh).
  --num-pages NUM            Optional number of pages.
  --reference PATH_OR_URL    Optional reference image. May be repeated.
  --reference-content TEXT  Optional reference content.
  --aspect-ratio RATIO       Optional aspect ratio (default: 16:9).
  --resolution RESOLUTION    Optional resolution (default: 2K).
  --help                    Show this message.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --idea)
      [ "$#" -ge 2 ] || die "--idea requires a value"
      IDEA="$2"
      shift 2
      ;;
    --language)
      [ "$#" -ge 2 ] || die "--language requires a value"
      LANGUAGE="$2"
      shift 2
      ;;
    --num-pages)
      [ "$#" -ge 2 ] || die "--num-pages requires a value"
      NUM_PAGES="$2"
      shift 2
      ;;
    --reference)
      [ "$#" -ge 2 ] || die "--reference requires a value"
      REFERENCES+=("$2")
      shift 2
      ;;
    --reference-content)
      [ "$#" -ge 2 ] || die "--reference-content requires a value"
      REFERENCE_CONTENT="$2"
      shift 2
      ;;
    --aspect-ratio)
      [ "$#" -ge 2 ] || die "--aspect-ratio requires a value"
      ASPECT_RATIO="$2"
      shift 2
      ;;
    --resolution)
      [ "$#" -ge 2 ] || die "--resolution requires a value"
      RESOLUTION="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

[ -n "$IDEA" ] || {
  usage >&2
  exit 1
}

require_tools
require_api_key

# Set defaults
LANGUAGE="${LANGUAGE:-zh}"
ASPECT_RATIO="${ASPECT_RATIO:-16:9}"
RESOLUTION="${RESOLUTION:-2K}"

# Sanitize idea for filename (portable: works on both macOS BSD sed and GNU sed)
IDEA_SANITIZED="$(echo "$IDEA" | LC_ALL=C tr -cs 'a-zA-Z0-9[:space:]' '_' | tr ' ' '_' | sed 's/__*/_/g' | sed 's/^_//;s/_$//' | cut -c1-30)"
if [ -z "$IDEA_SANITIZED" ]; then
  IDEA_SANITIZED="ppt"
fi
OUTPUT_BASENAME="$IDEA_SANITIZED"

# If no references provided via command line, try to get from OpenClaw attachments
if [ ${#REFERENCES[@]} -eq 0 ]; then
  echo "No --reference specified, checking for OpenClaw image attachments..." >&2
  attachment_images=$(get_openclaw_images) || true
  if [ -n "$attachment_images" ]; then
    while IFS= read -r img; do
      [ -n "$img" ] && REFERENCES+=("$img")
    done <<< "$attachment_images"
    echo "Loaded ${#REFERENCES[@]} reference image(s) from OpenClaw attachments" >&2
  fi
fi

# Check for duplicate reference images before uploading
# URLs pass through unchanged; local files are uploaded by resolve_image_inputs_json
if [ ${#REFERENCES[@]} -gt 0 ]; then
  echo "Processing ${#REFERENCES[@]} reference(s)..." >&2
fi

# If no reference content, check for PDF attachments
if [ -z "$REFERENCE_CONTENT" ]; then
  echo "Checking for OpenClaw PDF attachments as reference..." >&2
  attachment_pdfs=$(get_openclaw_pdfs) || true
  if [ -n "$attachment_pdfs" ]; then
    first_pdf=$(echo "$attachment_pdfs" | head -1)
    # Note: files from get_openclaw_pdfs() are already from media/inbound
    # No need to check for duplicates here
    echo "Found PDF reference from OpenClaw: $first_pdf" >&2
    # Upload PDF as reference content
    REFERENCE_CONTENT="$(upload_local_file "$first_pdf")"
  fi
fi

if [ "${#REFERENCES[@]}" -gt 0 ]; then
  REFERENCES_JSON="$(resolve_image_inputs_json "${REFERENCES[@]}")"
else
  REFERENCES_JSON='[]'
fi

# Build request payload
PAYLOAD="$(jq -n \
  --arg idea "$IDEA" \
  --arg language "$LANGUAGE" \
  --arg num_pages "$NUM_PAGES" \
  --arg aspect_ratio "$ASPECT_RATIO" \
  --arg resolution "$RESOLUTION" \
  --arg reference_content "$REFERENCE_CONTENT" \
  --argjson reference_images "$REFERENCES_JSON" '
  {
    idea: $idea,
    language: $language
  }
  + (if $num_pages != "" then {num_pages: (($num_pages | tonumber) // null)} else {} end)
  + (if $aspect_ratio != "" then {aspect_ratio: $aspect_ratio} else {} end)
  + (if $resolution != "" then {resolution: $resolution} else {} end)
  + (if $reference_content != "" then {reference_content: $reference_content} else {} end)
  + (if ($reference_images | length) > 0 then {reference_images: $reference_images} else {} end)
  ' | jq -c 'del(.[] | select(. == null))')"

json_request POST "${BASE_URL}/api/v2/ppt/generate" auth \
  -H "Content-Type: application/json" \
  --data "$PAYLOAD"
api_assert_ok "$GOAI_LAST_JSON"

TASK_ID="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.taskId // empty')"
PROJECT_ID="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.projectId // empty')"
[ -n "$TASK_ID" ] || die "taskId missing in generate response"
[ -n "$PROJECT_ID" ] || die "projectId missing in generate response"

attempt=1
LAST_STATUS=""
while [ "$attempt" -le "$GENERATION_POLL_MAX_ATTEMPTS" ]; do
  json_request GET "${BASE_URL}/api/v2/ppt/tasks/${TASK_ID}" auth
  api_assert_ok "$GOAI_LAST_JSON"

  STATUS="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.status // empty')"
  if [ "$STATUS" = "completed" ]; then
    PROJECT_ID="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.projectId // empty')"
    [ -n "$PROJECT_ID" ] || die "projectId missing in completed task response"
    break
  fi
  if [ "$STATUS" = "failed" ] || [ "$STATUS" = "timeout" ]; then
    ERROR_MSG="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.error // .data.message // .message // empty')"
    if [ -n "$ERROR_MSG" ]; then
      die "task ${STATUS}: ${ERROR_MSG}"
    fi
    die "task ${STATUS}"
  fi
  if [ -z "$STATUS" ]; then
    die "task status missing"
  fi

  if [ "$STATUS" != "$LAST_STATUS" ] || [ "$attempt" -eq 1 ] || [ $((attempt % GOAI_TASK_STATUS_LOG_INTERVAL)) -eq 0 ]; then
    printf 'Task status: %s (%s/%s)\n' "$STATUS" "$attempt" "$GENERATION_POLL_MAX_ATTEMPTS" >&2
    LAST_STATUS="$STATUS"
  fi

  sleep 5
  attempt=$((attempt + 1))
done

[ "$attempt" -le "$GENERATION_POLL_MAX_ATTEMPTS" ] || die "PPT generation timed out"

json_request POST "${BASE_URL}/api/v2/projects/${PROJECT_ID}/export/noteslide-pptx" auth \
  -H "Content-Type: application/json" \
  --data '{}'
api_assert_ok "$GOAI_LAST_JSON"

JOB_ID="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.jobId // empty')"
[ -n "$JOB_ID" ] || die "jobId missing in export response"

poll_task "${BASE_URL}/api/v2/projects/${PROJECT_ID}/export/noteslide-pptx/${JOB_ID}" "downloadUrl" 5 "$EXPORT_POLL_MAX_ATTEMPTS" "PPT export timed out"
DOWNLOAD_URL="$GOAI_LAST_MEDIA_URL"

OUTPUT_PATH="$(download_media "$DOWNLOAD_URL" "${OUTPUT_BASENAME}-$(date +%Y%m%d-%H%M%S).pptx")"
open_local_ppt "$OUTPUT_PATH"

printf 'MEDIA:%s\n' "$OUTPUT_PATH"
printf 'MEDIA_URL:%s\n' "$DOWNLOAD_URL"
