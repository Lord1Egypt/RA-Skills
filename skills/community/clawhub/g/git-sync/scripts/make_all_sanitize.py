#!/usr/bin/env python3
"""将扫描结果 JSON 转为「全部脱敏」决策 JSON（供 always-sanitize 模式用）"""
import json, sys

def main():
    if len(sys.argv) < 2:
        print("{}")
        return
    try:
        results = json.load(open(sys.argv[1]))
        decisions = {e["file"]: "sanitize" for e in results}
        print(json.dumps(decisions, ensure_ascii=False, indent=2))
    except Exception as e:
        print("{}")

if __name__ == "__main__":
    main()
