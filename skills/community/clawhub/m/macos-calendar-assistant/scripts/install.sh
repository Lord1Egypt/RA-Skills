#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_PATH="$SKILL_DIR/config.json"

if [[ ! -f "$CONFIG_PATH" ]]; then
  cp "$SKILL_DIR/config.example.json" "$CONFIG_PATH"
  echo "Created $CONFIG_PATH (please review it)."
fi

CHECK_TIME=$(/usr/bin/python3 - <<'PY' "$CONFIG_PATH"
import json,sys
cfg=json.load(open(sys.argv[1]))
print(cfg.get('check_time','22:20'))
PY
)

HOUR="${CHECK_TIME%%:*}"
MIN="${CHECK_TIME##*:}"
if [[ -z "$HOUR" || -z "$MIN" ]]; then
  echo "Invalid check_time in config.json, expected HH:MM"
  exit 1
fi

chmod +x "$SCRIPT_DIR/calendar_clean_notify.sh" "$SCRIPT_DIR/calendar_clean.py" "$SCRIPT_DIR/upsert_event.py" "$SCRIPT_DIR/env_check.py" "$SCRIPT_DIR/regression_test.py"

TMPENV=$(mktemp /tmp/mca_env_check_XXXXXX)
trap 'rm -f "$TMPENV" "$TMPCRON"' EXIT

/usr/bin/python3 "$SCRIPT_DIR/env_check.py" >"$TMPENV"

echo "Environment check passed."

TMPCRON=$(mktemp /tmp/mca_cron_XXXXXX)
( crontab -l 2>/dev/null || true ) | sed '/calendar_clean_notify.sh/d' > "$TMPCRON"

echo "$MIN $HOUR * * * CAL_SKILL_CONFIG=$CONFIG_PATH $SCRIPT_DIR/calendar_clean_notify.sh" >> "$TMPCRON"
crontab "$TMPCRON"

echo "Installed cron: $MIN $HOUR * * * calendar_clean_notify.sh"
