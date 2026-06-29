#!/usr/bin/env python3
"""从 _meta.json 读取 description 字段"""
import json, sys

def main():
    if len(sys.argv) < 2:
        print("")
        return
    try:
        d = json.load(open(sys.argv[1]))
        print(d.get("description", ""))
    except Exception:
        print("")

if __name__ == "__main__":
    main()
