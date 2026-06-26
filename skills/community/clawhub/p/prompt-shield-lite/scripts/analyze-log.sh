#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/load-config.sh"

DEFAULT_LOG="$PSL_LOG_PATH"
LOG_PATH="${1:-$DEFAULT_LOG}"
HOURS="${2:-24}"

if [[ "$PSL_ALLOW_ANY_LOG_PATH" != "1" && "$LOG_PATH" != "$DEFAULT_LOG" ]]; then
  echo "[analyze-log] blocked: custom log path disabled by default."
  echo "[analyze-log] use default path or set PSL_ALLOW_ANY_LOG_PATH=1 explicitly."
  exit 2
fi

if [[ ! -f "$LOG_PATH" ]]; then
  echo "[analyze-log] log file not found: $LOG_PATH"
  exit 2
fi

python3 - "$LOG_PATH" "$HOURS" <<'PY'
import json,sys,datetime
from collections import Counter,defaultdict

log_path=sys.argv[1]
hours=float(sys.argv[2])
now=datetime.datetime.now(datetime.timezone.utc)
start=now-datetime.timedelta(hours=hours)

rows=[]
with open(log_path,encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line:
            continue
        try:
            obj=json.loads(line)
        except Exception:
            continue
        ts=obj.get('ts')
        try:
            t=datetime.datetime.fromisoformat(ts.replace('Z','+00:00')) if ts else None
        except Exception:
            t=None
        if t and t>=start:
            rows.append(obj)

if not rows:
    print(f"Prompt Shield Lite Log Report (last {hours:g}h)")
    print("No entries in time window.")
    sys.exit(0)

actions=Counter(r.get('action','unknown') for r in rows)
severities=Counter(r.get('severity','unknown') for r in rows)
rule_hits=Counter()
reason_hits=Counter()
by_mode=defaultdict(Counter)

for r in rows:
    mode=r.get('mode','unknown')
    by_mode[mode][r.get('action','unknown')]+=1
    for mr in r.get('matched_rules',[]) or []:
        rule_hits[mr]+=1
    for rs in r.get('reasons',[]) or []:
        reason_hits[rs]+=1

total=len(rows)
block_rate=actions['block']/total
warn_rate=actions['warn']/total

print(f"Prompt Shield Lite Log Report (last {hours:g}h)")
print(f"Entries: {total}")
print(f"Action mix: allow={actions['allow']} warn={actions['warn']} block={actions['block']} unknown={actions['unknown']}")
print(f"Block rate: {block_rate:.1%} | Warn rate: {warn_rate:.1%}")

print("\nSeverity distribution:")
for k in ['SAFE','LOW','MEDIUM','HIGH','CRITICAL','unknown']:
    if severities[k]:
        print(f"- {k}: {severities[k]}")

print("\nTop matched rules:")
for rule,cnt in rule_hits.most_common(10):
    print(f"- {rule}: {cnt}")
if not rule_hits:
    print("- (none)")

print("\nTop reasons:")
for reason,cnt in reason_hits.most_common(10):
    print(f"- {reason}: {cnt}")

print("\nBy mode (allow/warn/block):")
for mode,c in sorted(by_mode.items()):
    print(f"- {mode}: allow={c['allow']} warn={c['warn']} block={c['block']}")
PY
