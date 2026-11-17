#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reminder.py — 火一五 Odoo 统一提醒入口

把「提醒我…」这句话落地的统一入口。根据用户输入自动判断建什么：

  ┌──────────────────────────┬───────────────────────────────────────┐
  │ 输入特征                  │ 创建什么                              │
  ├──────────────────────────┼───────────────────────────────────────┤
  │ --when "2026-08-05 09:00"│ calendar.event + alarm（到点推送）    │
  │ 有精确时间，无关联记录     │                                       │
  ├──────────────────────────┼───────────────────────────────────────┤
  │ --model crm.lead --id 88 │ mail.activity（挂在商机/任务/客户上）  │
  │ 关联了业务记录             │                                       │
  ├──────────────────────────┼───────────────────────────────────────┤
  │ --date 2026-08-05         │ project.task（待办+截止日）           │
  │ 只有日期，无时间无关联     │                                       │
  ├──────────────────────────┼───────────────────────────────────────┤
  │ --model + --when          │ mail.activity（关联记录+日期）        │
  │ 关联记录 + 时间            │                                       │
  └──────────────────────────┴───────────────────────────────────────┘

命令
  create    创建提醒     --title 必填；--when/--date/--model+--id 选一；--remind/--note 可选
  due       查到期/即将  --within 30m / --overdue / --today
  list      列出未完成   活动活动+今日会议
  done      完成         done <id> [--type activity|event]
  cancel    取消         cancel <id> [--type activity|event]

示例
  python3 reminder.py create --title "开会" --when "2026-08-05 09:00" --remind 15m
  python3 reminder.py create --title "回访客户" --model crm.lead --id 88 --type call --date 2026-08-06
  python3 reminder.py create --title "交报告" --date 2026-08-10
  python3 reminder.py due --within 60m
  python3 reminder.py due --overdue
  python3 reminder.py done 123 --type activity
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table, to_utc, today

ACT_MODEL = "mail.activity"
EVENT_MODEL = "calendar.event"
TASK_MODEL = "project.task"

ACT_TYPES = {
    "todo": "mail.mail_activity_data_todo",
    "call": "mail.mail_activity_data_call",
    "meeting": "mail.mail_activity_data_meeting",
    "email": "mail.mail_activity_data_email",
    "upload": "mail.mail_activity_data_upload_document",
}


def _has_time(s: str) -> bool:
    """判断日期字符串是否包含时间部分。"""
    s = (s or "").strip()
    return len(s) > 10 and ":" in s[10:]


def _parse_remind(s) -> tuple[int, str]:
    """把 '30m'/'1h'/'1d' 解析成 (数值, 单位)。"""
    s = str(s).strip().lower()
    unit = {"m": "minutes", "h": "hours", "d": "days"}
    if s and s[-1] in unit:
        return int(s[:-1]), unit[s[-1]]
    return int(s), "minutes"


def _resolve_user(odoo: Odoo, ref):
    if not ref:
        return odoo.ensure_uid()
    s = str(ref)
    if s in ("我", "me", "self"):
        return odoo.ensure_uid()
    if s.isdigit():
        return int(s)
    r = odoo.name_search("res.users", s, args=[["share", "=", False]], limit=1)
    if not r:
        raise OdooError(f"找不到用户「{ref}」。")
    return r[0][0]


def _resolve_partner(odoo: Odoo, ref) -> int:
    """名字/id → partner_id。"""
    s = str(ref).strip()
    if s in ("我", "me", "self"):
        uid = odoo.ensure_uid()
        pr = odoo.read("res.users", [uid], ["partner_id"])
        return pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0
    if s.isdigit():
        return int(s)
    r = odoo.name_search("res.partner", s, limit=1)
    if not r:
        raise OdooError(f"找不到联系人「{ref}」。")
    return r[0][0]


