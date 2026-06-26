#!/usr/bin/env bash
# hitem3d.sh — CLI wrapper for Hitem3D API
#
# Commands:
#   auth                                  Get access token
#   balance                               Query credit balance
#   generate <image> [options]            Submit single-image task
#   generate-multi <img...> --views BITS  Submit multi-view task (2-4 images)
#   status <task_id>                      Query task status
#   wait <task_id> [--download DIR]       Poll until done, optionally download
#                                         Supports --poll-seconds and --timeout-seconds
#   run <image> [options]                 Generate + wait + download
#   run-multi <img...> --views BITS       Multi-view generate + wait + download
#   batch <dir> [options]                 Batch-submit a folder and wait/download each result
#
# Environment:
#   HITEM3D_AK      Access Key
#   HITEM3D_SK      Secret Key
#   HITEM3D_TOKEN   Optional cached token

set -euo pipefail

API_BASE="https://api.hitem3d.ai"
DEFAULT_MODEL="hitem3dv2.0"
DEFAULT_TYPE="3"
DEFAULT_RESOLUTION="1536"
DEFAULT_FORMAT="2"
DEFAULT_DOWNLOAD_DIR="./output/hitem3d"
DEFAULT_TIMEOUT_SECONDS="1800"
DEFAULT_POLL_SECONDS="5"

_die() { echo "ERROR: $*" >&2; exit 1; }
_info() { echo "$*" >&2; }
_json_get() {
  local expr="$1"
  python3 -c "import sys,json; d=json.load(sys.stdin); print(${expr})" 2>/dev/null || true
}

_require_file() {
  [[ -f "$1" ]] || _die "File not found: $1"
}

_file_size_bytes() {
  if stat -f%z "$1" >/dev/null 2>&1; then
    stat -f%z "$1"
  else
    stat -c%s "$1"
  fi
}

_preflight_image() {
  local f="$1"
  _require_file "$f"
  case "${f##*.}" in
    png|PNG|jpg|JPG|jpeg|JPEG|webp|WEBP) ;;
    *) _die "Unsupported image format: $f (allowed: png jpg jpeg webp)" ;;
  esac
  local size
  size=$(_file_size_bytes "$f")
  (( size <= 20971520 )) || _die "Image exceeds 20MB limit: $f"
}

_validate_face() {
  local face="$1"
  [[ -z "$face" ]] && return 0
  [[ "$face" =~ ^[0-9]+$ ]] || _die "Face count must be an integer"
  (( face >= 100000 && face <= 2000000 )) || _die "Face count must be between 100000 and 2000000"
}

_validate_resolution() {
  case "$1" in
    512|1024|1536|1536pro) ;;
    *) _die "Unsupported resolution: $1" ;;
  esac
}

_validate_format() {
  case "$1" in
    1|2|3|4|5) ;;
    *) _die "Unsupported format: $1" ;;
  esac
}

_validate_type() {
  case "$1" in
    1|2|3) ;;
    *) _die "Unsupported request type: $1" ;;
  esac
}

_validate_model() {
  case "$1" in
    hitem3dv1.5|hitem3dv2.0|scene-portraitv1.5|scene-portraitv2.0|scene-portraitv2.1) ;;
    *) _die "Unsupported model: $1" ;;
  esac
}

_validate_views() {
  [[ "$1" =~ ^[01]{4}$ ]] || _die "--views must be a 4-bit bitmap in front/back/left/right order, e.g. 1010"
}

_format_ext() {
  case "$1" in
    1) echo "obj" ;;
    2) echo "glb" ;;
    3) echo "stl" ;;
    4) echo "fbx" ;;
    5) echo "usdz" ;;
    *) echo "bin" ;;
  esac
}

