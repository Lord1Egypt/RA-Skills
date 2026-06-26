#!/usr/bin/env bash
set -euo pipefail

resolve_state_dir() {
  if [[ -n "${OPENCLAW_STATE_DIR:-}" ]]; then
    printf '%s\n' "$OPENCLAW_STATE_DIR"
    return 0
  fi
  printf '%s\n' "${HOME}/.openclaw"
}

resolve_preferences_path() {
  local state_dir
  state_dir="$(resolve_state_dir)"
  printf '%s\n' "${state_dir}/skill-state/mx-auto/preferences.json"
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

read_preferences_json() {
  local pref_path="$1"
  if [[ -f "$pref_path" ]]; then
    cat "$pref_path"
    return 0
  fi
  printf '{}\n'
}

normalize_key() {
  local key="${1:-}"
  case "$key" in
    mode|connectionMode|defaultConnectionMode)
      printf '%s\n' "defaultConnectionMode"
      ;;
    localBaseUrl|baseUrl|defaultLocalBaseUrl)
      printf '%s\n' "defaultLocalBaseUrl"
      ;;
    appHome|defaultAppHome)
      printf '%s\n' "defaultAppHome"
      ;;
    cloudBaseUrl|defaultCloudBaseUrl)
      printf '%s\n' "defaultCloudBaseUrl"
      ;;
    dispatchPath|defaultCloudDispatchPath)
      printf '%s\n' "defaultCloudDispatchPath"
      ;;
    statusPathTemplate|defaultCloudCommandStatusPathTemplate)
      printf '%s\n' "defaultCloudCommandStatusPathTemplate"
      ;;
    listPath|defaultCloudCommandListPath)
      printf '%s\n' "defaultCloudCommandListPath"
      ;;
    deviceId|cloudDeviceId|defaultCloudDeviceId)
      printf '%s\n' "defaultCloudDeviceId"
      ;;
    token|cloudToken|defaultCloudToken)
      printf '%s\n' "defaultCloudToken"
      ;;
    wait|defaultWait)
      printf '%s\n' "defaultWait"
      ;;
    leaseTtlMs|defaultLeaseTtlMs)
      printf '%s\n' "defaultLeaseTtlMs"
      ;;
    pollSec|defaultPollSec)
      printf '%s\n' "defaultPollSec"
      ;;
    timeoutSec|defaultTimeoutSec)
      printf '%s\n' "defaultTimeoutSec"
      ;;
    browserProfile|defaultBrowserProfile)
      printf '%s\n' "defaultBrowserProfile"
      ;;
    sandboxSnapshotMaxChars|defaultSandboxSnapshotMaxChars)
      printf '%s\n' "defaultSandboxSnapshotMaxChars"
      ;;
    triggerSnapshot)
      printf '%s\n' "triggerSnapshot"
      ;;
    scriptSnapshot)
      printf '%s\n' "scriptSnapshot"
      ;;
    "")
      printf '%s\n' ""
      ;;
    *)
      printf '%s\n' "$key"
      ;;
  esac
}

validate_key_value() {
  local key="$1"
  local value="$2"

  case "$key" in
    defaultConnectionMode)
      [[ "$value" == "local" || "$value" == "cloud" ]] || {
        echo "invalid connection mode: $value (expected local or cloud)" >&2
        exit 1
      }
      ;;
    defaultAppHome|defaultLocalBaseUrl|defaultCloudBaseUrl|defaultCloudDispatchPath|defaultCloudCommandStatusPathTemplate|defaultCloudCommandListPath|defaultCloudDeviceId|defaultCloudToken|defaultBrowserProfile)
      [[ -n "$value" ]] || {
        echo "invalid value for $key: empty" >&2
        exit 1
      }
      ;;
    defaultWait)
      [[ "$value" == "true" || "$value" == "false" ]] || {
        echo "invalid wait value: $value (expected true or false)" >&2
        exit 1
      }
      ;;
    defaultLeaseTtlMs|defaultPollSec|defaultTimeoutSec|defaultSandboxSnapshotMaxChars)
      [[ "$value" =~ ^[0-9]+$ && "$value" != "0" ]] || {
        echo "invalid numeric value for $key: $value" >&2
        exit 1
      }
      ;;
    triggerSnapshot|scriptSnapshot)
      node -e '
const parsed = JSON.parse(process.argv[1]);
if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) process.exit(1);
' "$value" >/dev/null 2>&1 || {
        echo "$key must be a JSON object" >&2
        exit 1
      }
      ;;
  esac
}

