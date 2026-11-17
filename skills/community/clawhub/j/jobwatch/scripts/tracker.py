#!/usr/bin/env python3
"""投递状态跟踪：applied → interview → offer/rejected 的 pipeline 管理。

数据：HOME/state/applications.json  {doc_id: {status, note, title, company, url, history[]}}

敏感性说明：这个文件记录你投了哪些公司、面到哪一轮、被拒没有，note 里还可能有你自己
写的私人备注——属于敏感求职信息。它**只写在本机** `HOME/state/` 下，不加密、不上传，
也不参与任何出网调用（本模块不 import 任何网络函数）。保护它靠的是文件系统权限：
它继承你 HOME 目录的权限，请别把 `<workspace>/jobwatch/` 放进会同步到云端或共享的目录。
想彻底清除：删掉该文件或整个 `<workspace>/jobwatch/` 目录。
用法（agent 在用户说「我投了 X」「X 进面试了」时调用）：
  tracker.py find <关键词>                 # 从已见岗位里模糊找 doc_id
  tracker.py set <doc_id> <status> [note]  # applied|interview|offer|rejected|archived
  tracker.py list [status]
  tracker.py stats
  tracker.py stale [days=7]                # 投递后 N 天无更新的（日摘要提醒用）
"""
import json
import sys
from datetime import datetime, timedelta

from common import ROOT, load_state, now_iso

APP_FILE = ROOT / "state" / "applications.json"
STATUSES = ("applied", "interview", "offer", "rejected", "archived")


def load_apps():
    return json.loads(APP_FILE.read_text()) if APP_FILE.exists() else {}


def save_apps(apps):
    APP_FILE.parent.mkdir(parents=True, exist_ok=True)
    APP_FILE.write_text(json.dumps(apps, ensure_ascii=False, indent=1))


def find(keyword):
    kw = keyword.lower()
    hits = []
    for doc_id, v in load_state().items():
        title = (v.get("title") or "").lower()
        if kw in title or kw in doc_id.lower():
            hits.append({"doc_id": doc_id, "title": v.get("title"),
                         "priority": v.get("priority")})
    return hits[:10]


def set_status(doc_id, status, note=""):
    assert status in STATUSES, f"status must be one of {STATUSES}"
    apps = load_apps()
    seen = load_state().get(doc_id, {})
    rec = apps.get(doc_id, {"title": seen.get("title", doc_id), "history": []})
    rec.update({"status": status, "note": note, "updated_at": now_iso()})
    rec["history"].append({"ts": now_iso(), "status": status, "note": note})
    apps[doc_id] = rec
    save_apps(apps)
    return rec


def stale(days=7):
    cutoff = (datetime.now().astimezone() - timedelta(days=days)).isoformat()
    return {k: v for k, v in load_apps().items()
            if v["status"] in ("applied", "interview") and v["updated_at"] < cutoff}


def stats():
    from collections import Counter
    return dict(Counter(v["status"] for v in load_apps().values()))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "find":
        print(json.dumps(find(sys.argv[2]), ensure_ascii=False, indent=1))
    elif cmd == "set":
        print(json.dumps(set_status(sys.argv[2], sys.argv[3],
                                    " ".join(sys.argv[4:])), ensure_ascii=False, indent=1))
    elif cmd == "list":
        apps = load_apps()
        want = sys.argv[2] if len(sys.argv) > 2 else None
        out = {k: v for k, v in apps.items() if not want or v["status"] == want}
        print(json.dumps(out, ensure_ascii=False, indent=1))
    elif cmd == "stale":
        print(json.dumps(stale(int(sys.argv[2]) if len(sys.argv) > 2 else 7),
                         ensure_ascii=False, indent=1))
    else:
        print(json.dumps(stats(), ensure_ascii=False))
