#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${GOAI_BASE_URL:-https://ppt.mustgoai.com}"
GOAI_LAST_JSON=""
GOAI_LAST_MEDIA_URL=""
GOAI_HTTP_MAX_ATTEMPTS=3
GOAI_HTTP_RETRY_DELAY_SECONDS=2
GOAI_HTTP_CONNECT_TIMEOUT_SECONDS="${GOAI_HTTP_CONNECT_TIMEOUT_SECONDS:-10}"
GOAI_HTTP_JSON_TIMEOUT_SECONDS="${GOAI_HTTP_JSON_TIMEOUT_SECONDS:-45}"
GOAI_HTTP_TRANSFER_TIMEOUT_SECONDS="${GOAI_HTTP_TRANSFER_TIMEOUT_SECONDS:-300}"
GOAI_TASK_STATUS_LOG_INTERVAL="${GOAI_TASK_STATUS_LOG_INTERVAL:-3}"
GOAI_AUTO_OPEN_OUTPUT="${GOAI_AUTO_OPEN_OUTPUT:-1}"

# Detect the current Cursor project directory dynamically.
# Priority: OPENCLAW_PROJECT_DIR env var -> infer from script path.
detect_openclaw_project_dir() {
  # 1. Use environment variable if set
  if [ -n "${OPENCLAW_PROJECT_DIR:-}" ] && [ -d "${OPENCLAW_PROJECT_DIR}/.cursor" ]; then
    printf '%s\n' "$OPENCLAW_PROJECT_DIR"
    return 0
  fi

  # 2. Try to infer from script location (scripts are in .cursor/skills/<name>/scripts/)
  local script_path="${BASH_SOURCE[0]:-$0}"
  local skill_dir
  skill_dir="$(cd "$(dirname "$script_path")" && pwd -P)"
  local cursor_dir="$(dirname "$(dirname "$skill_dir")")"  # go up: scripts -> skill -> .cursor
  local project_dir
  project_dir="$(dirname "$cursor_dir")"  # go up: .cursor -> project root

  if [ -d "$project_dir/.cursor" ]; then
    printf '%s\n' "$project_dir"
    return 0
  fi

  return 1
}

# Get the media/inbound directory for the current project
get_openclaw_media_inbound() {
  local project_dir
  project_dir="$(detect_openclaw_project_dir)" || return 1
  printf '%s/.cursor/media/inbound\n' "$project_dir"
}

# Get the assets directory for the current project
get_openclaw_assets_dir() {
  local project_dir
  project_dir="$(detect_openclaw_project_dir)" || return 1
  printf '%s/.cursor/assets\n' "$project_dir"
}

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

require_tools() {
  command -v curl >/dev/null 2>&1 || die "curl is required. Install curl and retry."
  command -v jq >/dev/null 2>&1 || die "jq is required. Install jq and retry."
}

require_api_key() {
  if [ -n "${GOAI_API_KEY:-}" ]; then
    return 0
  fi

  cat >&2 <<'EOF'
Error: GOAI_API_KEY is required.

Get a test API key and recharge:
1. Visit http://mustgoai.com
2. Register or log in
3. Open Settings -> API Key to create a key
4. Configure GOAI_API_KEY as an environment variable or in ~/.openclaw/openclaw.json:

   "skills": {
     "entries": {
       "goai-ppt-gen": {
         "enabled": true,
         "env": {
           "GOAI_API_KEY": "your-api-key"
         }
       }
     }
   }

Optional:
- Set GOAI_BASE_URL to override the default PPT service endpoint

Demo PPT: https://ai-neuralforge.oss-cn-hangzhou.aliyuncs.com/aippt/ppt/example_ppt/%E7%94%9F%E6%88%90%E4%B8%80%E4%BB%A5%E4%B8%AD%E5%9B%BD%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E4%B8%BA%E4%B8%BB%E9%A2%98%E7%9A%84%E7%A7%91%E6%99%AE%E6%BC%94%E7%A4%BA%E6%96%87%E7%A8%BF%E5%86%85%E5%AE%B9%E9%9C%80%E6%B6%B5%E7%9B%96%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E7%9A%84%E5%8E%86%E5%8F%B2%E6%B8%8A%E6%BA%90%E5%A4%A9%E6%96%87%E5%88%92%E5%88%86%E6%A0%87%E5%87%86%E4%BB%A5%E5%8F%8A%E5%9B%BD%E5%9B%BE.pptx
  Click the link above to preview the PPT generation effect.
EOF
  exit 1
}

