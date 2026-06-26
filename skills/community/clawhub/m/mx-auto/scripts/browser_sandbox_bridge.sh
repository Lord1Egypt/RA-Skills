#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PREFERENCE_SCRIPT="$SKILL_DIR/scripts/export_preference.sh"
DEFAULT_RUNTIME_BROWSER_URL="http://127.0.0.1:8877/browser"
DEFAULT_RUNTIME_BASE_URL="http://127.0.0.1:8877"
DEFAULT_PROFILE="browser-1"
DEFAULT_MAX_CHARS="6000"

ACTION="${1:-}"
if [[ $# -gt 0 ]]; then
  shift
fi

PROFILE=""
BASE_URL=""
TOKEN=""
APP_HOME=""
TARGET_ID=""
MAX_CHARS=""
FORMAT="text"
URL_CONTAINS=()
URL_NOT_CONTAINS=()

usage() {
  cat <<'EOF'
Usage:
  run.sh tabs [options]
  run.sh snapshot [options]

Actions:
  tabs                      List already-open tabs in the browser sandbox
  snapshot                  Snapshot an existing tab by targetId or URL match

Options:
  --profile <name>          Browser sandbox profile (default: browser-1)
  --base-url <url>          Runtime browser endpoint or Runtime base URL
  --token <token>           Runtime management token
  --app-home <path>         Runtime state directory root
  --target-id <id>          Existing targetId to snapshot
  --url-contains <text>     Filter snapshot target URL must include this text
  --url-not-contains <text> Filter snapshot target URL must not include this text
  --max-chars <n>           Snapshot maxChars (default: 6000)
  --format <text|json>      Output format (default: text)
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

normalize_endpoint() {
  local raw="${1:-}"
  node -e '
const raw = String(process.argv[1] || "").trim();
if (!raw) process.exit(1);
const withoutSlash = raw.replace(/\/+$/, "");
process.stdout.write(withoutSlash.endsWith("/browser") ? withoutSlash : `${withoutSlash}/browser`);
' "$raw"
}

normalize_positive_integer() {
  local raw="${1:-}"
  [[ "$raw" =~ ^[0-9]+$ && "$raw" != "0" ]] || die "invalid positive integer: $raw"
  printf '%s\n' "$raw"
}

discover_token() {
  local app_home="${1:-}"
  local env_token="${BROWSER_SANDBOX_BRIDGE_TOKEN:-${MX_APP_RUNTIME_ADMIN_TOKEN:-${RPA_RUNTIME_ADMIN_TOKEN:-}}}"
  if [[ -n "$env_token" ]]; then
    printf '%s\n' "$env_token"
    return 0
  fi

  local candidates=()
  if [[ -n "$app_home" ]]; then
    candidates+=("$app_home")
  fi
  if [[ -n "${RPA_APP_HOME:-}" ]]; then
    candidates+=("$RPA_APP_HOME")
  fi
  candidates+=("$(resolve_app_home "")")

  local candidate
  for candidate in "${candidates[@]}"; do
    [[ -n "$candidate" ]] || continue
    local token_file="$candidate/runtime/admin-token.json"
    if [[ -f "$token_file" ]]; then
      node -e '
const fs = require("node:fs");
const file = process.argv[1];
try {
  const raw = JSON.parse(fs.readFileSync(file, "utf8"));
  const token = typeof raw?.token === "string" ? raw.token.trim() : "";
  if (token) process.stdout.write(token);
} catch {}
' "$token_file"
      return 0
    fi
  done
}

build_tabs_payload() {
  local profile="$1"
  node -e '
process.stdout.write(JSON.stringify({
  action: "tabs",
  profile: process.argv[1],
}));
' "$profile"
}

build_snapshot_payload() {
  local profile="$1"
  local target_id="$2"
  local max_chars="$3"
  node -e '
process.stdout.write(JSON.stringify({
  action: "snapshot",
  profile: process.argv[1],
  targetId: process.argv[2],
  maxChars: Number(process.argv[3]),
}));
' "$profile" "$target_id" "$max_chars"
}

bridge_post() {
  local endpoint="$1"
  local token="$2"
  local payload_json="$3"
  curl -sS \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    -d "$payload_json" \
    "$endpoint"
}

print_tabs() {
  local raw_json="$1"
  local format="$2"
  node -e '
const data = JSON.parse(process.argv[1]);
const format = process.argv[2];

function extractTabs(root) {
  const candidates = [
    root?.tabs,
    root?.targets,
    root?.result?.tabs,
    root?.result?.targets,
    root?.data?.tabs,
    root?.data?.targets,
  ];
  for (const value of candidates) {
    if (Array.isArray(value)) return value;
  }
  return [];
}

const tabs = extractTabs(data).map((tab) => ({
  targetId: String(tab?.targetId ?? tab?.id ?? "").trim(),
  title: String(tab?.title ?? "").trim(),
  url: String(tab?.url ?? "").trim(),
  type: String(tab?.type ?? "").trim(),
}));

if (format === "json") {
  process.stdout.write(JSON.stringify({
    ok: true,
    action: "tabs",
    tabCount: tabs.length,
    tabs,
  }, null, 2) + "\n");
  process.exit(0);
}

const lines = [];
lines.push(`当前打开 tab（${tabs.length}）`);
for (const [index, tab] of tabs.entries()) {
  lines.push(`${index + 1}. ${tab.title || "(untitled)"}`);
  lines.push(`targetId: ${tab.targetId || "-"}`);
  lines.push(`url: ${tab.url || "-"}`);
}
process.stdout.write(lines.join("\n") + "\n");
' "$raw_json" "$format"
}

resolve_target_id() {
  local raw_json="$1"
  local explicit_target_id="$2"
  local includes_json="$3"
  local excludes_json="$4"

  node -e '
const data = JSON.parse(process.argv[1]);
const explicitTargetId = String(process.argv[2] || "").trim();
const includes = JSON.parse(process.argv[3]);
const excludes = JSON.parse(process.argv[4]);

function extractTabs(root) {
  const candidates = [
    root?.tabs,
    root?.targets,
    root?.result?.tabs,
    root?.result?.targets,
    root?.data?.tabs,
    root?.data?.targets,
  ];
  for (const value of candidates) {
    if (Array.isArray(value)) return value;
  }
  return [];
}

const tabs = extractTabs(data).map((tab) => ({
  targetId: String(tab?.targetId ?? tab?.id ?? "").trim(),
  title: String(tab?.title ?? "").trim(),
  url: String(tab?.url ?? "").trim(),
})).filter((tab) => tab.targetId);

if (explicitTargetId) {
  const found = tabs.find((tab) => tab.targetId === explicitTargetId);
  if (!found) {
    console.error(`targetId not found in current tabs: ${explicitTargetId}`);
    process.exit(2);
  }
  process.stdout.write(JSON.stringify(found));
  process.exit(0);
}

const filtered = tabs.filter((tab) => {
  const url = tab.url;
  if (!url) return false;
  if (includes.some((value) => !url.includes(value))) return false;
  if (excludes.some((value) => url.includes(value))) return false;
  return true;
});

if (filtered.length === 1) {
  process.stdout.write(JSON.stringify(filtered[0]));
  process.exit(0);
}

if (filtered.length === 0) {
  console.error("no tab matched the requested URL filters");
  process.exit(3);
}

console.error(JSON.stringify({
  error: "multiple_matches",
  matches: filtered,
}, null, 2));
process.exit(4);
' "$raw_json" "$explicit_target_id" "$includes_json" "$excludes_json"
}

print_snapshot() {
  local target_meta_json="$1"
  local raw_json="$2"
  local format="$3"
  node -e '
const target = JSON.parse(process.argv[1]);
const data = JSON.parse(process.argv[2]);
const format = process.argv[3];

function extractText(root) {
  const candidates = [
    root?.text,
    root?.snapshot?.text,
    root?.result?.text,
    root?.result?.snapshot?.text,
    root?.data?.text,
    root?.data?.snapshot?.text,
  ];
  for (const value of candidates) {
    if (typeof value === "string" && value.trim()) return value;
  }
  return "";
}

const text = extractText(data);
if (format === "json") {
  process.stdout.write(JSON.stringify({
    ok: true,
    action: "snapshot",
    target,
    text,
  }, null, 2) + "\n");
  process.exit(0);
}

const lines = [];
lines.push(`targetId: ${target.targetId}`);
lines.push(`title: ${target.title || "-"}`);
lines.push(`url: ${target.url || "-"}`);
lines.push("");
lines.push(text || "(empty snapshot)");
process.stdout.write(lines.join("\n") + "\n");
' "$target_meta_json" "$raw_json" "$format"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --token)
      TOKEN="${2:-}"
      shift 2
      ;;
    --app-home)
      APP_HOME="${2:-}"
      shift 2
      ;;
    --target-id)
      TARGET_ID="${2:-}"
      shift 2
      ;;
    --url-contains)
      URL_CONTAINS+=("${2:-}")
      shift 2
      ;;
    --url-not-contains)
      URL_NOT_CONTAINS+=("${2:-}")
      shift 2
      ;;
    --max-chars)
      MAX_CHARS="${2:-}"
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
      die "unknown arg: $1"
      ;;
  esac
