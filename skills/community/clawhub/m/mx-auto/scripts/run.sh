#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PREFERENCE_SCRIPT="$SKILL_DIR/scripts/export_preference.sh"
PREFLIGHT_SCRIPT="$SKILL_DIR/scripts/preflight_check.sh"
LOCAL_LOOP_SCRIPT="$SKILL_DIR/scripts/local_dispatch_loop.sh"
CLOUD_LOOP_SCRIPT="$SKILL_DIR/scripts/cloud_dispatch_loop.sh"
BROWSER_SANDBOX_SCRIPT="$SKILL_DIR/scripts/browser_sandbox_bridge.sh"
SCRIPT_CATALOG_SCRIPT="$SKILL_DIR/scripts/script_catalog.sh"
DEFAULT_RUNTIME_BASE_URLS=(
  "http://127.0.0.1:8877"
  "http://localhost:8877"
  "http://127.0.0.1:8878"
  "http://localhost:8878"
  "http://127.0.0.1:8879"
  "http://localhost:8879"
)

CONNECTION_MODE=""
TRIGGER_ID=""
TRIGGER_NAME=""
INPUT_JSON=""
LOCAL_BASE_URL=""
APP_HOME=""
CLOUD_BASE_URL=""
DISPATCH_PATH=""
STATUS_PATH_TEMPLATE=""
LIST_PATH=""
DEVICE_ID=""
TOKEN=""
WAIT_VALUE=""
LEASE_TTL_MS=""
POLL_SEC=""
TIMEOUT_SEC=""
REFRESH_TRIGGERS="false"
LIST_TRIGGERS="false"
LIST_FORMAT="text"
PREFLIGHT_SUMMARY_JSON=""

HAS_CONNECTION_MODE_ARG="false"
HAS_LOCAL_BASE_URL_ARG="false"
HAS_APP_HOME_ARG="false"
HAS_CLOUD_BASE_URL_ARG="false"
HAS_DISPATCH_PATH_ARG="false"
HAS_STATUS_PATH_TEMPLATE_ARG="false"
HAS_LIST_PATH_ARG="false"
HAS_DEVICE_ID_ARG="false"
HAS_TOKEN_ARG="false"
HAS_WAIT_ARG="false"
HAS_LEASE_TTL_MS_ARG="false"
HAS_POLL_SEC_ARG="false"
HAS_TIMEOUT_SEC_ARG="false"

usage() {
  cat <<'EOF'
Usage:
  run.sh [legacy trigger options]
  run.sh triggers list [options]
  run.sh triggers run [options]
  run.sh triggers refresh [options]
  run.sh sandbox tabs|snapshot [options]
  run.sh scripts list|show|run [options]

Options:
  --connection-mode <local|cloud>
  --list-triggers
  --list-format <text|json>
  --trigger-id <id>
  --trigger-name <name>
  --input-json <json>
  --local-base-url <url>
  --app-home <path>
  --cloud-base-url <url>
  --dispatch-path <path>
  --status-path-template <path>
  --list-path <path>
  --device-id <id>
  --token <token>
  --wait <true|false>
  --lease-ttl-ms <n>
  --poll-sec <n>
  --timeout-sec <n>
  --refresh-triggers
  --format <text|json>     Alias for --list-format in trigger list mode
  -h, --help
EOF
}

die() {
  echo "$*" >&2
  exit 1
}

minimal_local_setup_guidance() {
  cat <<'EOF' >&2
本地模式会先自动查找本地 Runtime。通常不需要手动配置。
如果自动发现失败，优先检查：
1. Runtime 是否正在本机运行
2. Runtime 的本地配置是否已准备好
3. 如果路径或端口不是默认值，再显式设置对应环境变量或运行参数
EOF
}

pref_get() {
  local key="$1"
  if [[ -f "$PREFERENCE_SCRIPT" ]]; then
    bash "$PREFERENCE_SCRIPT" get "$key" 2>/dev/null || true
  fi
}

normalize_mode() {
  local raw="${1:-}"
  if [[ -z "$raw" ]]; then
    printf '%s\n' ""
    return 0
  fi
  local lower
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    local|cloud) printf '%s\n' "$lower" ;;
    *) die "invalid connection mode: $raw" ;;
  esac
}

