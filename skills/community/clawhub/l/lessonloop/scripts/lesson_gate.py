#!/usr/bin/env python3
import json
import sys

HIGH_STAKES = [
    'billing', 'cost', 'token', 'oauth', 'api', 'auth', 'safety', 'trust',
    'memory', 'default', 'routing', 'priority', 'telegram', 'voice'
]

def main():
    text = ' '.join(sys.argv[1:]).strip().lower()
    if not text:
        print(json.dumps({"needsEscalation": True, "reason": "empty-input"}))
        return
    hit = [k for k in HIGH_STAKES if k in text]
    out = {
        "needsEscalation": bool(hit),
        "reason": f"matched:{','.join(hit)}" if hit else "simple-case"
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == '__main__':
    main()
