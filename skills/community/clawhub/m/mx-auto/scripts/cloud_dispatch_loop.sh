#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  cloud_dispatch_loop.sh --payload-json <json> --base-url <url> --dispatch-path <path> --status-path-template <template> --device-id <id> --token <token> [options]

Options:
  --target <trigger.execute>
  --payload-json <json>          Trigger payload JSON
  --command-id <id>              Optional explicit command id
  --base-url <url>               Cloud API base URL
  --dispatch-path <path>         Dispatch path or full URL
  --status-path-template <path>  Query path template containing {commandId}
  --list-path <path>             Optional fallback list path
  --device-id <id>               Target cloud device id
  --token <token>                Bearer token
  --wait <true|false>            default: true
  --lease-ttl-ms <n>             default: 60000
  --poll-sec <n>                 default: 3
  --timeout-sec <n>              default: 1200
  -h, --help
EOF
}

log() {
  printf '[mx-auto] %s\n' "$*" >&2
}

emit_error_json() {
  local error_message="$1"
  local command_id="${2:-}"
  local target="${3:-}"
  local status="${4:-error}"
  node -e '
const out = {
  ok: false,
  commandId: process.argv[1] || "",
  target: process.argv[2] || "",
  status: process.argv[3] || "error",
  resultType: "",
  result: null,
  taskUpdates: [],
  error: process.argv[4] || "Unknown dispatch error",
};
process.stdout.write(JSON.stringify(out, null, 2) + "\n");
' "$command_id" "$target" "$status" "$error_message"
}

die() {
  emit_error_json "$1" "${2:-}" "${3:-}" "${4:-error}"
  exit 1
}

require_bin() {
  local name="$1"
  command -v "$name" >/dev/null 2>&1 || die "missing required binary: $name"
}

join_url() {
  node -e '
const base = String(process.argv[1] || "").trim().replace(/\/+$/, "");
const path = String(process.argv[2] || "").trim();
if (!path) process.stdout.write(base);
else if (/^https?:\/\//i.test(path)) process.stdout.write(path);
else process.stdout.write(`${base}${path.startsWith("/") ? path : `/${path}`}`);
' "$1" "$2"
}

expand_path_template() {
  node -e '
const template = String(process.argv[1] || "");
const values = {
  commandId: encodeURIComponent(String(process.argv[2] || "")),
  deviceId: encodeURIComponent(String(process.argv[3] || "")),
  target: encodeURIComponent(String(process.argv[4] || "")),
};
let out = template;
for (const [key, value] of Object.entries(values)) {
  out = out.replaceAll(`{${key}}`, value);
  out = out.replaceAll(`:${key}`, value);
  out = out.replaceAll(`$${key}`, value);
}
process.stdout.write(out);
' "$1" "$2" "$3" "$4"
}

generate_command_id() {
  node -e 'process.stdout.write(`mxa_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`);'
}

normalize_bool_or_empty() {
  local raw="${1:-}"
  local lower
  if [[ -z "$raw" ]]; then
    echo ""
    return 0
  fi
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    true|1|yes|y|on) echo "true" ;;
    false|0|no|n|off) echo "false" ;;
    *) die "invalid boolean value: $raw" ;;
  esac
}

build_command_json() {
  node -e '
const target = process.argv[1];
const payload = JSON.parse(process.argv[2]);
const wait = process.argv[3] === "true";
const leaseTtlMs = Number(process.argv[4]);
process.stdout.write(JSON.stringify({ target, payload, wait, leaseTtlMs }));
' "$1" "$2" "$3" "$4"
}

build_envelope_json() {
  node -e '
const deviceId = process.argv[1];
const command = JSON.parse(process.argv[2]);
const commandId = process.argv[3];
process.stdout.write(JSON.stringify({ deviceId, command, commandId }));
' "$1" "$2" "$3"
}