is_url() {
  case "$1" in
    http://*|https://*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

abs_path() {
  local target="$1"
  local dir
  local base

  dir="$(cd "$(dirname "$target")" && pwd -P)"
  base="$(basename "$target")"
  printf '%s/%s\n' "$dir" "$base"
}

api_error_message() {
  local body="$1"

  printf '%s' "$body" | jq -r '
    .data.error_message
    // .error_message
    // .message
    // .msg
    // .error
    // empty
  ' 2>/dev/null || true
}

retryable_http_status() {
  case "$1" in
    408|425|500|502|503|504)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

wait_before_retry() {
  sleep "$GOAI_HTTP_RETRY_DELAY_SECONDS"
}

json_request() {
  local method="$1"
  local url="$2"
  local auth_mode="$3"
  shift 3

  local response
  local status
  local body
  local message
  local curl_args
  local attempt

  curl_args=(-sS --connect-timeout "$GOAI_HTTP_CONNECT_TIMEOUT_SECONDS" --max-time "$GOAI_HTTP_JSON_TIMEOUT_SECONDS" -X "$method" "$url" -H "Accept: application/json")
  if [ "$auth_mode" = "auth" ]; then
    curl_args+=(-H "Authorization: Bearer ${GOAI_API_KEY}")
  fi
  while [ "$#" -gt 0 ]; do
    curl_args+=("$1")
    shift
  done

  attempt=1
  while [ "$attempt" -le "$GOAI_HTTP_MAX_ATTEMPTS" ]; do
    if response="$(curl "${curl_args[@]}" -w $'\n%{http_code}')"; then
      status="${response##*$'\n'}"
      body="${response%$'\n'*}"
      GOAI_LAST_JSON="$body"

      case "$status" in
        200|201)
          return 0
          ;;
        401)
          die "unauthorized: check GOAI_API_KEY"
          ;;
        402)
          die "insufficient credits. Recharge at http://mustgoai.com. Demo PPT: https://ai-neuralforge.oss-cn-hangzhou.aliyuncs.com/aippt/ppt/example_ppt/%E7%94%9F%E6%88%90%E4%B8%80%E4%BB%A5%E4%B8%AD%E5%9B%BD%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E4%B8%BA%E4%B8%BB%E9%A2%98%E7%9A%84%E7%A7%91%E6%99%AE%E6%BC%94%E7%A4%BA%E6%96%87%E7%A8%BF%E5%86%85%E5%AE%B9%E9%9C%80%E6%B6%B5%E7%9B%96%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E7%9A%84%E5%8E%86%E5%8F%B2%E6%B8%8A%E6%BA%90%E5%A4%A9%E6%96%87%E5%88%92%E5%88%86%E6%A0%87%E5%87%86%E4%BB%A5%E5%8F%8A%E5%9B%BD%E5%9B%BE.pptx"
          ;;
        429)
          die "rate limited"
          ;;
      esac

      if retryable_http_status "$status" && [ "$attempt" -lt "$GOAI_HTTP_MAX_ATTEMPTS" ]; then
        attempt=$((attempt + 1))
        wait_before_retry
        continue
      fi

      message="$(api_error_message "$body")"
      if [ -n "$message" ]; then
        die "request failed (${status}): ${message}"
      fi
      die "request failed (${status})"
    fi

    if [ "$attempt" -lt "$GOAI_HTTP_MAX_ATTEMPTS" ]; then
      attempt=$((attempt + 1))
      wait_before_retry
      continue
    fi

    die "request failed: ${url}"
  done
}

