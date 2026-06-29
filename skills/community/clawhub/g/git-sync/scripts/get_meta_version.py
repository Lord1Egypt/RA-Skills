#!/usr/bin/env python3
"""从 _meta.json 读取 version 字段"""
import json, sys

def main():
    if len(sys.argv) < 2:
        print("1.0.0")
        return
    try:
        d = json.load(open(sys.argv[1]))
        print(d.get("version", "1.0.0"))
    except Exception:
        print("1.0.0")

if __name__ == "__main__":
    main()