validate_target_payload() {
  node -e '
const target = process.argv[1];
const payload = JSON.parse(process.argv[2]);
if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
  console.error("payload must be a JSON object");
  process.exit(1);
}
if (target !== "trigger.execute") {
  console.error("target must be trigger.execute");
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

extract_dispatch_command_id() {
  local json="$1"
  node -e '
const data = JSON.parse(process.argv[1]);
const candidates = [
  data.commandId,
  data.command_id,
  data.id,
  data.data?.commandId,
  data.data?.command_id,
  data.data?.id,
  data.command?.commandId,
  data.command?.command_id,
  data.command?.id,
];
const first = candidates.find((value) => typeof value === "string" && value.trim());
if (first) process.stdout.write(first.trim());
' "$json"
}

extract_snapshot() {
  local json="$1"
  local command_id="$2"
  node -e '
const payload = JSON.parse(process.argv[1]);
const requestedId = String(process.argv[2] || "").trim();

const asObjects = (root) => {
  const out = [];
  if (!root) return out;
  if (Array.isArray(root)) {
    for (const item of root) {
      if (item && typeof item === "object" && !Array.isArray(item)) out.push(item);
    }
    return out;
  }
  if (typeof root === "object") out.push(root);
  return out;
};

const roots = [
  payload,
  payload.data,
  payload.command,
  payload.item,
  payload.result,
  payload.data?.command,
  payload.data?.result,
  payload.commands,
  payload.data?.commands,
  payload.items,
  payload.list,
  payload.data?.items,
  payload.data?.list,
];

let objects = [];
for (const root of roots) objects = objects.concat(asObjects(root));

const getCommandId = (entry) => [
  entry.commandId,
  entry.command_id,
  entry.id,
  entry.command?.commandId,
  entry.command?.command_id,
  entry.command?.id,
  entry.data?.commandId,
  entry.data?.command_id,
  entry.data?.id,
].find((value) => typeof value === "string" && value.trim()) || "";

let match = null;
if (requestedId) {
  match = objects.find((entry) => getCommandId(entry) === requestedId) || null;
}
if (!match) {
  match = objects.find((entry) => {
    const status = [
      entry.status,
      entry.state,
      entry.stage,
      entry.commandStatus,
      entry.command?.status,
      entry.data?.status,
    ].find((value) => typeof value === "string" && value.trim());
    return Boolean(status) || Boolean(getCommandId(entry));
  }) || null;
}

if (!match) {
  process.stdout.write(JSON.stringify({ found: false }));
  process.exit(0);
}

const status = [
  match.status,
  match.state,
  match.stage,
  match.commandStatus,
  match.command?.status,
  match.data?.status,
].find((value) => typeof value === "string" && value.trim()) || "";

const target = [
  match.target,
  match.commandTarget,
  match.command?.target,
  match.data?.target,
].find((value) => typeof value === "string" && value.trim()) || "";

const resultType = [
  match.resultType,
  match.commandResultType,
  match.result?.resultType,
  match.data?.resultType,
].find((value) => typeof value === "string" && value.trim()) || "";

const taskUpdates = [
  match.taskUpdates,
  match.task_updates,
  match.updates,
  match.data?.taskUpdates,
  match.data?.task_updates,
].find((value) => Array.isArray(value)) || [];

const result = [
  match.result,
  match.commandResult,
  match.data?.result,
].find((value) => value !== undefined) ?? null;

const explicitOk = [
  match.ok,
  match.data?.ok,
  match.result?.ok,
].find((value) => typeof value === "boolean");

const error = [
  match.error,
  match.message && explicitOk === false ? match.message : undefined,
  match.result?.error,
  match.data?.error,
  match.data?.message && explicitOk === false ? match.data?.message : undefined,
].find((value) => typeof value === "string" && value.trim()) || "";

process.stdout.write(JSON.stringify({
  found: true,
  commandId: getCommandId(match) || requestedId,
  target,
  status,
  resultType,
  result,
  taskUpdates,
  error,
  ok: explicitOk,
}));
' "$json" "$command_id"
}

snapshot_is_terminal() {
  local snapshot_json="$1"
  node -e '
const snapshot = JSON.parse(process.argv[1]);
if (snapshot.ok === false) process.exit(0);
const status = String(snapshot.status || "").trim().toLowerCase();
const terminal = new Set(["completed", "complete", "succeeded", "success", "ok", "failed", "error", "cancelled", "canceled", "timeout", "timed_out", "rejected"]);
process.exit(terminal.has(status) ? 0 : 1);
' "$snapshot_json"
}

snapshot_is_success() {
  local snapshot_json="$1"
  node -e '
const snapshot = JSON.parse(process.argv[1]);
if (snapshot.ok === false) process.exit(1);
const status = String(snapshot.status || "").trim().toLowerCase();
const success = new Set(["completed", "complete", "succeeded", "success", "ok"]);
process.exit(success.has(status) ? 0 : 1);
' "$snapshot_json"
}

emit_summary_from_snapshot() {
  local snapshot_json="$1"
  node -e '
const snapshot = JSON.parse(process.argv[1]);
const status = String(snapshot.status || "").trim().toLowerCase();
const success = new Set(["completed", "complete", "succeeded", "success", "ok"]);
const out = {
  ok: snapshot.ok === false ? false : success.has(status),
  commandId: snapshot.commandId || "",
  target: snapshot.target || "",
  status: snapshot.status || "",
  resultType: snapshot.resultType || "",
  result: snapshot.result ?? null,
  taskUpdates: Array.isArray(snapshot.taskUpdates) ? snapshot.taskUpdates : [],
  error: snapshot.error || "",
};
process.stdout.write(JSON.stringify(out, null, 2) + "\n");
' "$snapshot_json"
}

TARGET="trigger.execute"
PAYLOAD_JSON=""
COMMAND_ID=""
BASE_URL=""
DISPATCH_PATH=""
STATUS_PATH_TEMPLATE=""
LIST_PATH=""
DEVICE_ID=""
TOKEN=""
WAIT="true"
LEASE_TTL_MS="60000"
POLL_SEC="3"
TIMEOUT_SEC="1200"

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
    --command-id)
      COMMAND_ID="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --dispatch-path)
      DISPATCH_PATH="${2:-}"
      shift 2
      ;;
    --status-path-template)
      STATUS_PATH_TEMPLATE="${2:-}"
      shift 2
      ;;
    --list-path)
      LIST_PATH="${2:-}"
      shift 2
      ;;
    --device-id)
      DEVICE_ID="${2:-}"
      shift 2
      ;;
    --token)
      TOKEN="${2:-}"
      shift 2
      ;;
    --wait)
      WAIT="${2:-}"
      shift 2
      ;;
    --lease-ttl-ms)
      LEASE_TTL_MS="${2:-}"
      shift 2
      ;;
    --poll-sec)
      POLL_SEC="${2:-3}"
      shift 2
      ;;
    --timeout-sec)
      TIMEOUT_SEC="${2:-1200}"
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

