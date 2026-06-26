#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PREFERENCE_SCRIPT="$SKILL_DIR/scripts/export_preference.sh"
DEFAULT_RUNTIME_BASE_URLS=(
  "http://127.0.0.1:8877"
  "http://localhost:8877"
  "http://127.0.0.1:8878"
  "http://localhost:8878"
  "http://127.0.0.1:8879"
  "http://localhost:8879"
)

CONNECTION_MODE=""
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
PROBE_LOCAL="false"
FORMAT="json"
QUIET_SUCCESS="false"

usage() {
  cat <<'EOF'
Usage:
  preflight_check.sh [options]

Options:
  --connection-mode <local|cloud>
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
  --probe-local
  --format <json|text>
  --quiet-success
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

mask_token() {
  local value="${1:-}"
  if [[ -z "$value" ]]; then
    printf '%s\n' ""
    return 0
  fi
  if (( ${#value} <= 8 )); then
    printf '%s\n' "****"
    return 0
  fi
  printf '%s\n' "${value:0:4}...${value: -4}"
}

read_runtime_admin_token() {
  local app_home="${1:-}"
  local env_token="${MX_APP_RUNTIME_ADMIN_TOKEN:-${RPA_RUNTIME_ADMIN_TOKEN:-}}"
  if [[ -n "$env_token" ]]; then
    printf '%s\n' "$env_token"
    return 0
  fi

  local base_home
  if [[ -n "$app_home" ]]; then
    base_home="$app_home"
  elif [[ -n "${RPA_APP_HOME:-}" ]]; then
    base_home="$RPA_APP_HOME"
  else
    base_home=""
  fi

  if [[ -n "$base_home" ]]; then
    node -e '
const fs = require("node:fs");
const path = require("node:path");
const appHome = process.argv[1];
const file = path.join(appHome, "runtime", "admin-token.json");
try {
  const raw = JSON.parse(fs.readFileSync(file, "utf8"));
  const token = typeof raw?.token === "string" ? raw.token.trim() : "";
  if (token) process.stdout.write(token);
} catch {}
' "$base_home"
  fi
}

probe_runtime_status() {
  local base_url="$1"
  local token="$2"
  local raw
  raw="$(curl -sS -w $'\n%{http_code}' \
    -H "Authorization: Bearer $token" \
    "$base_url/local/status" 2>/dev/null || true)"
  local http_code="${raw##*$'\n'}"
  local body="${raw%$'\n'*}"
  node -e '
const httpCode = process.argv[1];
const body = process.argv[2];
let parsed = null;
try { parsed = JSON.parse(body); } catch {}
const out = {
  attempted: true,
  reachable: httpCode.startsWith("2"),
  httpCode,
  ok: parsed?.ok === true,
  message: typeof parsed?.message === "string" ? parsed.message : "",
  body: parsed,
};
process.stdout.write(JSON.stringify(out));
' "$http_code" "$body"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --connection-mode)
      CONNECTION_MODE="${2:-}"
      shift 2
      ;;
    --local-base-url)
      LOCAL_BASE_URL="${2:-}"
      shift 2
      ;;
    --app-home)
      APP_HOME="${2:-}"
      shift 2
      ;;
    --cloud-base-url)
      CLOUD_BASE_URL="${2:-}"
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
      WAIT_VALUE="${2:-}"
      shift 2
      ;;
    --lease-ttl-ms)
      LEASE_TTL_MS="${2:-}"
      shift 2
      ;;
    --poll-sec)
      POLL_SEC="${2:-}"
      shift 2
      ;;
    --timeout-sec)
      TIMEOUT_SEC="${2:-}"
      shift 2
      ;;
    --probe-local)
      PROBE_LOCAL="true"
      shift 1
      ;;
    --format)
      FORMAT="${2:-json}"
      shift 2
      ;;
    --quiet-success)
      QUIET_SUCCESS="true"
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

[[ "$FORMAT" == "json" || "$FORMAT" == "text" ]] || die "invalid --format: $FORMAT"

MODE="$(normalize_mode "${CONNECTION_MODE:-${MX_AUTO_CONNECTION_MODE:-$(pref_get defaultConnectionMode)}}")"
[[ -n "$MODE" ]] || MODE="local"

if [[ "$MODE" == "cloud" ]]; then
  SUMMARY_JSON="$(node -e '
process.stdout.write(JSON.stringify({
  ready: false,
  missingDefaults: ["cloudReserved"],
  effectiveConfig: {
    connectionMode: "cloud",
    reserved: true,
    message: "cloud mode is reserved and not enabled in this version"
  },
  checks: {
    localProbe: null
  }
}, null, 2));
')"

  if [[ "$FORMAT" == "text" ]]; then
    printf '[mx-auto] ready=false\n[mx-auto] mode=cloud\n[mx-auto] reserved=cloud mode is reserved and not enabled in this version\n'
  else
    printf '%s\n' "$SUMMARY_JSON"
  fi
  exit 2
