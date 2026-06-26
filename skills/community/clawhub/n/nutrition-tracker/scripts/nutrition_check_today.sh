#!/usr/bin/env bash
set -euo pipefail

VAULT="${OBSIDIAN_VAULT:-$HOME/Documents/obsidian/yzhai-daily}"
LANG_OPT="zh-CN"
DATE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date) DATE="$2"; shift 2;;
    --lang) LANG_OPT="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ -z "$DATE" ]]; then
  DATE=$(date +%F)
fi

PROFILE="$VAULT/health/eat/profile.json"
if [[ ! -f "$PROFILE" ]]; then
  python3 - <<PY
from i18n import t
print(t("${LANG_OPT}", "missing_profile"))
PY
  exit 2
fi

MONTH=${DATE:0:7}
YYYY=${DATE:0:4}
MM=${DATE:5:2}
FILE="$VAULT/health/eat/$MONTH/${YYYY}${MM}_calories_macros.md"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export VAULT PROFILE DATE FILE LANG_OPT SCRIPT_DIR

python3 - <<'PY'
import json, re, os, sys
from pathlib import Path

lang = os.environ.get('LANG_OPT','zh-CN')
sys.path.insert(0, os.environ['SCRIPT_DIR'])
from i18n import t

profile_path = Path(os.environ['PROFILE'])
date = os.environ['DATE']
log_path = Path(os.environ['FILE'])

profile = json.loads(profile_path.read_text(encoding='utf-8'))
weight = profile.get('weight_kg') or 0
kcal_target = int(profile.get('kcalTarget') or 2200)
goal = (profile.get('goal') or 'cut').lower()

# derive macro targets
mt = profile.get('macroTargets') or {}

p_target = mt.get('p')
f_target = mt.get('f')
c_target = mt.get('c')

if goal == 'cut':
    if not p_target and weight:
        p_target = int(round(2.0 * float(weight)))
    if not f_target and weight:
        f_target = int(round(0.8 * float(weight)))

# fat range
f_min = int(round((f_target or 60) * 0.9))
f_max = int(round((f_target or 60) * 1.1))

# carb range (remaining)
if c_target:
    c_min = int(round(c_target * 0.9))
    c_max = int(round(c_target * 1.1))
else:
    # remaining from kcal
    p_use = int(p_target or 120)
    f_use = int(f_target or 60)
    c_mid = max(0, int(round((kcal_target - p_use*4 - f_use*9) / 4)))
    c_min = int(round(c_mid * 0.85))
    c_max = int(round(c_mid * 1.15))

# parse totals for date
kcal=p=c=f=0
if log_path.exists():
    txt = log_path.read_text(encoding='utf-8')
    # Prefer DAILY_TOTALS section
    m = re.search(r"<!-- DAILY_TOTALS_START -->\n(.*?)<!-- DAILY_TOTALS_END -->", txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"- (\d{4}-\d{2}-\d{2}): kcal=(\d+) .*\| P=(\d+)g C=(\d+)g F=(\d+)g", line.strip())
            if mm and mm.group(1) == date:
                kcal,p,c,f = map(int, mm.group(2,3,4,5))

kcal_remain = kcal_target - kcal

print(t(lang,'today_summary', date=date, kcal=kcal, kcalRemain=kcal_remain, p=p, c=c, f=f))
print(t(lang,'targets', kcalTarget=kcal_target, pTarget=int(p_target or 0), fMin=f_min, fMax=f_max, cMin=c_min, cMax=c_max))

ok=[]
bad=[]

# kcal: for cut, we treat <= target as ok
if kcal <= kcal_target:
    ok.append('kcal')
else:
    bad.append('kcal')

if p_target and p >= int(p_target):
    ok.append('protein')
else:
    bad.append('protein')

if f_min <= f <= f_max:
    ok.append('fat')
else:
    bad.append('fat')

if c_min <= c <= c_max:
    ok.append('carbs')
else:
    bad.append('carbs')

if not bad:
    print(t(lang,'status_all_ok'))
else:
    print(t(lang,'status_ok', ok=','.join(ok) or '-', bad=','.join(bad) or '-'))

print(t(lang,'diff',
        kcalDiff=(kcal_target-kcal),
        pDiff=(int(p_target or 0)-p),
        cDiff=(int((c_min+c_max)/2)-c),
        fDiff=(int((f_min+f_max)/2)-f)))
PY
