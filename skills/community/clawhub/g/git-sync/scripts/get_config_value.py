#!/usr/bin/env python3
"""从 config.json 读取值，返回纯文本（供 bash 使用）"""
import json, sys

def main():
    if len(sys.argv) < 3:
        print("")
        return
    config_file = sys.argv[1]
    key = sys.argv[2]          # 如 "gitee.user" 或 "github.user"
    try:
        d = json.load(open(config_file))
        keys = key.split(".")
        val = d
        for k in keys:
            val = val[k]
        print(val)
    except Exception:
        print("")

if __name__ == "__main__":
    main()
