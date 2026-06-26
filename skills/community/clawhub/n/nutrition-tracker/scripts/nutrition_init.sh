#!/usr/bin/env bash
set -euo pipefail

# Save nutrition profile for later target checks.
# Writes to: $OBSIDIAN_VAULT/health/eat/profile.json

VAULT="${OBSIDIAN_VAULT:-$HOME/Documents/obsidian/yzhai-daily}"
LANG_OPT="zh-CN"

SEX=""
HEIGHT=""
WEIGHT=""
ACTIVITY="office"
GOAL="cut"
KCAL="2200"

PTARGET=""  # grams
CTARGET=""  # grams
FTARGET=""  # grams

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sex) SEX="$2"; shift 2;;
    --height) HEIGHT="$2"; shift 2;;
    --weight) WEIGHT="$2"; shift 2;;
    --activity) ACTIVITY="$2"; shift 2;;
    --goal) GOAL="$2"; shift 2;;
    --kcal) KCAL="$2"; shift 2;;
    --pTarget) PTARGET="$2"; shift 2;;
    --cTarget) CTARGET="$2"; shift 2;;
    --fTarget) FTARGET="$2"; shift 2;;
    --lang) LANG_OPT="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

mkdir -p "$VAULT/health/eat"
PROFILE="$VAULT/health/eat/profile.json"

python3 - <<PY
import json
from pathlib import Path

profile = {
  "sex": "${SEX}",
  "height_cm": float("${HEIGHT}") if "${HEIGHT}" else None,
  "weight_kg": float("${WEIGHT}") if "${WEIGHT}" else None,
  "activity": "${ACTIVITY}",
  "goal": "${GOAL}",
  "kcalTarget": int(float("${KCAL}")),
  "macroTargets": {
    "p": int(float("${PTARGET}")) if "${PTARGET}" else None,
    "c": int(float("${CTARGET}")) if "${CTARGET}" else None,
    "f": int(float("${FTARGET}")) if "${FTARGET}" else None,
  }
}

p = Path("${PROFILE}")
p.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(p)
PY

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export LANG_OPT PROFILE SCRIPT_DIR
python3 - <<'PY'
import sys, os
sys.path.insert(0, os.environ['SCRIPT_DIR'])
from i18n import t
lang=os.environ.get('LANG_OPT','zh-CN')
profile=os.environ['PROFILE']
print(t(lang, 'profile_saved', path=profile))
PY
