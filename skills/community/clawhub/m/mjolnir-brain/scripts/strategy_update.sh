#!/bin/bash
# strategy_update.sh — Update success rate for a strategy solution
# Usage: ./strategy_update.sh <problem_key> <solution_index> <success|fail>

set -e

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
STRATEGIES="$WORKSPACE/strategies.json"

if [ $# -lt 3 ]; then
    echo "Usage: $0 <problem_key> <solution_index> <success|fail>"
    echo ""
    echo "Available keys:"
    python3 -c "
import json
with open('$STRATEGIES') as f:
    data = json.load(f)
for k,v in data.items():
    if k == '_meta': continue
    print(f'  {k}: {v[\"description\"]}')
"
    exit 1
fi

KEY="$1"
IDX="$2"
RESULT="$3"

python3 << PYTHON
import json
from datetime import datetime

with open('$STRATEGIES') as f:
    data = json.load(f)

if '$KEY' not in data:
    print(f"❌ Strategy not found: $KEY")
    exit(1)

solutions = data['$KEY']['solutions']
idx = int('$IDX')

if idx >= len(solutions):
    print(f"❌ Index out of range (0-{len(solutions)-1})")
    exit(1)

sol = solutions[idx]
old_rate = sol['successRate']
old_tries = sol['tries']

if '$RESULT' == 'success':
    new_rate = (old_rate * old_tries + 1.0) / (old_tries + 1)
else:
    new_rate = (old_rate * old_tries + 0.0) / (old_tries + 1)

sol['successRate'] = round(new_rate, 3)
sol['tries'] = old_tries + 1

data['$KEY']['solutions'] = sorted(solutions, key=lambda x: -x['successRate'])
data['_meta']['updated'] = datetime.now().strftime('%Y-%m-%d')

with open('$STRATEGIES', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ {data['$KEY']['description']}")
print(f"   Solution {idx}: {sol['action'][:60]}...")
print(f"   Rate: {old_rate:.3f} → {sol['successRate']:.3f} ({old_tries} → {sol['tries']} tries)")
PYTHON
