#!/usr/bin/env bash
set -euo pipefail

# heartbeat-to-poke.sh — Convert OpenClaw heartbeat configs into poke commands
# and (optionally, with --apply) disable the native heartbeat by editing
# openclaw.json. Linux entry point; works on macOS too but prefer the *-mac.sh
# wrapper there for the right default config path.
#
# Reads heartbeat config from openclaw.json and/or HEARTBEAT.md, then prints
# the equivalent poke commands to stdout. Active hours convert to either
# --active-hours (default) or --quiet-hours (inverse).
#
# --apply also patches the openclaw.json to disable the native heartbeat in
# place (with a timestamped .bak-* alongside).

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
POKE_CMD="poke"

# Config/state locations come from the environment (or --flags below); no
# paths are hardcoded. Falls back to $OPENCLAW_STATE_DIR/openclaw.json when
# only the state dir is exported. If neither is set, pass --openclaw-config
# explicitly.
OPENCLAW_CONFIG="${OPENCLAW_CONFIG_PATH:-}"
if [[ -z "$OPENCLAW_CONFIG" && -n "${OPENCLAW_STATE_DIR:-}" ]]; then
  OPENCLAW_CONFIG="${OPENCLAW_STATE_DIR}/openclaw.json"
fi
HEARTBEAT_MD=""
HEARTBEAT_STATE=""
AGENT=""
CHANNEL=""
TARGET=""
MODE="active-hours"
APPLY="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --openclaw-config) OPENCLAW_CONFIG="$2"; shift 2 ;;
    --heartbeat-md) HEARTBEAT_MD="$2"; shift 2 ;;
    --heartbeat-state) HEARTBEAT_STATE="$2"; shift 2 ;;
    --agent) AGENT="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    --quiet-hours) MODE="quiet-hours"; shift ;;
    --active-hours) MODE="active-hours"; shift ;;
    --apply) APPLY="1"; shift ;;
    -h|--help)
      cat <<EOF
Usage: heartbeat-to-poke.sh [OPTIONS]

Converts OpenClaw heartbeat configs into poke commands. Prints to stdout.

Options:
  --openclaw-config PATH   OpenClaw config (default: \$OPENCLAW_CONFIG_PATH,
                           else \$OPENCLAW_STATE_DIR/openclaw.json)
  --heartbeat-md PATH      HEARTBEAT.md file with task definitions
  --heartbeat-state PATH   Heartbeat state file (last run times)
  --agent AG               Agent ID for poke commands
  --channel CH             Channel for delivery
  --target TGT             Target for delivery
  --active-hours           Convert to --active-hours (default)
  --quiet-hours            Convert to --quiet-hours (inverse) instead
  --apply                  Also edit openclaw.json in place to disable native
                           heartbeat (backs up to <path>.bak-<unix-ts>). Off
                           by default — this script is non-destructive
                           unless you opt in.
  -h, --help               Show this help
EOF
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Export OPENCLAW_CONFIG so subsequent python3 heredocs that use os.environ
# see it (S2.9 fix — previously the python heredoc only worked accidentally).
export OPENCLAW_CONFIG

# Build a single route-args string, quoting each value to survive whitespace.
# When this is *printed* into a generated command it ends up in the user's
# shell history; the quotes there are intentional.
ROUTE_ARGS=""
[[ -n "$AGENT" ]]   && ROUTE_ARGS="${ROUTE_ARGS} --agent '${AGENT}'"
[[ -n "$CHANNEL" ]] && ROUTE_ARGS="${ROUTE_ARGS} --channel '${CHANNEL}'"
[[ -n "$TARGET" ]]  && ROUTE_ARGS="${ROUTE_ARGS} --target '${TARGET}'"
# Trim leading space.
ROUTE_ARGS="${ROUTE_ARGS# }"

generated=0

# --- Extract heartbeat config from openclaw.json ---
hb_every=""
hb_active_start=""
hb_active_end=""
hb_active_tz=""
hb_prompt=""