fi

LOCAL_BASE_URL="${LOCAL_BASE_URL:-${MX_AUTO_LOCAL_BASE_URL:-${MX_APP_RUNTIME_BASE_URL:-${RPA_RUNTIME_BASE_URL:-$(pref_get defaultLocalBaseUrl)}}}}"
APP_HOME="$(resolve_app_home "$APP_HOME")"
CLOUD_BASE_URL="${CLOUD_BASE_URL:-${MX_AUTO_CLOUD_BASE_URL:-$(pref_get defaultCloudBaseUrl)}}"
DISPATCH_PATH="${DISPATCH_PATH:-${MX_AUTO_CLOUD_DISPATCH_PATH:-$(pref_get defaultCloudDispatchPath)}}"
STATUS_PATH_TEMPLATE="${STATUS_PATH_TEMPLATE:-${MX_AUTO_CLOUD_COMMAND_STATUS_PATH_TEMPLATE:-$(pref_get defaultCloudCommandStatusPathTemplate)}}"
LIST_PATH="${LIST_PATH:-${MX_AUTO_CLOUD_COMMAND_LIST_PATH:-$(pref_get defaultCloudCommandListPath)}}"
DEVICE_ID="${DEVICE_ID:-${MX_AUTO_CLOUD_DEVICE_ID:-$(pref_get defaultCloudDeviceId)}}"
TOKEN="${TOKEN:-${MX_AUTO_CLOUD_TOKEN:-$(pref_get defaultCloudToken)}}"
WAIT_VALUE="$(normalize_bool "${WAIT_VALUE:-${MX_AUTO_WAIT:-$(pref_get defaultWait)}}")"
LEASE_TTL_MS="$(normalize_positive_integer "${LEASE_TTL_MS:-${MX_AUTO_LEASE_TTL_MS:-$(pref_get defaultLeaseTtlMs)}}")"
POLL_SEC="$(normalize_positive_integer "${POLL_SEC:-${MX_AUTO_POLL_SEC:-$(pref_get defaultPollSec)}}")"
TIMEOUT_SEC="$(normalize_positive_integer "${TIMEOUT_SEC:-${MX_AUTO_TIMEOUT_SEC:-$(pref_get defaultTimeoutSec)}}")"

[[ -n "$WAIT_VALUE" ]] || WAIT_VALUE="true"
[[ -n "$LEASE_TTL_MS" ]] || LEASE_TTL_MS="60000"
[[ -n "$POLL_SEC" ]] || POLL_SEC="3"
[[ -n "$TIMEOUT_SEC" ]] || TIMEOUT_SEC="1200"

RUNTIME_ADMIN_TOKEN="$(read_runtime_admin_token "$APP_HOME")"

missing_defaults=()
[[ -n "$RUNTIME_ADMIN_TOKEN" ]] || missing_defaults+=("runtimeAdminToken")

probe_json='null'
if [[ "$PROBE_LOCAL" == "true" && -n "$RUNTIME_ADMIN_TOKEN" ]]; then
  probe_target="$LOCAL_BASE_URL"
  if [[ -z "$probe_target" ]]; then
    for candidate in "${DEFAULT_RUNTIME_BASE_URLS[@]}"; do
      probe_result="$(probe_runtime_status "$candidate" "$RUNTIME_ADMIN_TOKEN")"
      if node -e 'const r=JSON.parse(process.argv[1]); process.exit(r.reachable ? 0 : 1);' "$probe_result"; then
        probe_target="$candidate"
        probe_json="$probe_result"
        break
      fi
      probe_json="$probe_result"
    done
  else
    probe_json="$(probe_runtime_status "$probe_target" "$RUNTIME_ADMIN_TOKEN")"
  fi
fi

SUMMARY_JSON="$(node -e '
const fs = require("node:fs");
const skillDir = process.argv[1];
const mode = process.argv[2];
const localBaseUrl = process.argv[3];
const appHome = process.argv[4];
const cloudBaseUrl = process.argv[5];
const dispatchPath = process.argv[6];
const statusPathTemplate = process.argv[7];
const listPath = process.argv[8];
const deviceId = process.argv[9];
const maskedToken = process.argv[10];
const waitValue = process.argv[11];
const leaseTtlMs = Number(process.argv[12]);
const pollSec = Number(process.argv[13]);
const timeoutSec = Number(process.argv[14]);
const runtimeAdminTokenPresent = process.argv[15] === "true";
const probeJson = process.argv[16];
const missing = JSON.parse(process.argv[17]);

