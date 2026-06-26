#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 2 ]; then
  echo '{"ok":false,"error":"usage: contacts_dedupe.sh <keep_identifier> <drop_identifier> [drop_identifier...]"}'
  exit 2
fi
KEEP="$1"
shift
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OPS=()
for DROP in "$@"; do
  if [ "$DROP" = "$KEEP" ]; then
    continue
  fi
  JSON="$(bash "$SCRIPT_DIR/contacts_txn.sh" swift "$SCRIPT_DIR/contacts_swift.swift" delete --identifier "$DROP")"
  OPS+=("$JSON")
done
python3 - <<PY
import json
ops = [json.loads(x) for x in [$(printf '"%s",' "${OPS[@]}" | sed 's/,$//')]] if "${#OPS[@]}" != "0" else []
print(json.dumps({
  'ok': True,
  'kept_identifier': '$KEEP',
  'deleted_count': len(ops),
  'operations': ops,
}, ensure_ascii=False, indent=2))
PY