_estimate_credits() {
  local model="$1" resolution="$2" request_type="$3"

  local textured="no"
  [[ "$request_type" == "2" || "$request_type" == "3" ]] && textured="yes"

  case "$model:$resolution:$textured" in
    hitem3dv1.5:512:no) echo 5 ;;
    hitem3dv1.5:512:yes) echo 15 ;;
    hitem3dv1.5:1024:no) echo 10 ;;
    hitem3dv1.5:1024:yes) echo 20 ;;
    hitem3dv1.5:1536:no) echo 40 ;;
    hitem3dv1.5:1536:yes) echo 50 ;;
    hitem3dv2.0:1536:no) echo 40 ;;
    hitem3dv2.0:1536:yes) echo 50 ;;
    hitem3dv2.0:1536pro:no) echo 60 ;;
    hitem3dv2.0:1536pro:yes) echo 70 ;;
    scene-portraitv2.0:1536pro:yes) echo 70 ;;
    scene-portraitv2.1:1536pro:yes) echo 70 ;;
    *) echo "unknown" ;;
  esac
}

cmd_auth() {
  [[ -n "${HITEM3D_AK:-}" ]] || _die "HITEM3D_AK not set"
  [[ -n "${HITEM3D_SK:-}" ]] || _die "HITEM3D_SK not set"
  local basic resp code token
  basic=$(printf '%s:%s' "$HITEM3D_AK" "$HITEM3D_SK" | base64)
  resp=$(curl -fsS -X POST "${API_BASE}/open-api/v1/auth/token" \
    -H "Authorization: Basic ${basic}" \
    -H "Content-Type: application/json") || _die "Auth request failed"
  code=$(printf '%s' "$resp" | _json_get "d.get('code','')")
  if [[ "$code" == "200" || "$code" == "0" ]]; then
    token=$(printf '%s' "$resp" | _json_get "d.get('data',{}).get('accessToken','')")
    [[ -n "$token" ]] || _die "Auth succeeded but token missing"
    echo "$token"
  else
    echo "$resp" >&2
    _die "Auth failed"
  fi
}

get_token() {
  if [[ -n "${HITEM3D_TOKEN:-}" ]]; then
    echo "$HITEM3D_TOKEN"
  else
    cmd_auth
  fi
}

cmd_balance() {
  local token
  token=$(get_token)
  curl -fsS -X GET "${API_BASE}/open-api/v1/balance" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json"
}

_parse_generate_args() {
  IMAGE=""
  MODEL="$DEFAULT_MODEL"
  REQUEST_TYPE="$DEFAULT_TYPE"
  RESOLUTION="$DEFAULT_RESOLUTION"
  FORMAT="$DEFAULT_FORMAT"
  FACE=""
  CALLBACK_URL=""

  [[ $# -ge 1 ]] || _die "Missing image path"
  IMAGE="$1"; shift
  _preflight_image "$IMAGE"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --model) MODEL="$2"; shift 2 ;;
      --type) REQUEST_TYPE="$2"; shift 2 ;;
      --resolution) RESOLUTION="$2"; shift 2 ;;
      --format) FORMAT="$2"; shift 2 ;;
      --face) FACE="$2"; shift 2 ;;
      --callback) CALLBACK_URL="$2"; shift 2 ;;
      *) _die "Unknown option: $1" ;;
    esac
  done

  _validate_model "$MODEL"
  _validate_type "$REQUEST_TYPE"
  _validate_resolution "$RESOLUTION"
  _validate_format "$FORMAT"
  _validate_face "$FACE"

  if [[ "$MODEL" == "hitem3dv2.0" && "$REQUEST_TYPE" == "2" ]]; then
    _die "request_type=2 is not supported by hitem3dv2.0"
  fi
}

_submit_single() {
  local token="$1"
  local curl_args=(
    -fsS -X POST "${API_BASE}/open-api/v1/submit-task"
    -H "Authorization: Bearer ${token}"
    -F "model=${MODEL}"
    -F "request_type=${REQUEST_TYPE}"
    -F "resolution=${RESOLUTION}"
    -F "format=${FORMAT}"
    -F "images=@${IMAGE}"
  )
  [[ -n "$FACE" ]] && curl_args+=(-F "face=${FACE}")
  [[ -n "$CALLBACK_URL" ]] && curl_args+=(-F "callback_url=${CALLBACK_URL}")
  curl "${curl_args[@]}"
}