api_assert_ok() {
  local body="$1"
  local code
  local message

  code="$(printf '%s' "$body" | jq -r '.code // empty' 2>/dev/null || true)"
  [ -n "$code" ] || die "invalid API response"

  if [ "$code" != "0" ]; then
    message="$(api_error_message "$body")"
    if [ "$code" = "-5" ]; then
      if [ -n "$message" ]; then
        die "content blocked: ${message}"
      fi
      die "content blocked"
    fi
    if [ -n "$message" ]; then
      die "api error (code ${code}): ${message}"
    fi
    die "api error (code ${code})"
  fi
}

select_default_model() {
  local category="$1"
  local preferred="$2"
  local model

  json_request GET "${BASE_URL}/api/v1/models/capabilities" public
  api_assert_ok "$GOAI_LAST_JSON"

  model="$(printf '%s' "$GOAI_LAST_JSON" | jq -r --arg category "$category" --arg preferred "$preferred" '
    .data.capabilities as $caps
    | if (($caps[$preferred].display.category // "") == $category and ($caps[$preferred].display.enabled // false)) then
        $preferred
      else
        ($caps
          | to_entries
          | map(select((.value.display.category // "") == $category and (.value.display.enabled // false)))
          | .[0].key // empty)
      end
  ' 2>/dev/null)"

  [ -n "$model" ] || die "no enabled ${category} model available"
  printf '%s\n' "$model"
}

content_type_for_file() {
  local file="$1"

  case "${file##*.}" in
    png|PNG)
      printf '%s\n' "image/png"
      ;;
    jpg|JPG|jpeg|JPEG)
      printf '%s\n' "image/jpeg"
      ;;
    webp|WEBP)
      printf '%s\n' "image/webp"
      ;;
    gif|GIF)
      printf '%s\n' "image/gif"
      ;;
    *)
      die "unsupported image file type: ${file}"
      ;;
  esac
}

upload_local_image() {
  local file="$1"
  local mime_type
  local signed_url
  local final_url
  local status
  local attempt

  [ -r "$file" ] || die "local image not found or unreadable: ${file}"
  mime_type="$(content_type_for_file "$file")"

  json_request GET "${BASE_URL}/api/v2/oss/sign-url" auth \
    -G \
    --data-urlencode "filename=$(basename "$file")" \
    --data-urlencode "contentType=${mime_type}" \
    --data-urlencode "folder=inputs"
  api_assert_ok "$GOAI_LAST_JSON"

  signed_url="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.signedUrl // empty')"
  final_url="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.finalUrl // empty')"
  [ -n "$signed_url" ] || die "signedUrl missing from upload response"
  [ -n "$final_url" ] || die "finalUrl missing from upload response"

  attempt=1
  while [ "$attempt" -le "$GOAI_HTTP_MAX_ATTEMPTS" ]; do
    if status="$(curl -sS --connect-timeout "$GOAI_HTTP_CONNECT_TIMEOUT_SECONDS" --max-time "$GOAI_HTTP_TRANSFER_TIMEOUT_SECONDS" -X PUT "$signed_url" -H "Content-Type: ${mime_type}" --data-binary "@${file}" -o /dev/null -w '%{http_code}')"; then
      case "$status" in
        200|201)
          printf '%s\n' "$final_url"
          return 0
          ;;
      esac

      if retryable_http_status "$status" && [ "$attempt" -lt "$GOAI_HTTP_MAX_ATTEMPTS" ]; then
        attempt=$((attempt + 1))
        wait_before_retry
        continue
      fi

      die "upload failed (${status}): ${file}"
    fi

    if [ "$attempt" -lt "$GOAI_HTTP_MAX_ATTEMPTS" ]; then
      attempt=$((attempt + 1))
      wait_before_retry
      continue
    fi

    die "upload failed: ${file}"
  done

  die "upload failed: ${file}"
}

