#!/bin/bash
# Render memory/graph.jsonl as a Mermaid diagram
echo "graph LR"
cat /root/clawd/memory/graph.jsonl | python3 -c "
import sys, json
seen = set()
for line in sys.stdin:
    t = json.loads(line)
    s = t['subject'].replace(' ', '_').replace('#', 'Nr')
    o = t['object'].replace(' ', '_').replace('#', 'Nr')
    p = t['predicate']
    key = f'{s}-{p}-{o}'
    if key not in seen:
        seen.add(key)
        print(f'    {s} -->|{p}| {o}')
"
