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
      echo "If no --map or --tool values are provided, enabled macOS-backed channels in --openclaw-config are used."
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
[[ "$WAKE_PORT" =~ ^[0-9]+$ ]] || { echo "wake-port must be an integer" >&2; exit 1; }
[[ "$WAKE_WAIT" =~ ^[0-9]+$ ]] || { echo "wake-wait must be an integer" >&2; exit 1; }
[[ "$WAKE_RETRIES" =~ ^[0-9]+$ ]] || { echo "wake-retries must be an integer" >&2; exit 1; }

TOOL_HOST_PAIRS=()
REQUESTED_TOOLS=()

array_len() {
  local name="$1"
  eval "echo \${#$name[@]}"
}

append_requested_tool() {
  local candidate="$1"
  local existing

  if [[ "$(array_len REQUESTED_TOOLS)" -gt 0 ]]; then
    for existing in "${REQUESTED_TOOLS[@]}"; do
      if [[ "$existing" == "$candidate" ]]; then
        return 0
      fi
    done
  fi

  REQUESTED_TOOLS+=("$candidate")
}

set_tool_host() {
  local tool="$1"
  local host="$2"
  local index=0
  local count
  local entry
  local key

  count="$(array_len TOOL_HOST_PAIRS)"
  while [[ "$index" -lt "$count" ]]; do
    entry="${TOOL_HOST_PAIRS[$index]}"
    key="${entry%%=*}"
    if [[ "$key" == "$tool" ]]; then
      TOOL_HOST_PAIRS[$index]="${tool}=${host}"
      return 0
    fi
    index=$((index + 1))
  done

  TOOL_HOST_PAIRS+=("${tool}=${host}")
}

get_tool_host() {
  local tool="$1"
  local entry
  local key
  local value
  local count
  local index=0

  count="$(array_len TOOL_HOST_PAIRS)"
  while [[ "$index" -lt "$count" ]]; do
    entry="${TOOL_HOST_PAIRS[$index]}"
    key="${entry%%=*}"
    value="${entry#*=}"
    if [[ "$key" == "$tool" ]]; then
      printf '%s' "$value"
      return 0
    fi
    index=$((index + 1))
  done

  return 1
}

discover_enabled_tools() {
  if [[ -n "$OPENCLAW_CONFIG" && -f "$OPENCLAW_CONFIG" ]] && command -v python3 >/dev/null 2>&1; then
    python3 - "$OPENCLAW_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
cfg = json.loads(config_path.read_text())
channels = cfg.get("channels") or {}

channel_by_tool = {
    "imsg": "imessage",
    "remindctl": "reminders",
    "memo": "notes",
    "things": "things",
    "peekaboo": "peekaboo",
}

def channel_enabled(channel):
    if not isinstance(channel, dict):
        return False
    enabled = channel.get("enabled")
    if isinstance(enabled, bool):
        return enabled
    return bool(channel)

for tool, channel_name in channel_by_tool.items():
    if channel_enabled(channels.get(channel_name)):
        print(tool)
PY
  fi
}

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

  if [[ "$(array_len WAKE_MAPS)" -gt 0 ]]; then
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
  fi

  return 1
}

if [[ "$(array_len MAPS)" -gt 0 ]]; then
  for mapping in "${MAPS[@]}"; do
    tool="${mapping%%=*}"
    host="${mapping#*=}"
    [[ -n "$tool" && -n "$host" && "$mapping" == *=* ]] || {
      echo "invalid map: $mapping" >&2
      exit 1
    }
    set_tool_host "$tool" "$host"
    append_requested_tool "$tool"
  done
fi

if [[ "$(array_len MAPS)" -eq 0 && "$(array_len TOOLS)" -eq 0 ]]; then
  while IFS= read -r tool; do
    [[ -n "$tool" ]] || continue
    TOOLS+=("$tool")
  done < <(discover_enabled_tools)
fi

[[ "$(array_len MAPS)" -gt 0 || "$(array_len TOOLS)" -gt 0 ]] || {
  echo "missing tool selection: provide --map tool=user@host, --tool TOOL, or enable supported channels in $OPENCLAW_CONFIG" >&2
  exit 1
}

if [[ "$(array_len TOOLS)" -gt 0 ]]; then
  for tool in "${TOOLS[@]}"; do
    [[ -n "$tool" ]] || {
      echo "invalid empty --tool value" >&2
      exit 1
    }
    append_requested_tool "$tool"
  done
fi

if [[ "$(array_len REQUESTED_TOOLS)" -gt 0 ]]; then
  for tool in "${REQUESTED_TOOLS[@]}"; do
    host="$(get_tool_host "$tool" || true)"
    if [[ -z "$host" ]]; then
      host="$(discover_host_for_tool "$tool" || true)"
    fi
    [[ -n "$host" ]] || {
      echo "missing host for tool: $tool" >&2
      echo "Provide --map $tool=user@host, --default-host user@host, or configure a matching remoteHost in $OPENCLAW_CONFIG." >&2
      exit 1
    }

    case "$tool" in
      imsg|remindctl|memo|things|peekaboo)
        remote_bin="/opt/homebrew/bin/$tool"
        ;;
      *)
        echo "unsupported macOS bridge tool: $tool" >&2
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
fi