normalize_bool() {
  local raw="${1:-}"
  if [[ -z "$raw" ]]; then
    printf '%s\n' ""
    return 0
  fi
  local lower
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    true|1|yes|y|on) printf '%s\n' "true" ;;
    false|0|no|n|off) printf '%s\n' "false" ;;
    *) die "invalid boolean value: $raw" ;;
  esac
}

normalize_positive_integer() {
  local raw="${1:-}"
  if [[ -z "$raw" ]]; then
    printf '%s\n' ""
    return 0
  fi
  [[ "$raw" =~ ^[0-9]+$ && "$raw" != "0" ]] || die "invalid positive integer: $raw"
  printf '%s\n' "$raw"
}

resolve_default_app_home() {
  case "$(uname -s 2>/dev/null || printf unknown)" in
    Darwin)
      printf '%s\n' "${HOME}/Library/Application Support/rpa-app-executor"
      ;;
    Linux)
      printf '%s\n' "${XDG_DATA_HOME:-${HOME}/.local/share}/rpa-app-executor"
      ;;
    MINGW*|MSYS*|CYGWIN*)
      printf '%s\n' "${APPDATA:-${HOME}/AppData/Roaming}/rpa-app-executor"
      ;;
    *)
      printf '%s\n' "${HOME}/.local/share/rpa-app-executor"
      ;;
  esac
}