cmd_generate() {
  _parse_generate_args "$@"
  local token
  token=$(get_token)
  _submit_single "$token"
}

_parse_multi_args() {
  MULTI_IMAGES=()
  MODEL="$DEFAULT_MODEL"
  REQUEST_TYPE="$DEFAULT_TYPE"
  RESOLUTION="$DEFAULT_RESOLUTION"
  FORMAT="$DEFAULT_FORMAT"
  FACE=""
  CALLBACK_URL=""
  MULTI_VIEWS=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --views) MULTI_VIEWS="$2"; shift 2 ;;
      --model) MODEL="$2"; shift 2 ;;
      --type) REQUEST_TYPE="$2"; shift 2 ;;
      --resolution) RESOLUTION="$2"; shift 2 ;;
      --format) FORMAT="$2"; shift 2 ;;
      --face) FACE="$2"; shift 2 ;;
      --callback) CALLBACK_URL="$2"; shift 2 ;;
      --*) _die "Unknown option: $1" ;;
      *) MULTI_IMAGES+=("$1"); shift ;;
    esac
  done

  (( ${#MULTI_IMAGES[@]} >= 2 && ${#MULTI_IMAGES[@]} <= 4 )) || _die "Multi-view requires 2-4 images"
  [[ -n "$MULTI_VIEWS" ]] || _die "Multi-view requires --views"
  _validate_views "$MULTI_VIEWS"
  [[ ${#MULTI_IMAGES[@]} -eq $(printf '%s' "$MULTI_VIEWS" | tr -cd '1' | wc -c | tr -d ' ') ]] || _die "Number of images must match count of 1s in --views bitmap"

  for img in "${MULTI_IMAGES[@]}"; do _preflight_image "$img"; done
  _validate_model "$MODEL"
  _validate_type "$REQUEST_TYPE"
  _validate_resolution "$RESOLUTION"
  _validate_format "$FORMAT"
  _validate_face "$FACE"

  if [[ "$MODEL" == "hitem3dv2.0" && "$REQUEST_TYPE" == "2" ]]; then
    _die "request_type=2 is not supported by hitem3dv2.0"
  fi
}

cmd_generate_multi() {
  _parse_multi_args "$@"
  local token
  token=$(get_token)

  local curl_args=(
    -fsS -X POST "${API_BASE}/open-api/v1/submit-task"
    -H "Authorization: Bearer ${token}"
    -F "model=${MODEL}"
    -F "request_type=${REQUEST_TYPE}"
    -F "resolution=${RESOLUTION}"
    -F "format=${FORMAT}"
    -F "multi_images_bit=${MULTI_VIEWS}"
  )

  for img in "${MULTI_IMAGES[@]}"; do
    curl_args+=(-F "multi_images=@${img}")
  done

  [[ -n "$FACE" ]] && curl_args+=(-F "face=${FACE}")
  [[ -n "$CALLBACK_URL" ]] && curl_args+=(-F "callback_url=${CALLBACK_URL}")

  curl "${curl_args[@]}"
}

cmd_status() {
  local task_id="${1:-}"
  [[ -n "$task_id" ]] || _die "Missing task_id"
  local token
  token=$(get_token)
  curl -fsS -X GET "${API_BASE}/open-api/v1/query-task?task_id=${task_id}" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json"
}

_download_from_status() {
  local resp="$1" download_dir="$2" task_id="$3" format_code="$4"
  mkdir -p "$download_dir"
  local url filename ext
  url=$(printf '%s' "$resp" | _json_get "d.get('data',{}).get('url','')")
  [[ -n "$url" ]] || _die "No download URL found in task response"
  filename=$(basename "${url%%\?*}")
  ext=$(_format_ext "$format_code")
  [[ -n "$filename" && "$filename" != "/" ]] || filename="${task_id}.${ext}"
  if [[ "$filename" != *.* ]]; then
    filename="${filename}.${ext}"
  fi
  curl -fsS -L -o "${download_dir}/${filename}" "$url" || _die "Download failed"
  printf '%s\n' "${download_dir}/${filename}"
}

cmd_wait() {
  local task_id="${1:-}"
  [[ -n "$task_id" ]] || _die "Missing task_id"
  shift || true

  local download_dir=""
  local poll_seconds="$DEFAULT_POLL_SECONDS"
  local timeout_seconds="$DEFAULT_TIMEOUT_SECONDS"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --download) download_dir="$2"; shift 2 ;;
      --poll-seconds) poll_seconds="$2"; shift 2 ;;
      --timeout-seconds) timeout_seconds="$2"; shift 2 ;;
      *) _die "Unknown option: $1" ;;
    esac
  done

  [[ "$poll_seconds" =~ ^[0-9]+$ ]] || _die "--poll-seconds must be an integer"
  [[ "$timeout_seconds" =~ ^[0-9]+$ ]] || _die "--timeout-seconds must be an integer"
  (( poll_seconds >= 1 )) || _die "--poll-seconds must be >= 1"
  (( timeout_seconds >= poll_seconds )) || _die "--timeout-seconds must be >= --poll-seconds"

  _info "Waiting for task ${task_id}..."
  local max_attempts=$(( timeout_seconds / poll_seconds ))
  local attempt=0
  while (( attempt < max_attempts )); do
    local resp state format_code output_path
    resp=$(cmd_status "$task_id") || {
      (( attempt++ ))
      sleep 5
      continue
    }
    state=$(printf '%s' "$resp" | _json_get "d.get('data',{}).get('state','unknown')")
    case "$state" in
      success)
        _info "Task completed"
        echo "$resp"
        if [[ -n "$download_dir" ]]; then
          format_code=$(printf '%s' "$resp" | _json_get "d.get('data',{}).get('format', 2)")
          output_path=$(_download_from_status "$resp" "$download_dir" "$task_id" "$format_code")
          _info "Saved: ${output_path}"
        fi
        return 0
        ;;
      failed)
        echo "$resp"
        return 1
        ;;
      created|queueing|processing|unknown|"")
        _info "Status: ${state:-unknown} (${attempt}/${max_attempts})"
        sleep "$poll_seconds"
        ;;
      *)
        _info "Status: ${state} (${attempt}/${max_attempts})"
        sleep "$poll_seconds"
        ;;
    esac
    (( attempt++ ))
  done
  _die "Timeout waiting for task"
}

