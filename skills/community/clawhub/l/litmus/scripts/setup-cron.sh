#!/usr/bin/env bash
# setup-cron.sh — register the Litmus cron jobs via the OpenClaw cron tool.
#
# All times are configurable. Defaults match the standard circadian schedule.
# The onboarding agent reads these from config.json and passes them here.
#
# Usage:
#   bash scripts/setup-cron.sh --timezone "America/New_York"
#   bash scripts/setup-cron.sh --timezone "Europe/London" \
#     --leisure-start 01:00 --synthesizer-time 02:30 --dawn-time 04:00 \
#     --digest-time 07:00 --director-hours 1 --watchdog-minutes 20
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
BASE_DIR="${LITMUS_BASE:-$HOME/.litmus}"
SHARED_DIR="$BASE_DIR/shared"
REFERENCES_DIR="$REPO_DIR/references"

# --- Defaults ---
TZ="UTC"
LEISURE_START="03:00"
SYNTHESIZER_TIME="04:00"
DAWN_TIME="06:00"
DIGEST_TIME="08:00"
DIRECTOR_HOURS=2
WATCHDOG_MINUTES=30

while [[ $# -gt 0 ]]; do
  case "$1" in
    --timezone)         TZ="$2";               shift 2 ;;
    --leisure-start)    LEISURE_START="$2";    shift 2 ;;
    --synthesizer-time) SYNTHESIZER_TIME="$2"; shift 2 ;;
    --dawn-time)        DAWN_TIME="$2";        shift 2 ;;
    --digest-time)      DIGEST_TIME="$2";      shift 2 ;;
    --director-hours)   DIRECTOR_HOURS="$2";   shift 2 ;;
    --watchdog-minutes) WATCHDOG_MINUTES="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# --- Helper: parse HH:MM → hour and minute integers ---
parse_hhmm() {
  local t="$1"
  local h m
  h=$(echo "$t" | cut -d: -f1 | sed 's/^0*//' )
  m=$(echo "$t" | cut -d: -f2 | sed 's/^0*//' )
  H="${h:-0}"
  M="${m:-0}"
}

# Parse each time
parse_hhmm "$LEISURE_START";    L_H=$H; L_M=$M
parse_hhmm "$SYNTHESIZER_TIME"; S_H=$H; S_M=$M
parse_hhmm "$DAWN_TIME";        D_H=$H; D_M=$M
parse_hhmm "$DIGEST_TIME";      DG_H=$H; DG_M=$M

# --- Watchdog interval: convert minutes → milliseconds ---
WATCHDOG_MS=$(( WATCHDOG_MINUTES * 60000 ))

# --- Director research-hours range: dawn → leisure_start (wraps midnight) ---
# e.g. dawn=06:00, leisure=03:00 → "0 */2 6-2 * * *"
# We express the hour range as "DAWN_H through LEISURE_H (exclusive)"
# If LEISURE_H > DAWN_H (leisure starts after dawn, unusual) we warn.
if [ "$D_H" -lt "$L_H" ] || { [ "$D_H" -eq "$L_H" ] && [ "$D_M" -lt "$L_M" ]; }; then
  # Normal case: dawn before leisure (e.g. dawn 06:00, leisure 03:00 next night)
  # Director runs during hours D_H through L_H
  DIRECTOR_RANGE="${D_H}-${L_H}"
else
  # Unusual: leisure starts before dawn — director runs all day except leisure window
  DIRECTOR_RANGE="*"
fi

# Build cron expressions
LEISURE_CRON="0 $L_M $L_H * * *"
SYNTH_CRON="0 $S_M $S_H * * *"
DAWN_CRON="0 $D_M $D_H * * *"
DIGEST_CRON="0 $DG_M $DG_H * * *"
DIRECTOR_CRON="0 */${DIRECTOR_HOURS} ${DIRECTOR_RANGE} * * *"

echo "=== Litmus Cron Setup ==="
echo "Timezone:       $TZ"
echo "Leisure start:  $LEISURE_START  (workers enter creative mode)"
echo "Synthesizer:    $SYNTHESIZER_TIME  (distills knowledge into skills library)"
echo "Dawn:           $DAWN_TIME  (workers wake, experiment queue loaded)"
echo "Digest:         $DIGEST_TIME  (morning briefing delivered to you)"
echo "Director:       every ${DIRECTOR_HOURS}h during ${DIRECTOR_RANGE}:xx research hours"
echo "Watchdog:       every ${WATCHDOG_MINUTES} min"
echo ""
echo "Ask your OpenClaw agent to run these 6 cron tool calls:"
echo ""

