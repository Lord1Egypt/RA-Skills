#!/bin/bash
# strategy_lookup.sh — Look up known solutions by error keyword, sorted by success rate
# Usage: ./strategy_lookup.sh <keyword or error message>

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
STRATEGIES="$WORKSPACE/strategies.json"

if [ -z "$1" ]; then
    echo "🔍 strategy_lookup — Find known solutions by error message"
    echo ""
    echo "Usage: $0 <keyword or error message>"
    echo ""
    echo "Registered strategies:"
    python3 -c "
import json
with open('$STRATEGIES') as f:
    data = json.load(f)
for k,v in data.items():
    if k == '_meta': continue
    n = len(v['solutions'])
    best = max(v['solutions'], key=lambda x: x['successRate'])
    print(f'  {k}: {v[\"description\"]} ({n} solutions, best {best[\"successRate\"]:.0%})')
"
    exit 0
fi

KEYWORD="$*"

python3 << PYTHON
import json

with open('$STRATEGIES') as f:
    data = json.load(f)

keyword = '''$KEYWORD'''.lower()
matches = []

for key, val in data.items():
    if key == '_meta':
        continue
    score = 0
    if keyword in key.lower():
        score += 10
    if keyword in val.get('description', '').lower():
        score += 5
    for m in val.get('match', []):
        if keyword in m.lower() or m.lower() in keyword:
            score += 8
    if score > 0:
        matches.append((score, key, val))

if not matches:
    print(f"❌ No match for: {keyword}")
    print("💡 Add new strategies to strategies.json")
else:
    matches.sort(key=lambda x: -x[0])
    for score, key, val in matches:
        print(f"🎯 {val['description']} [{key}]")
        print(f"   Solutions (by success rate):")
        for i, sol in enumerate(sorted(val['solutions'], key=lambda x: -x['successRate'])):
            rate = sol['successRate']
            bar = '█' * int(rate * 10) + '░' * (10 - int(rate * 10))
            env = f" ({sol['env']})" if 'env' in sol else ""
            print(f"   {i}. [{bar}] {rate:.0%} ({sol['tries']}x) {sol['action']}{env}")
        print()
PYTHON
