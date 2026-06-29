#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crm.py — 火一五 Odoo「CRM / 客户关系」线索与商机管理

线索和商机是同一个模型 crm.lead，靠 type 字段区分（'lead'/'opportunity'）。
字段坑（详见 references/odoo-crm-api.md）：
  - 建商机必须显式传 type='opportunity'（默认值依赖配置，可能是 lead）。
  - 负责人 user_id 是单数 Many2one（不是 m2m）；团队 team_id。
  - crm.stage 的团队关联是 team_ids（复数 m2m），空=全团队共享。
  - 手机号写 phone（crm.lead 没有 mobile 字段）；description 是 Html。
  - 赢单/输单/复活必须调专用方法（action_set_won / action_set_lost / action_restore），
    别手动 write stage/active/probability——否则破坏概率模型与不变式。

命令
  list      列商机（默认我的进行中）  --all/--won/--lost/--user/--team/--stage
  show      商机详情
  add       新建商机（--name 必填，可选 --customer/--revenue/--user/--team/--stage/...）
  update    改字段
  move      推进阶段     move <id> --stage 报价
  won       标记赢单     won <id> ...
  lost      标记输单     lost <id> --reason "价格太高"
  restore   复活已输单   restore <id> ...
  convert   线索转商机   convert <id> [--customer X]
  pipeline  管道统计     --by stage|user|team
  activity  安排跟进     activity <id> --type call --date 2026-06-10 --summary "回访"

示例
  python3 crm.py add --name "某客户-ERP项目" --customer "某客户" --revenue 50000 --user 我
  python3 crm.py pipeline --by stage
  python3 crm.py won 88
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import m2o_name, render_table

LEAD = "crm.lead"
STAGE = "crm.stage"
TEAM = "crm.team"
REASON = "crm.lost.reason"

PRIORITY = {"0": "低", "1": "中", "2": "高", "3": "很高"}
WON_STATUS = {"won": "✅赢单", "lost": "❌输单", "pending": "进行中"}
ACT_TYPES = {
    "call": "mail.mail_activity_data_call",
    "meeting": "mail.mail_activity_data_meeting",
    "todo": "mail.mail_activity_data_todo",
    "email": "mail.mail_activity_data_email",
}


def _money(v) -> str:
    try:
        return f"{float(v or 0):,.0f}"
    except (TypeError, ValueError):
        return str(v)


def _resolve(odoo: Odoo, model: str, ref, label: str, args=None):
    """名字/id/我 → id。"""
    if ref in (None, ""):
        return None
    s = str(ref)
    if model == "res.users" and s in ("我", "me", "self"):
        return odoo.ensure_uid()
    if s.isdigit():
        return int(s)
    res = odoo.name_search(model, s, args=args or [], limit=1)
    if not res:
        raise OdooError(f"找不到{label}「{ref}」。")
    return res[0][0]


def _resolve_lost_reason(odoo: Odoo, name: str) -> int:
    ids = odoo.search(REASON, [["name", "ilike", name]], limit=1)
    return ids[0] if ids else odoo.create(REASON, {"name": name})