resolve_app_home() {
  local explicit="${1:-}"
  if [[ -n "$explicit" ]]; then
    printf '%s\n' "$explicit"
    return 0
  fi
  if [[ -n "${MX_AUTO_APP_HOME:-}" ]]; then
    printf '%s\n' "$MX_AUTO_APP_HOME"
    return 0
  fi
  if [[ -n "${RPA_APP_HOME:-}" ]]; then
    printf '%s\n' "$RPA_APP_HOME"
    return 0
  fi

  local stored
  stored="$(pref_get defaultAppHome)"
  if [[ -n "$stored" ]]; then
    printf '%s\n' "$stored"
    return 0
  fi

  resolve_default_app_home
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

discover_local_base_url() {
  local preferred="${1:-}"
  local candidates=()

  if [[ -n "$preferred" ]]; then
    candidates+=("$preferred")
  fi
  if [[ -n "${MX_APP_RUNTIME_BASE_URL:-}" ]]; then
    candidates+=("$MX_APP_RUNTIME_BASE_URL")
  fi
  if [[ -n "${RPA_RUNTIME_BASE_URL:-}" ]]; then
    candidates+=("$RPA_RUNTIME_BASE_URL")
  fi
  if [[ -n "$(pref_get defaultLocalBaseUrl)" ]]; then
    candidates+=("$(pref_get defaultLocalBaseUrl)")
  fi
  candidates+=("${DEFAULT_RUNTIME_BASE_URLS[@]}")

  local candidate
  for candidate in "${candidates[@]}"; do
    [[ -n "$candidate" ]] || continue
    if curl -fsS --max-time 2 "$candidate/health" >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  local fallback="${preferred:-${MX_APP_RUNTIME_BASE_URL:-${RPA_RUNTIME_BASE_URL:-$(pref_get defaultLocalBaseUrl)}}}"
  if [[ -n "$fallback" ]]; then
    printf '%s\n' "$fallback"
  else
    printf '%s\n' "${DEFAULT_RUNTIME_BASE_URLS[0]}"
  fi
}

validate_input_json() {
  local raw="${1:-}"
  if [[ -z "$raw" ]]; then
    printf '%s\n' ""
    return 0
  fi
  node -e '
const value = JSON.parse(process.argv[1]);
if (!value || typeof value !== "object" || Array.isArray(value)) {
  console.error("--input-json must be a JSON object");
  process.exit(1);
}
process.stdout.write(JSON.stringify(value));
' "$raw"
}

fetch_trigger_services() {
  local base_url="$1"
  local token="$2"
  curl -fsS \
    -H "Authorization: Bearer $token" \
    "$base_url/trigger-services"
}

persist_trigger_snapshot() {
  local raw_json="$1"
  local source_mode="$2"

  local snapshot_json
  snapshot_json="$(node -e '
const payload = JSON.parse(process.argv[1]);
const sourceMode = process.argv[2];
const services = Array.isArray(payload.services) ? payload.services : [];
const filtered = services
  .filter((service) => service && service.callable === true && service.available === true)
  .map((service) => ({
    id: typeof service.id === "string" ? service.id : "",
    name: typeof service.name === "string" ? service.name : "",
    summary: typeof service.summary === "string" ? service.summary : "",
    status: typeof service.status === "string" ? service.status : "",
    callable: service.callable === true,
    available: service.available === true,
    lastRunAt: typeof service.lastRunAt === "string" ? service.lastRunAt : "",
    updatedAt: typeof service.updatedAt === "string" ? service.updatedAt : "",
  }))
  .filter((service) => service.id && service.name);
process.stdout.write(JSON.stringify({
  loadedAt: new Date().toISOString(),
  sourceMode,
  registryPath: typeof payload?.registry?.path === "string" ? payload.registry.path : "",
  services: filtered,
}));
' "$raw_json" "$source_mode")"
  bash "$PREFERENCE_SCRIPT" set-trigger-snapshot "$snapshot_json" >/dev/null
}

resolve_trigger_id_from_snapshot() {
  local trigger_name="$1"
  local snapshot_json
  snapshot_json="$(bash "$PREFERENCE_SCRIPT" get-trigger-snapshot 2>/dev/null || true)"
  [[ -n "$snapshot_json" ]] || return 1

  node -e '
const snapshot = JSON.parse(process.argv[1]);
const triggerName = process.argv[2];
const services = Array.isArray(snapshot.services) ? snapshot.services : [];
const matches = services.filter((service) => typeof service?.name === "string" && service.name === triggerName);
if (matches.length !== 1) process.exit(1);
process.stdout.write(String(matches[0].id || ""));
' "$snapshot_json" "$trigger_name"
}

list_cached_trigger_names() {
  local snapshot_json
  snapshot_json="$(bash "$PREFERENCE_SCRIPT" get-trigger-snapshot 2>/dev/null || true)"
  [[ -n "$snapshot_json" ]] || return 0

  node -e '
const snapshot = JSON.parse(process.argv[1]);
const services = Array.isArray(snapshot.services) ? snapshot.services : [];
const names = services
  .map((service) => typeof service?.name === "string" ? service.name.trim() : "")
  .filter(Boolean);
process.stdout.write(names.join(", "));
' "$snapshot_json"
}

build_payload_json() {
  local trigger_id="$1"
  local input_json="$2"
  node -e '
const triggerId = process.argv[1];
const inputRaw = process.argv[2];
const payload = { triggerId };
if (inputRaw) payload.input = JSON.parse(inputRaw);
process.stdout.write(JSON.stringify(payload));
' "$trigger_id" "$input_json"
}

route_subcommand() {
  local command="${1:-}"
  local subcommand="${2:-}"

  case "$command" in
    sandbox)
      shift 1
      exec bash "$BROWSER_SANDBOX_SCRIPT" "$@"
      ;;
    scripts)
      shift 1
      exec bash "$SCRIPT_CATALOG_SCRIPT" "$@"
      ;;
    triggers)
      case "$subcommand" in
        list)
          shift 2
          set -- --list-triggers "$@"
          ;;
        run)
          shift 2
          ;;
        refresh)
          shift 2
          set -- --refresh-triggers "$@"
          ;;
        ""|-h|--help)
          usage
          exit 0
          ;;
        *)
          die "unknown triggers subcommand: $subcommand"
          ;;
      esac
      ;;
  esac

  ROUTED_ARGS=("$@")
}