if [[ -f "$OPENCLAW_CONFIG" ]]; then
  eval "$(python3 << 'PYEOF'
import json, os
config_path = os.path.expanduser(os.environ.get("OPENCLAW_CONFIG", ""))
try:
    with open(config_path) as f:
        cfg = json.load(f)
except Exception:
    cfg = {}
hb = cfg.get("agents", {}).get("defaults", {}).get("heartbeat", {})
ah = hb.get("activeHours", {})
def q(s):
    if not s: return '""'
    return "'" + s.replace("'", "'\\''") + "'"
print(f"hb_every={q(hb.get('every',''))}")
print(f"hb_active_start={q(ah.get('start',''))}")
print(f"hb_active_end={q(ah.get('end',''))}")
print(f"hb_active_tz={q(ah.get('timezone',''))}")
print(f"hb_prompt={q(hb.get('prompt',''))}")
PYEOF
)"
fi

# --- Build active-hours or quiet-hours flag ---
HOURS_FLAG=""
if [[ -n "$hb_active_start" && -n "$hb_active_end" ]]; then
  hours_range="${hb_active_start}-${hb_active_end}"
  if [[ "$MODE" == "active-hours" ]]; then
    HOURS_FLAG="--active-hours '${hours_range}'"
  else
    HOURS_FLAG="--quiet-hours '${hb_active_end}-${hb_active_start}'"
  fi
fi

# --- Convert HEARTBEAT.md tasks ---
HEARTBEAT_MD="${HEARTBEAT_MD:-}"
if [[ -f "$HEARTBEAT_MD" && -s "$HEARTBEAT_MD" ]]; then
  export HEARTBEAT_MD
  tasks=$(python3 << 'PYEOF'
import os
with open(os.environ["HEARTBEAT_MD"]) as f:
    content = f.read()
tasks = []
in_tasks = False
current = {}
for line in content.split('\n'):
    stripped = line.strip()
    if stripped == 'tasks:':
        in_tasks = True
        continue
    if not in_tasks:
        continue
    if stripped.startswith('- name:'):
        if current.get('name') and current.get('interval') and current.get('prompt'):
            tasks.append(current)
        name = stripped.replace('- name:', '').strip().strip("'\"")
        current = {'name': name}
    elif stripped.startswith('interval:'):
        current['interval'] = stripped.replace('interval:', '').strip().strip("'\"")
    elif stripped.startswith('prompt:'):
        current['prompt'] = stripped.replace('prompt:', '').strip().strip("'\"")
    elif stripped and not stripped.startswith(' ') and not stripped.startswith('\t') and not stripped.startswith('-'):
        in_tasks = False
        if current.get('name') and current.get('interval') and current.get('prompt'):
            tasks.append(current)
        current = {}
if current.get('name') and current.get('interval') and current.get('prompt'):
    tasks.append(current)
for t in tasks:
    print(f"{t['name']}|{t['interval']}|{t['prompt']}")
PYEOF
  )

  if [[ -n "$tasks" ]]; then
    echo "# Tasks from HEARTBEAT.md"
    while IFS='|' read -r name interval prompt; do
      echo "# Task: ${name} (interval: ${interval})"
      echo "${POKE_CMD} --task \"${prompt}\" \\"
      echo "  --on-calendar '*-*-* *:0/5' \\"
      echo "  --task-interval \"${interval}\" \\"
      if [[ -n "$HOURS_FLAG" ]]; then
        echo "  ${HOURS_FLAG} \\"
      fi
      echo "  ${ROUTE_ARGS}"
      echo ""
      generated=$((generated + 1))
    done <<< "$tasks"
  fi
fi

# --- Convert openclaw.json heartbeat (global polling) ---
if [[ -n "$hb_every" && "$hb_every" != "0m" && "$hb_every" != "0" ]]; then
  echo "# From openclaw.json heartbeat (every: ${hb_every})"
  prompt="${hb_prompt:-Run periodic checks: email, calendar, weather, todo. Report anything urgent or interesting.}"
  echo "${POKE_CMD} --task \"${prompt}\" \\"
  echo "  --on-calendar '*-*-* *:0/5' \\"
  echo "  --task-interval \"${hb_every}\" \\"
  if [[ -n "$HOURS_FLAG" ]]; then
    echo "  ${HOURS_FLAG} \\"
  fi
  echo "  ${ROUTE_ARGS}"
  echo ""
  generated=$((generated + 1))