# --------------------------------------------------------------------------- #
LIST_FIELDS = ["id", "name", "partner_id", "stage_id", "expected_revenue",
               "probability", "user_id", "date_deadline", "priority", "won_status"]


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = [("type", "=", "opportunity")]
    if args.won:
        domain.append(("won_status", "=", "won"))
    elif args.lost:
        domain += [("active", "=", False), ("won_status", "=", "lost")]
    elif not args.all:
        domain += [("user_id", "=", uid), ("won_status", "=", "pending")]
    if args.user:
        domain.append(("user_id", "=", _resolve(odoo, "res.users", args.user, "用户")))
    if args.team:
        domain.append(("team_id", "=", _resolve(odoo, TEAM, args.team, "团队")))
    if args.stage:
        domain.append(("stage_id.name", "ilike", args.stage))

    rows_data = odoo.search_read(
        LEAD, domain, LIST_FIELDS,
        order="priority desc, expected_revenue desc, id desc", limit=args.limit)
    if args.json:
        print(json.dumps(rows_data, ensure_ascii=False, default=str))
        return
    rows, total = [], 0.0
    for r in rows_data:
        total += r.get("expected_revenue") or 0
        rows.append([
            r["id"], m2o_name(r.get("stage_id")) or "-",
            _money(r.get("expected_revenue")),
            f"{int(r.get('probability') or 0)}%",
            m2o_name(r.get("partner_id")) or "-",
            m2o_name(r.get("user_id")) or "-",
            (r["name"][:28] + "…") if len(r.get("name") or "") > 29 else r.get("name"),
        ])
    print(render_table(rows, ["ID", "阶段", "预期收入", "概率", "客户", "负责人", "商机"]))
    scope = "已赢" if args.won else "已输" if args.lost else "全部进行中" if args.all else "我的进行中"
    print(f"\n共 {len(rows_data)} 条（{scope}），预期收入合计 {_money(total)}")


def cmd_show(odoo: Odoo, args):
    r = odoo.read(LEAD, [args.id], [
        "name", "type", "partner_id", "contact_name", "email_from", "phone",
        "partner_name", "expected_revenue", "probability", "stage_id", "user_id",
        "team_id", "priority", "date_deadline", "won_status", "lost_reason_id", "tag_ids"])
    if not r:
        raise OdooError(f"商机 #{args.id} 不存在。")
    r = r[0]
    print(f"💼 {'商机' if r['type'] == 'opportunity' else '线索'} #{args.id}：{r['name']}")
    print(f"   客户：{m2o_name(r.get('partner_id')) or '-'}  联系人：{r.get('contact_name') or '-'}  电话：{r.get('phone') or '-'}")
    print(f"   预期收入：{_money(r.get('expected_revenue'))}  概率：{int(r.get('probability') or 0)}%  状态：{WON_STATUS.get(r.get('won_status'), r.get('won_status'))}")
    print(f"   阶段：{m2o_name(r.get('stage_id')) or '-'}  负责人：{m2o_name(r.get('user_id')) or '-'}  团队：{m2o_name(r.get('team_id')) or '-'}")
    print(f"   优先级：{PRIORITY.get(str(r.get('priority')), r.get('priority'))}  预计成交：{r.get('date_deadline') or '-'}")
    if r.get("lost_reason_id"):
        print(f"   输单原因：{m2o_name(r['lost_reason_id'])}")


def cmd_add(odoo: Odoo, args):
    vals = {
        "name": args.name,
        "type": "lead" if args.lead else "opportunity",
    }
    if args.customer:
        vals["partner_id"] = _resolve(odoo, "res.partner", args.customer, "客户")
    if args.revenue is not None:
        vals["expected_revenue"] = args.revenue
    if args.user:
        vals["user_id"] = _resolve(odoo, "res.users", args.user, "负责人", args=[["share", "=", False]])
    if args.team:
        vals["team_id"] = _resolve(odoo, TEAM, args.team, "团队")
    if args.stage:
        vals["stage_id"] = _resolve(odoo, STAGE, args.stage, "阶段")
    if args.priority is not None:
        vals["priority"] = str(args.priority)
    if args.deadline:
        vals["date_deadline"] = args.deadline.strip()[:10]
    if args.phone:
        vals["phone"] = args.phone
    if args.email:
        vals["email_from"] = args.email
    if args.company:
        vals["partner_name"] = args.company
    if args.contact:
        vals["contact_name"] = args.contact
    if args.desc:
        vals["description"] = f"<p>{args.desc}</p>"
    lid = odoo.create(LEAD, vals)
    kind = "线索" if args.lead else "商机"
    print(f"✅ 已新建{kind} #{lid}：{args.name}")


