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
    print("# Auto-discovered Homebrew tool ownership map")
    print(f"# Source: {config_path}")
    print()
    default_host = hosts[0]
    print(f"brew={default_host}")
    print(f"gh={default_host}")
    print("# Add other tools as needed:")
    print(f"# claude={default_host}")
    print(f"# uv={default_host}")
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
# Recommended Homebrew tool ownership map

brew=mac-ops@mac-node.local
gh=mac-ops@mac-node.local
# claude=mac-ops@mac-node.local
# uv=mac-ops@mac-node.local

# Optional Wake-on-LAN map by host or user@host
# mac-node.local=AA:BB:CC:DD:EE:FF
EOF
