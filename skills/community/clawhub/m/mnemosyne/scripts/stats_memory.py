#!/usr/bin/env python3
import json, sys

index_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/index.json'

with open(index_file, 'r', encoding='utf-8') as f:
    index = json.load(f)

memories = index.get('memories', [])
total = len(memories)
types, tiers, importance = {}, {}, {}

for m in memories:
    t = m.get('type', 'unknown')
    types[t] = types.get(t, 0) + 1
    tier = m.get('tier', 'unknown')
    tiers[tier] = tiers.get(tier, 0) + 1
    imp = m.get('importance', 0)
    importance[imp] = importance.get(imp, 0) + 1

print(f"📊 记忆统计")
print(f"总数: {total} 条")
print(f"\n按类型: {types}")
print(f"按层级: {tiers}")
print(f"按重要度: {dict(sorted(importance.items()))}")
