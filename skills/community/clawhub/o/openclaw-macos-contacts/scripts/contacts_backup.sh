#!/usr/bin/env bash
set -euo pipefail
SRC="$HOME/Library/Application Support/AddressBook"
STATE_DIR="$HOME/.openclaw/state/macos-contacts"
mkdir -p "$STATE_DIR/backups"
TS="$(date +%Y%m%d-%H%M%S)"
DST="$STATE_DIR/backups/AddressBook-$TS"
mkdir -p "$DST"
cp -av "$SRC/AddressBook-v22.abcddb" "$DST/" >/dev/null
[ -f "$SRC/AddressBook-v22.abcddb-wal" ] && cp -av "$SRC/AddressBook-v22.abcddb-wal" "$DST/" >/dev/null || true
[ -f "$SRC/AddressBook-v22.abcddb-shm" ] && cp -av "$SRC/AddressBook-v22.abcddb-shm" "$DST/" >/dev/null || true
LATEST="$STATE_DIR/latest-backup.txt"
printf '%s\n' "$DST" > "$LATEST"
python3 - <<PY
import json, pathlib, time
state = pathlib.Path("$STATE_DIR")
manifest = state / 'backup-manifest.jsonl'
record = {
  'timestamp': '$TS',
  'path': '$DST',
  'created_at_epoch': int(time.time())
}
with manifest.open('a', encoding='utf-8') as f:
  f.write(json.dumps(record, ensure_ascii=False) + '\n')
print(json.dumps({'ok': True, 'backup_path': '$DST'}, ensure_ascii=False, indent=2))
PY