# --------------------------------------------------------------------------- #
# create
# --------------------------------------------------------------------------- #
def cmd_create(odoo: Odoo, args):
    title = args.title
    uid = odoo.ensure_uid()

    # 情况 1：有精确时间 + 无关联记录 → calendar.event + alarm
    if args.when and _has_time(args.when) and not args.model:
        vals = {
            "name": title,
            "user_id": uid,
            "start": to_utc(args.when, "09:00:00"),
            "duration": args.duration if args.duration else 0.5,
        }
        if args.location:
            vals["location"] = args.location
        if args.desc:
            vals["description"] = f"<p>{args.desc}</p>"
        # 默认提醒：到点通知（提前 0 分钟）；用户可 --remind 覆盖
        remind_str = args.remind or "0m"
        dur, iv = _parse_remind(remind_str)
        vals["alarm_ids"] = [(0, 0, {
            "name": f"提前{remind_str}" if dur > 0 else "到点提醒",
            "alarm_type": args.alarm_type,
            "duration": dur, "interval": iv,
        })]
        eid = odoo.create(EVENT_MODEL, vals)
        print(f"✅ 已创建提醒（日历事件 #{eid}）：{title}")
        print(f"   时间：{args.when}  提醒：提前{remind_str}（{args.alarm_type}）")
        return

    # 情况 2：关联了业务记录 → mail.activity
    if args.model and args.id:
        kw = {
            "act_type_xmlid": ACT_TYPES.get(args.act_type, ACT_TYPES["todo"]),
            "user_id": _resolve_user(odoo, args.user),
            "summary": title,
        }
        if args.note:
            kw["note"] = f"<p>{args.note}</p>"
        # 日期：优先 --when 的日期部分，其次 --date
        deadline = None
        if args.when:
            deadline = args.when.strip()[:10]
        elif args.date:
            deadline = args.date.strip()[:10]
        else:
            # 默认 3 天后
            deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        kw["date_deadline"] = deadline
        try:
            odoo.execute_kw(args.model, "activity_schedule", [[args.id]], kw)
        except OdooError as e:
            raise OdooError(f"给 {args.model}#{args.id} 加提醒失败：{e}")
        print(f"✅ 已创建提醒（活动挂在 {args.model}#{args.id}）：{title}")
        print(f"   截止：{deadline}  类型：{args.act_type}")
        return

    # 情况 3：只有日期（无时间无关联）→ project.task（待办）
    if args.date and not args.when:
        vals = {
            "name": title,
            "user_ids": [(6, 0, [uid])],
            "date_deadline": to_utc(args.date, "09:00:00"),
        }
        if args.desc:
            from todo import _html
            vals["description"] = _html(args.desc)
        tid = odoo.create(TASK_MODEL, vals)
        print(f"✅ 已创建提醒（待办 #{tid}）：{title}")
        print(f"   截止：{args.date}")
        return

    # 情况 4：--when 有时间 + --model → activity（关联记录+日期）
    if args.when and args.model and args.id:
        kw = {
            "act_type_xmlid": ACT_TYPES.get(args.act_type, ACT_TYPES["todo"]),
            "user_id": _resolve_user(odoo, args.user),
            "summary": title,
            "date_deadline": args.when.strip()[:10],
        }
        if args.note:
            kw["note"] = f"<p>{args.note}</p>"
        try:
            odoo.execute_kw(args.model, "activity_schedule", [[args.id]], kw)
        except OdooError as e:
            raise OdooError(f"给 {args.model}#{args.id} 加提醒失败：{e}")
        print(f"✅ 已创建提醒（活动挂在 {args.model}#{args.id}）：{title}")
        print(f"   截止：{args.when.strip()[:10]}  类型：{args.act_type}")
        return

    # 情况 5：--when 只有日期（无时间）→ project.task
    if args.when and not _has_time(args.when) and not args.model:
        vals = {
            "name": title,
            "user_ids": [(6, 0, [uid])],
            "date_deadline": to_utc(args.when, "09:00:00"),
        }
        if args.desc:
            from todo import _html
            vals["description"] = _html(args.desc)
        tid = odoo.create(TASK_MODEL, vals)
        print(f"✅ 已创建提醒（待办 #{tid}）：{title}")
        print(f"   截止：{args.when.strip()[:10]}")
        return

    raise OdooError(
        "参数不足。用 --when \"YYYY-MM-DD HH:MM\"（精确时间提醒）、"
        "--date YYYY-MM-DD（截止日待办）、或 --model + --id（关联业务记录）指定。"
    )


