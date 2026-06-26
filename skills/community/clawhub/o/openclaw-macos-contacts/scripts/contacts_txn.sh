#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo '{"ok":false,"error":"usage: contacts_txn.sh <command...>"}'
  exit 2
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_JSON="$($SCRIPT_DIR/contacts_backup.sh)"
BACKUP_PATH="$(printf '%s' "$BACKUP_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["backup_path"])')"
TMP_OUT="$(mktemp)"
TMP_ERR="$(mktemp)"
set +e
"$@" >"$TMP_OUT" 2>"$TMP_ERR"
CMD_CODE=$?
set -e
if [ $CMD_CODE -ne 0 ]; then
  ROLLBACK_JSON="$($SCRIPT_DIR/contacts_restore.sh "$BACKUP_PATH" 2>/dev/null || echo '{"ok":false,"error":"rollback_failed"}')"
  python3 - <<PY
import json, pathlib
out = pathlib.Path("$TMP_OUT").read_text(encoding='utf-8', errors='ignore')
err = pathlib.Path("$TMP_ERR").read_text(encoding='utf-8', errors='ignore')
rb = json.loads('''$ROLLBACK_JSON''') if '''$ROLLBACK_JSON'''.strip() else {"ok": False}
print(json.dumps({
  'ok': False,
  'backup_path': '$BACKUP_PATH',
  'rolled_back': bool(rb.get('ok')),
  'command_exit_code': $CMD_CODE,
  'stdout': out,
  'stderr': err,
}, ensure_ascii=False, indent=2))
PY
  exit $CMD_CODE
fi
python3 - <<PY
import json, pathlib
out = pathlib.Path("$TMP_OUT").read_text(encoding='utf-8', errors='ignore').strip()
parsed = None
if out:
  try:
    parsed = json.loads(out)
  except Exception:
    parsed = {'raw': out}
print(json.dumps({
  'ok': True,
  'backup_path': '$BACKUP_PATH',
  'rolled_back': False,
  'result': parsed,
}, ensure_ascii=False, indent=2))
PY
