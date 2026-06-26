#!/usr/bin/env python3
import json
import os
import shutil
import sys
import time

path = os.path.expanduser('~/.openclaw/openclaw.json')
if not os.path.exists(path):
    print(f'Config not found: {path}', file=sys.stderr)
    sys.exit(1)

backup = f"{path}.bak.browser-skill-{time.strftime('%Y%m%d-%H%M%S')}"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

shutil.copy2(path, backup)

browser = data.get('browser', {})
browser['enabled'] = True
browser['executablePath'] = '/usr/bin/chromium'
browser['headless'] = True
browser['noSandbox'] = True
browser['attachOnly'] = True
data['browser'] = browser

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated:', path)
print('Backup :', backup)
print(json.dumps(data['browser'], ensure_ascii=False, indent=2))