# --------------------------------------------------------------------------- #
# due
# --------------------------------------------------------------------------- #
def cmd_due(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    t = today()
    results = {"activities": [], "events": [], "todos": []}

    if args.overdue:
        # 逾期活动
        results["activities"] = odoo.search_read(
            ACT_MODEL,
            [("user_id", "=", uid), ("active", "=", True), ("date_deadline", "<", t)],
            ["id", "summary", "res_name", "date_deadline", "activity_type_id"],
            order="date_deadline asc", limit=50)
        # 逾期待办
        results["todos"] = odoo.search_read(
            TASK_MODEL,
            [("user_ids", "in", [uid]), ("project_id", "=", False), ("parent_id", "=", False),
             ("is_closed", "=", False), ("active", "=", True),
             ("date_deadline", "!=", False), ("date_deadline", "<", to_utc(t + " 00:00:00"))],
            ["id", "name", "date_deadline", "priority"],
            order="date_deadline asc", limit=50)
    elif args.today:
        # 今日到期活动
        results["activities"] = odoo.search_read(
            ACT_MODEL,
            [("user_id", "=", uid), ("active", "=", True), ("date_deadline", "=", t)],
            ["id", "summary", "res_name", "date_deadline", "activity_type_id"],
            order="date_deadline asc", limit=50)
    elif args.within:
        # N 分钟内要开始的会议
        within_min = _parse_duration_to_minutes(args.within)
        now_local = datetime.now()
        lo = to_utc(now_local.strftime("%Y-%m-%d %H:%M:%S"))
        hi = to_utc((now_local + timedelta(minutes=within_min)).strftime("%Y-%m-%d %H:%M:%S"))
        pr = odoo.read("res.users", [uid], ["partner_id"])
        mp = pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0
        results["events"] = odoo.search_read(
            EVENT_MODEL,
            ["&", "|", ("user_id", "=", uid), ("partner_ids", "in", [mp]),
             "&", ("start", ">=", lo), ("start", "<=", hi)],
            ["id", "name", "start", "stop", "location"],
            order="start asc", limit=20)
    else:
        # 默认：逾期 + 今日
        results["activities"] = odoo.search_read(
            ACT_MODEL,
            [("user_id", "=", uid), ("active", "=", True), ("date_deadline", "<=", t)],
            ["id", "summary", "res_name", "date_deadline", "activity_type_id"],
            order="date_deadline asc", limit=50)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, default=str))
        return

    total = sum(len(v) for v in results.values())
    if total == 0:
        scope = "逾期" if args.overdue else "今日" if args.today else f"{args.within}内" if args.within else "逾期+今日"
        print(f"✅ 无{scope}到期提醒。")
        return

    scope = "逾期" if args.overdue else "今日" if args.today else f"{args.within}内" if args.within else "逾期+今日"
    print(f"⏰ {scope}到期提醒\n")

    if results["todos"]:
        print(f"📝 逾期待办（{len(results['todos'])}）")
        rows = [[t_item["id"],
                 from_utc(t_item.get("date_deadline") or "", "%m-%d %H:%M") or "-",
                 (t_item.get("name") or "")[:34]]
                for t_item in results["todos"]]
        print(render_table(rows, ["ID", "截止", "标题"]))
        print()

    if results["activities"]:
        label = "逾期活动" if args.overdue else "今日活动"
        print(f"🔔 {label}（{len(results['activities'])}）")
        rows = [[a["id"], a.get("date_deadline") or "-",
                 m2o_name(a.get("activity_type_id")) or "-",
                 (a.get("res_name") or "-")[:16],
                 (a.get("summary") or "")[:24]]
                for a in results["activities"]]
        print(render_table(rows, ["ID", "截止", "类型", "关联", "摘要"]))
        print()

    if results["events"]:
        print(f"📅 即将开始（{len(results['events'])}）")
        rows = [[e["id"],
                 from_utc(e.get("start"), "%H:%M") + "-" + from_utc(e.get("stop"), "%H:%M"),
                 (e.get("name") or "")[:26],
                 (e.get("location") or "-")[:14]]
                for e in results["events"]]
        print(render_table(rows, ["ID", "时间", "主题", "地点"]))
        print()

    print(f"合计 {total} 项")


def _parse_duration_to_minutes(s: str) -> int:
    s = str(s).strip().lower()
    if s.endswith("h"):
        return int(float(s[:-1]) * 60)
    if s.endswith("m"):
        return int(s[:-1])
    return int(s)