_extract_task_id() {
  printf '%s' "$1" | _json_get "d.get('data',{}).get('task_id','')"
}

_print_run_summary() {
  local task_id="$1" saved_path="$2" model="$3" resolution="$4" format="$5" request_type="$6"
  local credits
  credits=$(_estimate_credits "$model" "$resolution" "$request_type")
  cat <<EOF
{
  "task_id": "${task_id}",
  "saved_path": "${saved_path}",
  "model": "${model}",
  "resolution": "${resolution}",
  "format": "${format}",
  "request_type": "${request_type}",
  "estimated_credits": "${credits}"
}
EOF
}

cmd_run() {
  local download_dir="$DEFAULT_DOWNLOAD_DIR"
  local poll_seconds="$DEFAULT_POLL_SECONDS"
  local timeout_seconds="$DEFAULT_TIMEOUT_SECONDS"
  local args=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --download-dir) download_dir="$2"; shift 2 ;;
      --poll-seconds) poll_seconds="$2"; shift 2 ;;
      --timeout-seconds) timeout_seconds="$2"; shift 2 ;;
      *) args+=("$1"); shift ;;
    esac
  done

  _parse_generate_args "${args[@]}"
  local resp task_id wait_resp saved_path
  resp=$(cmd_generate "${args[@]}")
  task_id=$(_extract_task_id "$resp")
  [[ -n "$task_id" ]] || { echo "$resp" >&2; _die "Task submission succeeded but task_id missing"; }
  wait_resp=$(cmd_wait "$task_id" --download "$download_dir" --poll-seconds "$poll_seconds" --timeout-seconds "$timeout_seconds")
  saved_path=$(printf '%s' "$wait_resp" >/dev/null 2>&1; find "$download_dir" -type f -mmin -5 | sort | tail -n 1)
  _print_run_summary "$task_id" "${saved_path:-}" "$MODEL" "$RESOLUTION" "$FORMAT" "$REQUEST_TYPE"
}

