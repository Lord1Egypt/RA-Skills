#!/usr/bin/env bash
set -euo pipefail

PLUGIN_SPEC="${PLUGIN_SPEC:-@art_style666/hi-light}"
PLUGIN_ID="${PLUGIN_ID:-hi-light}"
DEFAULT_WS_URL="wss://open.guangfan.com/open-apis/device-agent/v1/websocket"
DEFAULT_DM_POLICY="open"
DEFAULT_ALLOW_FROM='["*"]'

API_KEY=""
WS_URL="$DEFAULT_WS_URL"
DM_POLICY="$DEFAULT_DM_POLICY"
ALLOW_FROM="$DEFAULT_ALLOW_FROM"
INSTALL_PLUGIN=1
RESTART_GATEWAY=1
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  setup_hi_light.sh --api-key <token> [options]

Options:
  --api-key <token>      Required HiLight API key
  --ws-url <url>         WebSocket URL (default: official HiLight URL)
  --dm-policy <policy>   DM policy (default: open)
  --allow-from <json>    JSON array for allowFrom (default: ["*"])
  --skip-install         Skip plugin installation and only update config
  --no-restart           Skip gateway restart
  --dry-run              Print actions without changing OpenClaw state
  -h, --help             Show help
EOF
}

fail() {
  echo "[ERROR] $*" >&2
  exit 1
}

need_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || fail "Missing required command: $cmd"
}

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] '
    printf '%q ' "$@"
    printf '\n'
    return 0
  fi
  "$@"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --api-key)
        [[ $# -ge 2 ]] || fail "Missing value for --api-key"
        API_KEY="$2"
        shift 2
        ;;
      --ws-url)
        [[ $# -ge 2 ]] || fail "Missing value for --ws-url"
        WS_URL="$2"
        shift 2
        ;;
      --dm-policy)
        [[ $# -ge 2 ]] || fail "Missing value for --dm-policy"
        DM_POLICY="$2"
        shift 2
        ;;
      --allow-from)
        [[ $# -ge 2 ]] || fail "Missing value for --allow-from"
        ALLOW_FROM="$2"
        shift 2
        ;;
      --skip-install)
        INSTALL_PLUGIN=0
        shift
        ;;
      --no-restart)
        RESTART_GATEWAY=0
        shift
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        fail "Unknown argument: $1"
        ;;
    esac
  done
}

main() {
  parse_args "$@"

  [[ -n "$API_KEY" ]] || fail "--api-key is required"

  need_cmd openclaw
  need_cmd node

  echo "[INFO] Using config file: $(openclaw config file)"

  if [[ "$INSTALL_PLUGIN" -eq 1 ]]; then
    echo "[INFO] Installing plugin ${PLUGIN_SPEC}"
    run_cmd openclaw plugins install "$PLUGIN_SPEC"
  else
    echo "[INFO] Skipping plugin install"
  fi

  echo "[INFO] Enabling plugin ${PLUGIN_ID}"
  run_cmd openclaw plugins enable "$PLUGIN_ID"

  echo "[INFO] Writing hi-light channel config"
  run_cmd openclaw config set 'channels["hi-light"].enabled' true
  run_cmd openclaw config set 'channels["hi-light"].wsUrl' "$WS_URL"
  run_cmd openclaw config set 'channels["hi-light"].authToken' "$API_KEY"
  run_cmd openclaw config set 'channels["hi-light"].dmPolicy' "$DM_POLICY"
  run_cmd openclaw config set 'channels["hi-light"].allowFrom' "$ALLOW_FROM"

  echo "[INFO] Validating config"
  run_cmd openclaw config validate

  if [[ "$RESTART_GATEWAY" -eq 1 ]]; then
    echo "[INFO] Restarting gateway"
    run_cmd openclaw gateway restart
  else
    echo "[INFO] Skipping gateway restart"
  fi

  echo "[INFO] Current hi-light channel summary"
  run_cmd openclaw config get 'channels["hi-light"]' --json
  echo "[OK] HiLight setup complete"
}

main "$@"
