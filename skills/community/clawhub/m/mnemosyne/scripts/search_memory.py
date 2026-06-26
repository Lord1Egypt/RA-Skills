#!/usr/bin/env python3
import json, sys

if len(sys.argv) < 3:
    print("Usage: search_memory.py <index_file> <query>")
    sys.exit(1)

index_file = sys.argv[1]
query = sys.argv[2].lower()

with open(index_file, 'r', encoding='utf-8') as f:
    index = json.load(f)

results = []
for mem in index.get('memories', []):
    if query in mem.get('content','').lower() or \
       query in mem.get('tags','').lower() or \
       query in mem.get('type','').lower():
        results.append(mem)

results.sort(key=lambda x: (-x.get('importance',0), x.get('timestamp',0)))

print(f"找到 {len(results)} 条记忆：\n")
for r in results[:20]:
    print(f"[{r['type']}] [{r['importance']}⭐] {r['date']}")
    print(f"  {r['content'][:80]}{'...' if len(r['content'])>80 else ''}")
    print()
