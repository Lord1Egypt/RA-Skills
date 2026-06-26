#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_WRAPPER="$SCRIPT_DIR/install-wrapper.sh"

TARGET_DIR=""
SSH_KEY=""
KNOWN_HOSTS=""
OPENCLAW_CONFIG=""
DEFAULT_HOST=""
MAPS=()
TOOLS=()
WAKE_MAPS=()
WAKE_BROADCAST="255.255.255.255"
WAKE_PORT="9"
WAKE_WAIT="20"
WAKE_RETRIES="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --map) MAPS+=("${2:-}"); shift 2 ;;
    --tool) TOOLS+=("${2:-}"); shift 2 ;;
    --ssh-key) SSH_KEY="${2:-}"; shift 2 ;;
    --known-hosts) KNOWN_HOSTS="${2:-}"; shift 2 ;;
    --openclaw-config) OPENCLAW_CONFIG="${2:-}"; shift 2 ;;
    --default-host) DEFAULT_HOST="${2:-}"; shift 2 ;;
    --wake-map) WAKE_MAPS+=("${2:-}"); shift 2 ;;
    --wake-broadcast) WAKE_BROADCAST="${2:-}"; shift 2 ;;
    --wake-port) WAKE_PORT="${2:-}"; shift 2 ;;
    --wake-wait) WAKE_WAIT="${2:-}"; shift 2 ;;
    --wake-retries) WAKE_RETRIES="${2:-}"; shift 2 ;;
    -h|--help)
      echo "usage: install-macos-pack.sh --target-dir DIR [--map tool=user@host ...] [--tool TOOL ...] [--openclaw-config FILE] [--default-host user@host] [--wake-map host-or-user@host=AA:BB:CC:DD:EE:FF ...] [--wake-broadcast IP] [--wake-port PORT] [--wake-wait SECONDS] [--wake-retries N] [--ssh-key KEY] [--known-hosts FILE]"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

[[ -n "$TARGET_DIR" ]] || { echo "missing --target-dir" >&2; exit 1; }
if [[ -z "$OPENCLAW_CONFIG" && -f "${HOME}/.openclaw/openclaw.json" ]]; then
  OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
fi
[[ "${#MAPS[@]}" -gt 0 || "${#TOOLS[@]}" -gt 0 ]] || {
  echo "missing tool selection: provide --map tool=user@host and/or --tool TOOL" >&2
  exit 1
}
[[ "$WAKE_PORT" =~ ^[0-9]+$ ]] || { echo "wake-port must be an integer" >&2; exit 1; }
[[ "$WAKE_WAIT" =~ ^[0-9]+$ ]] || { echo "wake-wait must be an integer" >&2; exit 1; }
[[ "$WAKE_RETRIES" =~ ^[0-9]+$ ]] || { echo "wake-retries must be an integer" >&2; exit 1; }

declare -A TOOL_HOSTS=()
declare -A SEEN_TOOLS=()
REQUESTED_TOOLS=()

discover_host_for_tool() {
  local tool="$1"

  if [[ -n "$OPENCLAW_CONFIG" && -f "$OPENCLAW_CONFIG" ]] && command -v python3 >/dev/null 2>&1; then
    local discovered
    discovered="$(python3 - "$OPENCLAW_CONFIG" "$tool" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
tool = sys.argv[2]
cfg = json.loads(config_path.read_text())
channels = cfg.get("channels") or {}

channel_by_tool = {
    "imsg": "imessage",
    "remindctl": "reminders",
    "memo": "notes",
    "things": "things",
    "peekaboo": "peekaboo",
}

channel_name = channel_by_tool.get(tool)
if channel_name:
    channel = channels.get(channel_name) or {}
    remote_host = channel.get("remoteHost")
    if isinstance(remote_host, str) and remote_host.strip():
        print(remote_host.strip())
        raise SystemExit(0)

hosts = []
for channel in channels.values():
    if not isinstance(channel, dict):
        continue
    remote_host = channel.get("remoteHost")
    if isinstance(remote_host, str) and remote_host.strip():
        host = remote_host.strip()
        if host not in hosts:
            hosts.append(host)

if len(hosts) == 1:
    print(hosts[0])
PY
)"
    if [[ -n "$discovered" ]]; then
      printf '%s' "$discovered"
      return 0
    fi
  fi

  if [[ -n "$DEFAULT_HOST" ]]; then
    printf '%s' "$DEFAULT_HOST"
    return 0
  fi

  return 1
}

lookup_wake_mac() {
  local host="$1"
  local host_only="${host#*@}"
  local mapping key value

  for mapping in "${WAKE_MAPS[@]}"; do
    [[ "$mapping" == *=* ]] || {
      echo "invalid wake-map: $mapping" >&2
      exit 1
    }
    key="${mapping%%=*}"
    value="${mapping#*=}"
    [[ -n "$key" && -n "$value" ]] || {
      echo "invalid wake-map: $mapping" >&2
      exit 1
    }
    if [[ "$key" == "$host" || "$key" == "$host_only" ]]; then
      printf '%s' "$value"
      return 0
    fi
  done

  return 1
}

for mapping in "${MAPS[@]}"; do
  tool="${mapping%%=*}"
  host="${mapping#*=}"
  [[ -n "$tool" && -n "$host" && "$mapping" == *=* ]] || {
    echo "invalid map: $mapping" >&2
    exit 1
  }
  TOOL_HOSTS["$tool"]="$host"
  if [[ -z "${SEEN_TOOLS[$tool]:-}" ]]; then
    REQUESTED_TOOLS+=("$tool")
    SEEN_TOOLS["$tool"]=1
  fi
done

for tool in "${TOOLS[@]}"; do
  [[ -n "$tool" ]] || {
    echo "invalid empty --tool value" >&2
    exit 1
  }
  if [[ -z "${SEEN_TOOLS[$tool]:-}" ]]; then
    REQUESTED_TOOLS+=("$tool")
    SEEN_TOOLS["$tool"]=1
  fi
done

for tool in "${REQUESTED_TOOLS[@]}"; do
  host="${TOOL_HOSTS[$tool]:-}"
  if [[ -z "$host" ]]; then
    host="$(discover_host_for_tool "$tool" || true)"
  fi
  [[ -n "$host" ]] || {
    echo "missing host for tool: $tool" >&2
    echo "Provide --map $tool=user@host, --default-host user@host, or configure a matching remoteHost in $OPENCLAW_CONFIG." >&2
    exit 1
  }

  case "$tool" in
    imsg|remindctl|memo|things|peekaboo|brew|gh)
      remote_bin="/opt/homebrew/bin/$tool"
      ;;
    *)
      echo "unsupported tool: $tool" >&2
      exit 1
      ;;
  esac

  wake_mac=""
  if wake_mac="$(lookup_wake_mac "$host")"; then
    :
  fi

  cmd=(
    "$INSTALL_WRAPPER"
    --name "$tool"
    --host "$host"
    --remote-bin "$remote_bin"
    --target-dir "$TARGET_DIR"
  )
  [[ -n "$SSH_KEY" ]] && cmd+=(--ssh-key "$SSH_KEY")
  [[ -n "$KNOWN_HOSTS" ]] && cmd+=(--known-hosts "$KNOWN_HOSTS")
  if [[ -n "$wake_mac" ]]; then
    cmd+=(
      --wake-mac "$wake_mac"
      --wake-broadcast "$WAKE_BROADCAST"
      --wake-port "$WAKE_PORT"
      --wake-wait "$WAKE_WAIT"
      --wake-retries "$WAKE_RETRIES"
    )
  fi
  "${cmd[@]}"
done
