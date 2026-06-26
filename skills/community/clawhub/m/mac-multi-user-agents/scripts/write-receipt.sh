#!/usr/bin/env bash
set -euo pipefail

ACTION=""
STATUS=""
DETAIL=""
TARGET="$(hostname -s)"
RECEIPT_ROOT="${RECEIPT_ROOT:-$PWD/.mac-multi-user-agents/receipts}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --action) ACTION="${2:-}"; shift 2 ;;
    --status) STATUS="${2:-}"; shift 2 ;;
    --detail) DETAIL="${2:-}"; shift 2 ;;
    --target) TARGET="${2:-}"; shift 2 ;;
    --root) RECEIPT_ROOT="${2:-}"; shift 2 ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$ACTION" || -z "$STATUS" ]]; then
  echo "usage: write-receipt.sh --action NAME --status STATUS [--detail TEXT] [--target NAME] [--root DIR]" >&2
  exit 1
fi

mkdir -p "$RECEIPT_ROOT"
receipt_file="$RECEIPT_ROOT/$(date +%F).jsonl"

python3 - "$receipt_file" "$ACTION" "$STATUS" "$DETAIL" "$TARGET" <<'PY'
import json
import sys
from datetime import datetime, timezone

path, action, status, detail, target = sys.argv[1:]
payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "action": action,
    "status": status,
    "detail": detail,
    "target": target,
}
with open(path, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=True) + "\n")
print(path)
PY