# --------------------------------------------------------------------------- #
# list
# --------------------------------------------------------------------------- #
def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    t = today()

    acts = odoo.search_read(
        ACT_MODEL,
        [("user_id", "=", uid), ("active", "=", True)],
        ["id", "summary", "res_name", "res_model", "date_deadline", "activity_type_id"],
        order="date_deadline asc", limit=args.limit)

    if args.json:
        print(json.dumps(acts, ensure_ascii=False, default=str))
        return

    if not acts:
        print("✅ 无未完成提醒。")
        return

    print(f"📋 未完成提醒（{len(acts)}）")
    rows = []
    for a in acts:
        dd = a.get("date_deadline") or "-"
        flag = "🔴" if dd < t else "🟡" if dd == t else ""
        rows.append([flag, a["id"], dd,
                     m2o_name(a.get("activity_type_id")) or "-",
                     (a.get("res_name") or "-")[:16],
                     (a.get("summary") or "")[:24]])
    print(render_table(rows, ["", "ID", "截止", "类型", "关联", "摘要"]))


# --------------------------------------------------------------------------- #
# done / cancel
# --------------------------------------------------------------------------- #
def cmd_done(odoo: Odoo, args):
    if args.type == "event":
        odoo.unlink(EVENT_MODEL, [args.id])
        print(f"✅ 已删除日历事件 #{args.id}")
        return
    # 默认 activity
    try:
        kw = {"feedback": args.feedback} if args.feedback else {}
        odoo.execute_kw(ACT_MODEL, "action_feedback", [[args.id]], kw)
        print(f"✅ 已完成提醒 #{args.id}（活动已归档）")
    except OdooError:
        # 尝试当作待办完成
        try:
            odoo.write(TASK_MODEL, [args.id], {"state": "1_done"})
            print(f"✅ 已完成提醒 #{args.id}（待办标记完成）")
        except OdooError:
            raise OdooError(f"#{args.id} 既不是活动也不是待办，或无权操作。用 --type event|activity 指定。")


def cmd_cancel(odoo: Odoo, args):
    if args.type == "event":
        odoo.unlink(EVENT_MODEL, [args.id])
        print(f"✅ 已取消日历事件 #{args.id}")
        return
    if args.type == "todo":
        odoo.write(TASK_MODEL, [args.id], {"state": "1_canceled"})
        print(f"✅ 已取消待办 #{args.id}")
        return
    # 默认尝试 activity
    try:
        odoo.unlink(ACT_MODEL, [args.id])
        print(f"✅ 已取消提醒 #{args.id}（活动已删除）")
    except OdooError:
        raise OdooError(f"#{args.id} 无法取消。用 --type event|todo|activity 指定类型。")


# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 统一提醒入口")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    # create
    cr = sub.add_parser("create", help="创建提醒")
    cr.add_argument("--title", required=True, help="提醒标题")
    cr.add_argument("--when", help="时间 YYYY-MM-DD HH:MM（有精确时间→日历事件+闹钟）")
    cr.add_argument("--date", help="日期 YYYY-MM-DD（仅日期→待办截止日）")
    cr.add_argument("--model", help="关联模型，如 crm.lead / project.task")
    cr.add_argument("--id", type=int, help="关联记录 id")
    cr.add_argument("--act-type", choices=list(ACT_TYPES), default="todo",
                    help="活动类型（关联记录时用）")
    cr.add_argument("--remind", help="提前提醒量 0m/15m/30m/1h/1d（日历事件用，默认到点）")
    cr.add_argument("--alarm-type", choices=["notification", "email"], default="notification")
    cr.add_argument("--duration", type=float, help="事件时长（小时，默认 0.5）")
    cr.add_argument("--location", help="事件地点")
    cr.add_argument("--desc", help="描述")
    cr.add_argument("--note", help="备注（活动用）")
    cr.add_argument("--user", help="负责人（名字/id/我），默认我")

    # due
    du = sub.add_parser("due", help="查到期/即将到期的提醒")
    du.add_argument("--within", help="N 分钟内到期的会议，如 30m/1h")
    du.add_argument("--overdue", action="store_true", help="只看逾期")
    du.add_argument("--today", action="store_true", help="只看今日到期")

    # list
    li = sub.add_parser("list", help="列出未完成提醒")
    li.add_argument("--limit", type=int, default=100)

    # done
    dn = sub.add_parser("done", help="完成提醒")
    dn.add_argument("id", type=int)
    dn.add_argument("--type", choices=["activity", "event", "todo"], help="提醒类型")
    dn.add_argument("--feedback", help="完成反馈（活动用）")

    # cancel
    ca = sub.add_parser("cancel", help="取消提醒")
    ca.add_argument("id", type=int)
    ca.add_argument("--type", choices=["activity", "event", "todo"], help="提醒类型")

    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "create": cmd_create,
            "due": cmd_due,
            "list": cmd_list,
            "done": cmd_done,
            "cancel": cmd_cancel,
        }
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