cmd_run_multi() {
  local download_dir="$DEFAULT_DOWNLOAD_DIR"
  local poll_seconds="$DEFAULT_POLL_SECONDS"
  local timeout_seconds="$DEFAULT_TIMEOUT_SECONDS"
  local args=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --download-dir) download_dir="$2"; shift 2 ;;
      --poll-seconds) poll_seconds="$2"; shift 2 ;;
      --timeout-seconds) timeout_seconds="$2"; shift 2 ;;
      *) args+=("$1"); shift ;;
    esac
  done

  _parse_multi_args "${args[@]}"
  local resp task_id wait_resp saved_path
  resp=$(cmd_generate_multi "${args[@]}")
  task_id=$(_extract_task_id "$resp")
  [[ -n "$task_id" ]] || { echo "$resp" >&2; _die "Task submission succeeded but task_id missing"; }
  wait_resp=$(cmd_wait "$task_id" --download "$download_dir" --poll-seconds "$poll_seconds" --timeout-seconds "$timeout_seconds")
  saved_path=$(printf '%s' "$wait_resp" >/dev/null 2>&1; find "$download_dir" -type f -mmin -5 | sort | tail -n 1)
  _print_run_summary "$task_id" "${saved_path:-}" "$MODEL" "$RESOLUTION" "$FORMAT" "$REQUEST_TYPE"
}

cmd_batch() {
  local dir="${1:-}"
  [[ -n "$dir" ]] || _die "Missing directory"
  [[ -d "$dir" ]] || _die "Directory not found: $dir"
  shift || true

  local glob="*.png"
  local download_dir="$DEFAULT_DOWNLOAD_DIR/batch"
  local model="$DEFAULT_MODEL"
  local request_type="$DEFAULT_TYPE"
  local resolution="$DEFAULT_RESOLUTION"
  local format="$DEFAULT_FORMAT"
  local face=""
  local poll_seconds="$DEFAULT_POLL_SECONDS"
  local timeout_seconds="$DEFAULT_TIMEOUT_SECONDS"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --glob) glob="$2"; shift 2 ;;
      --download-dir) download_dir="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      --type) request_type="$2"; shift 2 ;;
      --resolution) resolution="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --face) face="$2"; shift 2 ;;
      --poll-seconds) poll_seconds="$2"; shift 2 ;;
      --timeout-seconds) timeout_seconds="$2"; shift 2 ;;
      *) _die "Unknown option: $1" ;;
    esac
  done

  _validate_model "$model"
  _validate_type "$request_type"
  _validate_resolution "$resolution"
  _validate_format "$format"
  _validate_face "$face"

  if [[ "$model" == "hitem3dv2.0" && "$request_type" == "2" ]]; then
    _die "request_type=2 is not supported by hitem3dv2.0"
  fi

  [[ "$poll_seconds" =~ ^[0-9]+$ ]] || _die "--poll-seconds must be an integer"
  [[ "$timeout_seconds" =~ ^[0-9]+$ ]] || _die "--timeout-seconds must be an integer"

  files=()
  while IFS= read -r line; do
    files+=("$line")
  done < <(find "$dir" -maxdepth 1 -type f -name "$glob" | sort)
  (( ${#files[@]} > 0 )) || _die "No files matched ${glob} in ${dir}"

  mkdir -p "$download_dir"
  local out_json="${download_dir}/batch-results.jsonl"
  : > "$out_json"

  local img resp task_id item_dir wait_resp saved_path
  for img in "${files[@]}"; do
    _preflight_image "$img"
    _info "Submitting: $img"
    if [[ -n "$face" ]]; then
      resp=$(cmd_generate "$img" --model "$model" --type "$request_type" --resolution "$resolution" --format "$format" --face "$face")
    else
      resp=$(cmd_generate "$img" --model "$model" --type "$request_type" --resolution "$resolution" --format "$format")
    fi
    task_id=$(_extract_task_id "$resp")
    [[ -n "$task_id" ]] || { echo "$resp" >&2; _die "Missing task_id for $img"; }
    item_dir="${download_dir}/$(basename "${img%.*}")"
    mkdir -p "$item_dir"
    if wait_resp=$(cmd_wait "$task_id" --download "$item_dir" --poll-seconds "$poll_seconds" --timeout-seconds "$timeout_seconds"); then
      saved_path=$(find "$item_dir" -type f | sort | tail -n 1)
      printf '{"input":"%s","task_id":"%s","status":"success","saved_path":"%s"}\n' "$img" "$task_id" "$saved_path" >> "$out_json"
    else
      printf '{"input":"%s","task_id":"%s","status":"failed"}\n' "$img" "$task_id" >> "$out_json"
    fi
  done

  cat "$out_json"
}

case "${1:-help}" in
  auth) shift; cmd_auth "$@" ;;
  balance) shift; cmd_balance "$@" ;;
  generate) shift; cmd_generate "$@" ;;
  generate-multi) shift; cmd_generate_multi "$@" ;;
  status) shift; cmd_status "$@" ;;
  wait) shift; cmd_wait "$@" ;;
  run) shift; cmd_run "$@" ;;
  run-multi) shift; cmd_run_multi "$@" ;;
  batch) shift; cmd_batch "$@" ;;
  help|--help|-h)
    cat <<'EOF'