emit_refresh_only_summary() {
  local snapshot_json
  snapshot_json="$(bash "$PREFERENCE_SCRIPT" get-trigger-snapshot 2>/dev/null || true)"
  node -e '
const snapshot = process.argv[1] ? JSON.parse(process.argv[1]) : {};
const services = Array.isArray(snapshot.services) ? snapshot.services : [];
process.stdout.write(JSON.stringify({
  ok: true,
  mode: "refresh_only",
  loadedAt: typeof snapshot.loadedAt === "string" ? snapshot.loadedAt : "",
  sourceMode: typeof snapshot.sourceMode === "string" ? snapshot.sourceMode : "",
  registryPath: typeof snapshot.registryPath === "string" ? snapshot.registryPath : "",
  triggerCount: services.length,
  triggers: services,
}, null, 2) + "\n");
' "$snapshot_json"
}

emit_trigger_list_text() {
  local snapshot_json
  snapshot_json="$(bash "$PREFERENCE_SCRIPT" get-trigger-snapshot 2>/dev/null || true)"
  local discovery_json="${PREFLIGHT_SUMMARY_JSON:-}"
  node -e '
const snapshot = process.argv[1] ? JSON.parse(process.argv[1]) : {};
const discovery = process.argv[2] ? JSON.parse(process.argv[2]) : null;
const services = Array.isArray(snapshot.services) ? snapshot.services : [];
const lowSignalPatterns = [
  /通过统一入口执行数据传输/u,
  /未选择传输方案/u,
  /统一入口/u,
  /data transfer/i,
];
const sanitizeSummary = (value) => {
  if (typeof value !== "string") return "";
  const trimmed = value.trim();
  if (!trimmed) return "";
  if (lowSignalPatterns.some((pattern) => pattern.test(trimmed))) return "";
  return trimmed;
};
const lines = [];
if (discovery?.effectiveConfig?.localBaseUrl) {
  lines.push(`已自动发现 Runtime：${discovery.effectiveConfig.localBaseUrl}`);
} else {
  lines.push("未自动发现 Runtime");
}
lines.push(`当前可用触发器（${services.length}）`);
for (const [index, service] of services.entries()) {
  lines.push(`${index + 1}. ${service.name || "未命名触发器"}`);
  lines.push(`状态：${service.status || "-"}`);
  const summary = sanitizeSummary(service.summary);
  if (summary) {
    lines.push(`摘要：${summary}`);
  }
}
process.stdout.write(lines.join("\n") + "\n");
' "$snapshot_json" "$discovery_json"
}

emit_trigger_list_json() {
  local snapshot_json
  snapshot_json="$(bash "$PREFERENCE_SCRIPT" get-trigger-snapshot 2>/dev/null || true)"
  node -e '
const snapshot = process.argv[1] ? JSON.parse(process.argv[1]) : {};
const services = Array.isArray(snapshot.services) ? snapshot.services : [];
process.stdout.write(JSON.stringify({
  ok: true,
  mode: "list_triggers",
  sourceMode: typeof snapshot.sourceMode === "string" ? snapshot.sourceMode : "local",
  loadedAt: typeof snapshot.loadedAt === "string" ? snapshot.loadedAt : "",
  registryPath: typeof snapshot.registryPath === "string" ? snapshot.registryPath : "",
  triggerCount: services.length,
  triggers: services.map((service) => ({
    id: service.id || "",
    name: service.name || "",
    status: service.status || "",
    summary: service.summary || "",
    callable: service.callable === true,
    available: service.available === true,
    lastRunAt: service.lastRunAt || "",
    updatedAt: service.updatedAt || "",
  })),
}, null, 2) + "\n");
' "$snapshot_json"
}

ROUTED_ARGS=("$@")
route_subcommand "$@"
set -- "${ROUTED_ARGS[@]}"

