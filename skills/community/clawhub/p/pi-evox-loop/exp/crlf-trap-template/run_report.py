#!/usr/bin/env python3
import json
with open('data/metrics.json', encoding='utf-8') as f:
    m = json.load(f)
print('total:', sum(m.values()))
