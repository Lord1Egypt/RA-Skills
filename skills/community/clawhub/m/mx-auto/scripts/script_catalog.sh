#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PREFERENCE_SCRIPT="$SKILL_DIR/scripts/export_preference.sh"
LOCAL_LOOP_SCRIPT="$SKILL_DIR/scripts/local_dispatch_loop.sh"
DEFAULT_RUNTIME_BASE_URLS=(
  "http://127.0.0.1:8877"
  "http://localhost:8877"
  "http://127.0.0.1:8878"
  "http://localhost:8878"
  "http://127.0.0.1:8879"
  "http://localhost:8879"
)

ACTION="${1:-list}"
if [[ $# -gt 0 ]]; then
  shift
fi

SCRIPT_NAME=""
INPUT_JSON=""
LOCAL_BASE_URL=""
APP_HOME=""
WAIT_VALUE=""
LEASE_TTL_MS=""
FORMAT="text"

usage() {
  cat <<'EOF'
Usage:
  script_catalog.sh list [options]
  script_catalog.sh show <script-name> [options]
  script_catalog.sh run <script-name> [options]

Options:
  --input-json <json>      JSON object passed as inputOverrides when running
  --local-base-url <url>   Runtime base URL
  --app-home <path>        Runtime app home
  --wait <true|false>      default: true
  --lease-ttl-ms <n>       default: 60000
  --format <text|json>     default: text
  -h, --help
EOF
}

die() {
  echo "$*" >&2
  exit 1
}

pref_get() {
  local key="$1"
  if [[ -f "$PREFERENCE_SCRIPT" ]]; then
    bash "$PREFERENCE_SCRIPT" get "$key" 2>/dev/null || true
  fi
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

  node -e '
const fs = require("node:fs");
const path = require("node:path");
const file = path.join(process.argv[1], "runtime", "admin-token.json");
try {
  const raw = JSON.parse(fs.readFileSync(file, "utf8"));
  const token = typeof raw?.token === "string" ? raw.token.trim() : "";
  if (token) process.stdout.write(token);
} catch {}
' "$app_home"
}

discover_local_base_url() {
  local preferred="${1:-}"
  local candidates=()
  [[ -n "$preferred" ]] && candidates+=("$preferred")
  [[ -n "${MX_APP_RUNTIME_BASE_URL:-}" ]] && candidates+=("$MX_APP_RUNTIME_BASE_URL")
  [[ -n "${RPA_RUNTIME_BASE_URL:-}" ]] && candidates+=("$RPA_RUNTIME_BASE_URL")
  [[ -n "$(pref_get defaultLocalBaseUrl)" ]] && candidates+=("$(pref_get defaultLocalBaseUrl)")
  candidates+=("${DEFAULT_RUNTIME_BASE_URLS[@]}")

  local candidate
  for candidate in "${candidates[@]}"; do
    [[ -n "$candidate" ]] || continue
    if curl -fsS --max-time 2 "$candidate/health" >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  printf '%s\n' "${DEFAULT_RUNTIME_BASE_URLS[0]}"
}

join_url() {
  node -e '
const base = String(process.argv[1] || "").trim().replace(/\/+$/, "");
const path = String(process.argv[2] || "").trim();
process.stdout.write(`${base}${path.startsWith("/") ? path : `/${path}`}`);
' "$1" "$2"
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

fetch_catalog() {
  local base_url="$1"
  local token="$2"
  curl -fsS \
    -H "Authorization: Bearer $token" \
    "$(join_url "$base_url" "/examples/catalog")"
}

persist_script_snapshot() {
  local raw_json="$1"
  local snapshot_json
  snapshot_json="$(node -e '
const payload = JSON.parse(process.argv[1]);
const examples = Array.isArray(payload.examples) ? payload.examples : [];
const scripts = examples
  .map((script) => ({
    name: typeof script.name === "string" ? script.name : "",
    workflowId: typeof script.workflowId === "string" ? script.workflowId : "",
    platform: typeof script.platform === "string" ? script.platform : "",
    platformLabel: typeof script.platformLabel === "string" ? script.platformLabel : "",
    feature: typeof script.feature === "string" ? script.feature : "",
    featureLabel: typeof script.featureLabel === "string" ? script.featureLabel : "",
    method: typeof script.method === "string" ? script.method : "",
    displayName: typeof script.displayName === "string" ? script.displayName : "",
    description: typeof script.description === "string" ? script.description : "",
    runner: typeof script.runner === "string" ? script.runner : "",
    inputSchema: Array.isArray(script.inputSchema) ? script.inputSchema : [],
    inputDefaults: script.inputDefaults && typeof script.inputDefaults === "object" && !Array.isArray(script.inputDefaults) ? script.inputDefaults : {},
    updatedAt: typeof script.updatedAt === "string" ? script.updatedAt : "",
  }))
  .filter((script) => script.name);
process.stdout.write(JSON.stringify({
  loadedAt: new Date().toISOString(),
  sourcePath: "/examples/catalog",
  scriptCount: scripts.length,
  scripts,
}));
' "$raw_json")"
  bash "$PREFERENCE_SCRIPT" set-script-snapshot "$snapshot_json" >/dev/null
}

emit_list() {
  local raw_json="$1"
  local format="$2"
  node -e '
const payload = JSON.parse(process.argv[1]);
const format = process.argv[2];
const scripts = Array.isArray(payload.examples) ? payload.examples : [];
const normalized = scripts.map((script) => ({
  name: String(script?.name || ""),
  workflowId: String(script?.workflowId || ""),
  platform: String(script?.platformLabel || script?.platform || ""),
  runner: String(script?.runner || ""),
  description: String(script?.description || ""),
  updatedAt: String(script?.updatedAt || ""),
})).filter((script) => script.name);
if (format === "json") {
  process.stdout.write(JSON.stringify({ ok: true, mode: "scripts_list", scriptCount: normalized.length, scripts: normalized }, null, 2) + "\n");
  process.exit(0);
}
const lines = [`当前可用脚本（${normalized.length}）`];
for (const [index, script] of normalized.entries()) {
  lines.push(`${index + 1}. ${script.name}`);
  lines.push(`平台：${script.platform || "-"}`);
  lines.push(`Runner：${script.runner || "-"}`);
}
process.stdout.write(lines.join("\n") + "\n");
' "$raw_json" "$format"
}

emit_show() {
  local raw_json="$1"
  local script_name="$2"
  local format="$3"
  node -e '
const payload = JSON.parse(process.argv[1]);
const scriptName = process.argv[2];
const format = process.argv[3];
const scripts = Array.isArray(payload.examples) ? payload.examples : [];
const script = scripts.find((item) => item?.name === scriptName);
if (!script) {
  const names = scripts.map((item) => item?.name).filter(Boolean);
  console.error(`script not found: ${scriptName}${names.length ? `; available scripts: ${names.join(", ")}` : ""}`);
  process.exit(2);
}
if (format === "json") {
  process.stdout.write(JSON.stringify({ ok: true, mode: "scripts_show", script }, null, 2) + "\n");
  process.exit(0);
}
const schema = Array.isArray(script.inputSchema) ? script.inputSchema : [];
const lines = [];
lines.push(`脚本：${script.name}`);
lines.push(`Workflow：${script.workflowId || "-"}`);
lines.push(`平台：${script.platformLabel || script.platform || "-"}`);
lines.push(`Runner：${script.runner || "-"}`);
lines.push(`描述：${script.description || "-"}`);
lines.push("输入：");
if (schema.length) {
  for (const field of schema) lines.push(`- ${field.key || field.name || ""}${field.required ? " *" : ""}`);
} else {
  lines.push("-");
}
process.stdout.write(lines.join("\n") + "\n");
' "$raw_json" "$script_name" "$format"
}

build_run_payload() {
  local script_name="$1"
  local input_json="$2"
  node -e '
const name = process.argv[1];
const inputRaw = process.argv[2];
const payload = { name };
if (inputRaw) payload.inputOverrides = JSON.parse(inputRaw);
process.stdout.write(JSON.stringify(payload));
' "$script_name" "$input_json"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input-json)
      INPUT_JSON="${2:-}"
      shift 2
      ;;
    --local-base-url|--base-url)
      LOCAL_BASE_URL="${2:-}"
      shift 2
      ;;
    --app-home)
      APP_HOME="${2:-}"
      shift 2
      ;;
    --wait)
      WAIT_VALUE="${2:-}"
      shift 2
      ;;
    --lease-ttl-ms)
      LEASE_TTL_MS="${2:-}"
      shift 2
      ;;
    --format)
      FORMAT="${2:-text}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$SCRIPT_NAME" ]]; then
        SCRIPT_NAME="$1"
        shift 1
      else
        die "unknown arg: $1"
      fi
      ;;
  esac
