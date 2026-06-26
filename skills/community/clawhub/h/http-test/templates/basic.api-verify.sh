#!/usr/bin/env bash

set -uo pipefail

SCRIPT_DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
SCRIPT_NAME="$(basename -- "$0")"
DEFAULT_HTTP_FILE="${SCRIPT_DIR}/${SCRIPT_NAME%.api-verify.sh}.api-tests.http"

if [[ ! -f "$DEFAULT_HTTP_FILE" ]]; then
  ALT_HTTP_FILE="${SCRIPT_DIR}/${SCRIPT_NAME%.api-verify.sh}.api-tests.http.txt"
  if [[ -f "$ALT_HTTP_FILE" ]]; then
    DEFAULT_HTTP_FILE="$ALT_HTTP_FILE"
  else
    DEFAULT_HTTP_FILE="${SCRIPT_DIR}/basic.api-tests.http"
    if [[ ! -f "$DEFAULT_HTTP_FILE" ]]; then
      DEFAULT_HTTP_FILE="${SCRIPT_DIR}/basic.api-tests.http.txt"
    fi
  fi
fi

HTTP_FILE="${1:-$DEFAULT_HTTP_FILE}"
MAX_TIME="${MAX_TIME:-20}"

if [[ ! -f "$HTTP_FILE" ]]; then
  echo "HTTP definition file not found: $HTTP_FILE" >&2
  exit 2
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required." >&2
  exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required." >&2
  exit 2
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

declare -A VARS

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

env_override_for() {
  local key="$1"
  local env_name=""
  case "$key" in
    host) env_name="HOST" ;;
    cookie) env_name="COOKIE" ;;
    token|authToken|auth_token) env_name="AUTH_TOKEN" ;;
    resourceId|resource_id) env_name="RESOURCE_ID" ;;
    userId|user_id) env_name="USER_ID" ;;
    *)
      env_name="$(printf '%s' "$key" | sed -E 's/([a-z0-9])([A-Z])/\1_\2/g' | tr '[:lower:]' '[:upper:]')"
      ;;
  esac
  printf '%s' "${!env_name-}"
}

set_var() {
  local key="$1"
  local value="$2"
  local override
  override="$(env_override_for "$key")"
  if [[ -n "$override" ]]; then
    value="$override"
  fi
  VARS["$key"]="$value"
}

substitute_vars() {
  local text="$1"
  local key
  for key in "${!VARS[@]}"; do
    text="${text//\{\{$key\}\}/${VARS[$key]}}"
  done
  printf '%s' "$text"
}