print_value() {
  local key="$1"
  local pref_path="$2"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const key = process.argv[2];

let data = {};
try {
  data = JSON.parse(fs.readFileSync(prefPath, "utf8"));
} catch {}

const value = data[key];
if (value === undefined || value === null) process.exit(0);
if (typeof value === "object") {
  process.stdout.write(JSON.stringify(value));
} else {
  process.stdout.write(String(value));
}
' "$pref_path" "$key"
}

write_value() {
  local key="$1"
  local value="$2"
  local pref_path="$3"

  mkdir -p "$(dirname "$pref_path")"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const key = process.argv[2];
const rawValue = process.argv[3];

let data = {};
try {
  data = JSON.parse(fs.readFileSync(prefPath, "utf8"));
} catch {}

let value = rawValue;
if (rawValue === "true") value = true;
else if (rawValue === "false") value = false;
else if (/^[0-9]+$/.test(rawValue)) value = Number(rawValue);
else if (key === "triggerSnapshot" || key === "scriptSnapshot") value = JSON.parse(rawValue);

data[key] = value;
data.updatedAt = new Date().toISOString();
data.updatedBy = "user";

const tempPath = `${prefPath}.tmp-${process.pid}`;
fs.writeFileSync(tempPath, JSON.stringify(data, null, 2) + "\n", "utf8");
fs.renameSync(tempPath, prefPath);
' "$pref_path" "$key" "$value"
}

unset_value() {
  local key="$1"
  local pref_path="$2"

  mkdir -p "$(dirname "$pref_path")"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const key = process.argv[2];

let data = {};
try {
  data = JSON.parse(fs.readFileSync(prefPath, "utf8"));
} catch {}

delete data[key];
data.updatedAt = new Date().toISOString();
data.updatedBy = "user";

const tempPath = `${prefPath}.tmp-${process.pid}`;
fs.writeFileSync(tempPath, JSON.stringify(data, null, 2) + "\n", "utf8");
fs.renameSync(tempPath, prefPath);
' "$pref_path" "$key"
}

show_preferences() {
  local pref_path="$1"
  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];

let data = {};
try {
  data = JSON.parse(fs.readFileSync(prefPath, "utf8"));
} catch {}

const mask = (value) => {
  if (typeof value !== "string" || value.length === 0) return value;
  if (value.length <= 8) return "****";
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
};

if (typeof data.defaultCloudToken === "string" && data.defaultCloudToken) {
  data.defaultCloudToken = mask(data.defaultCloudToken);
}

process.stdout.write(JSON.stringify(data, null, 2) + "\n");
' "$pref_path"
}

check_preferences() {
  local pref_path="$1"
  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];

let data = {};
try {
  data = JSON.parse(fs.readFileSync(prefPath, "utf8"));
} catch {}

const env = process.env;
const mode = String(
  env.MX_AUTO_CONNECTION_MODE ||
  data.defaultConnectionMode ||
  "local"
).trim();

const missing = [];
if (mode === "cloud") {
  const cloudBaseUrl = String(env.MX_AUTO_CLOUD_BASE_URL || data.defaultCloudBaseUrl || "").trim();
  const dispatchPath = String(env.MX_AUTO_CLOUD_DISPATCH_PATH || data.defaultCloudDispatchPath || "").trim();
  const statusPathTemplate = String(env.MX_AUTO_CLOUD_COMMAND_STATUS_PATH_TEMPLATE || data.defaultCloudCommandStatusPathTemplate || "").trim();
  const deviceId = String(env.MX_AUTO_CLOUD_DEVICE_ID || data.defaultCloudDeviceId || "").trim();
  const token = String(env.MX_AUTO_CLOUD_TOKEN || data.defaultCloudToken || "").trim();
  if (!cloudBaseUrl) missing.push("defaultCloudBaseUrl");
  if (!dispatchPath) missing.push("defaultCloudDispatchPath");
  if (!statusPathTemplate) missing.push("defaultCloudCommandStatusPathTemplate");
  if (!deviceId) missing.push("defaultCloudDeviceId");
  if (!token) missing.push("defaultCloudToken");
}

const result = {
  complete: missing.length === 0,
  mode,
  missing,
  preferencesPath: prefPath,
  defaultAppHome: String(data.defaultAppHome || "").trim(),
  hasTriggerSnapshot: Boolean(
    data.triggerSnapshot &&
    typeof data.triggerSnapshot === "object" &&
    Array.isArray(data.triggerSnapshot.services)
  )
};

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exit(missing.length === 0 ? 0 : 1);
' "$pref_path"
}