done

case "$ACTION" in
  tabs|snapshot) ;;
  ""|-h|--help)
    usage
    exit 0
    ;;
  *)
    die "unknown action: $ACTION"
    ;;
esac

case "$FORMAT" in
  text|json) ;;
  *) die "invalid format: $FORMAT" ;;
esac

PROFILE="${PROFILE:-$(pref_get defaultBrowserProfile)}"
[[ -n "$PROFILE" ]] || PROFILE="$DEFAULT_PROFILE"
MAX_CHARS="${MAX_CHARS:-$(pref_get defaultSandboxSnapshotMaxChars)}"
[[ -n "$MAX_CHARS" ]] || MAX_CHARS="$DEFAULT_MAX_CHARS"
MAX_CHARS="$(normalize_positive_integer "$MAX_CHARS")"
APP_HOME="$(resolve_app_home "$APP_HOME")"

if [[ -z "$BASE_URL" ]]; then
  BASE_URL="${BROWSER_SANDBOX_BRIDGE_BASE_URL:-${MX_APP_RUNTIME_BASE_URL:-${RPA_RUNTIME_BASE_URL:-$(pref_get defaultLocalBaseUrl)}}}"
  [[ -n "$BASE_URL" ]] || BASE_URL="$DEFAULT_RUNTIME_BROWSER_URL"
