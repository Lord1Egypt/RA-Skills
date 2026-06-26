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

hosts = []
for channel in channels.values():
    if not isinstance(channel, dict):
        continue
    remote_host = channel.get("remoteHost")
    if isinstance(remote_host, str) and remote_host.strip():
        host = remote_host.strip()
        if host not in hosts:
            hosts.append(host)

if hosts:
    print("# Auto-discovered Mac tool ownership map")
    print(f"# Source: {config_path}")
    imsg_host = None
    imessage = channels.get("imessage")
    if isinstance(imessage, dict):
        remote_host = imessage.get("remoteHost")
        if isinstance(remote_host, str) and remote_host.strip():
            imsg_host = remote_host.strip()

    default_host = hosts[0]
    print()
    print(f"imsg={imsg_host or default_host}")
    print(f"memo={default_host}")
    print(f"things={default_host}")
    print(f"remindctl={default_host}")
    print(f"gh={default_host}")
    print(f"brew={default_host}")
    print(f"peekaboo={default_host}")
    print()
    print("# Optional Wake-on-LAN map by host or user@host")
    for host in hosts:
        print(f"# {host}=AA:BB:CC:DD:EE:FF")
    raise SystemExit(0)
PY
  then
    exit 0
  fi
fi

cat <<'EOF'
# Recommended Mac tool ownership map

imsg=mac-ops@mac-messages.local
memo=mac-ops@mac-messages.local
things=mac-ops@mac-messages.local

remindctl=mac-ops@mac-tools.local
gh=mac-ops@mac-tools.local
brew=mac-ops@mac-tools.local
peekaboo=mac-ops@mac-tools.local

# Optional Wake-on-LAN map by host or user@host
# mac-messages.local=AA:BB:CC:DD:EE:FF
# mac-ops@mac-tools.local=11:22:33:44:55:66
EOF