apply_recommended_preferences() {
  local pref_path="$1"
  write_value "defaultConnectionMode" "local" "$pref_path"
  write_value "defaultAppHome" "$(resolve_default_app_home)" "$pref_path"
  write_value "defaultWait" "true" "$pref_path"
  write_value "defaultLeaseTtlMs" "60000" "$pref_path"
  write_value "defaultPollSec" "3" "$pref_path"
  write_value "defaultTimeoutSec" "1200" "$pref_path"
  write_value "defaultBrowserProfile" "browser-1" "$pref_path"
  write_value "defaultSandboxSnapshotMaxChars" "6000" "$pref_path"
  show_preferences "$pref_path"
}

usage() {
  cat <<'EOF'
Usage:
  export_preference.sh path
  export_preference.sh show
  export_preference.sh check
  export_preference.sh get <key>
  export_preference.sh set-key <key> <value>
  export_preference.sh unset-key <key>
  export_preference.sh apply-recommended
  export_preference.sh set-trigger-snapshot <json>
  export_preference.sh get-trigger-snapshot
  export_preference.sh clear-trigger-snapshot
  export_preference.sh clear

Supported keys:
  defaultConnectionMode                  local | cloud
  defaultAppHome                         string
  defaultLocalBaseUrl                   string
  defaultCloudBaseUrl                   string
  defaultCloudDispatchPath              string
  defaultCloudCommandStatusPathTemplate string
  defaultCloudCommandListPath           string
  defaultCloudDeviceId                  string
  defaultCloudToken                     string
  defaultWait                           true | false
  defaultLeaseTtlMs                     integer
  defaultPollSec                        integer
  defaultTimeoutSec                     integer
  defaultBrowserProfile                 string
  defaultSandboxSnapshotMaxChars        integer
  triggerSnapshot                       JSON object
  scriptSnapshot                        JSON object
EOF
}

main() {
  local cmd="${1:-}"
  local pref_path key value
  pref_path="$(resolve_preferences_path)"

  case "$cmd" in
    path)
      printf '%s\n' "$pref_path"
      ;;
    show)
      show_preferences "$pref_path"
      ;;
    check)
      check_preferences "$pref_path"
      ;;
    get)
      key="$(normalize_key "${2:-}")"
      [[ -n "$key" ]] || {
        echo "get requires <key>" >&2
        exit 1
      }
      print_value "$key" "$pref_path"
      ;;
    set-key)
      key="$(normalize_key "${2:-}")"
      value="${3:-}"
      [[ -n "$key" && -n "$value" ]] || {
        echo "set-key requires <key> <value>" >&2
        exit 1
      }
      validate_key_value "$key" "$value"
      write_value "$key" "$value" "$pref_path"
      printf '%s=%s\n' "$key" "$value"
      ;;
    unset-key)
      key="$(normalize_key "${2:-}")"
      [[ -n "$key" ]] || {
        echo "unset-key requires <key>" >&2
        exit 1
      }
      unset_value "$key" "$pref_path"
      ;;
    apply-recommended)
      apply_recommended_preferences "$pref_path"
      ;;
    set-trigger-snapshot)
      value="${2:-}"
      [[ -n "$value" ]] || {
        echo "set-trigger-snapshot requires <json>" >&2
        exit 1
      }
      validate_key_value "triggerSnapshot" "$value"
      write_value "triggerSnapshot" "$value" "$pref_path"
      ;;
    get-trigger-snapshot)
      print_value "triggerSnapshot" "$pref_path"
      ;;
    clear-trigger-snapshot)
      unset_value "triggerSnapshot" "$pref_path"
      ;;
    set-script-snapshot)
      value="${2:-}"
      [[ -n "$value" ]] || {
        echo "set-script-snapshot requires <json>" >&2
        exit 1
      }
      validate_key_value "scriptSnapshot" "$value"
      write_value "scriptSnapshot" "$value" "$pref_path"
      ;;
    get-script-snapshot)
      print_value "scriptSnapshot" "$pref_path"
      ;;
    clear-script-snapshot)
      unset_value "scriptSnapshot" "$pref_path"
      ;;
    clear)
      rm -f "$pref_path"
      ;;
    -h|--help|help|"")
      usage
      ;;
    *)
      echo "unknown subcommand: $cmd" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