require_bin curl
require_bin node

[[ -n "$BASE_URL" ]] || die "--base-url is required"
[[ -n "$DISPATCH_PATH" ]] || die "--dispatch-path is required"
[[ -n "$STATUS_PATH_TEMPLATE" ]] || die "--status-path-template is required"
[[ -n "$DEVICE_ID" ]] || die "--device-id is required"
[[ -n "$TOKEN" ]] || die "--token is required"
[[ -n "$TARGET" ]] || die "--target is required"
[[ -n "$PAYLOAD_JSON" ]] || die "--payload-json is required"
[[ "$POLL_SEC" =~ ^[0-9]+$ && "$POLL_SEC" != "0" ]] || die "--poll-sec must be a positive integer"
[[ "$TIMEOUT_SEC" =~ ^[0-9]+$ && "$TIMEOUT_SEC" != "0" ]] || die "--timeout-sec must be a positive integer"
[[ "$LEASE_TTL_MS" =~ ^[0-9]+$ && "$LEASE_TTL_MS" != "0" ]] || die "--lease-ttl-ms must be a positive integer"
WAIT="$(normalize_bool_or_empty "$WAIT")"

node -e 'JSON.parse(process.argv[1]);' "$PAYLOAD_JSON" >/dev/null 2>&1 || die "--payload-json is not valid JSON" "" "$TARGET"
validation_output="$(validate_target_payload "$TARGET" "$PAYLOAD_JSON" 2>&1)" || die "${validation_output:-invalid payload for target=$TARGET}" "" "$TARGET"
COMMAND_JSON="$(build_command_json "$TARGET" "$PAYLOAD_JSON" "$WAIT" "$LEASE_TTL_MS")"

if [[ -z "$COMMAND_ID" ]]; then
  COMMAND_ID="$(generate_command_id)"
fi

ENVELOPE_JSON="$(build_envelope_json "$DEVICE_ID" "$COMMAND_JSON" "$COMMAND_ID")"
DISPATCH_URL="$(join_url "$BASE_URL" "$DISPATCH_PATH")"
log "dispatching target=$TARGET commandId=$COMMAND_ID"

dispatch_raw="$(curl -sS -w $'\n%{http_code}' -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "$ENVELOPE_JSON" \
  "$DISPATCH_URL" || true)"

dispatch_http_code="${dispatch_raw##*$'\n'}"
dispatch_body="${dispatch_raw%$'\n'*}"

if [[ -z "$dispatch_http_code" || "$dispatch_http_code" == "000" ]]; then
  die "dispatch request failed before receiving an HTTP response" "$COMMAND_ID" "$TARGET"
fi

node -e 'JSON.parse(process.argv[1]);' "$dispatch_body" >/dev/null 2>&1 || die "dispatch response is not valid JSON" "$COMMAND_ID" "$TARGET"

if [[ "$dispatch_http_code" != 2* ]]; then
  error_message="$(node -e '
const data = JSON.parse(process.argv[1]);
const message = data.message || data.error || `dispatch failed with HTTP ${process.argv[2]}`;
process.stdout.write(String(message));
' "$dispatch_body" "$dispatch_http_code")"
  die "$error_message" "$COMMAND_ID" "$TARGET" "dispatch_failed"
fi

REMOTE_COMMAND_ID="$(extract_dispatch_command_id "$dispatch_body")"
if [[ -z "$REMOTE_COMMAND_ID" ]]; then
  REMOTE_COMMAND_ID="$COMMAND_ID"
