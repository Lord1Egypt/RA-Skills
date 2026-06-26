#!/usr/bin/env bash
set -euo pipefail

# Log one meal entry and update monthly daily totals.

VAULT="${OBSIDIAN_VAULT:-$HOME/Documents/obsidian/yzhai-daily}"
LANG_OPT="zh-CN"

DATE=""
TIME=""
MEAL=""
DESC=""
KCAL=""
P=""; C=""; F=""
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date) DATE="$2"; shift 2;;
    --time) TIME="$2"; shift 2;;
    --meal) MEAL="$2"; shift 2;;
    --desc) DESC="$2"; shift 2;;
    --kcal) KCAL="$2"; shift 2;;
    --p) P="$2"; shift 2;;
    --c) C="$2"; shift 2;;
    --f) F="$2"; shift 2;;
    --target) TARGET="$2"; shift 2;;
    --lang) LANG_OPT="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ -z "$DATE" || -z "$MEAL" || -z "$DESC" || -z "$KCAL" || -z "$P" || -z "$C" || -z "$F" ]]; then
  echo "Missing required args. Need --date --meal --desc --kcal --p --c --f" >&2
  exit 2
fi

if [[ -z "$TIME" ]]; then
  TIME=$(date +%H:%M)
fi

MONTH=${DATE:0:7}
YYYY=${DATE:0:4}
MM=${DATE:5:2}
MONTH_DIR="$VAULT/health/eat/$MONTH"
FILE="$MONTH_DIR/${YYYY}${MM}_calories_macros.md"

mkdir -p "$MONTH_DIR"

export DATE TIME MEAL DESC KCAL P C F MONTH FILE TARGET

python3 - <<'PY'
from pathlib import Path
import re, os

date = os.environ["DATE"]
time = os.environ["TIME"]
meal = os.environ["MEAL"]
desc = os.environ["DESC"]
kcal = int(float(os.environ["KCAL"]))
p = int(float(os.environ["P"]))
c = int(float(os.environ["C"]))
f = int(float(os.environ["F"]))
month = os.environ["MONTH"]
file = os.environ["FILE"]
target_env = os.environ.get("TARGET", "").strip()

path = Path(file)
if not path.exists():
    path.write_text(f"""---
created: {date}
modified: {date}
author: yzhai
tags:
  - health
  - eat
  - calories
  - macros
category: health
---

# Eat log {month} (calories + macros)

> Target: 2200 kcal/day (default; per-entry target allowed)

---

## Daily totals (auto)

<!-- DAILY_TOTALS_START -->
<!-- DAILY_TOTALS_END -->

---

## Entries

<!-- ENTRIES_START -->
<!-- ENTRIES_END -->
""", encoding="utf-8")

txt = path.read_text(encoding="utf-8")

entry = f"- {date} {time} [{meal}] kcal={kcal} P={p} C={c} F={f} | {desc}\n"
if "<!-- ENTRIES_START -->" not in txt:
    raise SystemExit("Missing ENTRIES_START marker")

txt = txt.replace("<!-- ENTRIES_START -->\n", "<!-- ENTRIES_START -->\n" + entry)

entries_block = re.search(r"<!-- ENTRIES_START -->\n(.*?)<!-- ENTRIES_END -->", txt, re.S)
entries = entries_block.group(1).strip().splitlines() if entries_block else []

daily = {}
for line in entries:
    m = re.match(r"- (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) \[(.*?)\] kcal=(\d+) P=(\d+) C=(\d+) F=(\d+)", line)
    if not m:
        continue
    d = m.group(1)
    kcal_i, p_i, c_i, f_i = map(int, m.group(4,5,6,7))
    s = daily.setdefault(d, {"kcal":0,"p":0,"c":0,"f":0})
    s["kcal"] += kcal_i
    s["p"] += p_i
    s["c"] += c_i
    s["f"] += f_i

lines=[]
for d in sorted(daily.keys()):
    s = daily[d]
    target = int(float(target_env)) if target_env else 2200
    remain = target - s["kcal"]
    lines.append(f"- {d}: kcal={s['kcal']} (remain {remain}) | P={s['p']}g C={s['c']}g F={s['f']}g")

new_totals = "\n".join(lines) + ("\n" if lines else "")

txt = re.sub(r"<!-- DAILY_TOTALS_START -->\n.*?<!-- DAILY_TOTALS_END -->",
             "<!-- DAILY_TOTALS_START -->\n" + new_totals + "<!-- DAILY_TOTALS_END -->",
             txt, flags=re.S)

txt = re.sub(r"modified: .*", f"modified: {date}", txt, count=1)
path.write_text(txt, encoding="utf-8")
print(path)
PY

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export LANG_OPT SCRIPT_DIR
python3 - <<'PY'
import sys, os
sys.path.insert(0, os.environ['SCRIPT_DIR'])
from i18n import t
print(t(os.environ.get('LANG_OPT','zh-CN'), 'logged', path=os.environ['FILE']))
PY
