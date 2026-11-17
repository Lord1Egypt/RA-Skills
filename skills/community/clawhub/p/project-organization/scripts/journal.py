#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""journal.py — 查看/渲染大项目操作日志（skill: project-organization）。

日志源：`<大项目根>/.tools/journal.jsonl`（append-only，每行一个事件 JSON）。
由 new_big_project / new_subproject / trash / audit_project 在成功时写入。

用法:
  python scripts/journal.py                       # 列出全部（JSON）
  python scripts/journal.py --tail 20             # 最近 20 条
  python scripts/journal.py --event trash --since 2026-09-01
  python scripts/journal.py --render              # 生成 .tools/_log.md（Markdown）
  python scripts/journal.py --root /path/to/root --tail 5

stdout: {"status":"ok","root":...,"count":N,"records":[...]}（默认）
        --render 时: {"status":"ok","root":...,"path":...,"count":N}
"""
import argparse
import datetime
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def parse_since(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def resolve_root(explicit):
    if explicit:
        return Path(explicit).expanduser().resolve()
    root = C.find_root(Path.cwd())
    if root is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)
    return root


def main():
    ap = argparse.ArgumentParser(description="查看/渲染大项目操作日志")
    ap.add_argument("--root", help="大项目根（默认从 cwd 向上查找标记）")
    ap.add_argument("--tail", type=int, default=None, help="只显示最近 N 条")
    ap.add_argument("--since", help="起始时间（YYYY-MM-DD 或 ISO）")
    ap.add_argument("--event", help="事件过滤（子串匹配，如 trash / created / audit）")
    ap.add_argument("--actor", help="操作者过滤（子串匹配）")
    ap.add_argument("--render", action="store_true", help="生成 .tools/_log.md")
    ap.add_argument("--out", help="--render 的输出路径（默认 .tools/_log.md）")
    args = ap.parse_args()

    root = resolve_root(args.root)
    records = C.read_journal(root)

    since = parse_since(args.since)
    if since is not None or args.event or args.actor:
        filtered = []
        for r in records:
            if args.event and args.event.lower() not in str(r.get("event", "")).lower():
                continue
            if args.actor and args.actor.lower() not in str(r.get("actor", "")).lower():
                continue
            if since is not None:
                try:
                    ts = datetime.datetime.fromisoformat(r.get("ts", ""))
                    if ts < since:
                        continue
                except ValueError:
                    if str(r.get("ts", "")) < args.since:
                        continue
            filtered.append(r)
        records = filtered

    if args.tail is not None and args.tail >= 0:
        records = records[-args.tail:] if args.tail else []

    if args.render:
        out = Path(args.out).expanduser() if args.out else C.journal_path(root, markdown=True)
        C.write_text(out, C.render_journal(records))
        C.emit({"status": "ok", "root": str(root), "path": str(out),
                "count": len(records)}, 0)

    C.emit({"status": "ok", "root": str(root),
            "count": len(records), "records": records}, 0)


if __name__ == "__main__":
    main()
