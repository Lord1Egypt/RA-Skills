#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_CONFIG="${1:-${OPENCLAW_CONFIG:-${HOME}/.openclaw/openclaw.json}}"

if [[ -f "$OPENCLAW_CONFIG" ]] && command -v python3 >/dev/null 2>&1; then
  if python3 - "$OPENCLAW_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
cfg = json.loads(config_path.read_text())
channels = cfg.get("channels") or {}

channel_by_tool = [
    ("imsg", "imessage"),
    ("remindctl", "reminders"),
    ("memo", "notes"),
    ("things", "things"),
    ("peekaboo", "peekaboo"),
]

def channel_enabled(channel):
    if not isinstance(channel, dict):
        return False
    enabled = channel.get("enabled")
    if isinstance(enabled, bool):
        return enabled
    return bool(channel)

entries = []
hosts = []
for tool, channel_name in channel_by_tool:
    channel = channels.get(channel_name)
    if not channel_enabled(channel):
        continue
    remote_host = channel.get("remoteHost") if isinstance(channel, dict) else None
    host = remote_host.strip() if isinstance(remote_host, str) and remote_host.strip() else None
    if host and host not in hosts:
        hosts.append(host)
    entries.append((tool, host))

if entries:
    print("# Auto-discovered macOS tool ownership map for enabled channels")
    print(f"# Source: {config_path}")
    print()
    default_host = hosts[0] if len(hosts) == 1 else "mac-ops@mac-node.local"
    for tool, host in entries:
        print(f"{tool}={host or default_host}")
    print()
    print("# Optional Wake-on-LAN map by host or user@host")
    for host in hosts or [default_host]:
        print(f"# {host}=AA:BB:CC:DD:EE:FF")
    raise SystemExit(0)
PY
  then
    exit 0
  fi
fi

cat <<'EOF'
# Recommended macOS tool ownership map

imsg=mac-ops@mac-node.local
remindctl=mac-ops@mac-node.local
memo=mac-ops@mac-node.local
things=mac-ops@mac-node.local
peekaboo=mac-ops@mac-node.local

# Optional Wake-on-LAN map by host or user@host
# mac-node.local=AA:BB:CC:DD:EE:FF
EOF
