#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
briefing.py — 火一五 Odoo「我的一天/一周」总览（聚合待办 + 活动 + 会议）

把三处该做的事汇总到一个视图，辅助做提醒和待办：
  - 待办 project.task（我的、未完成、到期 <= 范围末，含逾期）
  - 活动 mail.activity（指派给我、未完成、到期 <= 范围末，含逾期）
  - 会议 calendar.event（我参与的、start 落在范围内）

命令
  briefing.py            今天总览（默认）
  briefing.py today
  briefing.py week       本周总览
  --json                 输出结构化 JSON

示例
  python3 briefing.py            # 我今天要做什么
  python3 briefing.py week
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, priority_label, render_table, to_utc, today


def _range(when: str):
    """返回 (截止末-Date, 会议起-UTC, 会议止-UTC, 标签)。"""
    t = today()
    base = datetime.strptime(t, "%Y-%m-%d")
    if when == "week":
        mon = base - timedelta(days=base.weekday())
        end_date = (mon + timedelta(days=6)).strftime("%Y-%m-%d")
        ev_lo = to_utc(mon.strftime("%Y-%m-%d") + " 00:00:00")
        ev_hi = to_utc((mon + timedelta(days=7)).strftime("%Y-%m-%d") + " 00:00:00")
        return end_date, ev_lo, ev_hi, f"本周（~{end_date}）"
    return t, to_utc(t + " 00:00:00"), to_utc(t + " 23:59:59"), f"今天 {t}"


def _overdue(date_str: str, today_str: str) -> str:
    d = (date_str or "")[:10]
    return "🔴" if d and d < today_str else ""


def run(odoo: Odoo, when: str, as_json: bool):
    uid = odoo.ensure_uid()
    t = today()
    end_date, ev_lo, ev_hi, label = _range(when)
    deadline_end = to_utc(end_date + " 23:59:59")  # 待办 date_deadline 是 datetime

    todos = odoo.search_read(
        "project.task",
        [("user_ids", "in", [uid]), ("project_id", "=", False), ("parent_id", "=", False),
         ("is_closed", "=", False), ("active", "=", True), ("date_deadline", "<=", deadline_end)],
        ["id", "name", "date_deadline", "priority"], order="date_deadline asc")
    acts = odoo.search_read(
        "mail.activity",
        [("user_id", "=", uid), ("active", "=", True), ("date_deadline", "<=", end_date)],
        ["id", "summary", "res_name", "res_model", "res_id", "date_deadline", "activity_type_id"],
        order="date_deadline asc")
    pr = odoo.read("res.users", [uid], ["partner_id"])
    mp = pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0
    evs = odoo.search_read(
        "calendar.event",
        ["&", "|", ("user_id", "=", uid), ("partner_ids", "in", [mp]),
         "&", ("start", ">=", ev_lo), ("start", "<", ev_hi)],
        ["id", "name", "start", "stop", "allday", "location"], order="start asc")

    if as_json:
        print(json.dumps({"todos": todos, "activities": acts, "meetings": evs},
                         ensure_ascii=False, default=str))
        return

    print(f"🗓️  我的{label}\n")

    print(f"⏰ 待办（{len(todos)}）")
    if todos:
        rows = [[_overdue(x.get("date_deadline"), t), x["id"],
                 from_utc(x.get("date_deadline") or "", "%m-%d %H:%M") or "无期限",
                 priority_label(str(x.get("priority", "0"))),
                 (x.get("name") or "")[:34]] for x in todos]
        print(render_table(rows, ["", "ID", "截止", "优先级", "标题"]))
    else:
        print("   （无）")

    print(f"\n🔔 活动（{len(acts)}）")
    if acts:
        rows = [[_overdue(a.get("date_deadline"), t), a["id"], a.get("date_deadline") or "-",
                 m2o_name(a.get("activity_type_id")) or "-",
                 (a.get("res_name") or (f"{a.get('res_model')}#{a.get('res_id')}" if a.get("res_model") else "-"))[:16],
                 (a.get("summary") or "")[:24]] for a in acts]
        print(render_table(rows, ["", "ID", "截止", "类型", "关联", "摘要"]))
    else:
        print("   （无）")

    print(f"\n📅 会议（{len(evs)}）")
    if evs:
        rows = []
        for e in evs:
            when_s = (e.get("start") or "")[:10] + " 全天" if e.get("allday") else \
                from_utc(e.get("start"), "%m-%d %H:%M") + "-" + from_utc(e.get("stop"), "%H:%M")
            rows.append([e["id"], when_s, (e.get("name") or "")[:26], (e.get("location") or "-")[:14]])
        print(render_table(rows, ["ID", "时间", "主题", "地点"]))
    else:
        print("   （无）")

    total = len(todos) + len(acts) + len(evs)
    print(f"\n合计 {total} 项（待办 {len(todos)} / 活动 {len(acts)} / 会议 {len(evs)}）")


def main(argv=None):
    p = argparse.ArgumentParser(description="火一五 Odoo 我的一天/一周总览")
    p.add_argument("when", nargs="?", choices=["today", "week"], default="today")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv if argv is not None else sys.argv[1:])
    try:
        run(Odoo(tools_md=args.tools_md), args.when, args.json)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