done

case "$ACTION" in
  list|show|run) ;;
  ""|-h|--help)
    usage
    exit 0
    ;;
  *) die "unknown scripts action: $ACTION" ;;
esac

case "$FORMAT" in
  text|json) ;;
  *) die "invalid format: $FORMAT" ;;
esac

APP_HOME="$(resolve_app_home "$APP_HOME")"
LOCAL_BASE_URL="$(discover_local_base_url "$LOCAL_BASE_URL")"
TOKEN="$(discover_runtime_admin_token "$APP_HOME")"
[[ -n "$TOKEN" ]] || die "runtime admin token is missing; set MX_APP_RUNTIME_ADMIN_TOKEN or point --app-home to a Runtime state dir"

CATALOG_JSON="$(fetch_catalog "$LOCAL_BASE_URL" "$TOKEN")"
node -e 'JSON.parse(process.argv[1]);' "$CATALOG_JSON" >/dev/null 2>&1 || die "script catalog returned invalid JSON"
persist_script_snapshot "$CATALOG_JSON"

if [[ "$ACTION" == "list" ]]; then
  emit_list "$CATALOG_JSON" "$FORMAT"
  exit 0
fi

[[ -n "$SCRIPT_NAME" ]] || die "$ACTION requires <script-name>"

if [[ "$ACTION" == "show" ]]; then
  emit_show "$CATALOG_JSON" "$SCRIPT_NAME" "$FORMAT"
  exit 0
fi

emit_show "$CATALOG_JSON" "$SCRIPT_NAME" "json" >/dev/null
INPUT_JSON="$(validate_input_json "$INPUT_JSON")"
WAIT_VALUE="$(normalize_bool "${WAIT_VALUE:-$(pref_get defaultWait)}")"
LEASE_TTL_MS="$(normalize_positive_integer "${LEASE_TTL_MS:-$(pref_get defaultLeaseTtlMs)}")"
[[ -n "$WAIT_VALUE" ]] || WAIT_VALUE="true"
[[ -n "$LEASE_TTL_MS" ]] || LEASE_TTL_MS="60000"
PAYLOAD_JSON="$(build_run_payload "$SCRIPT_NAME" "$INPUT_JSON")"

exec bash "$LOCAL_LOOP_SCRIPT" \
  --target script.run \
  --payload-json "$PAYLOAD_JSON" \
  --base-url "$LOCAL_BASE_URL" \
  --app-home "$APP_HOME" \
  --wait "$WAIT_VALUE" \
  --lease-ttl-ms "$LEASE_TTL_MS"