run_preflight() {
  local cmd=(
    bash "$PREFLIGHT_SCRIPT"
    --connection-mode "$CONNECTION_MODE"
    --wait "$WAIT_VALUE"
    --lease-ttl-ms "$LEASE_TTL_MS"
    --poll-sec "$POLL_SEC"
    --timeout-sec "$TIMEOUT_SEC"
    --format json
  )

  [[ -n "$LOCAL_BASE_URL" ]] && cmd+=(--local-base-url "$LOCAL_BASE_URL")
  [[ -n "$APP_HOME" ]] && cmd+=(--app-home "$APP_HOME")
  [[ -n "$CLOUD_BASE_URL" ]] && cmd+=(--cloud-base-url "$CLOUD_BASE_URL")
  [[ -n "$DISPATCH_PATH" ]] && cmd+=(--dispatch-path "$DISPATCH_PATH")
  [[ -n "$STATUS_PATH_TEMPLATE" ]] && cmd+=(--status-path-template "$STATUS_PATH_TEMPLATE")
  [[ -n "$LIST_PATH" ]] && cmd+=(--list-path "$LIST_PATH")
  [[ -n "$DEVICE_ID" ]] && cmd+=(--device-id "$DEVICE_ID")
  [[ -n "$TOKEN" ]] && cmd+=(--token "$TOKEN")
  [[ "$CONNECTION_MODE" == "local" ]] && cmd+=(--probe-local)

  local output
if ! output="$("${cmd[@]}" 2>&1)"; then
    if node -e 'JSON.parse(process.argv[1]);' "$output" >/dev/null 2>&1; then
      node -e '
const summary = JSON.parse(process.argv[1]);
const missing = Array.isArray(summary.missingDefaults) ? summary.missingDefaults : [];
const probe = summary?.checks?.localProbe;
const httpCode = String(probe?.httpCode || "");
if (missing.includes("runtimeAdminToken")) {
  console.error("本地 Runtime 当前缺少可用鉴权或本地配置未就绪，无法自动完成本地模式。");
} else if (httpCode === "401") {
  console.error("本地 Runtime 鉴权失败，请检查本地 Runtime 权限或本地配置。");
} else if (probe && probe.attempted === true && probe.reachable !== true) {
  console.error("本地 Runtime 当前不可达，请先确认 Runtime 已启动。");
} else {
  console.error("mx-auto 预检查失败。");
}
' "$output" >&2
      minimal_local_setup_guidance
    else
      printf '%s\n' "$output" >&2
    fi
    exit 1
  fi
  PREFLIGHT_SUMMARY_JSON="$output"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --connection-mode)
      CONNECTION_MODE="${2:-}"
      HAS_CONNECTION_MODE_ARG="true"
      shift 2
      ;;
    --trigger-id)
      TRIGGER_ID="${2:-}"
      shift 2
      ;;
    --list-triggers)
      LIST_TRIGGERS="true"
      shift 1
      ;;
    --list-format)
      LIST_FORMAT="${2:-text}"
      shift 2
      ;;
    --format)
      LIST_FORMAT="${2:-text}"
      shift 2
      ;;
    --trigger-name)
      TRIGGER_NAME="${2:-}"
      shift 2
      ;;
    --input-json)
      INPUT_JSON="${2:-}"
      shift 2
      ;;
    --local-base-url)
      LOCAL_BASE_URL="${2:-}"
      HAS_LOCAL_BASE_URL_ARG="true"
      shift 2
      ;;
    --app-home)
      APP_HOME="${2:-}"
      HAS_APP_HOME_ARG="true"
      shift 2
      ;;
    --cloud-base-url)
      CLOUD_BASE_URL="${2:-}"
      HAS_CLOUD_BASE_URL_ARG="true"
      shift 2
      ;;
    --dispatch-path)
      DISPATCH_PATH="${2:-}"
      HAS_DISPATCH_PATH_ARG="true"
      shift 2
      ;;
    --status-path-template)
      STATUS_PATH_TEMPLATE="${2:-}"
      HAS_STATUS_PATH_TEMPLATE_ARG="true"
      shift 2
      ;;
    --list-path)
      LIST_PATH="${2:-}"
      HAS_LIST_PATH_ARG="true"
      shift 2
      ;;
    --device-id)
      DEVICE_ID="${2:-}"
      HAS_DEVICE_ID_ARG="true"
      shift 2
      ;;
    --token)
      TOKEN="${2:-}"
      HAS_TOKEN_ARG="true"
      shift 2
      ;;
    --wait)
      WAIT_VALUE="${2:-}"
      HAS_WAIT_ARG="true"
      shift 2
      ;;
    --lease-ttl-ms)
      LEASE_TTL_MS="${2:-}"
      HAS_LEASE_TTL_MS_ARG="true"
      shift 2
      ;;
    --poll-sec)
      POLL_SEC="${2:-}"
      HAS_POLL_SEC_ARG="true"
      shift 2
      ;;
    --timeout-sec)
      TIMEOUT_SEC="${2:-}"
      HAS_TIMEOUT_SEC_ARG="true"
      shift 2
      ;;
    --refresh-triggers)
      REFRESH_TRIGGERS="true"
      shift 1
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