resolve_image_inputs_json() {
  local tmp_file
  local input
  local final_url
  local json_output

  if [ "$#" -eq 0 ]; then
    printf '%s\n' "[]"
    return 0
  fi

  tmp_file="$(mktemp)"

  for input in "$@"; do
    if is_url "$input"; then
      printf '%s\n' "$input" >>"$tmp_file"
    else
      final_url="$(upload_local_image "$input")"
      printf '%s\n' "$final_url" >>"$tmp_file"
    fi
  done

  json_output="$(jq -R . <"$tmp_file" | jq -s .)"
  rm -f "$tmp_file"
  printf '%s\n' "$json_output"
}

task_error_message() {
  local body="$1"

  printf '%s' "$body" | jq -r '
    .data.error_message
    // .error_message
    // .message
    // .msg
    // .error
    // empty
  ' 2>/dev/null || true
}

poll_task() {
  local task_url="$1"
  local media_field="$2"
  local interval_seconds="$3"
  local max_attempts="$4"
  local timeout_message="$5"
  local attempt
  local status
  local media_url
  local error_message
  local last_status

  attempt=1
  last_status=""
  while [ "$attempt" -le "$max_attempts" ]; do
    json_request GET "$task_url" auth
    api_assert_ok "$GOAI_LAST_JSON"

    status="$(printf '%s' "$GOAI_LAST_JSON" | jq -r '.data.status // empty')"
    case "$status" in
      completed)
        media_url="$(printf '%s' "$GOAI_LAST_JSON" | jq -r --arg field "$media_field" '.data[$field] // empty')"
        [ -n "$media_url" ] || die "${media_field} missing in completed task response"
        GOAI_LAST_MEDIA_URL="$media_url"
        return 0
        ;;
      failed|timeout)
        error_message="$(task_error_message "$GOAI_LAST_JSON")"
        if [ -n "$error_message" ]; then
          die "task ${status}: ${error_message}"
        fi
        die "task ${status}"
        ;;
      "")
        die "task status missing"
        ;;
    esac

    if [ "$status" != "$last_status" ] || [ "$attempt" -eq 1 ] || [ $((attempt % GOAI_TASK_STATUS_LOG_INTERVAL)) -eq 0 ]; then
      printf 'Task status: %s (%s/%s)\n' "$status" "$attempt" "$max_attempts" >&2
      last_status="$status"
    fi

    sleep "$interval_seconds"
    attempt=$((attempt + 1))
  done

  die "$timeout_message"
}

download_media() {
  local media_url="$1"
  local output_name="$2"
  local output_path
  local temp_path
  local attempt

  [ -n "$media_url" ] || die "download URL is required"
  output_path="$(abs_path "${output_name}")"
  temp_path="${output_path}.part"

  attempt=1
  while [ "$attempt" -le "$GOAI_HTTP_MAX_ATTEMPTS" ]; do
    if curl -fsSL --connect-timeout "$GOAI_HTTP_CONNECT_TIMEOUT_SECONDS" --max-time "$GOAI_HTTP_TRANSFER_TIMEOUT_SECONDS" "$media_url" -o "$temp_path"; then
      mv "$temp_path" "$output_path"
      printf '%s\n' "$output_path"
      return 0
    fi

    rm -f "$temp_path"
    if [ "$attempt" -lt "$GOAI_HTTP_MAX_ATTEMPTS" ]; then
      attempt=$((attempt + 1))
      wait_before_retry
      continue
    fi

    die "download failed: ${media_url}"
  done

  rm -f "$temp_path"
  die "download failed: ${media_url}"
}

open_local_ppt() {
  local file_path="$1"

  [ -n "$file_path" ] || die "local file path is required"
  [ -f "$file_path" ] || die "local file not found: ${file_path}"
  [ "$GOAI_AUTO_OPEN_OUTPUT" = "1" ] || return 0

  case "$(uname -s)" in
    Darwin)
      open "$file_path" >/dev/null 2>&1 || printf 'Warning: failed to open local PPT: %s\n' "$file_path" >&2
      ;;
    Linux)
      if ! command -v xdg-open >/dev/null 2>&1; then
        printf 'Warning: xdg-open is required to open local PPT files\n' >&2
        return 0
      fi
      xdg-open "$file_path" >/dev/null 2>&1 || printf 'Warning: failed to open local PPT: %s\n' "$file_path" >&2
      ;;
    *)
      printf 'Warning: automatic local PPT opening is not supported on this OS\n' >&2
      ;;
  esac
}