def cmd_update(odoo: Odoo, args):
    vals = {}
    if args.name:
        vals["name"] = args.name
    if args.revenue is not None:
        vals["expected_revenue"] = args.revenue
    if args.user:
        vals["user_id"] = _resolve(odoo, "res.users", args.user, "负责人", args=[["share", "=", False]])
    if args.team:
        vals["team_id"] = _resolve(odoo, TEAM, args.team, "团队")
    if args.priority is not None:
        vals["priority"] = str(args.priority)
    if args.deadline:
        vals["date_deadline"] = args.deadline.strip()[:10]
    if args.probability is not None:
        vals["probability"] = args.probability
    if args.phone:
        vals["phone"] = args.phone
    if args.desc is not None:
        vals["description"] = f"<p>{args.desc}</p>"
    if not vals:
        raise OdooError("没有要更新的字段。")
    odoo.write(LEAD, [args.id], vals)
    print(f"✅ 已更新商机 #{args.id}：{', '.join(vals.keys())}")


def cmd_move(odoo: Odoo, args):
    sid = _resolve(odoo, STAGE, args.stage, "阶段")
    odoo.write(LEAD, [args.id], {"stage_id": sid})
    print(f"✅ 商机 #{args.id} 已推进到阶段「{args.stage}」")


def cmd_won(odoo: Odoo, args):
    odoo.execute_kw(LEAD, "action_set_won", [args.ids])
    print(f"✅ 已标记赢单：{', '.join('#' + str(i) for i in args.ids)}（自动置入赢单阶段，概率 100%）")


def cmd_lost(odoo: Odoo, args):
    kwargs = {}
    if args.reason:
        kwargs["lost_reason_id"] = _resolve_lost_reason(odoo, args.reason)
    odoo.execute_kw(LEAD, "action_set_lost", [args.ids], kwargs)
    tail = f"，原因「{args.reason}」" if args.reason else ""
    print(f"❌ 已标记输单：{', '.join('#' + str(i) for i in args.ids)}{tail}（已归档，概率 0）")


def cmd_restore(odoo: Odoo, args):
    odoo.execute_kw(LEAD, "action_restore", [args.ids])
    print(f"♻️  已复活：{', '.join('#' + str(i) for i in args.ids)}（清除输单原因，恢复自动概率）")


def cmd_convert(odoo: Odoo, args):
    partner = _resolve(odoo, "res.partner", args.customer, "客户") if args.customer else False
    odoo.execute_kw(LEAD, "convert_opportunity", [[args.id], partner])
    print(f"✅ 线索 #{args.id} 已转为商机" + (f"（关联客户 {args.customer}）" if args.customer else ""))


def cmd_pipeline(odoo: Odoo, args):
    field = {"stage": "stage_id", "user": "user_id", "team": "team_id"}[args.by]
    domain = [("type", "=", "opportunity")]
    if args.user:
        domain.append(("user_id", "=", _resolve(odoo, "res.users", args.user, "用户")))
    if args.team:
        domain.append(("team_id", "=", _resolve(odoo, TEAM, args.team, "团队")))
    groups = odoo.read_group(
        LEAD, domain, ["expected_revenue:sum", "prorated_revenue:sum"], [field], lazy=False)
    rows, total, total_w = [], 0.0, 0.0
    for g in groups:
        exp = g.get("expected_revenue") or 0
        wt = g.get("prorated_revenue") or 0
        cnt = g.get("__count") or g.get(field + "_count") or 0
        total += exp
        total_w += wt
        rows.append([m2o_name(g.get(field)) or "(未分组)", cnt, _money(exp), _money(wt)])
    rows.sort(key=lambda r: -float(str(r[2]).replace(",", "") or 0))
    if args.json:
        print(json.dumps([{"key": r[0], "count": r[1], "expected": r[2], "weighted": r[3]} for r in rows], ensure_ascii=False))
        return
    by_label = {"stage": "阶段", "user": "负责人", "team": "团队"}[args.by]
    print(f"📈 销售管道（按{by_label}）")
    print(render_table(rows, [by_label, "商机数", "预期收入", "加权预测"]))
    print(f"\n合计：预期收入 {_money(total)}，加权预测 {_money(total_w)}，{len(rows)} 组")