case "$LIST_FORMAT" in
  text|json) ;;
  *)
    die "invalid list format: $LIST_FORMAT (expected text or json)"
    ;;
esac

CONNECTION_MODE="$(normalize_mode "${CONNECTION_MODE:-${MX_AUTO_CONNECTION_MODE:-$(pref_get defaultConnectionMode)}}")"
[[ -n "$CONNECTION_MODE" ]] || CONNECTION_MODE="local"

if [[ "$CONNECTION_MODE" == "cloud" ]]; then
  die "cloud mode is reserved and not enabled in this version"
fi

if [[ "$HAS_LOCAL_BASE_URL_ARG" != "true" ]]; then
  LOCAL_BASE_URL="${MX_AUTO_LOCAL_BASE_URL:-${LOCAL_BASE_URL:-$(pref_get defaultLocalBaseUrl)}}"
fi
APP_HOME="$(resolve_app_home "$APP_HOME")"
if [[ "$HAS_CLOUD_BASE_URL_ARG" != "true" ]]; then
  CLOUD_BASE_URL="${MX_AUTO_CLOUD_BASE_URL:-${CLOUD_BASE_URL:-$(pref_get defaultCloudBaseUrl)}}"
fi
if [[ "$HAS_DISPATCH_PATH_ARG" != "true" ]]; then
  DISPATCH_PATH="${MX_AUTO_CLOUD_DISPATCH_PATH:-${DISPATCH_PATH:-$(pref_get defaultCloudDispatchPath)}}"
fi
if [[ "$HAS_STATUS_PATH_TEMPLATE_ARG" != "true" ]]; then
  STATUS_PATH_TEMPLATE="${MX_AUTO_CLOUD_COMMAND_STATUS_PATH_TEMPLATE:-${STATUS_PATH_TEMPLATE:-$(pref_get defaultCloudCommandStatusPathTemplate)}}"
fi
if [[ "$HAS_LIST_PATH_ARG" != "true" ]]; then
  LIST_PATH="${MX_AUTO_CLOUD_COMMAND_LIST_PATH:-${LIST_PATH:-$(pref_get defaultCloudCommandListPath)}}"
fi
if [[ "$HAS_DEVICE_ID_ARG" != "true" ]]; then
  DEVICE_ID="${MX_AUTO_CLOUD_DEVICE_ID:-${DEVICE_ID:-$(pref_get defaultCloudDeviceId)}}"
fi
if [[ "$HAS_TOKEN_ARG" != "true" ]]; then
  TOKEN="${MX_AUTO_CLOUD_TOKEN:-${TOKEN:-$(pref_get defaultCloudToken)}}"
fi

WAIT_VALUE="$(normalize_bool "${WAIT_VALUE:-${MX_AUTO_WAIT:-$(pref_get defaultWait)}}")"
LEASE_TTL_MS="$(normalize_positive_integer "${LEASE_TTL_MS:-${MX_AUTO_LEASE_TTL_MS:-$(pref_get defaultLeaseTtlMs)}}")"
POLL_SEC="$(normalize_positive_integer "${POLL_SEC:-${MX_AUTO_POLL_SEC:-$(pref_get defaultPollSec)}}")"
TIMEOUT_SEC="$(normalize_positive_integer "${TIMEOUT_SEC:-${MX_AUTO_TIMEOUT_SEC:-$(pref_get defaultTimeoutSec)}}")"
[[ -n "$WAIT_VALUE" ]] || WAIT_VALUE="true"
[[ -n "$LEASE_TTL_MS" ]] || LEASE_TTL_MS="60000"
[[ -n "$POLL_SEC" ]] || POLL_SEC="3"
[[ -n "$TIMEOUT_SEC" ]] || TIMEOUT_SEC="1200"

