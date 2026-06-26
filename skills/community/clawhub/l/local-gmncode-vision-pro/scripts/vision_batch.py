#!/usr/bin/env python3
import os, sys, json, subprocess

if len(sys.argv) < 2:
    print('Usage: vision_batch.py <img1> [img2 ...]', file=sys.stderr)
    sys.exit(2)

script = '/home/ubuntu/.openclaw/workspace/skills/local-gmncode-vision-pro/scripts/vision_json.py'
results = []
for p in sys.argv[1:]:
    proc = subprocess.run([script, p], capture_output=True, text=True)
    results.append({
        'image': p,
        'ok': proc.returncode == 0,
        'output': proc.stdout.strip(),
        'error': proc.stderr.strip(),
    })
print(json.dumps(results, ensure_ascii=False, indent=2))
