#!/usr/bin/env bash

set -euo pipefail

# Used by scripts that source this file.
# shellcheck disable=SC2034
BASE_URL="https://mongol.open-idea.net/api/v1"
MAX_UPLOAD_BYTES=10485760
HTTP_STATUS=""
# Used by scripts that source this file.
# shellcheck disable=SC2034
KEY=""

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

require_commands() {
  local command_name
  for command_name in "$@"; do
    command -v "$command_name" >/dev/null 2>&1 ||
      die "required command is not installed: $command_name"
  done
}

load_key() {
  if [ -n "${MONGOL_AI_SKILL_API_KEY:-}" ]; then
    # shellcheck disable=SC2034
    KEY="$MONGOL_AI_SKILL_API_KEY"
    case "$KEY" in
      *$'\r'*|*$'\n'*) die "MONGOL_AI_SKILL_API_KEY contains an invalid newline" ;;
    esac
    return 0
  fi

  if [ -n "${MENGGUYU_API_KEY:-}" ]; then
    die "MENGGUYU_API_KEY is deprecated. Rename it to MONGOL_AI_SKILL_API_KEY in your local environment; do not paste the key into chat."
  fi

  die "MONGOL_AI_SKILL_API_KEY is not configured. Create a key at https://mongol.open-idea.net and configure it locally; do not paste the key into chat."
}

read_text_argument() {
  if [ "$#" -gt 0 ]; then
    printf '%s' "$1"
    return 0
  fi
  if [ -t 0 ]; then
    die "text is required as an argument or on standard input"
  fi
  cat
}

validate_language() {
  case "$1" in
    zh|mw|mn) return 0 ;;
    *) die "language must be one of: zh, mw, mn" ;;
  esac
}

validate_ocr_language() {
  case "$1" in
    mw|mn) return 0 ;;
    *) die "OCR/ASR language must be 'mw' or 'mn'" ;;
  esac
}

validate_file() {
  local path="$1"
  [ -f "$path" ] || die "file does not exist: $path"
  [ -r "$path" ] || die "file is not readable: $path"
  local size
  size=$(wc -c < "$path" | tr -d '[:space:]')
  [ "$size" -le "$MAX_UPLOAD_BYTES" ] ||
    die "file exceeds the 10 MiB limit: $path"
}

unicode_length() {
  python3 - "$1" <<'PY'
import sys
print(len(sys.argv[1]))
PY
}

json_extract() {
  local file="$1" path="$2"
  python3 - "$file" "$path" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    value = json.load(handle)
for part in sys.argv[2].split("."):
    value = value[int(part)] if isinstance(value, list) else value[part]
if value is None:
    raise ValueError("null value")
if isinstance(value, (dict, list)):
    print(json.dumps(value, ensure_ascii=False))
else:
    print(value)
PY
}

json_extract_first() {
  local file="$1"
  shift
  local path
  for path in "$@"; do
    if json_extract "$file" "$path" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}

json_status() {
  local file="$1"
  json_extract_first "$file" status data.status 2>/dev/null ||
    printf 'unknown\n'
}

sanitized_error() {
  local file="$1"
  python3 - "$file" <<'PY'
import json
import os
import sys

try:
    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
except Exception:
    sys.exit(1)

candidates = []
if isinstance(payload, dict):
    for key in ("message", "error", "detail", "requestId", "request_id"):
        value = payload.get(key)
        if isinstance(value, str):
            candidates.append(value)
        elif isinstance(value, dict):
            nested = value.get("message")
            if isinstance(nested, str):
                candidates.append(nested)

if not candidates:
    sys.exit(1)

message = candidates[0].replace("\r", " ").replace("\n", " ")[:300]
secret = os.environ.get("MONGOL_AI_SKILL_API_KEY", "")
if secret:
    message = message.replace(secret, "[REDACTED]")
print(message)
PY
}

header_value() {
  local file="$1" header="$2"
  awk -v wanted="$header" '
    {
      line=$0
      sub(/\r$/, "", line)
      split(line, parts, ":")
      if (tolower(parts[1]) == tolower(wanted)) {
        sub(/^[^:]*:[[:space:]]*/, "", line)
        value=line
      }
    }
    END { if (value != "") print value }
  ' "$file"
}