Usage: hitem3d.sh {auth|balance|generate|generate-multi|status|wait|run|run-multi|batch} [args]

Commands:
  auth                                  Get access token
  balance                               Query credit balance
  generate <image> [options]            Submit single-image task
  generate-multi <img...> --views BITS  Submit multi-view task
  status <task_id>                      Query task status
  wait <task_id> [--download DIR]       Poll until done, optionally download
  run <image> [options]                 Submit, wait, and download single-image result
    --download-dir <dir>                Output directory (default: ./output/hitem3d)
    --poll-seconds <n>                  Poll interval in seconds (default: 5)
    --timeout-seconds <n>               Max wait time in seconds (default: 1800)
  run-multi <img...> --views BITS       Submit, wait, and download multi-view result
    --download-dir <dir>                Output directory (default: ./output/hitem3d)
    --poll-seconds <n>                  Poll interval in seconds (default: 5)
    --timeout-seconds <n>               Max wait time in seconds (default: 1800)
  batch <dir> [options]                 Batch process a folder
    --glob <pattern>                    File glob (default: *.png)
    --download-dir <dir>                Output directory (default: ./output/hitem3d/batch)
    --poll-seconds <n>                  Poll interval in seconds (default: 5)
    --timeout-seconds <n>               Max wait time in seconds (default: 1800)

Generate/Run options:
  --model <name>                        hitem3dv1.5 | hitem3dv2.0 | scene-portraitv1.5 | scene-portraitv2.0 | scene-portraitv2.1
  --type <1|2|3>                        1=mesh only, 2=texture existing mesh, 3=mesh+texture
  --resolution <res>                    512 | 1024 | 1536 | 1536pro
  --format <1-5>                        1=obj 2=glb 3=stl 4=fbx 5=usdz
  --face <count>                        Face count 100000-2000000
  --callback <url>                      Webhook callback URL

Multi-view:
  --views <bits>                        4-bit front/back/left/right bitmap, e.g. 1010

Environment:
  HITEM3D_AK, HITEM3D_SK required
  HITEM3D_TOKEN optional
EOF
    ;;
  *) _die "Unknown command: $1. Use --help for usage." ;;
esac
