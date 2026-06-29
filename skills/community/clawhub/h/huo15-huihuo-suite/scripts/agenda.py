#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agenda.py — 火一五 Odoo「日历 / Calendar」事件、重复、参与人、提醒、忙闲

> 脚本名特意叫 agenda（不叫 calendar），避免遮蔽 Python 标准库 calendar
> （odoo_utils / timesheet 都 import 了它）。

字段坑（详见 references/odoo-calendar-advanced-api.md + odoo-activity-calendar-api.md）：
  - start/stop 是 Datetime/UTC（脚本自动把本地时间转 UTC）。
  - 重复事件走 calendar.event 的 create/write（recurrency=True 必须）；rrule 串只读，用结构化字段。
  - 改重复事件要带 scope（self/future/all → recurrence_update）；all 不能改时间。
  - 加/减参与人用 partner_ids 的 (4,id)/(3,id)；写它自动建/删 attendee。
  - 找空闲用区间重叠 + show_as=busy；crm 商机用 opportunity_id 关联。

命令
  list       我的日程（默认本周）  --today/--month/--from --to
  show       事件详情（重复/参与人响应/关联）
  add        新建事件   --name --start --end|--duration --location --with --remind
             重复：--repeat weekly --on mon --count 52 / --repeat monthly --day 1
             关联：--opportunity <商机>   标签：--tags
  update     改事件     --name/--start/--end/--location  重复事件加 --scope self|future|all
  cancel     删除事件   cancel <id> ...  （重复系列见 --series）
  remind     加提醒     remind <id> --before 30m [--type notification|email]
  invite     加/减参与人 invite <id> --add 张三 / --remove 李四
  attendees  查参与人响应（接受/拒绝/待定/待回复 + 统计）
  rsvp       代参与人回复  rsvp <id> --who 张三 --status accept|decline|tentative
  busy       查某人某时段忙闲  busy --who 张三 --date 2026-06-25 （或 --from --to）

示例
  python3 agenda.py add --name "周例会" --start "2026-06-29 09:00" --duration 1 --repeat weekly --on mon --count 52
  python3 agenda.py attendees 5
  python3 agenda.py busy --who 张三 --date 2026-06-25
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table, to_utc, today

EVENT = "calendar.event"
ALARM = "calendar.alarm"
ATTENDEE = "calendar.attendee"
DEFAULT_TZ = "Asia/Shanghai"
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
ATT_STATE = {"accepted": "✅接受", "declined": "❌拒绝",
             "tentative": "🤔待定", "needsAction": "⏳待回复"}
SCOPE = {"self": "self_only", "future": "future_events", "all": "all_events"}


def _parse_remind(s) -> tuple[int, str]:
    s = str(s).strip().lower()
    unit = {"m": "minutes", "h": "hours", "d": "days"}
    if s and s[-1] in unit:
        return int(s[:-1]), unit[s[-1]]
    return int(s), "minutes"


def _resolve_partners(odoo: Odoo, s: str) -> list[int]:
    out = []
    for n in s.split(","):
        n = n.strip()
        if not n:
            continue
        if n in ("我", "me", "self"):
            uid = odoo.ensure_uid()
            pr = odoo.read("res.users", [uid], ["partner_id"])
            if pr and pr[0].get("partner_id"):
                out.append(pr[0]["partner_id"][0])
            continue
        if n.isdigit():
            out.append(int(n))
            continue
        r = odoo.name_search("res.partner", n, limit=1)
        if not r:
            raise OdooError(f"找不到联系人「{n}」。")
        out.append(r[0][0])
    return out


def _my_partner(odoo: Odoo) -> int:
    pr = odoo.read("res.users", [odoo.ensure_uid()], ["partner_id"])
    return pr[0]["partner_id"][0] if pr and pr[0].get("partner_id") else 0


