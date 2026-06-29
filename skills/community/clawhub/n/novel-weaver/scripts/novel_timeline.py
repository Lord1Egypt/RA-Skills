#!/usr/bin/env python3
"""
Timeline — 时间线管理
记录故事内时间事件
"""
import json, sys
from pathlib import Path

def add_timeline(state_path, time_point, event):
    data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))
    tl = data.get("timeline", [])
    tl.append({"event": event, "time_point": time_point})
    data["timeline"] = tl
    Path(state_path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[时间线] {time_point}: {event}")

def list_timeline(state_path):
    data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))
    tl = data.get("timeline", [])
    print(f"[时间线一览] (共{len(tl)}条)")
    for t in tl:
        print(f"  {t.get('time_point','?')} → {t.get('event','?')}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python novel_timeline.py <add|list> <state_path> [time_point] [event]")
        sys.exit(1)
    cmd = sys.argv[1]
    sp = sys.argv[2]
    if cmd == "add":
        add_timeline(sp, sys.argv[3], sys.argv[4])
    elif cmd == "list":
        list_timeline(sp)
