#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SOURCE="local"
VALUE=""
USE_LINK="false"
BIND_SLOT="false"
RESTART_GATEWAY="false"

usage() {
  cat <<'USAGE'
Usage:
  install_plugin.sh [options]

Options:
  --source <local|spec|archive>   Install source type (default: local)
  --value <path-or-spec>          Path/spec value (required for spec/archive)
  --link                          Pass --link for local path installs
  --bind-slot                     Set plugins.slots.memory=evermemory
  --restart-gateway               Restart gateway after install/config changes
  -h, --help                      Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      SOURCE="${2:-}"
      shift 2
      ;;
    --value)
      VALUE="${2:-}"
      shift 2
      ;;
    --link)
      USE_LINK="true"
      shift
      ;;
    --bind-slot)
      BIND_SLOT="true"
      shift
      ;;
    --restart-gateway)
      RESTART_GATEWAY="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unsupported argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

install_target=""
case "$SOURCE" in
  local)
    install_target="${VALUE:-$ROOT_DIR}"
    ;;
  spec|archive)
    if [[ -z "$VALUE" ]]; then
      echo "[ERROR] --value is required when --source is '$SOURCE'" >&2
      exit 1
    fi
    install_target="$VALUE"
    ;;
  *)
    echo "[ERROR] Invalid --source value: $SOURCE" >&2
    exit 1
    ;;
esac

cmd=(openclaw plugins install "$install_target")
if [[ "$SOURCE" == "local" && "$USE_LINK" == "true" ]]; then
  cmd+=(--link)
fi

echo "[INFO] Installing plugin: ${cmd[*]}"
"${cmd[@]}"

echo "[INFO] Enabling plugin entry: evermemory"
openclaw plugins enable evermemory || true

if [[ "$BIND_SLOT" == "true" ]]; then
  echo "[INFO] Binding memory slot to evermemory"
  openclaw config set plugins.slots.memory evermemory
fi

if [[ "$RESTART_GATEWAY" == "true" ]]; then
  echo "[INFO] Restarting gateway"
  openclaw gateway restart
fi

echo "[INFO] Verifying install"
openclaw plugins info evermemory
openclaw gateway status

echo "[PASS] EverMemory plugin install flow completed."