INPUT_JSON="$(validate_input_json "$INPUT_JSON")"
run_preflight

LOCAL_RUNTIME_TOKEN=""
EFFECTIVE_LOCAL_BASE_URL=""
if [[ "$CONNECTION_MODE" == "local" || "$REFRESH_TRIGGERS" == "true" ]]; then
  LOCAL_RUNTIME_TOKEN="$(discover_runtime_admin_token "$APP_HOME")"
  if [[ -n "$LOCAL_RUNTIME_TOKEN" ]]; then
    EFFECTIVE_LOCAL_BASE_URL="$(discover_local_base_url "$LOCAL_BASE_URL")"
  fi
fi

if [[ "$CONNECTION_MODE" == "local" || "$REFRESH_TRIGGERS" == "true" ]]; then
  if [[ -n "$LOCAL_RUNTIME_TOKEN" && -n "$EFFECTIVE_LOCAL_BASE_URL" ]]; then
    trigger_catalog_raw="$(fetch_trigger_services "$EFFECTIVE_LOCAL_BASE_URL" "$LOCAL_RUNTIME_TOKEN" 2>/dev/null || true)"
    if [[ -n "$trigger_catalog_raw" ]]; then
      node -e 'JSON.parse(process.argv[1]);' "$trigger_catalog_raw" >/dev/null 2>&1 || die "trigger catalog returned invalid JSON"
      persist_trigger_snapshot "$trigger_catalog_raw" "local"
    elif [[ "$CONNECTION_MODE" == "local" && "$REFRESH_TRIGGERS" == "true" ]]; then
      die "failed to refresh trigger snapshot from local Runtime"
    fi
  elif [[ "$CONNECTION_MODE" == "local" && "$REFRESH_TRIGGERS" == "true" ]]; then
    die "cannot refresh triggers without a local Runtime admin token"
  fi
fi

if [[ "$LIST_TRIGGERS" == "true" ]]; then
  if [[ "$LIST_FORMAT" == "json" ]]; then
    emit_trigger_list_json
  else
    emit_trigger_list_text
  fi
  exit 0
fi

if [[ "$REFRESH_TRIGGERS" == "true" && -z "$TRIGGER_ID" && -z "$TRIGGER_NAME" ]]; then
  emit_refresh_only_summary
  exit 0
fi

if [[ -n "$TRIGGER_NAME" ]]; then
  TRIGGER_ID="$(resolve_trigger_id_from_snapshot "$TRIGGER_NAME" 2>/dev/null || true)"
fi

if [[ -z "$TRIGGER_ID" ]]; then
  if [[ -n "$TRIGGER_NAME" ]]; then
    CACHED_TRIGGER_NAMES="$(list_cached_trigger_names)"
    if [[ -n "$CACHED_TRIGGER_NAMES" ]]; then
      die "trigger name not found in cached snapshot: $TRIGGER_NAME; cached names: $CACHED_TRIGGER_NAMES; refresh triggers locally or pass --trigger-id"
    fi
    die "trigger name not found in cached snapshot: $TRIGGER_NAME; refresh triggers locally or pass --trigger-id"
  fi
  die "trigger identity is missing; prefer --trigger-name, or pass --trigger-id if you already know the exact id"
fi

PAYLOAD_JSON="$(build_payload_json "$TRIGGER_ID" "$INPUT_JSON")"

if [[ "$CONNECTION_MODE" == "local" ]]; then
  [[ -n "$EFFECTIVE_LOCAL_BASE_URL" ]] || EFFECTIVE_LOCAL_BASE_URL="$(discover_local_base_url "$LOCAL_BASE_URL")"
  exec bash "$LOCAL_LOOP_SCRIPT" \
    --target trigger.execute \
    --payload-json "$PAYLOAD_JSON" \
    --base-url "$EFFECTIVE_LOCAL_BASE_URL" \
    ${APP_HOME:+--app-home "$APP_HOME"} \
    --wait "$WAIT_VALUE" \
    --lease-ttl-ms "$LEASE_TTL_MS"
fi
