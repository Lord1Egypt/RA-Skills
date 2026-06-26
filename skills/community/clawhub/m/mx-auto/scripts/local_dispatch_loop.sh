#!/usr/bin/env bash
set -euo pipefail

DEFAULT_RUNTIME_BASE_URLS=(
  "http://127.0.0.1:8877"
  "http://localhost:8877"
  "http://127.0.0.1:8878"
  "http://localhost:8878"
  "http://127.0.0.1:8879"
  "http://localhost:8879"
)

usage() {
  cat <<'EOF'
Usage:
  local_dispatch_loop.sh --payload-json <json> [options]

Options:
  --target <trigger.execute|script.run>
  --payload-json <json>    Payload object for target
  --base-url <url>         Runtime base URL
  --app-home <path>        Optional App home for token discovery
  --wait <true|false>      default: true
  --lease-ttl-ms <n>       default: 60000
  -h, --help
EOF
}

emit_error_json() {
  local message="$1"
  local status="${2:-error}"
  node -e '
const out = {
  ok: false,
  status: process.argv[2] || "error",
  message: process.argv[1] || "local dispatch failed",
};
process.stdout.write(JSON.stringify(out, null, 2) + "\n");
' "$message" "$status"
}

die() {
  emit_error_json "$1" "${2:-error}"
  exit 1
}

normalize_bool() {
  local raw="${1:-}"
  local lower
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    true|1|yes|y|on) printf '%s\n' "true" ;;
    false|0|no|n|off) printf '%s\n' "false" ;;
    *) die "invalid boolean value: $raw" ;;
  esac
}

join_url() {
  node -e '
const base = String(process.argv[1] || "").trim().replace(/\/+$/, "");
const path = String(process.argv[2] || "").trim();
process.stdout.write(`${base}${path.startsWith("/") ? path : `/${path}`}`);
' "$1" "$2"
}

discover_runtime_admin_token() {
  local app_home="${1:-}"
  local env_token="${MX_APP_RUNTIME_ADMIN_TOKEN:-${RPA_RUNTIME_ADMIN_TOKEN:-}}"
  if [[ -n "$env_token" ]]; then
    printf '%s\n' "$env_token"
    return 0
  fi

  local effective_app_home="${app_home:-${RPA_APP_HOME:-}}"
  if [[ -z "$effective_app_home" ]]; then
    return 0
  fi

  node -e '
const fs = require("node:fs");
const path = require("node:path");
const file = path.join(process.argv[1], "runtime", "admin-token.json");
try {
  const raw = JSON.parse(fs.readFileSync(file, "utf8"));
  const token = typeof raw?.token === "string" ? raw.token.trim() : "";
  if (token) process.stdout.write(token);
} catch {}
' "$effective_app_home"
}

discover_base_url() {
  local preferred="${1:-}"
  if [[ -n "$preferred" ]]; then
    printf '%s\n' "$preferred"
    return 0
  fi

  local env_url="${MX_APP_RUNTIME_BASE_URL:-${RPA_RUNTIME_BASE_URL:-}}"
  if [[ -n "$env_url" ]]; then
    printf '%s\n' "$env_url"
    return 0
  fi

  local candidate
  for candidate in "${DEFAULT_RUNTIME_BASE_URLS[@]}"; do
    if curl -fsS --max-time 2 "$candidate/health" >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  printf '%s\n' "${DEFAULT_RUNTIME_BASE_URLS[0]}"
}

validate_payload() {
  node -e '
const target = process.argv[2];
const payload = JSON.parse(process.argv[1]);
if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
  console.error("payload must be a JSON object");
  process.exit(1);
}
if (target === "script.run") {
  const name = typeof payload.name === "string" ? payload.name.trim() : "";
  if (!name) {
    console.error("script.run requires payload.name");
    process.exit(1);
  }
  const input = payload.inputOverrides ?? payload.input;
  if (input !== undefined && (!input || typeof input !== "object" || Array.isArray(input))) {
    console.error("script input must be a JSON object when present");
    process.exit(1);
  }
  process.exit(0);
}
if (target !== "trigger.execute") {
  console.error("target must be trigger.execute or script.run");
  process.exit(1);
}
const triggerId = typeof payload.triggerId === "string" ? payload.triggerId.trim() : "";
if (!triggerId) {
  console.error("trigger.execute requires payload.triggerId");
  process.exit(1);
}
if (payload.input !== undefined && (!payload.input || typeof payload.input !== "object" || Array.isArray(payload.input))) {
  console.error("payload.input must be a JSON object when present");
  process.exit(1);
}
' "$1" "$2"
}

TARGET="trigger.execute"
PAYLOAD_JSON=""
BASE_URL=""
APP_HOME=""
WAIT_VALUE="true"
LEASE_TTL_MS="60000"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --payload-json)
      PAYLOAD_JSON="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --app-home)
      APP_HOME="${2:-}"
      shift 2
      ;;
    --wait)
      WAIT_VALUE="${2:-true}"
      shift 2
      ;;
    --lease-ttl-ms)
      LEASE_TTL_MS="${2:-60000}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown arg: $1"
      ;;
  esac
done

case "$TARGET" in
  trigger.execute|script.run) ;;
  *) die "--target must be trigger.execute or script.run" ;;
esac
[[ -n "$PAYLOAD_JSON" ]] || die "--payload-json is required"
WAIT_VALUE="$(normalize_bool "$WAIT_VALUE")"
[[ "$LEASE_TTL_MS" =~ ^[0-9]+$ && "$LEASE_TTL_MS" != "0" ]] || die "--lease-ttl-ms must be a positive integer"
node -e 'JSON.parse(process.argv[1]);' "$PAYLOAD_JSON" >/dev/null 2>&1 || die "--payload-json is not valid JSON"
validation_output="$(validate_payload "$PAYLOAD_JSON" "$TARGET" 2>&1)" || die "${validation_output:-invalid payload}" "invalid_payload"

TOKEN="$(discover_runtime_admin_token "$APP_HOME")"
[[ -n "$TOKEN" ]] || die "runtime admin token is missing; set MX_APP_RUNTIME_ADMIN_TOKEN or point --app-home to a Runtime state dir" "unauthorized"

BASE_URL="$(discover_base_url "$BASE_URL")"
REQUEST_JSON="$(node -e '
const target = process.argv[1];
const payload = JSON.parse(process.argv[2]);
const wait = process.argv[3] === "true";
const leaseTtlMs = Number(process.argv[4]);
process.stdout.write(JSON.stringify({ target, payload, wait, leaseTtlMs }));
' "$TARGET" "$PAYLOAD_JSON" "$WAIT_VALUE" "$LEASE_TTL_MS")"

SEND_URL="$(join_url "$BASE_URL" "/local/commands/send")"

raw="$(curl -sS -w $'\n%{http_code}' -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "$REQUEST_JSON" \
  "$SEND_URL" || true)"

http_code="${raw##*$'\n'}"
body="${raw%$'\n'*}"

if [[ -z "$http_code" || "$http_code" == "000" ]]; then
  die "runtime is not available at $BASE_URL" "runtime_unavailable"
fi

node -e 'JSON.parse(process.argv[1]);' "$body" >/dev/null 2>&1 || die "runtime returned invalid JSON" "invalid_json"

node -e '
const data = JSON.parse(process.argv[1]);
process.stdout.write(JSON.stringify(data, null, 2) + "\n");
' "$body"

[[ "$http_code" == 2* ]] || exit 1