json_billing_values() {
  local file="$1"
  python3 - "$file" <<'PY'
import json
import sys

try:
    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
except Exception:
    print("\t\t")
    sys.exit(0)

found = {}
wanted = {
    "billingcharged": "charged",
    "billingbalance": "balance",
    "billingcurrency": "currency",
}

def walk(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).replace("_", "").lower()
            if normalized in wanted and wanted[normalized] not in found:
                found[wanted[normalized]] = str(nested)
            walk(nested)
    elif isinstance(value, list):
        for nested in value:
            walk(nested)

walk(payload)
print("\t".join((found.get("charged", ""), found.get("balance", ""), found.get("currency", ""))))
PY
}

emit_billing_summary() {
  local header_file="$1" body_file="${2:-}"
  local charged balance currency json_values
  charged=$(header_value "$header_file" "X-Mengguyu-Billing-Charged" || true)
  balance=$(header_value "$header_file" "X-Mengguyu-Billing-Balance" || true)
  currency=$(header_value "$header_file" "X-Mengguyu-Billing-Currency" || true)

  if [ -n "$body_file" ] && [ -s "$body_file" ]; then
    json_values=$(json_billing_values "$body_file")
    if [ -z "$charged" ]; then
      charged=$(printf '%s' "$json_values" | cut -f1)
    fi
    if [ -z "$balance" ]; then
      balance=$(printf '%s' "$json_values" | cut -f2)
    fi
    if [ -z "$currency" ]; then
      currency=$(printf '%s' "$json_values" | cut -f3)
    fi
  fi

  if [ -n "$charged" ] && [ -n "$balance" ]; then
    printf '本次扣费: %s %s, 余额: %s %s\n' \
      "$charged" "${currency:-CNY}" "$balance" "${currency:-CNY}" >&2
  fi
}

retry_delay() {
  case "$1" in
    1) printf '5\n' ;;
    *) printf '15\n' ;;
  esac
}

perform_request() {
  local method="$1" header_file="$2" body_file="$3"
  shift 3

  local attempt=1 curl_exit=0 delay message
  HTTP_STATUS=""

  while [ "$attempt" -le 3 ]; do
    : > "$header_file"
    : > "$body_file"

    if HTTP_STATUS=$(curl -sS -o "$body_file" -D "$header_file" \
      -w '%{http_code}' -X "$method" "$@"); then
      curl_exit=0
    else
      curl_exit=$?
    fi

    if [ "$curl_exit" -ne 0 ]; then
      if [ "$method" = "GET" ] && [ "$attempt" -lt 3 ]; then
        delay=$(retry_delay "$attempt")
        printf 'Temporary polling transport error; retrying in %ss.\n' "$delay" >&2
        sleep "$delay"
        attempt=$((attempt + 1))
        continue
      fi
      if [ "$method" = "POST" ]; then
        printf 'Request transport failed before a response was received; the POST was not retried to avoid a duplicate charge.\n' >&2
      else
        printf 'Request transport failed after %s attempt(s).\n' "$attempt" >&2
      fi
      return 1
    fi

    case "$HTTP_STATUS" in
      2??) return 0 ;;
      429|5??)
        if [ "$attempt" -lt 3 ]; then
          delay=$(retry_delay "$attempt")
          printf 'HTTP %s; retrying in %ss.\n' "$HTTP_STATUS" "$delay" >&2
          sleep "$delay"
          attempt=$((attempt + 1))
          continue
        fi
        ;;
    esac
    break
  done

  message=$(sanitized_error "$body_file" 2>/dev/null || true)
  if [ -n "$message" ]; then
    printf 'HTTP %s: %s\n' "${HTTP_STATUS:-unknown}" "$message" >&2
  else
    printf 'HTTP %s request failed.\n' "${HTTP_STATUS:-unknown}" >&2
  fi
  return 1
}

extract_business_value() {
  local body_file="$1"
  shift
  local value
  if value=$(json_extract_first "$body_file" "$@" 2>/dev/null); then
    printf '%s\n' "$value"
    return 0
  fi
  die "the service response did not contain the expected result"
}

extract_job_id() {
  json_extract_first "$1" jobId job_id data.jobId data.job_id 2>/dev/null
}

validate_job_id() {
  case "$1" in
    ''|*[!A-Za-z0-9._-]*) die "the service returned an invalid job identifier" ;;
  esac
}

validate_audio_file() {
  local path="$1"
  python3 - "$path" <<'PY'
import sys

with open(sys.argv[1], "rb") as handle:
    head = handle.read(12)
if len(head) < 4:
    raise SystemExit(1)
valid = (
    head.startswith(b"RIFF") and head[8:12] == b"WAVE"
    or head.startswith(b"ID3")
    or head[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")
)
raise SystemExit(0 if valid else 1)
PY
}