cat << EOF
============================================================
CRON 1: Director (every ${DIRECTOR_HOURS}h during research hours)
Expr: "${DIRECTOR_CRON}"
============================================================
cron action:"add" job:{
  "name": "litmus-director",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "${DIRECTOR_CRON}", "tz": "$TZ" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the Litmus Director cycle. Full instructions in $REFERENCES_DIR/director.md — read that file first. Read attempts from $SHARED_DIR/attempts/ for all metrics."
  },
  "delivery": { "mode": "none" }
}

============================================================
CRON 2: Leisure Mode ($LEISURE_START — enters creative thinking mode)
Expr: "${LEISURE_CRON}"
============================================================
cron action:"add" job:{
  "name": "litmus-leisure",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "${LEISURE_CRON}", "tz": "$TZ" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the Litmus leisure session. Full instructions in $REFERENCES_DIR/leisure.md — read that file first. Write structured YAML-frontmatter notes to $SHARED_DIR/notes/. The Synthesizer reads these at $SYNTHESIZER_TIME."
  },
  "delivery": { "mode": "none" }
}

============================================================
CRON 3: Synthesizer ($SYNTHESIZER_TIME — distills knowledge into skills library)
Expr: "${SYNTH_CRON}"
============================================================
cron action:"add" job:{
  "name": "litmus-synthesizer",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "${SYNTH_CRON}", "tz": "$TZ" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the Litmus Synthesizer. Full instructions in $REFERENCES_DIR/synthesizer.md — read that file first. Read all attempts from $SHARED_DIR/attempts/, all notes from $SHARED_DIR/notes/, extract validated skills to $SHARED_DIR/skills/, write research synthesis."
  },
  "delivery": { "mode": "none" }
}

============================================================
CRON 4: Dawn ($DAWN_TIME — wakes workers, queues experiments)
Expr: "${DAWN_CRON}"
============================================================
cron action:"add" job:{
  "name": "litmus-dawn",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "${DAWN_CRON}", "tz": "$TZ" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the Litmus dawn session. Full instructions in $REFERENCES_DIR/dawn.md — read that file first. Wake workers from leisure mode and queue overnight ideas from the synthesizer output."
  },
  "delivery": { "mode": "none" }
}

============================================================
CRON 5: Watchdog (every ${WATCHDOG_MINUTES} minutes)
============================================================
cron action:"add" job:{
  "name": "litmus-watchdog",
  "enabled": true,
  "schedule": { "kind": "every", "everyMs": ${WATCHDOG_MS} },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the Litmus watchdog check. Full instructions in $REFERENCES_DIR/watchdog.md — read that file first. Read from $SHARED_DIR/attempts/ for metrics. Keep it under 3 minutes total."
  },
  "delivery": { "mode": "none" }
}

============================================================
CRON 6: Morning Digest ($DIGEST_TIME — delivered to you)
Expr: "${DIGEST_CRON}"
============================================================
cron action:"add" job:{
  "name": "litmus-digest",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "${DIGEST_CRON}", "tz": "$TZ" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Write and deliver the Litmus morning research digest. Full instructions in $REFERENCES_DIR/digest.md — read that file first. Include the git tree snapshot from $BASE_DIR/repo. Write for a researcher, not a sysadmin."
  },
  "delivery": {
    "mode": "announce",
    "channel": "last",
    "bestEffort": true
  }
}
EOF

echo ""
echo "=== Schedule (${TZ}) ==="
echo "  $LEISURE_START  Leisure  — workers enter creative mode (papers, moonshots)"
echo "  $SYNTHESIZER_TIME  Synthesizer — distills notes into skills library"
echo "  $DAWN_TIME  Dawn     — workers wake, queue experiments"
echo "  $DIGEST_TIME  Digest   — morning research narrative delivered to you"
echo "  Every ${DIRECTOR_HOURS}h  Director  — steers workers, Compass Reset on stagnation"
echo "  Every ${WATCHDOG_MINUTES}m   Watchdog  — liveness check, escape mode"