fi

INITIAL_SNAPSHOT="$(extract_snapshot "$dispatch_body" "$REMOTE_COMMAND_ID")"

if [[ "$WAIT" == "false" ]]; then
  if node -e 'const s=JSON.parse(process.argv[1]); process.exit(s.found ? 0 : 1);' "$INITIAL_SNAPSHOT"; then
    emit_summary_from_snapshot "$INITIAL_SNAPSHOT"
  else
    node -e '
const out = {
  ok: true,
  commandId: process.argv[1],
  target: process.argv[2],
  status: "dispatched",
  resultType: "",
  result: null,
  taskUpdates: [],
  error: "",
};
process.stdout.write(JSON.stringify(out, null, 2) + "\n");
' "$REMOTE_COMMAND_ID" "$TARGET"
  fi
  exit 0
fi

if node -e 'const s=JSON.parse(process.argv[1]); process.exit(s.found ? 0 : 1);' "$INITIAL_SNAPSHOT" && snapshot_is_terminal "$INITIAL_SNAPSHOT"; then
  emit_summary_from_snapshot "$INITIAL_SNAPSHOT"
  snapshot_is_success "$INITIAL_SNAPSHOT"
  exit $?
fi

START_TS="$(date +%s)"

while :; do
  STATUS_PATH="$(expand_path_template "$STATUS_PATH_TEMPLATE" "$REMOTE_COMMAND_ID" "$DEVICE_ID" "$TARGET")"
  STATUS_URL="$(join_url "$BASE_URL" "$STATUS_PATH")"

  status_raw="$(curl -sS -w $'\n%{http_code}' \
    -H "Authorization: Bearer $TOKEN" \
    "$STATUS_URL" || true)"
  status_http_code="${status_raw##*$'\n'}"
  status_body="${status_raw%$'\n'*}"

  SNAPSHOT_JSON='{"found":false}'
  if [[ "$status_http_code" == 2* ]]; then
    if node -e 'JSON.parse(process.argv[1]);' "$status_body" >/dev/null 2>&1; then
      SNAPSHOT_JSON="$(extract_snapshot "$status_body" "$REMOTE_COMMAND_ID")"
    else
      die "status query returned invalid JSON" "$REMOTE_COMMAND_ID" "$TARGET"
    fi
  elif [[ "$status_http_code" != "404" && "$status_http_code" != "000" && -n "$status_http_code" ]]; then
    die "status query failed with HTTP $status_http_code" "$REMOTE_COMMAND_ID" "$TARGET"
  fi

  FOUND="$(node -e 'const s=JSON.parse(process.argv[1]); process.stdout.write(s.found ? "true" : "false");' "$SNAPSHOT_JSON")"
  if [[ "$FOUND" != "true" && -n "$LIST_PATH" ]]; then
    LIST_QUERY_PATH="$(expand_path_template "$LIST_PATH" "$REMOTE_COMMAND_ID" "$DEVICE_ID" "$TARGET")"
    LIST_URL="$(join_url "$BASE_URL" "$LIST_QUERY_PATH")"
    list_raw="$(curl -sS -w $'\n%{http_code}' \
      -H "Authorization: Bearer $TOKEN" \
      "$LIST_URL" || true)"
    list_http_code="${list_raw##*$'\n'}"
    list_body="${list_raw%$'\n'*}"
    if [[ "$list_http_code" == 2* ]]; then
      if node -e 'JSON.parse(process.argv[1]);' "$list_body" >/dev/null 2>&1; then
        SNAPSHOT_JSON="$(extract_snapshot "$list_body" "$REMOTE_COMMAND_ID")"
        FOUND="$(node -e 'const s=JSON.parse(process.argv[1]); process.stdout.write(s.found ? "true" : "false");' "$SNAPSHOT_JSON")"
      else
        die "list query returned invalid JSON" "$REMOTE_COMMAND_ID" "$TARGET"
      fi
    elif [[ "$list_http_code" != "404" && "$list_http_code" != "000" && -n "$list_http_code" ]]; then
      die "list query failed with HTTP $list_http_code" "$REMOTE_COMMAND_ID" "$TARGET"
    fi
  fi

  if [[ "$FOUND" == "true" ]] && snapshot_is_terminal "$SNAPSHOT_JSON"; then
    emit_summary_from_snapshot "$SNAPSHOT_JSON"
    snapshot_is_success "$SNAPSHOT_JSON"
    exit $?
  fi

  NOW_TS="$(date +%s)"
  if (( NOW_TS - START_TS >= TIMEOUT_SEC )); then
    die "timed out waiting for cloud command completion" "$REMOTE_COMMAND_ID" "$TARGET" "timeout"
  fi

  sleep "$POLL_SEC"
done
