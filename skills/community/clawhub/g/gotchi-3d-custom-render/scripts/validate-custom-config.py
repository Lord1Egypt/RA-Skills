#!/usr/bin/env python3
import json
import sys
from pathlib import Path

SLOTS = ["body", "face", "eyes", "head", "pet", "hand_left", "hand_right"]
DEFAULTS = {
    "haunt_id": 1,
    "collateral": None,
    "eye_shape": None,
    "eye_color": None,
    "skin_id": 0,
    "wearables": {slot: 0 for slot in SLOTS},
    "background": "transparent",
    "pose": "idle",
    "output": {},
}


def die(msg: str) -> None:
    print(json.dumps({"ok": False, "error": msg}, indent=2))
    sys.exit(1)


def load_payload() -> dict:
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        return json.loads(Path(sys.argv[1]).read_text())
    return json.load(sys.stdin)


payload = load_payload()
normalized = json.loads(json.dumps(DEFAULTS))
normalized.update({k: v for k, v in payload.items() if k != 'wearables'})
wearables = dict(DEFAULTS['wearables'])
wearables.update(payload.get('wearables', {}))
normalized['wearables'] = wearables

for field in ['collateral', 'eye_shape', 'eye_color']:
    if not normalized.get(field):
        die(f'missing required field: {field}')

try:
    normalized['haunt_id'] = int(normalized['haunt_id'])
    normalized['skin_id'] = int(normalized['skin_id'])
except Exception:
    die('haunt_id and skin_id must be integers')

for slot, value in normalized['wearables'].items():
    if slot not in SLOTS:
        die(f'unknown wearable slot: {slot}')
    try:
        normalized['wearables'][slot] = int(value)
    except Exception:
        die(f'wearable slot {slot} must be an integer')

print(json.dumps({"ok": True, "payload": normalized}, indent=2))
