#!/usr/bin/env python3
"""快速查询（agent 回答「本周 top 岗位」「监控统计」时调用，免翻原始文件）。

  query.py top [days=7]      # 近 N 天 P1/P2 岗位
  query.py stats [days=7]    # 判级/信源统计
"""
import json
import sys
from datetime import datetime, timedelta

from common import load_state

def recent(days):
    cutoff = (datetime.now().astimezone() - timedelta(days=days)).isoformat()
    return {k: v for k, v in load_state().items()
            if v.get("priority") in ("P1", "P2") and v.get("seen_at", "") >= cutoff}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "top"
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    if cmd == "top":
        items = sorted(recent(days).items(), key=lambda kv: (kv[1]["priority"], kv[1]["seen_at"]))
        print(json.dumps([{"doc_id": k, **{f: v.get(f) for f in ("priority", "title", "seen_at")}}
                          for k, v in items], ensure_ascii=False, indent=1))
    else:
        from collections import Counter
        s = load_state()
        cutoff = (datetime.now().astimezone() - timedelta(days=days)).isoformat()
        rec = [v for v in s.values() if v.get("seen_at", "") >= cutoff]
        print(json.dumps({
            "window_days": days, "total_seen": len(s), "new_in_window": len(rec),
            "priority": dict(Counter(v.get("priority") or "unjudged" for v in rec)),
            "by_source": dict(Counter(k.split(":")[0] for k, v in s.items()
                                      if v.get("seen_at", "") >= cutoff)),
        }, ensure_ascii=False, indent=1))