else
  BASE_URL="$(normalize_endpoint "$BASE_URL")"
fi

if [[ "$BASE_URL" != */browser ]]; then
  BASE_URL="$(normalize_endpoint "$BASE_URL")"
fi

if [[ -z "$TOKEN" ]]; then
  TOKEN="$(discover_token "$APP_HOME")"
fi
[[ -n "$TOKEN" ]] || die "runtime management token not found; start with npm run dev:browser-sandbox or pass --token / --app-home explicitly"

TABS_JSON="$(bridge_post "$BASE_URL" "$TOKEN" "$(build_tabs_payload "$PROFILE")")"
node -e 'JSON.parse(process.argv[1]);' "$TABS_JSON" >/dev/null 2>&1 || die "browser bridge returned invalid JSON for tabs"

if [[ "$ACTION" == "tabs" ]]; then
  print_tabs "$TABS_JSON" "$FORMAT"
  exit 0
fi

if [[ -z "$TARGET_ID" && ${#URL_CONTAINS[@]} -eq 0 && ${#URL_NOT_CONTAINS[@]} -eq 0 ]]; then
  die "snapshot requires --target-id or at least one URL filter"
fi

URL_CONTAINS_JSON="$(printf '%s\n' "${URL_CONTAINS[@]:-}" | node -e 'const fs = require("node:fs"); const lines = fs.readFileSync(0, "utf8").split(/\n/).map((x) => x.trim()).filter(Boolean); process.stdout.write(JSON.stringify(lines));')"
URL_NOT_CONTAINS_JSON="$(printf '%s\n' "${URL_NOT_CONTAINS[@]:-}" | node -e 'const fs = require("node:fs"); const lines = fs.readFileSync(0, "utf8").split(/\n/).map((x) => x.trim()).filter(Boolean); process.stdout.write(JSON.stringify(lines));')"

if ! TARGET_META_JSON="$(resolve_target_id "$TABS_JSON" "$TARGET_ID" "$URL_CONTAINS_JSON" "$URL_NOT_CONTAINS_JSON" 2>&1)"; then
  printf '%s\n' "$TARGET_META_JSON" >&2
  exit 1
fi

RESOLVED_TARGET_ID="$(node -e 'const meta = JSON.parse(process.argv[1]); process.stdout.write(meta.targetId);' "$TARGET_META_JSON")"
SNAPSHOT_JSON="$(bridge_post "$BASE_URL" "$TOKEN" "$(build_snapshot_payload "$PROFILE" "$RESOLVED_TARGET_ID" "$MAX_CHARS")")"
node -e 'JSON.parse(process.argv[1]);' "$SNAPSHOT_JSON" >/dev/null 2>&1 || die "browser bridge returned invalid JSON for snapshot"

print_snapshot "$TARGET_META_JSON" "$SNAPSHOT_JSON" "$FORMAT"