const scripts = [
  "scripts/export_preference.sh",
  "scripts/preflight_check.sh",
  "scripts/run.sh",
  "scripts/local_dispatch_loop.sh",
  "scripts/cloud_dispatch_loop.sh",
  "scripts/browser_sandbox_bridge.sh",
  "scripts/script_catalog.sh",
];

const scriptChecks = Object.fromEntries(
  scripts.map((relativePath) => {
    const fullPath = `${skillDir}/${relativePath}`;
    let exists = false;
    try {
      exists = fs.statSync(fullPath).isFile();
    } catch {}
    return [relativePath, { exists }];
  })
);

const binChecks = Object.fromEntries(
  ["bash", "curl", "node"].map((name) => {
    try {
      const result = require("node:child_process").execFileSync("bash", ["-lc", `command -v ${name}`], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"],
      }).trim();
      return [name, { ok: Boolean(result), path: result }];
    } catch {
      return [name, { ok: false, path: "" }];
    }
  })
);

let probe = null;
if (probeJson && probeJson !== "null") {
  try { probe = JSON.parse(probeJson); } catch {}
}

const ready = missing.length === 0
  && Object.values(scriptChecks).every((item) => item.exists)
  && Object.values(binChecks).every((item) => item.ok)
  && (!probe || probe.reachable === true);

process.stdout.write(JSON.stringify({
  ready,
  missingDefaults: missing,
  effectiveConfig: {
    connectionMode: mode,
    appHome,
    localBaseUrl: localBaseUrl || "",
    localBaseUrlCandidates: localBaseUrl
      ? [localBaseUrl]
      : [
          "http://127.0.0.1:8877",
          "http://localhost:8877",
          "http://127.0.0.1:8878",
          "http://localhost:8878",
          "http://127.0.0.1:8879",
          "http://localhost:8879",
        ],
    cloudBaseUrl: cloudBaseUrl || "",
    dispatchPath: dispatchPath || "",
    statusPathTemplate: statusPathTemplate || "",
    listPath: listPath || "",
    deviceId: deviceId || "",
    cloudTokenMasked: maskedToken || "",
    runtimeAdminTokenPresent,
    wait: waitValue === "true",
    leaseTtlMs,
    pollSec,
    timeoutSec,
  },
  checks: {
    scripts: scriptChecks,
    bins: binChecks,
    localProbe: probe,
  },
}, null, 2));
' "$SKILL_DIR" "$MODE" "$LOCAL_BASE_URL" "$APP_HOME" "$CLOUD_BASE_URL" "$DISPATCH_PATH" "$STATUS_PATH_TEMPLATE" "$LIST_PATH" "$DEVICE_ID" "$(mask_token "$TOKEN")" "$WAIT_VALUE" "$LEASE_TTL_MS" "$POLL_SEC" "$TIMEOUT_SEC" "$([[ -n "$RUNTIME_ADMIN_TOKEN" ]] && printf true || printf false)" "$probe_json" "$(printf '%s' "${missing_defaults[@]:-}" | node -e 'const fs=require("node:fs"); const raw=fs.readFileSync(0,"utf8").trim(); process.stdout.write(JSON.stringify(raw ? raw.split(/\s+/) : []));')")"

READY="$(node -e 'const summary=JSON.parse(process.argv[1]); process.stdout.write(summary.ready ? "true" : "false");' "$SUMMARY_JSON")"

if [[ "$READY" == "true" && "$QUIET_SUCCESS" == "true" ]]; then
  exit 0
fi

if [[ "$FORMAT" == "text" ]]; then
  node -e '
const summary = JSON.parse(process.argv[1]);
const lines = [];
lines.push(`[mx-auto] ready=${summary.ready}`);
lines.push(`[mx-auto] mode=${summary.effectiveConfig.connectionMode}`);
if (summary.missingDefaults.length > 0) {
  lines.push(`[mx-auto] missingDefaults=${summary.missingDefaults.join(",")}`);
}
lines.push(`[mx-auto] appHome=${summary.effectiveConfig.appHome || "-"}`);
lines.push(`[mx-auto] localBaseUrl=${summary.effectiveConfig.localBaseUrl || "-"}`);
lines.push(`[mx-auto] runtimeAdminTokenPresent=${summary.effectiveConfig.runtimeAdminTokenPresent}`);
process.stdout.write(lines.join("\n") + "\n");
' "$SUMMARY_JSON"
else
  printf '%s\n' "$SUMMARY_JSON"
fi

[[ "$READY" == "true" ]] && exit 0
exit 2
