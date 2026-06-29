#!/usr/bin/env bash
#
# reap-callbacks.sh — MIAB orphan/stale callback reaper (deterministic, no LLM).
#
# Thin wrapper over `claw-callback.py sweep`. Marks `pending` bottles older than a
# configurable age as failed, appends a `fail` ledger event for each (so the observer
# surfaces the reap to Discord), purges the dead envelope, and sweeps dangling
# *.json.tmp write-handles left behind by interrupted atomic saves.
#
# Usage:
#   reap-callbacks.sh                 # reap bottles older than CALLBACK_TTL_MIN (default 120m)
#   reap-callbacks.sh --max-age 6h    # custom threshold; suffixes: s, m, h, d
#   reap-callbacks.sh --dry-run       # report what WOULD be reaped; change nothing
#
# Env:
#   CLAW_HOME          broker root (default: $HOME/.openclaw)
#   CALLBACK_TTL_MIN   default age threshold in minutes (default: 120)
#
# Exit non-zero on error so a scheduler (cron/launchd) can alert.
set -euo pipefail

export CLAW_HOME="${CLAW_HOME:-$HOME/.openclaw}"
CALLBACK_PY="$(dirname "$0")/bin/claw-callback.py"
CB_DIR="$CLAW_HOME/state/callbacks"
LOG_DIR="$CLAW_HOME/logs"
LOG="$LOG_DIR/callback-reaper.log"

DRY_RUN=0
MAX_AGE_RAW="${CALLBACK_TTL_MIN:-120}m"   # default expressed with a suffix for parse_age

# ----------------------------------------------------------------- arg parsing
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)  DRY_RUN=1; shift ;;
    --max-age)  MAX_AGE_RAW="${2:-}"; shift 2 ;;
    --max-age=*) MAX_AGE_RAW="${1#*=}"; shift ;;
    -h|--help)
      sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

# ----------------------------------------------------------------- helpers
# Convert a duration like 90s / 30m / 6h / 2d into whole minutes (rounded up, min 1).
parse_age_minutes() {
  local raw="$1" num unit
  num="${raw%[smhd]}"
  unit="${raw##*[0-9]}"
  case "$raw" in *[!0-9smhd]*) echo "invalid --max-age: $raw" >&2; exit 2 ;; esac
  [ -z "$num" ] && { echo "invalid --max-age: $raw" >&2; exit 2; }
  case "$unit" in
    s)  echo $(( (num + 59) / 60 )) ;;
    ""|m) echo "$num" ;;
    h)  echo $(( num * 60 )) ;;
    d)  echo $(( num * 60 * 24 )) ;;
    *)  echo "invalid --max-age unit: $unit" >&2; exit 2 ;;
  esac
}

TTL_MIN="$(parse_age_minutes "$MAX_AGE_RAW")"
[ "$TTL_MIN" -lt 1 ] && TTL_MIN=1

mkdir -p "$LOG_DIR"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ ! -f "$CALLBACK_PY" ]; then
  echo "[$ts] ERROR :: callback CLI not found at $CALLBACK_PY" >> "$LOG"
  echo "callback CLI not found at $CALLBACK_PY" >&2
  exit 1
fi

# ----------------------------------------------------------------- sweep
# --fail mutates+purges; dry-run omits it so sweep only reports stale candidates.
SWEEP_ARGS=(sweep --older-than "$TTL_MIN")
[ "$DRY_RUN" -eq 0 ] && SWEEP_ARGS+=(--fail)

if out="$(python3 "$CALLBACK_PY" "${SWEEP_ARGS[@]}" 2>&1)"; then
  reaped="$(printf '%s' "$out" | python3 -c \
    'import sys,json
try: print(json.load(sys.stdin).get("stale_count",0))
except Exception: print("?")' 2>/dev/null || echo "?")"

  # Cleanse dangling atomic-write handles left by interrupted saves.
  tmp_cleaned=0
  if [ "$DRY_RUN" -eq 0 ] && [ -d "$CB_DIR" ]; then
    while IFS= read -r -d '' f; do
      rm -f "$f" && tmp_cleaned=$((tmp_cleaned + 1))
    done < <(find "$CB_DIR" -maxdepth 1 -type f -name '*.json.tmp' -print0 2>/dev/null)
  fi

  mode="reap"; [ "$DRY_RUN" -eq 1 ] && mode="dry-run"
  if [ "$reaped" != "0" ]; then
    echo "[$ts] $mode reaped=$reaped tmp_cleaned=$tmp_cleaned ttl=${TTL_MIN}m :: $(printf '%s' "$out" | tr '\n' ' ')" >> "$LOG"
  else
    echo "[$ts] $mode ok reaped=0 tmp_cleaned=$tmp_cleaned ttl=${TTL_MIN}m" >> "$LOG"
  fi
  printf '%s\n' "$out"
else
  echo "[$ts] ERROR :: $out" >> "$LOG"
  printf '%s\n' "$out" >&2
  exit 1
fi