meta_value() {
  local key="$1"
  local meta="$2"
  local line raw_key raw_value
  while IFS= read -r line; do
    line="${line%$'\r'}"
    [[ -z "$line" ]] && continue
    [[ "$line" == *"="* ]] || continue
    raw_key="$(trim "${line%%=*}")"
    raw_value="$(trim "${line#*=}")"
    if [[ "$raw_key" == "$key" ]]; then
      printf '%s' "$raw_value"
      return 0
    fi
  done <<< "$meta"
  return 1
}

print_case_result() {
  local verdict="$1"
  local title="$2"
  local detail_file="$3"
  echo "[$verdict] $title"
  sed 's/^/  /' "$detail_file"
  echo
}

assert_case() {
  local title="$1"
  local method="$2"
  local url="$3"
  local meta_file="$4"
  local body_file="$5"
  local http_status="$6"
  local content_type="$7"
  local time_total="$8"
  local detail_file="$9"

  python3 - "$title" "$method" "$url" "$meta_file" "$body_file" "$http_status" "$content_type" "$time_total" >"$detail_file" <<'PY'
import json
import re
import shutil
import sys
from pathlib import Path

title, method, url, meta_path, body_path, http_status, content_type, time_total = sys.argv[1:]

meta = {}
with open(meta_path, "r", encoding="utf-8") as fh:
    for raw in fh:
        line = raw.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        meta[key.strip()] = value.strip()

body_text = Path(body_path).read_text(encoding="utf-8", errors="replace")
payload = None
json_error = None
if body_text.lstrip().startswith("{") or body_text.lstrip().startswith("["):
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        json_error = str(exc)


class PathMissing(Exception):
    pass


def parse_path(path: str):
    if not path:
        return []
    tokens = []
    for part in path.split("."):
        remainder = part
        while remainder:
            match = re.match(r"^([^\[\]]+)", remainder)
            if match:
                tokens.append(("key", match.group(1)))
                remainder = remainder[match.end():]
                continue
            if remainder.startswith("[]"):
                tokens.append(("all", None))
                remainder = remainder[2:]
                continue
            match = re.match(r"^\[(\d+)\]", remainder)
            if match:
                tokens.append(("index", int(match.group(1))))
                remainder = remainder[match.end():]
                continue
            raise PathMissing(path)
    return tokens


def resolve_path(obj, path: str):
    nodes = [obj]
    for kind, value in parse_path(path):
        next_nodes = []
        for node in nodes:
            if kind == "key":
                if isinstance(node, dict) and value in node:
                    next_nodes.append(node[value])
            elif kind == "index":
                if isinstance(node, list) and value < len(node):
                    next_nodes.append(node[value])
            elif kind == "all":
                if isinstance(node, list):
                    next_nodes.extend(node)
        if not next_nodes:
            raise PathMissing(path)
        nodes = next_nodes
    if len(nodes) == 1:
        return nodes[0]
    return nodes


def stringify(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def flatten_list(value):
    if isinstance(value, list):
        flat = []
        for item in value:
            if isinstance(item, list):
                flat.extend(flatten_list(item))
            else:
                flat.append(item)
        return flat
    return [value]


expectation_bits = []
reason = None

if "expect.status" in meta:
    expectation_bits.append(f"HTTP status == {meta['expect.status']}")
    if str(http_status) != meta["expect.status"]:
        reason = f"expected HTTP status {meta['expect.status']} but got {http_status}"

if not reason and "expect.contains" in meta:
    expectation_bits.append(f"contains {meta['expect.contains']}")
    if meta["expect.contains"] not in body_text:
        reason = f"expected response to contain {meta['expect.contains']!r}"

if not reason and "expect.not_contains" in meta:
    expectation_bits.append(f"not_contains {meta['expect.not_contains']}")
    if meta["expect.not_contains"] in body_text:
        reason = f"expected response to not contain {meta['expect.not_contains']!r}"

json_needed = any(
    key in meta
    for key in (
        "expect.errno",
        "expect.errno_not",
        "expect.json_path",
        "expect.exists",
        "expect.absent",
        "expect.list_contains",
        "expect.list_not_contains",
        "output.fields",
    )
)

if not reason and json_needed and payload is None:
    reason = (
        "response is not valid JSON for the requested assertions"
        if json_error is None
        else f"response JSON parse failed: {json_error}"
    )

if not reason and "expect.errno" in meta:
    expectation_bits.append(f"errno == {meta['expect.errno']}")
    try:
      actual_errno = resolve_path(payload, "errno")
    except PathMissing:
      reason = "expected errno field but it was missing"
    else:
      if stringify(actual_errno) != meta["expect.errno"]:
        reason = f"expected errno {meta['expect.errno']} but got {stringify(actual_errno)}"

if not reason and "expect.errno_not" in meta:
    expectation_bits.append(f"errno != {meta['expect.errno_not']}")
    try:
      actual_errno = resolve_path(payload, "errno")
    except PathMissing:
      actual_errno = None
    if stringify(actual_errno) == meta["expect.errno_not"]:
        reason = f"expected errno != {meta['expect.errno_not']}"

if not reason and "expect.json_path" in meta and "expect.equals" in meta:
    expectation_bits.append(f"{meta['expect.json_path']} == {meta['expect.equals']}")
    try:
        actual = resolve_path(payload, meta["expect.json_path"])
    except PathMissing:
        reason = f"JSON path missing: {meta['expect.json_path']}"
    else:
        if stringify(actual) != meta["expect.equals"]:
            reason = (
                f"expected {meta['expect.json_path']} == {meta['expect.equals']} "
                f"but got {stringify(actual)}"
            )

if not reason and "expect.exists" in meta:
    expectation_bits.append(f"exists {meta['expect.exists']}")
    try:
        resolve_path(payload, meta["expect.exists"])
    except PathMissing:
        reason = f"JSON path missing: {meta['expect.exists']}"

if not reason and "expect.absent" in meta:
    expectation_bits.append(f"absent {meta['expect.absent']}")
    try:
        resolve_path(payload, meta["expect.absent"])
    except PathMissing:
        pass
    else:
        reason = f"expected JSON path to be absent: {meta['expect.absent']}"

if not reason and "expect.list_contains" in meta:
    path, expected = meta["expect.list_contains"].split(":", 1)
    expectation_bits.append(f"{path} contains {expected}")
    try:
        values = flatten_list(resolve_path(payload, path))
    except PathMissing:
        reason = f"JSON path missing: {path}"
    else:
        rendered = [stringify(value) for value in values]
        if expected not in rendered:
            reason = f"expected {path} to contain {expected}; actual values: {rendered}"

if not reason and "expect.list_not_contains" in meta:
    path, expected = meta["expect.list_not_contains"].split(":", 1)
    expectation_bits.append(f"{path} not_contains {expected}")
    try:
        values = flatten_list(resolve_path(payload, path))
    except PathMissing:
        values = []
    rendered = [stringify(value) for value in values]
    if expected in rendered:
        reason = f"expected {path} to not contain {expected}; actual values: {rendered}"

if "expect.save" in meta:
    save_target = Path(meta["expect.save"])
    save_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(body_path, save_target)

print(f"URL: {url}")
print(f"method: {method}")
if expectation_bits:
    print(f"expectation: {'; '.join(expectation_bits)}")
millis = int(float(time_total) * 1000)
line = f"HTTP={http_status} cost={millis}ms"
if content_type:
    line += f" content-type={content_type}"
print(line)

if "output.fields" in meta and payload is not None:
    fields = []
    for raw_path in meta["output.fields"].split(","):
        path = raw_path.strip()
        if not path:
            continue
        try:
            value = resolve_path(payload, path)
        except PathMissing:
            value = "<missing>"
        fields.append(f"{path}={stringify(value)}")
    if fields:
        print(f"key fields: {','.join(fields)}")

if "expect.save" in meta:
    print(f"saved response: {meta['expect.save']}")

if reason:
    print(f"reason: {reason}")
    sys.exit(10)

sys.exit(0)
PY
}

run_case() {
  local title="$1"
  local meta="$2"
  local request_line="$3"
  local headers_raw="$4"
  local body_raw="$5"

  local method url auth cookie_value token_value line
  local detail_file meta_file response_file headers_file request_body_file
  local -a curl_args header_args

  [[ -z "$title" ]] && return 0
  [[ -z "$request_line" ]] && return 0

  method="$(trim "${request_line%% *}")"
  url="$(trim "${request_line#* }")"
  url="$(substitute_vars "$url")"
  auth="$(meta_value "auth" "$meta" || true)"
  cookie_value="${VARS[cookie]-}"
  token_value="${VARS[token]-}"

  case "$auth" in
    cookie)
      if [[ -z "${COOKIE-}" && ( -z "$cookie_value" || "$cookie_value" == "<set via COOKIE>" ) ]]; then
        detail_file="$TMP_DIR/detail.skip.$SKIP_COUNT"
        printf 'reason: missing COOKIE environment variable for cookie-authenticated case\n' >"$detail_file"
        print_case_result "SKIP" "$title" "$detail_file"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        return 0
      fi
      ;;
    bearer)
      if [[ -z "${AUTH_TOKEN-}" && -z "${TOKEN-}" && ( -z "$token_value" || "$token_value" == "<set via AUTH_TOKEN>" ) ]]; then
        detail_file="$TMP_DIR/detail.skip.$SKIP_COUNT"
        printf 'reason: missing AUTH_TOKEN environment variable for bearer-authenticated case\n' >"$detail_file"
        print_case_result "SKIP" "$title" "$detail_file"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        return 0
      fi
      ;;
  esac

  detail_file="$TMP_DIR/detail.$RANDOM"
  meta_file="$TMP_DIR/meta.$RANDOM"
  response_file="$TMP_DIR/response.$RANDOM"
  headers_file="$TMP_DIR/headers.$RANDOM"
  request_body_file="$TMP_DIR/request-body.$RANDOM"
  printf '%s' "$meta" >"$meta_file"

  while IFS= read -r line; do
    line="${line%$'\r'}"
    [[ -z "$line" ]] && continue
    header_args+=(-H "$(substitute_vars "$line")")
  done <<< "$headers_raw"

  body_raw="$(substitute_vars "$body_raw")"
  curl_args=(
    --silent
    --show-error
    --location
    --max-time "$MAX_TIME"
    -X "$method"
    "${header_args[@]}"
    -D "$headers_file"
    -o "$response_file"
    -w "%{http_code}\t%{content_type}\t%{time_total}"
    "$url"
  )

  if [[ -n "$body_raw" ]]; then
    printf '%s' "$body_raw" >"$request_body_file"
    curl_args+=(--data-binary "@$request_body_file")
  fi

  local curl_output curl_status http_status content_type time_total
  curl_output="$(curl "${curl_args[@]}" 2>"$detail_file")"
  curl_status=$?
  if [[ $curl_status -ne 0 ]]; then
    {
      echo "URL: $url"
      echo "method: $method"
      echo "reason: curl transport failure (exit=$curl_status)"
      sed 's/^/stderr: /' "$detail_file"
    } >"$detail_file.transport"
    print_case_result "FAIL" "$title" "$detail_file.transport"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    return 0
  fi

  IFS=$'\t' read -r http_status content_type time_total <<< "$curl_output"
  if assert_case "$title" "$method" "$url" "$meta_file" "$response_file" "$http_status" "$content_type" "$time_total" "$detail_file.assert"; then
    print_case_result "PASS" "$title" "$detail_file.assert"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    print_case_result "FAIL" "$title" "$detail_file.assert"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

current_title=""
current_meta=""
current_request=""
current_headers=""
current_body=""
state="preamble"

while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%$'\r'}"

  if [[ "$line" =~ ^@([A-Za-z0-9_]+)[[:space:]]*=[[:space:]]*(.*)$ ]]; then
    set_var "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
    continue
  fi

  if [[ "$line" == "### "* ]]; then
    run_case "$current_title" "$current_meta" "$current_request" "$current_headers" "$current_body"
    current_title="${line#"### "}"
    current_meta=""
    current_request=""
    current_headers=""
    current_body=""
    state="meta"
    continue
  fi

  [[ -z "$current_title" ]] && continue

  case "$state" in
    meta)
      if [[ -z "$line" ]]; then
        continue
      fi
      if [[ "$line" == \#* ]]; then
        current_meta+="${line#\# }"$'\n'
        continue
      fi
      current_request="$line"
      state="headers"
      ;;
    headers)
      if [[ -z "$line" ]]; then
        state="body"
        continue
      fi
      current_headers+="$line"$'\n'
      ;;
    body)
      current_body+="$line"$'\n'
      ;;
  esac
done <"$HTTP_FILE"

run_case "$current_title" "$current_meta" "$current_request" "$current_headers" "$current_body"

echo "Summary: PASS=$PASS_COUNT FAIL=$FAIL_COUNT SKIP=$SKIP_COUNT"

if [[ $FAIL_COUNT -gt 0 ]]; then
  exit 1
fi

exit 0
