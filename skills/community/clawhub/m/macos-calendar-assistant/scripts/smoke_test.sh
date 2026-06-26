#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TMP_CALS=$(mktemp /tmp/mca_calendars_XXXXXX)
TMP_EVTS=$(mktemp /tmp/mca_events_XXXXXX)
TMP_CLEAN=$(mktemp /tmp/mca_clean_XXXXXX)
TMP_UPSERT=$(mktemp /tmp/mca_upsert_XXXXXX)

cleanup() { rm -f "$TMP_CALS" "$TMP_EVTS" "$TMP_CLEAN" "$TMP_UPSERT"; }
trap cleanup EXIT

VALS=(${(s: :)$(python3 - <<'PY' "$SCRIPT_DIR"
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import json,sys
script_dir=Path(sys.argv[1])
cfg={}
cp=script_dir.parent/'config.json'
if cp.exists():
    try: cfg=json.loads(cp.read_text())
    except: cfg={}
tz=ZoneInfo(cfg.get('timezone','Asia/Shanghai'))
now=datetime.now(tz).replace(second=0,microsecond=0)
day=(now+timedelta(days=1)).strftime('%Y-%m-%d')
start_day=f"{day}T00:00:00{now.strftime('%z')[:3]}:{now.strftime('%z')[3:]}"
end_day=f"{day}T23:59:59{now.strftime('%z')[:3]}:{now.strftime('%z')[3:]}"
up_start=(now+timedelta(days=2)).replace(hour=10,minute=0)
up_end=up_start+timedelta(minutes=30)
clean_start=(now-timedelta(days=3)).replace(hour=0,minute=0)
clean_end=(now+timedelta(days=3)).replace(hour=23,minute=59)
fmt=lambda d:d.isoformat(timespec='seconds')
print(start_day, end_day, fmt(up_start), fmt(up_end), fmt(clean_start), fmt(clean_end))
PY
)})

START_DAY=${VALS[1]}
END_DAY=${VALS[2]}
UPSERT_START=${VALS[3]}
UPSERT_END=${VALS[4]}
CLEAN_START=${VALS[5]}
CLEAN_END=${VALS[6]}

echo "[1/4] list_calendars.swift"
swift "$SCRIPT_DIR/list_calendars.swift" >"$TMP_CALS"

echo "[2/4] list_events.swift"
swift "$SCRIPT_DIR/list_events.swift" "$START_DAY" "$END_DAY" >"$TMP_EVTS"

echo "[3/4] upsert_event.py --dry-run"
python3 "$SCRIPT_DIR/upsert_event.py" \
  --title "[测试] mca smoke" \
  --start "$UPSERT_START" \
  --end "$UPSERT_END" \
  --calendar "产品" \
  --notes "smoke" \
  --alarm-minutes 10 \
  --dry-run >"$TMP_UPSERT"

echo "[4/4] calendar_clean.py"
python3 "$SCRIPT_DIR/calendar_clean.py" \
  --start "$CLEAN_START" \
  --end "$CLEAN_END" >"$TMP_CLEAN"

echo "---- smoke outputs ----"
cat "$TMP_UPSERT"
python3 - "$TMP_CALS" "$TMP_EVTS" "$TMP_CLEAN" <<'PY'
import json,sys
for p in sys.argv[1:]:
    try:
        json.load(open(p))
        print('OK JSON', p)
    except Exception as e:
        print('BAD JSON', p, e)
        raise
print('SMOKE_TEST_OK')
PY