def _build_recurrence(args) -> dict:
    """把 --repeat/--on/--count/... 转成 calendar.event 的重复字段。"""
    if not args.repeat:
        return {}
    r = {"recurrency": True, "rrule_type": args.repeat,
         "interval": args.interval or 1, "event_tz": args.tz or DEFAULT_TZ}
    if args.repeat == "weekly" and args.on:
        for d in args.on.split(","):
            d = d.strip().lower()[:3]
            if d in WEEKDAYS:
                r[d] = True
    if args.repeat == "monthly":
        r["month_by"] = "date"
        r["day"] = args.day or 1
    if args.until:
        r["end_type"] = "end_date"
        r["until"] = args.until.strip()[:10]
    elif args.count:
        r["end_type"] = "count"
        r["count"] = args.count
    else:
        r["end_type"] = "forever"
    return r


def _resolve_event_for_partner(odoo: Odoo, event_id: int, who: str) -> list[int]:
    pid = _resolve_partners(odoo, who)[0]
    att = odoo.search(ATTENDEE, [["event_id", "=", event_id], ["partner_id", "=", pid]], limit=1)
    if not att:
        raise OdooError(f"「{who}」不是事件 #{event_id} 的参与人。")
    return att


# --------------------------------------------------------------------------- #
def _period(args):
    t = today()
    base = datetime.strptime(t, "%Y-%m-%d")
    if args.date_from or args.date_to:
        lo_d = args.date_from or t
        hi_d = args.date_to or t
        hi_next = (datetime.strptime(hi_d, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        return to_utc(lo_d + " 00:00:00"), to_utc(hi_next + " 00:00:00"), f"{lo_d}~{hi_d}"
    if args.today:
        lo, hi, label = base, base + timedelta(days=1), "今天"
    elif args.month:
        lo = base.replace(day=1)
        hi = (lo.replace(day=28) + timedelta(days=4)).replace(day=1)
        label = lo.strftime("%Y-%m")
    else:
        lo = base - timedelta(days=base.weekday())
        hi = lo + timedelta(days=7)
        label = "本周"
    return (to_utc(lo.strftime("%Y-%m-%d %H:%M:%S")),
            to_utc(hi.strftime("%Y-%m-%d %H:%M:%S")), label)


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    lo, hi, label = _period(args)
    mp = _my_partner(odoo)
    domain = ["&", "|", ("user_id", "=", uid), ("partner_ids", "in", [mp]),
              "&", ("start", ">=", lo), ("start", "<", hi)]
    evs = odoo.search_read(
        EVENT, domain,
        ["id", "name", "start", "stop", "allday", "location", "partner_ids", "alarm_ids", "recurrency"],
        order="start asc", limit=args.limit)
    if args.json:
        print(json.dumps(evs, ensure_ascii=False, default=str))
        return
    rows = []
    for e in evs:
        when = (e.get("start") or "")[:10] + " 全天" if e.get("allday") else \
            from_utc(e.get("start"), "%m-%d %H:%M") + "-" + from_utc(e.get("stop"), "%H:%M")
        rows.append([
            e["id"], when, (e.get("name") or "")[:22] + ("🔁" if e.get("recurrency") else ""),
            (e.get("location") or "-")[:12], f"{len(e.get('partner_ids') or [])}人",
            "🔔" if e.get("alarm_ids") else ""])
    print(render_table(rows, ["ID", "时间", "主题", "地点", "参与", "提醒"]))
    print(f"\n共 {len(evs)} 个事件（{label}）")


def cmd_show(odoo: Odoo, args):
    e = odoo.read(EVENT, [args.id], [
        "name", "start", "stop", "allday", "location", "description", "user_id",
        "partner_ids", "alarm_ids", "recurrency", "rrule", "opportunity_id",
        "res_model", "res_id", "accepted_count", "declined_count", "tentative_count", "awaiting_count"])
    if not e:
        raise OdooError(f"事件 #{args.id} 不存在。")
    e = e[0]
    print(f"📅 事件 #{args.id}：{e['name']}" + ("  🔁重复" if e.get("recurrency") else ""))
    if e.get("allday"):
        print(f"   时间：{(e.get('start') or '')[:10]} 全天")
    else:
        print(f"   时间：{from_utc(e.get('start'))} ~ {from_utc(e.get('stop'), '%H:%M')}（本地）")
    print(f"   地点：{e.get('location') or '-'}   组织者：{m2o_name(e.get('user_id')) or '-'}")
    if e.get("recurrency") and e.get("rrule"):
        print(f"   重复：{e['rrule']}")
    if e.get("opportunity_id"):
        print(f"   关联商机：{m2o_name(e['opportunity_id'])}")
    elif e.get("res_model"):
        print(f"   关联记录：{e['res_model']}#{e.get('res_id')}")
    pids = e.get("partner_ids") or []
    if pids:
        print(f"   参与人：{len(pids)}人（接受{e.get('accepted_count', 0)}/拒绝{e.get('declined_count', 0)}"
              f"/待定{e.get('tentative_count', 0)}/待回复{e.get('awaiting_count', 0)}）")
    aids = e.get("alarm_ids") or []
    if aids:
        al = odoo.read(ALARM, aids, ["name"])
        print(f"   提醒：{', '.join(a['name'] for a in al)}")


def _resolve_opportunity(odoo: Odoo, ref):
    if str(ref).isdigit():
        return int(ref)
    r = odoo.name_search("crm.lead", str(ref), limit=1)
    if not r:
        raise OdooError(f"找不到商机「{ref}」。")
    return r[0][0]


def cmd_add(odoo: Odoo, args):
    vals = {"name": args.name, "user_id": odoo.ensure_uid()}
    if args.allday:
        d = args.start.strip()[:10]
        end = args.end.strip()[:10] if args.end else d
        vals.update(allday=True, start=f"{d} 08:00:00", stop=f"{end} 18:00:00")
    else:
        vals["start"] = to_utc(args.start)
        if args.end:
            vals["stop"] = to_utc(args.end)
        else:
            vals["duration"] = args.duration if args.duration else 1.0
    if args.location:
        vals["location"] = args.location
    if getattr(args, "with_", None):
        vals["partner_ids"] = [(6, 0, _resolve_partners(odoo, args.with_))]
    if args.desc:
        vals["description"] = f"<p>{args.desc}</p>"
    if args.remind:
        dur, iv = _parse_remind(args.remind)
        vals["alarm_ids"] = [(0, 0, {"name": f"提前{args.remind}", "alarm_type": "notification",
                                     "duration": dur, "interval": iv})]
    if args.opportunity:
        vals["opportunity_id"] = _resolve_opportunity(odoo, args.opportunity)
    if args.tags:
        tids = []
        for n in args.tags.split(","):
            n = n.strip()
            if not n:
                continue
            ex = odoo.search("calendar.event.type", [["name", "=", n]], limit=1)
            tids.append(ex[0] if ex else odoo.create("calendar.event.type", {"name": n}))
        vals["categ_ids"] = [(6, 0, tids)]
    vals.update(_build_recurrence(args))
    eid = odoo.create(EVENT, vals)
    extra = []
    if args.repeat:
        extra.append(f"重复 {args.repeat}")
    if args.remind:
        extra.append(f"提前{args.remind}提醒")
    if args.opportunity:
        extra.append("已关联商机")
    print(f"✅ 已新建日历事件 #{eid}：{args.name}" + (f"（{'、'.join(extra)}）" if extra else ""))


def cmd_update(odoo: Odoo, args):
    vals = {}
    if args.name:
        vals["name"] = args.name
    if args.start:
        vals["start"] = to_utc(args.start)
    if args.end:
        vals["stop"] = to_utc(args.end)
    if args.location:
        vals["location"] = args.location
    if not vals:
        raise OdooError("没有要修改的字段。")
    if args.scope:
        vals["recurrence_update"] = SCOPE[args.scope]
    odoo.write(EVENT, [args.id], vals)
    tail = f"（范围：{args.scope}）" if args.scope else ""
    print(f"✅ 已更新事件 #{args.id}：{', '.join(k for k in vals if k != 'recurrence_update')}{tail}")


def cmd_cancel(odoo: Odoo, args):
    if args.series:
        # 删重复系列：future=将来所有，all=整个系列
        for i in args.ids:
            odoo.execute_kw(EVENT, "action_mass_deletion", [[i], SCOPE[args.series]])
        print(f"✅ 已删除事件系列（{args.series}）：{', '.join('#' + str(i) for i in args.ids)}")
    else:
        odoo.unlink(EVENT, args.ids)
        print(f"✅ 已删除事件：{', '.join('#' + str(i) for i in args.ids)}")


def cmd_remind(odoo: Odoo, args):
    dur, iv = _parse_remind(args.before)
    odoo.write(EVENT, [args.id], {"alarm_ids": [(0, 0, {
        "name": f"提前{args.before}", "alarm_type": args.type,
        "duration": dur, "interval": iv})]})
    print(f"✅ 已给事件 #{args.id} 加提醒：提前 {args.before}（{args.type}）")


def cmd_invite(odoo: Odoo, args):
    cmds = []
    added = removed = ""
    if args.add:
        ids = _resolve_partners(odoo, args.add)
        cmds += [(4, p) for p in ids]
        added = args.add
    if args.remove:
        ids = _resolve_partners(odoo, args.remove)
        cmds += [(3, p) for p in ids]
        removed = args.remove
    if not cmds:
        raise OdooError("用 --add 或 --remove 指定参与人。")
    odoo.write(EVENT, [args.id], {"partner_ids": cmds})
    msg = []
    if added:
        msg.append(f"加入 {added}")
    if removed:
        msg.append(f"移除 {removed}")
    print(f"✅ 事件 #{args.id} 参与人已更新：{'，'.join(msg)}")


def cmd_attendees(odoo: Odoo, args):
    e = odoo.read(EVENT, [args.id], [
        "name", "attendee_ids", "accepted_count", "declined_count", "tentative_count", "awaiting_count"])
    if not e:
        raise OdooError(f"事件 #{args.id} 不存在。")
    e = e[0]
    atts = odoo.read(ATTENDEE, e["attendee_ids"], ["common_name", "partner_id", "email", "state"]) \
        if e.get("attendee_ids") else []
    rows = [[a.get("common_name") or m2o_name(a.get("partner_id")),
             ATT_STATE.get(a.get("state"), a.get("state")), a.get("email") or "-"] for a in atts]
    print(f"📋 事件 #{args.id}「{e['name']}」参与人响应")
    print(render_table(rows, ["参与人", "状态", "邮箱"]))
    print(f"\n接受 {e.get('accepted_count', 0)} / 拒绝 {e.get('declined_count', 0)} / "
          f"待定 {e.get('tentative_count', 0)} / 待回复 {e.get('awaiting_count', 0)}")


def cmd_rsvp(odoo: Odoo, args):
    att = _resolve_event_for_partner(odoo, args.id, args.who)
    method = {"accept": "do_accept", "decline": "do_decline", "tentative": "do_tentative"}[args.status]
    odoo.execute_kw(ATTENDEE, method, [att])
    word = {"accept": "接受", "decline": "拒绝", "tentative": "待定"}[args.status]
    print(f"✅ 已代「{args.who}」{word}事件 #{args.id}")


def cmd_busy(odoo: Odoo, args):
    pid = _resolve_partners(odoo, args.who)[0]
    if args.date:
        d = args.date.strip()[:10]
        lo, hi = to_utc(f"{d} 00:00:00"), to_utc(f"{d} 23:59:59")
        label = d
    else:
        if not (args.date_from and args.date_to):
            raise OdooError("用 --date 或 --from + --to 指定时段。")
        lo, hi = to_utc(args.date_from), to_utc(args.date_to)
        label = f"{args.date_from}~{args.date_to}"
    evs = odoo.search_read(
        EVENT,
        [("partner_ids", "in", [pid]), ("stop", ">=", lo), ("start", "<=", hi), ("show_as", "=", "busy")],
        ["name", "start", "stop"], order="start asc")
    if not evs:
        print(f"✅ 「{args.who}」在 {label} 空闲（无占用事件）")
        return
    rows = [[from_utc(e.get("start"), "%m-%d %H:%M"), from_utc(e.get("stop"), "%H:%M"),
             (e.get("name") or "")[:30]] for e in evs]
    print(f"🔴 「{args.who}」在 {label} 有 {len(evs)} 个占用：")
    print(render_table(rows, ["开始", "结束", "事件"]))


# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 日历事件/重复/参与人/提醒/忙闲")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="我的日程")
    li.add_argument("--today", action="store_true")
    li.add_argument("--month", action="store_true")
    li.add_argument("--from", dest="date_from")
    li.add_argument("--to", dest="date_to")
    li.add_argument("--limit", type=int, default=100)

    sh = sub.add_parser("show", help="事件详情")
    sh.add_argument("id", type=int)

    ad = sub.add_parser("add", help="新建事件（支持重复/关联/标签）")
    ad.add_argument("--name", required=True)
    ad.add_argument("--start", required=True, help="开始 YYYY-MM-DD HH:MM（本地）")
    ad.add_argument("--end", help="结束 YYYY-MM-DD HH:MM")
    ad.add_argument("--duration", type=float, help="时长（小时）")
    ad.add_argument("--location")
    ad.add_argument("--with", dest="with_", help="参与人，逗号分隔")
    ad.add_argument("--remind", help="提醒 30m/1h/1d")
    ad.add_argument("--allday", action="store_true")
    ad.add_argument("--desc")
    ad.add_argument("--repeat", choices=["daily", "weekly", "monthly", "yearly"], help="重复频率")
    ad.add_argument("--on", help="weekly 周几，如 mon 或 mon,wed,fri")
    ad.add_argument("--day", type=int, help="monthly 第几号")
    ad.add_argument("--interval", type=int, help="每隔几（默认1）")
    ad.add_argument("--count", type=int, help="重复次数")
    ad.add_argument("--until", help="重复到 YYYY-MM-DD")
    ad.add_argument("--tz", help=f"时区，默认 {DEFAULT_TZ}")
    ad.add_argument("--opportunity", help="关联 CRM 商机（名字/id）")
    ad.add_argument("--tags", help="标签，逗号分隔")

    up = sub.add_parser("update", help="改事件")
    up.add_argument("id", type=int)
    up.add_argument("--name")
    up.add_argument("--start")
    up.add_argument("--end")
    up.add_argument("--location")
    up.add_argument("--scope", choices=["self", "future", "all"], help="重复事件改动范围")

    ca = sub.add_parser("cancel", help="删除事件")
    ca.add_argument("ids", nargs="+", type=int)
    ca.add_argument("--series", choices=["future", "all"], help="删重复系列（将来/全部）")

    rm = sub.add_parser("remind", help="加提醒")
    rm.add_argument("id", type=int)
    rm.add_argument("--before", required=True, help="提前量 30m/1h/1d")
    rm.add_argument("--type", choices=["notification", "email"], default="notification")

    iv = sub.add_parser("invite", help="加/减参与人")
    iv.add_argument("id", type=int)
    iv.add_argument("--add", help="加入参与人，逗号分隔")
    iv.add_argument("--remove", help="移除参与人，逗号分隔")

    at = sub.add_parser("attendees", help="查参与人响应")
    at.add_argument("id", type=int)

    rs = sub.add_parser("rsvp", help="代参与人回复")
    rs.add_argument("id", type=int)
    rs.add_argument("--who", required=True, help="参与人名字/id")
    rs.add_argument("--status", required=True, choices=["accept", "decline", "tentative"])

    bs = sub.add_parser("busy", help="查某人某时段忙闲")
    bs.add_argument("--who", required=True, help="名字/id")
    bs.add_argument("--date", help="某天 YYYY-MM-DD（全天）")
    bs.add_argument("--from", dest="date_from", help="YYYY-MM-DD HH:MM")
    bs.add_argument("--to", dest="date_to", help="YYYY-MM-DD HH:MM")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "list": cmd_list, "show": cmd_show, "add": cmd_add, "update": cmd_update,
            "cancel": cmd_cancel, "remind": cmd_remind, "invite": cmd_invite,
            "attendees": cmd_attendees, "rsvp": cmd_rsvp, "busy": cmd_busy,
        }
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
