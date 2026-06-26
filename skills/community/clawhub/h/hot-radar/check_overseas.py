import json, sys, os
sys.path.insert(0, '.')
data = json.load(open('data/2026-05-25.json', encoding='utf-8'))
print('Keys:', list(data.keys()))
raw = data.get('raw', {})
print('Raw keys:', list(raw.keys()))
tc = raw.get('TechCrunch', [])
print(f'TechCrunch items: {len(tc)}')
for it in tc[:2]:
    print('  title:', repr(it.get('title', '')[:60]))
    print('  excerpt:', repr(str(it.get('excerpt', ''))[:100]))
    print()
