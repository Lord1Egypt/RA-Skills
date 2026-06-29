#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
activity.py — 火一五 Odoo「活动 / Activity」管理（mail.activity）

活动 = 挂在任意记录（商机/项目任务/客户…）上的"下一步待办/提醒"。
字段坑（详见 references/odoo-activity-calendar-api.md）：
  - date_deadline 是 **Date**（不是 datetime）。
  - state 是 computed 无 search —— 查逾期/今日用 date_deadline 比较，别在 domain 写 state。
  - "完成"是 archive（active=False）不是删除，记录仍在，用 action_feedback。

命令
  list      我的活动（默认逾期+今日）  --all/--overdue/--today/--planned
  add       给某记录加活动            --model crm.lead --id 88 --type call --summary ... --date ...
  done      标记完成（archive）       done <id> ... [--feedback "..."]
  cancel    取消（删除）              cancel <id> ...
  reschedule 改期                     reschedule <id> --date YYYY-MM-DD

示例
  python3 activity.py add --model crm.lead --id 88 --type call --summary "3天后回访" --date 2026-06-10
  python3 activity.py list
  python3 activity.py done 123 --feedback "已回访"
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import m2o_name, render_table, today

MODEL = "mail.activity"
ACT_TYPES = {
    "todo": "mail.mail_activity_data_todo",
    "call": "mail.mail_activity_data_call",
    "meeting": "mail.mail_activity_data_meeting",
    "email": "mail.mail_activity_data_email",
    "upload": "mail.mail_activity_data_upload_document",
}


def _state(dd: str, t: str) -> str:
    if not dd:
        return ""
    return "🔴逾期" if dd < t else "🟡今日" if dd == t else "计划"


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


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    t = today()
    domain = [("user_id", "=", uid), ("active", "=", True)]
    if args.overdue:
        domain.append(("date_deadline", "<", t))
    elif args.today:
        domain.append(("date_deadline", "=", t))
    elif args.planned:
        domain.append(("date_deadline", ">", t))
    elif not args.all:
        domain.append(("date_deadline", "<=", t))  # 默认：逾期 + 今日
    acts = odoo.search_read(
        MODEL, domain,
        ["id", "summary", "res_model", "res_id", "res_name", "date_deadline", "activity_type_id"],
        order="date_deadline asc", limit=args.limit)
    if args.json:
        print(json.dumps(acts, ensure_ascii=False, default=str))
        return
    rows = []
    for a in acts:
        link = a.get("res_name") or (f"{a.get('res_model')}#{a.get('res_id')}" if a.get("res_model") else "-")
        rows.append([
            a["id"], _state(a.get("date_deadline"), t), a.get("date_deadline") or "-",
            m2o_name(a.get("activity_type_id")) or "-",
            link[:20], (a.get("summary") or "")[:30],
        ])
    print(render_table(rows, ["ID", "状态", "截止", "类型", "关联", "摘要"]))
    scope = "全部未完成" if args.all else "逾期" if args.overdue else "今日" if args.today else "计划" if args.planned else "逾期+今日"
    print(f"\n共 {len(acts)} 条活动（{scope}）")


def cmd_add(odoo: Odoo, args):
    kw = {"act_type_xmlid": ACT_TYPES[args.type], "user_id": _resolve_user(odoo, args.user)}
    if args.summary:
        kw["summary"] = args.summary
    if args.note:
        kw["note"] = f"<p>{args.note}</p>"
    if args.date:
        kw["date_deadline"] = args.date.strip()[:10]
    try:
        odoo.execute_kw(args.model, "activity_schedule", [[args.id]], kw)
    except OdooError as e:
        raise OdooError(f"给 {args.model}#{args.id} 加活动失败：{e}")
    print(f"✅ 已给 {args.model}#{args.id} 加「{args.type}」活动" + (f"：{args.summary}" if args.summary else ""))


def cmd_done(odoo: Odoo, args):
    kw = {"feedback": args.feedback} if args.feedback else {}
    odoo.execute_kw(MODEL, "action_feedback", [args.ids], kw)
    print(f"✅ 已完成活动：{', '.join('#' + str(i) for i in args.ids)}（已归档）")


def cmd_cancel(odoo: Odoo, args):
    odoo.unlink(MODEL, args.ids)
    print(f"✅ 已取消活动：{', '.join('#' + str(i) for i in args.ids)}")


def cmd_reschedule(odoo: Odoo, args):
    odoo.write(MODEL, [args.id], {"date_deadline": args.date.strip()[:10]})
    print(f"✅ 活动 #{args.id} 已改期到 {args.date}")


def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 活动管理")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="我的活动")
    li.add_argument("--all", action="store_true", help="全部未完成")
    li.add_argument("--overdue", action="store_true")
    li.add_argument("--today", action="store_true")
    li.add_argument("--planned", action="store_true")
    li.add_argument("--limit", type=int, default=100)

    ad = sub.add_parser("add", help="给某记录加活动")
    ad.add_argument("--model", required=True, help="关联模型，如 crm.lead / project.task")
    ad.add_argument("--id", required=True, type=int, help="关联记录 id")
    ad.add_argument("--type", choices=list(ACT_TYPES), default="todo")
    ad.add_argument("--summary")
    ad.add_argument("--note")
    ad.add_argument("--date", help="截止日 YYYY-MM-DD")
    ad.add_argument("--user", help="负责人（名字/id/我），默认我")

    dn = sub.add_parser("done", help="完成活动")
    dn.add_argument("ids", nargs="+", type=int)
    dn.add_argument("--feedback")

    ca = sub.add_parser("cancel", help="取消活动")
    ca.add_argument("ids", nargs="+", type=int)

    rs = sub.add_parser("reschedule", help="改期")
    rs.add_argument("id", type=int)
    rs.add_argument("--date", required=True, help="YYYY-MM-DD")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"list": cmd_list, "add": cmd_add, "done": cmd_done,
                    "cancel": cmd_cancel, "reschedule": cmd_reschedule}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
