#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
heartbeat_check.py — 火一五 Odoo 心跳巡检（为 OpenClaw heartbeat 优化）

在 OpenClaw 心跳（HEARTBEAT）触发时调用，主动检查辉火云企业套件中的：
  - 逾期待办（project.task，date_deadline < 今天）
  - 今日到期活动（mail.activity，date_deadline <= 今天，含逾期）
  - 即将开始的会议（calendar.event，start 在 N 分钟内）

输出精简、可操作，适合龙虾在心跳中直接转发给用户或静默。

命令
  heartbeat_check.py                    # 默认：逾期 + 今日 + 即将开始（30分钟内）
  heartbeat_check.py --imminent 60m     # 查 60 分钟内要开始的会议
  heartbeat_check.py --overdue-only     # 只报逾期项（待办+活动）
  heartbeat_check.py --today            # 只报今日到期项
  heartbeat_check.py --json             # JSON 输出（供 OpenClaw 解析）

示例
  python3 heartbeat_check.py                       # 默认巡检
  python3 heartbeat_check.py --imminent 15m        # 15分钟内的会议
  python3 heartbeat_check.py --json                # 结构化输出
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, priority_label, render_table, to_utc, today


def _parse_duration(s: str) -> int:
    """把 '30m' / '1h' / '2h' / '90' 解析成分钟数。"""
    s = str(s).strip().lower()
    if s.endswith("h"):
        return int(float(s[:-1]) * 60)
    if s.endswith("m"):
        return int(s[:-1])
    return int(s)


def _overdue_flag(date_str: str, today_str: str) -> str:
    d = (date_str or "")[:10]
    return "🔴" if d and d < today_str else ""


def _query_todos(odoo: Odoo, uid: int, t: str, overdue_only: bool):
    """查我的逾期待办（及今日到期）。"""
    domain = [
        ("user_ids", "in", [uid]),
        ("project_id", "=", False),
        ("parent_id", "=", False),
        ("is_closed", "=", False),
        ("active", "=", True),
    ]
    if overdue_only:
        deadline = to_utc(t + " 00:00:00")
        domain.append(("date_deadline", "<", deadline))
    else:
        deadline = to_utc(t + " 23:59:59")
        domain.append(("date_deadline", "<=", deadline))
        domain.append(("date_deadline", "!=", False))
    return odoo.search_read(
        "project.task", domain,
        ["id", "name", "date_deadline", "priority"],
        order="date_deadline asc", limit=50)


def _query_activities(odoo: Odoo, uid: int, t: str, overdue_only: bool):
    """查我的逾期/今日活动。"""
    domain = [("user_id", "=", uid), ("active", "=", True)]
    if overdue_only:
        domain.append(("date_deadline", "<", t))
    else:
        domain.append(("date_deadline", "<=", t))
    return odoo.search_read(
        "mail.activity", domain,
        ["id", "summary", "res_name", "res_model", "res_id",
         "date_deadline", "activity_type_id"],
        order="date_deadline asc", limit=50)


def _query_meetings(odoo: Odoo, uid: int, within_minutes: int):
    """查 N 分钟内要开始的会议。"""
    now_local = datetime.now()
    lo = to_utc(now_local.strftime("%Y-%m-%d %H:%M:%S"))
    hi = to_utc((now_local + timedelta(minutes=within_minutes)).strftime("%Y-%m-%d %H:%M:%S"))
    pr = odoo.read("res.users", [uid], ["partner_id"])
    mp = pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0
    domain = [
        "&", "|", ("user_id", "=", uid), ("partner_ids", "in", [mp]),
        "&", ("start", ">=", lo), ("start", "<=", hi),
    ]
    return odoo.search_read(
        "calendar.event", domain,
        ["id", "name", "start", "stop", "allday", "location"],
        order="start asc", limit=20)


def _query_today_meetings(odoo: Odoo, uid: int, t: str):
    """查今天的会议。"""
    lo = to_utc(t + " 00:00:00")
    hi = to_utc(t + " 23:59:59")
    pr = odoo.read("res.users", [uid], ["partner_id"])
    mp = pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0
    domain = [
        "&", "|", ("user_id", "=", uid), ("partner_ids", "in", [mp]),
        "&", ("start", ">=", lo), ("start", "<=", hi),
    ]
    return odoo.search_read(
        "calendar.event", domain,
        ["id", "name", "start", "stop", "allday", "location"],
        order="start asc", limit=20)