# get_openclaw_attachment_paths returns local file paths from OpenClaw uploaded attachments
# It scans the OpenClaw assets directory for images and PDFs
# Optional: set sort_newest_first=1 to output newest file first (by mtime)
# Portable: works on macOS (BSD find) and Linux (GNU find)
get_openclaw_attachment_paths() {
  local asset_dir="$1"
  local file_type="$2"  # "image" or "pdf"
  local sort_newest_first="${3:-0}"  # 1 = newest first

  if [ -z "$asset_dir" ] || [ ! -d "$asset_dir" ]; then
    return 1
  fi

  local out
  case "$file_type" in
    image)
      out=$(find "$asset_dir" -maxdepth 1 -type f \
        \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" -o -name "*.gif" \) \
        2>/dev/null)
      ;;
    pdf)
      out=$(find "$asset_dir" -maxdepth 1 -type f -name "*.pdf" 2>/dev/null)
      ;;
    *)
      return 1
      ;;
  esac

  if [ -z "$out" ]; then
    return 1
  fi

  if [ "$sort_newest_first" = "1" ]; then
    # Portable: sort by mtime newest first (macOS and Linux)
    echo "$out" | while IFS= read -r p; do
      [ -n "$p" ] && [ -f "$p" ] && printf '%s\0' "$p"
    done | xargs -0 ls -t 2>/dev/null | head -20
  else
    echo "$out" | head -20
  fi
}

OPENCLAW_MEDIA_INBOUND_DIR="${HOME}/.openclaw/media/inbound"

# Get the media/inbound directory for the current project
get_openclaw_media_inbound() {
  # Priority: OPENCLAW_MEDIA_INBOUND_DIR env var -> home-based default
  if [ -n "${OPENCLAW_MEDIA_INBOUND_DIR:-}" ]; then
    printf '%s\n' "$OPENCLAW_MEDIA_INBOUND_DIR"
    return 0
  fi
  printf '%s\n' "${HOME}/.openclaw/media/inbound"
  return 0
}

# get_openclaw_images returns image file paths from OpenClaw attachments (newest first).
# Priority: OPENCLAW_ASSETS_DIR -> media/inbound -> default assets.
get_openclaw_images() {
  local out
  local attempt_reason=""

  if [ -n "${OPENCLAW_ASSETS_DIR:-}" ]; then
    echo "Checking OpenClaw assets directory: $OPENCLAW_ASSETS_DIR" >&2
    out=$(get_openclaw_attachment_paths "$OPENCLAW_ASSETS_DIR" "image" "1") || true
    if [ -n "$out" ]; then
      echo "Found $(echo "$out" | wc -l | tr -d ' ') image(s) in assets directory" >&2
      printf '%s\n' "$out"
      return 0
    fi
    attempt_reason="assets dir empty or inaccessible"
  fi

  local media_inbound
  media_inbound="$(get_openclaw_media_inbound)" || {
    echo "Warning: Could not determine media/inbound directory" >&2
    media_inbound=""
  }
  if [ -n "$media_inbound" ]; then
    echo "Checking OpenClaw media/inbound directory: $media_inbound" >&2
    if [ -d "$media_inbound" ]; then
      out=$(get_openclaw_attachment_paths "$media_inbound" "image" "1") || true
      if [ -n "$out" ]; then
        echo "Found $(echo "$out" | wc -l | tr -d ' ') image(s) in media/inbound" >&2
        printf '%s\n' "$out"
        return 0
      fi
      attempt_reason="${attempt_reason:+$attempt_reason; }media/inbound empty"
    else
      echo "Warning: media/inbound directory does not exist: $media_inbound" >&2
      attempt_reason="${attempt_reason:+$attempt_reason; }media/inbound not found"
    fi
  fi

  local default_assets
  default_assets="$(get_openclaw_assets_dir)" || default_assets=""
  if [ -n "$default_assets" ]; then
    echo "Checking default assets directory: $default_assets" >&2
    out=$(get_openclaw_attachment_paths "$default_assets" "image" "1") || true
    if [ -n "$out" ]; then
      echo "Found $(echo "$out" | wc -l | tr -d ' ') image(s) in default assets" >&2
      printf '%s\n' "$out"
      return 0
    fi
    attempt_reason="${attempt_reason:+$attempt_reason; }default assets empty"
  fi

  echo "No image attachments found. ($attempt_reason)" >&2
  return 1
}

