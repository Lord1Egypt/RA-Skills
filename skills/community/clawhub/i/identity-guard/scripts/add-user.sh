#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../identities.json"

usage() {
  cat <<EOF_USAGE
Usage: ./add-user.sh <sender_id> [channel]
If channel is omitted, the sender is added to global_allowlist.
EOF_USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

SENDER_ID="$1"
CHANNEL="${2:-}"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Missing ${CONFIG_FILE}. Run ./scripts/init.sh first." >&2
  exit 1
fi

python3 - "${CONFIG_FILE}" "${SENDER_ID}" "${CHANNEL}" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
sender = sys.argv[2]
channel = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None

try:
    data = json.loads(config_path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"Invalid JSON in {config_path}: {exc}", file=sys.stderr)
    sys.exit(1)

channels = data.setdefault("channels", {})

if channel:
    ch = channels.setdefault(channel, {"master_id": "", "allowlist": []})
    allowlist = ch.setdefault("allowlist", [])
    if sender not in allowlist:
        allowlist.append(sender)
else:
    global_allowlist = data.setdefault("global_allowlist", [])
    if sender not in global_allowlist:
        global_allowlist.append(sender)

config_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

echo "Updated ${CONFIG_FILE}"