def cmd_activity(odoo: Odoo, args):
    xmlid = ACT_TYPES[args.type]
    kwargs = {"summary": args.summary or ""}
    if args.date:
        kwargs["date_deadline"] = args.date.strip()[:10]
    if args.note:
        kwargs["note"] = args.note
    if args.user:
        kwargs["user_id"] = _resolve(odoo, "res.users", args.user, "用户")
    odoo.execute_kw(LEAD, "activity_schedule", [[args.id], xmlid], kwargs)
    print(f"✅ 已为商机 #{args.id} 安排「{args.type}」活动" + (f"（{args.date}）" if args.date else ""))


# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo CRM 线索/商机管理")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="列商机")
    li.add_argument("--all", action="store_true", help="所有进行中（不限负责人）")
    li.add_argument("--won", action="store_true", help="已赢单")
    li.add_argument("--lost", action="store_true", help="已输单")
    li.add_argument("--user", help="按负责人")
    li.add_argument("--team", help="按团队")
    li.add_argument("--stage", help="按阶段名")
    li.add_argument("--limit", type=int, default=100)

    sh = sub.add_parser("show", help="商机详情")
    sh.add_argument("id", type=int)

    ad = sub.add_parser("add", help="新建商机")
    ad.add_argument("--name", required=True)
    ad.add_argument("--customer", help="客户（名字/id）")
    ad.add_argument("--revenue", type=float, help="预期收入")
    ad.add_argument("--user", help="负责人（名字/id/我）")
    ad.add_argument("--team", help="销售团队")
    ad.add_argument("--stage", help="阶段名")
    ad.add_argument("--priority", type=int, choices=[0, 1, 2, 3])
    ad.add_argument("--deadline", help="预计成交日 YYYY-MM-DD")
    ad.add_argument("--phone")
    ad.add_argument("--email")
    ad.add_argument("--company", help="公司名（partner_name）")
    ad.add_argument("--contact", help="联系人姓名")
    ad.add_argument("--desc")
    ad.add_argument("--lead", action="store_true", help="建成线索而非商机")

    up = sub.add_parser("update", help="改商机")
    up.add_argument("id", type=int)
    up.add_argument("--name")
    up.add_argument("--revenue", type=float)
    up.add_argument("--user")
    up.add_argument("--team")
    up.add_argument("--priority", type=int, choices=[0, 1, 2, 3])
    up.add_argument("--deadline")
    up.add_argument("--probability", type=float)
    up.add_argument("--phone")
    up.add_argument("--desc")

    mv = sub.add_parser("move", help="推进阶段")
    mv.add_argument("id", type=int)
    mv.add_argument("--stage", required=True)

    for name, hlp in [("won", "标记赢单"), ("restore", "复活已输单")]:
        sp = sub.add_parser(name, help=hlp)
        sp.add_argument("ids", nargs="+", type=int)

    lo = sub.add_parser("lost", help="标记输单")
    lo.add_argument("ids", nargs="+", type=int)
    lo.add_argument("--reason", help="输单原因（不存在自动创建）")

    cv = sub.add_parser("convert", help="线索转商机")
    cv.add_argument("id", type=int)
    cv.add_argument("--customer", help="关联客户（名字/id）")

    pl = sub.add_parser("pipeline", help="管道统计")
    pl.add_argument("--by", choices=["stage", "user", "team"], default="stage")
    pl.add_argument("--user")
    pl.add_argument("--team")

    ac = sub.add_parser("activity", help="安排跟进活动")
    ac.add_argument("id", type=int)
    ac.add_argument("--type", choices=list(ACT_TYPES), default="call")
    ac.add_argument("--date", help="截止 YYYY-MM-DD")
    ac.add_argument("--summary")
    ac.add_argument("--note")
    ac.add_argument("--user", help="指派给（名字/id/我）")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "list": cmd_list, "show": cmd_show, "add": cmd_add, "update": cmd_update,
            "move": cmd_move, "won": cmd_won, "lost": cmd_lost, "restore": cmd_restore,
            "convert": cmd_convert, "pipeline": cmd_pipeline, "activity": cmd_activity,
        }
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
