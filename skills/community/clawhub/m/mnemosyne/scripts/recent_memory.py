#!/usr/bin/env python3
import json, sys

if len(sys.argv) < 3:
    print("Usage: recent_memory.py <index_file> <limit>")
    sys.exit(1)

index_file = sys.argv[1]
limit = int(sys.argv[2])

with open(index_file, 'r', encoding='utf-8') as f:
    index = json.load(f)

memories = sorted(index.get('memories',[]), key=lambda x: x.get('timestamp',0), reverse=True)[:limit]

print(f"最近 {len(memories)} 条记忆：\n")
for m in memories:
    print(f"[{m['type']}] [{m['importance']}⭐] {m['date']} | {m['content'][:60]}...")