# get_openclaw_pdfs returns PDF file paths from OpenClaw attachments (newest first).
# Priority: OPENCLAW_ASSETS_DIR -> media/inbound -> default assets.
get_openclaw_pdfs() {
  local out
  local attempt_reason=""

  if [ -n "${OPENCLAW_ASSETS_DIR:-}" ]; then
    echo "Checking OpenClaw assets directory for PDFs: $OPENCLAW_ASSETS_DIR" >&2
    out=$(get_openclaw_attachment_paths "$OPENCLAW_ASSETS_DIR" "pdf" "1") || true
    if [ -n "$out" ]; then
      echo "Found $(echo "$out" | wc -l | tr -d ' ') PDF(s) in assets directory" >&2
      printf '%s\n' "$out"
      return 0
    fi
    attempt_reason="assets dir empty or inaccessible"
  fi

  local media_inbound
  media_inbound="$(get_openclaw_media_inbound)" || {
    echo "Warning: Could not determine media/inbound directory" >&2
    media_inbound=""
  }
  if [ -n "$media_inbound" ]; then
    echo "Checking OpenClaw media/inbound directory for PDFs: $media_inbound" >&2
    if [ -d "$media_inbound" ]; then
      out=$(get_openclaw_attachment_paths "$media_inbound" "pdf" "1") || true
      if [ -n "$out" ]; then
        echo "Found $(echo "$out" | wc -l | tr -d ' ') PDF(s) in media/inbound" >&2
        printf '%s\n' "$out"
        return 0
      fi
      attempt_reason="${attempt_reason:+$attempt_reason; }media/inbound empty"
    else
      echo "Warning: media/inbound directory does not exist: $media_inbound" >&2
      attempt_reason="${attempt_reason:+$attempt_reason; }media/inbound not found"
    fi
  fi

  local default_assets
  default_assets="$(get_openclaw_assets_dir)" || default_assets=""
  if [ -n "$default_assets" ]; then
    echo "Checking default assets directory for PDFs: $default_assets" >&2
    out=$(get_openclaw_attachment_paths "$default_assets" "pdf" "1") || true
    if [ -n "$out" ]; then
      echo "Found $(echo "$out" | wc -l | tr -d ' ') PDF(s) in default assets" >&2
      printf '%s\n' "$out"
      return 0
    fi
    attempt_reason="${attempt_reason:+$attempt_reason; }default assets empty"
  fi

  echo "No PDF attachments found. ($attempt_reason)" >&2
  return 1
}

# merge_image_inputs merges command-line image inputs with OpenClaw attachment images
# Usage: merge_image_inputs "img1.png" "img2.jpg"
merge_image_inputs() {
  local input_images=("$@")
  local attachment_images

  # Get OpenClaw attachment images if available
  attachment_images=$(get_openclaw_images) || attachment_images=""

  # If no command-line inputs, use attachments
  if [ ${#input_images[@]} -eq 0 ] && [ -n "$attachment_images" ]; then
    printf '%s\n' "$attachment_images"
    return 0
  fi

  # Merge both sources, deduplicating
  {
    printf '%s\n' "${input_images[@]}"
    printf '%s\n' "$attachment_images"
  } | sort -u | grep -v '^$'
}
