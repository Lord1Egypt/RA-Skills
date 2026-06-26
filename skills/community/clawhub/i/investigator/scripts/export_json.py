#!/usr/bin/env python3
import json
import sys


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print('{"error":"no input provided"}')
        return
    try:
        obj = json.loads(raw)
    except Exception as e:
        print(json.dumps({"error": f"invalid json: {e}"}))
        return
    print(json.dumps(obj, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
