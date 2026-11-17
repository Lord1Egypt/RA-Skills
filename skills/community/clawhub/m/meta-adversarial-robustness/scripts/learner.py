#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""learner: 记录本技能调用/成败，支撑 meta-evolver 闭环。"""
import os, json, sys
MEM = os.path.join(os.path.dirname(__file__), "learned_patterns.json")
def load():
    try:
        return json.load(open(MEM, encoding="utf-8"))
    except Exception:
        return {"total_ops": 0, "total_fails": 0, "patterns": []}
def record(op_ok=True, note=""):
    d = load(); d["total_ops"] += 1
    if not op_ok:
        d["total_fails"] += 1
    if note:
        d.setdefault("patterns", []).append(note)
    json.dump(d, open(MEM, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return d
if __name__ == "__main__":
    ok = (sys.argv[1] != "fail") if len(sys.argv) > 1 else True
    rec = (sys.argv[2] if len(sys.argv) > 2 else "")
    print(json.dumps(record(ok, rec), ensure_ascii=False))
