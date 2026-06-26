#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_PATH="${CAL_SKILL_CONFIG:-$SKILL_DIR/config.json}"

# Defaults
LOOKBACK_DAYS=1
LOOKAHEAD_DAYS=0
OUT_DIR="$HOME/clawd/memory"
NOTIFY_ENABLED=true
NOTIFY_TITLE="MemoryXBOT 日程提醒"
TIMEZONE="Asia/Shanghai"

if [[ -f "$CONFIG_PATH" ]]; then
  LOOKBACK_DAYS=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys
cfg=json.load(open(sys.argv[1]))
print(int(cfg.get('lookback_days',1)))
PY
)
  LOOKAHEAD_DAYS=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys
cfg=json.load(open(sys.argv[1]))
print(int(cfg.get('lookahead_days',0)))
PY
)
  OUT_DIR=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys,os
cfg=json.load(open(sys.argv[1]))
print(os.path.expanduser(cfg.get('output_dir','~/clawd/memory')))
PY
)
  NOTIFY_ENABLED=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys
cfg=json.load(open(sys.argv[1]))
notify=cfg.get('notification',{}) if isinstance(cfg.get('notification',{}),dict) else {}
print('true' if notify.get('enabled',True) else 'false')
PY
)
  NOTIFY_TITLE=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys
cfg=json.load(open(sys.argv[1]))
notify=cfg.get('notification',{}) if isinstance(cfg.get('notification',{}),dict) else {}
print(str(notify.get('title','MemoryXBOT 日程提醒')))
PY
)
  TIMEZONE=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys
cfg=json.load(open(sys.argv[1]))
print(str(cfg.get('timezone','Asia/Shanghai')))
PY
)
fi

mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/calendar-clean-last.json"
ALERT="$OUT_DIR/calendar-clean-alert.txt"

START=$(/usr/bin/python3 - <<'PY' "$TIMEZONE" "$LOOKBACK_DAYS"
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
z=ZoneInfo(sys.argv[1])
lookback=int(sys.argv[2])
d=(datetime.now(z)-timedelta(days=lookback)).strftime('%Y-%m-%d')
print(f"{d}T00:00:00{datetime.now(z).strftime('%z')[:3]}:{datetime.now(z).strftime('%z')[3:]}")
PY
)
END=$(/usr/bin/python3 - <<'PY' "$TIMEZONE" "$LOOKAHEAD_DAYS"
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
z=ZoneInfo(sys.argv[1])
lookahead=int(sys.argv[2])
now=datetime.now(z)
d=(now+timedelta(days=lookahead)).strftime('%Y-%m-%d')
o=now.strftime('%z')
print(f"{d}T23:59:59{o[:3]}:{o[3:]}")
PY
)

/usr/bin/python3 "$SCRIPT_DIR/calendar_clean.py" --start "$START" --end "$END" > "$OUT" 2>&1 || true

CANDIDATES=$(/usr/bin/python3 - <<'PY' "$OUT"
import json,sys
try:
    data=json.load(open(sys.argv[1]))
    print(int(data.get('delete_candidates',0)))
except Exception:
    print(0)
PY
)

if [[ "$CANDIDATES" -gt 0 ]]; then
  MSG="Calendar发现 ${CANDIDATES} 条重复候选，建议清理"
  echo "$(date '+%Y-%m-%d %H:%M:%S') $MSG" > "$ALERT"
  if [[ "$NOTIFY_ENABLED" == "true" ]]; then
    /usr/bin/osascript -e "display notification \"$MSG\" with title \"$NOTIFY_TITLE\""
  fi
fi