def run(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    t = today()
    overdue_only = args.overdue_only
    today_only = args.today and not overdue_only

    # 查询
    todos = []
    acts = []
    meetings = []

    if overdue_only:
        todos = _query_todos(odoo, uid, t, True)
        acts = _query_activities(odoo, uid, t, True)
    elif today_only:
        todos = _query_todos(odoo, uid, t, False)
        acts = _query_activities(odoo, uid, t, False)
        meetings = _query_today_meetings(odoo, uid, t)
    else:
        # 默认模式：逾期 + 今日 + 即将开始
        todos = _query_todos(odoo, uid, t, False)
        acts = _query_activities(odoo, uid, t, False)
        within = _parse_duration(args.imminent)
        meetings = _query_meetings(odoo, uid, within)

    # JSON 输出
    if args.json:
        result = {
            "date": t,
            "overdue_todos": todos,
            "today_activities": acts,
            "imminent_meetings": meetings,
            "summary": {
                "overdue_todo_count": sum(1 for x in todos if _overdue_flag(x.get("date_deadline"), t)),
                "today_todo_count": len(todos),
                "activity_count": len(acts),
                "meeting_count": len(meetings),
                "total": len(todos) + len(acts) + len(meetings),
            },
        }
        print(json.dumps(result, ensure_ascii=False, default=str))
        return

    # 文本输出（精简，适合心跳转发）
    total = len(todos) + len(acts) + len(meetings)
    if total == 0:
        print("✅ 无逾期/今日待办、活动或即将开始的会议。")
        return

    print(f"🗓️  巡检结果（{t}）\n")

    if todos:
        overdue_count = sum(1 for x in todos if _overdue_flag(x.get("date_deadline"), t))
        label = f"逾期待办（{overdue_count}）" if overdue_only else f"今日待办（{len(todos)}）"
        print(f"📝 {label}")
        rows = [
            [_overdue_flag(x.get("date_deadline"), t), x["id"],
             from_utc(x.get("date_deadline") or "", "%m-%d %H:%M") or "无期限",
             priority_label(str(x.get("priority", "0"))),
             (x.get("name") or "")[:34]]
            for x in todos
        ]
        print(render_table(rows, ["", "ID", "截止", "优先级", "标题"]))
        print()

    if acts:
        overdue_count = sum(1 for x in acts if _overdue_flag(x.get("date_deadline"), t))
        label = f"逾期活动（{overdue_count}）" if overdue_only else f"今日活动（{len(acts)}）"
        print(f"🔔 {label}")
        rows = [
            [_overdue_flag(a.get("date_deadline"), t), a["id"],
             a.get("date_deadline") or "-",
             m2o_name(a.get("activity_type_id")) or "-",
             (a.get("res_name") or "-")[:16],
             (a.get("summary") or "")[:24]]
            for a in acts
        ]
        print(render_table(rows, ["", "ID", "截止", "类型", "关联", "摘要"]))
        print()

    if meetings:
        within_label = f"{args.imminent}内" if not today_only else "今日"
        print(f"📅 即将开始（{within_label}，{len(meetings)}）")
        rows = []
        for e in meetings:
            if e.get("allday"):
                when_s = (e.get("start") or "")[:10] + " 全天"
            else:
                when_s = from_utc(e.get("start"), "%H:%M") + "-" + from_utc(e.get("stop"), "%H:%M")
            rows.append([e["id"], when_s, (e.get("name") or "")[:26], (e.get("location") or "-")[:14]])
        print(render_table(rows, ["ID", "时间", "主题", "地点"]))
        print()

    print(f"合计 {total} 项（待办 {len(todos)} / 活动 {len(acts)} / 会议 {len(meetings)}）")


def main(argv=None):
    p = argparse.ArgumentParser(description="火一五 Odoo 心跳巡检（OpenClaw heartbeat 专用）")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.add_argument("--imminent", default="30m",
                   help="查 N 分钟内要开始的会议（如 30m/1h/90），默认 30m")
    p.add_argument("--overdue-only", action="store_true", help="只报逾期项")
    p.add_argument("--today", action="store_true", help="只报今日到期项")
    args = p.parse_args(argv if argv is not None else sys.argv[1:])
    try:
        run(Odoo(tools_md=args.tools_md), args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