fi

# --- Convert heartbeat-state.json (legacy) ---
if [[ -n "$HEARTBEAT_STATE" && -f "$HEARTBEAT_STATE" ]]; then
  export HEARTBEAT_STATE
  echo "# From heartbeat-state.json (legacy)"
  python3 << PYEOF
import json, os
with open(os.environ["HEARTBEAT_STATE"]) as f:
    state = json.load(f)
checks = state.get("lastChecks", {})
for check_name, last_ts in checks.items():
    if check_name.endswith("_last_check"):
        continue
    print(f"# Check: {check_name}")
    print(f"# Last run: {last_ts or 'never'}")
    print(f"poke --task 'Check {check_name} and report anything urgent.' \\\\")
    print(f"  --once 2h \\\\")
    print(f"  ${ROUTE_ARGS}")
    print()
PYEOF
  generated=$((generated + 1))
fi

# --- If nothing found, suggest common poke setups ---
if [[ $generated -eq 0 ]]; then
  echo "# No heartbeat config found. Here are common poke setups:"
  echo ""
  echo "# Morning standup (weekdays 9am, active hours 8am-10pm)"
  echo "${POKE_CMD} --task \"Check email, calendar, and weather. Give me today's priorities.\" \\"
  echo "  --on-calendar 'Mon..Fri *-*-* 09:00:00' \\"
  echo "  --active-hours '08:00-22:00' \\"
  echo "  --preset morning-plan \\"
  echo "  ${ROUTE_ARGS}"
  echo ""
  echo "# Trash reminder (Sunday 7pm, escalating)"
  echo "${POKE_CMD} --remind \"Have you taken out the trash?\" \\"
  echo "  --on-calendar 'Sun *-*-* 19:00:00' \\"
  echo "  --escalation-intervals '60,30,15,10,5,5' \\"
  echo "  --max-pokes 6 \\"
  echo "  ${ROUTE_ARGS}"
  echo ""
  echo "# Heartbeat (every 30m, active hours only)"
  echo "${POKE_CMD} --task \"Check for urgent items and report.\" \\"
  echo "  --on-calendar '*-*-* *:0/5' \\"
  echo "  --task-interval '30m' \\"
  echo "  --active-hours '08:00-22:00' \\"
  echo "  --if-unconfirmed-after 15m --if-unconfirmed-remind 'Missed check-in!' \\"
  echo "  ${ROUTE_ARGS}"
fi

# --- Optional: disable native heartbeat in openclaw.json (S2.9 #2) ---
if [[ "$APPLY" == "1" ]]; then
  if [[ -z "$OPENCLAW_CONFIG" || ! -f "$OPENCLAW_CONFIG" ]]; then
    echo "" >&2
    echo "# --apply: skipped (no openclaw.json at '${OPENCLAW_CONFIG:-<unset>}')" >&2
  else
    bak="${OPENCLAW_CONFIG}.bak-$(date +%s)"
    cp "$OPENCLAW_CONFIG" "$bak"
    python3 << 'PYEOF'
import json, os
path = os.environ["OPENCLAW_CONFIG"]
with open(path) as f:
    cfg = json.load(f)
defaults = cfg.setdefault("agents", {}).setdefault("defaults", {})
hb = defaults.setdefault("heartbeat", {})
hb["enabled"] = False
# Belt-and-braces: also blank the polling interval so a non-`enabled`-aware
# heartbeat loop won't pick it up either.
if "every" in hb:
    hb["every"] = "0"
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")
PYEOF
    echo "" >&2
    echo "# --apply: disabled native heartbeat in '${OPENCLAW_CONFIG}' (backup: ${bak})" >&2
  fi
fi
