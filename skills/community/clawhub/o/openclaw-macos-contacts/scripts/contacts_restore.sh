#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo '{"ok":false,"error":"usage: contacts_restore.sh <backup_dir>"}'
  exit 2
fi
BACKUP_DIR="$1"
SRC="$HOME/Library/Application Support/AddressBook"
if [ ! -d "$BACKUP_DIR" ]; then
  echo "{\"ok\":false,\"error\":\"backup_dir_not_found\"}"
  exit 2
fi
# Best effort: stop Contacts UI if open to reduce contention
osascript -e 'tell application "Contacts" to quit' >/dev/null 2>&1 || true
sleep 1
cp -av "$BACKUP_DIR/AddressBook-v22.abcddb" "$SRC/AddressBook-v22.abcddb" >/dev/null
[ -f "$BACKUP_DIR/AddressBook-v22.abcddb-wal" ] && cp -av "$BACKUP_DIR/AddressBook-v22.abcddb-wal" "$SRC/AddressBook-v22.abcddb-wal" >/dev/null || true
[ -f "$BACKUP_DIR/AddressBook-v22.abcddb-shm" ] && cp -av "$BACKUP_DIR/AddressBook-v22.abcddb-shm" "$SRC/AddressBook-v22.abcddb-shm" >/dev/null || true
python3 - <<PY
import json
print(json.dumps({'ok': True, 'restored_from': '$BACKUP_DIR'}, ensure_ascii=False, indent=2))
PY
