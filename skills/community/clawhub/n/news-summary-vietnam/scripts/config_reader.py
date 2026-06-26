#!/usr/bin/env python3
# config_reader.py — đọc config.json cho shell script
import json, sys

try:
    cfg = json.load(open('/home/pc999/.openclaw/workspace/config.json'))
except:
    # Thử nhiều đường dẫn
    import os
    for path in [
        os.path.join(os.path.dirname(__file__), '../config.json'),
        os.path.join(os.path.dirname(__file__), '../../config.json'),
        os.path.join(os.path.dirname(__file__), 'config.json'),
    ]:
        try:
            cfg = json.load(open(path))
            break
        except:
            pass

key = sys.argv[1] if len(sys.argv) > 1 else None
if key:
    print(cfg.get(key, ''))
else:
    print(json.dumps(cfg))
