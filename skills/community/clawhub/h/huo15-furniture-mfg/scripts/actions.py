#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actions.py — 写操作（P1，确认制）

⚠️ 安全模型（必读）
  - 所有命令默认 **dry-run**：只打印「将要执行」预览，不碰系统。
  - 必须显式加 `--yes` 才真正执行。AI 调用时：先 dry-run 把预览给用户看，
    用户明确同意后才允许带 --yes 重跑。绝不跳过预览直接 --yes。
  - @人 / 提醒对象只接受内部用户名解析（res.users），不接受裸 partner id。

命令
  note <单号> --text "内容" [--at 姓名]...     在单据沟通流留言，可 @同事（会收到通知）
  remind <单号> --to 姓名 --date YYYY-MM-DD [--summary "..."] [--note "..."]
                                              给同事建跟进提醒（待办活动）
  reschedule <制造单号> --start "YYYY-MM-DD [HH:MM]"   调整制造单计划开始时间
  delay <销售单号> --date "YYYY-MM-DD"                调整销售单承诺交期
  undo-note <message_id>                       删除本工具发的留言（误发补救）

示例
  python3 actions.py note SO-260531-758 --text "客户催货，请优先安排" --at 一组-张三
  python3 actions.py note SO-260531-758 --text "..." --at 一组-张三 --yes
  python3 actions.py remind SO-260531-758 --to 冯广权 --date 2026-06-16 --summary "回复客户交期"
  python3 actions.py reschedule MO-260604-643 --start "2026-06-16 08:00" --yes
  python3 actions.py delay SO-260531-758 --date 2026-06-20 --yes
"""

from __future__ import annotations

import argparse
import html
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, to_utc

# 单号前缀 → 模型路由
PREFIX_MODEL = [
    ("SO", "sale.order"),
    ("MO", "mrp.production"),
    ("PO", "purchase.order"),
    ("DO", "stock.picking"),
    ("WH", "stock.picking"),
    ("QC", "quality.check"),
]


def resolve_record(odoo: Odoo, ref: str) -> tuple[str, dict]:
    """单号 → (model, record)。前缀路由 + ilike 模糊，多中取最新。"""
    ref = ref.strip()
    upper = ref.upper()
    candidates = [m for p, m in PREFIX_MODEL if upper.startswith(p)] or \
                 [m for _, m in PREFIX_MODEL]
    for model in dict.fromkeys(candidates):
        fields = ["name", "partner_id"] if model != "mrp.production" else ["name", "product_id"]
        recs = odoo.search_read(model, [["name", "ilike", ref]], fields,
                                limit=2, order="id desc")
        if recs:
            return model, recs[0]
    raise OdooError(f"找不到单据：{ref}（支持 SO-/MO-/PO-/DO-/QC 前缀）")


def resolve_users(odoo: Odoo, names: list[str]) -> list[dict]:
    """姓名/账号 → 内部用户（含 partner_id）。解析不到/歧义直接报错列候选。"""
    out = []
    for n in names:
        hits = odoo.search_read(
            "res.users",
            ["&", ["share", "=", False],
             "|", ["name", "ilike", n], ["login", "ilike", n]],
            ["name", "login", "partner_id"], limit=5)
        if not hits:
            raise OdooError(f"找不到内部用户：{n}")
        exact = [h for h in hits if h["name"] == n or h["login"] == n]
        if len(hits) > 1 and not exact:
            raise OdooError(
                f"用户「{n}」有多个匹配：{', '.join(h['name'] for h in hits)}，请写全名")
        out.append(exact[0] if exact else hits[0])
    return out


def _record_line(model: str, rec: dict) -> str:
    who = m2o_name(rec.get("partner_id")) or m2o_name(rec.get("product_id"))
    return f"{rec['name']}（{who}）" if who else rec["name"]


def _confirm_gate(yes: bool):
    if not yes:
        print("\n（以上为预览，未执行。确认无误后加 --yes 重跑执行。）")
        sys.exit(0)


# --------------------------------------------------------------------------- #
def cmd_note(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    users = resolve_users(odoo, args.at or [])
    print("📝 将要执行：单据留言")
    print(f"   单据: {_record_line(model, rec)}")
    print(f"   内容: {args.text}")
    if users:
        print(f"   通知: {', '.join(u['name'] for u in users)}")
    _confirm_gate(args.yes)

    body = "<p>" + html.escape(args.text).replace("\n", "<br/>") + "</p>"
    msg_id = odoo.call(
        model, "message_post", [rec["id"]],
        body=body,
        partner_ids=[u["partner_id"][0] for u in users],
        message_type="comment",
        subtype_xmlid="mail.mt_comment",
    )
    # XML-RPC 把 mail.message recordset 序列化成 [id]
    if isinstance(msg_id, list):
        msg_id = msg_id[0] if msg_id else "?"
    print(f"✅ 已留言（message_id={msg_id}）"
          + (f"，已通知 {', '.join(u['name'] for u in users)}" if users else ""))
    print(f"   误发可撤：python3 actions.py undo-note {msg_id} --yes")


def cmd_remind(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    user = resolve_users(odoo, [args.to])[0]
    summary = args.summary or f"跟进 {rec['name']}"
    print("⏰ 将要执行：创建跟进提醒（待办活动）")
    print(f"   单据: {_record_line(model, rec)}")
    print(f"   负责人: {user['name']} | 截止: {args.date}")
    print(f"   主题: {summary}" + (f" | 备注: {args.note}" if args.note else ""))
    _confirm_gate(args.yes)

    model_id = odoo.search("ir.model", [["model", "=", model]], limit=1)[0]
    act_id = odoo.create("mail.activity", {
        "res_model_id": model_id,
        "res_id": rec["id"],
        "activity_type_id": 4,            # To-Do（test 库实测 id）
        "summary": summary,
        "note": html.escape(args.note or ""),
        "date_deadline": args.date,       # mail.activity 是 Date 字段，直接 YYYY-MM-DD
        "user_id": user["id"],
    })
    print(f"✅ 已创建提醒（activity_id={act_id}），{user['name']} 将在系统/邮件收到。")


def cmd_reschedule(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    if model != "mrp.production":
        raise OdooError(f"{rec['name']} 不是制造单，reschedule 只支持 MO。")
    cur = odoo.read(model, [rec["id"]], ["date_start", "state"])[0]
    new_utc = to_utc(args.start, default_time="08:00:00")
    print("🗓 将要执行：调整制造单计划开始")
    print(f"   单据: {_record_line(model, rec)}（状态 {cur['state']}）")
    print(f"   计划开始: {from_utc(cur['date_start']) or '(空)'} → {args.start}")
    _confirm_gate(args.yes)
    odoo.write(model, rec["id"], {"date_start": new_utc})
    print("✅ 已调整。")


def cmd_delay(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    if model != "sale.order":
        raise OdooError(f"{rec['name']} 不是销售单，delay 只支持 SO。")
    cur = odoo.read(model, [rec["id"]], ["commitment_date", "state"])[0]
    new_utc = to_utc(args.date)
    print("🗓 将要执行：调整销售单承诺交期")
    print(f"   单据: {_record_line(model, rec)}（状态 {cur['state']}）")
    print(f"   承诺交期: {from_utc(cur['commitment_date'], '%Y-%m-%d') or '(空)'} → {args.date}")
    print("   提示: 调交期通常需先与客户达成一致；建议配合 note 通知跟单/销售。")
    _confirm_gate(args.yes)
    odoo.write(model, rec["id"], {"commitment_date": new_utc})
    print("✅ 已调整。")


def cmd_undo_note(args):
    odoo = Odoo()
    msgs = odoo.search_read("mail.message", [["id", "=", int(args.message_id)]],
                            ["model", "res_id", "body"], limit=1)
    if not msgs:
        print(f"留言 {args.message_id} 不存在（可能已删除）。")
        return
    m = msgs[0]
    print("🗑 将要执行：删除留言")
    print(f"   message_id={args.message_id} on {m.get('model')}#{m.get('res_id')}")
    print(f"   内容: {m.get('body', '')[:120]}")
    _confirm_gate(args.yes)
    odoo.unlink("mail.message", int(args.message_id))
    print("✅ 已删除。")


def cmd_worknote(args):
    """订单特殊要求 → 关联制造单备注 + @车间（兑现「订单备注直达车间看板」）。"""
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    users = resolve_users(odoo, args.at or [])
    mos = []
    if model == "sale.order":
        mos = odoo.search_read("mrp.production", [["origin", "=", rec["name"]]],
                               ["name"], limit=20)
    targets = mos if mos else [rec]
    target_model = "mrp.production" if mos else model
    print("🏭 将要执行：工艺/工单要求留言")
    print(f"   来源: {_record_line(model, rec)}")
    print(f"   写入: {'、'.join(t['name'] for t in targets)}"
          + ("（关联制造单）" if mos else "（无关联制造单，写在来源单上）"))
    print(f"   内容: {args.text}")
    if users:
        print(f"   通知: {', '.join(u['name'] for u in users)}")
    _confirm_gate(args.yes)
    body = "<p><b>【工艺要求】</b>" + html.escape(args.text).replace("\n", "<br/>") + "</p>"
    pids = [u["partner_id"][0] for u in users]
    for t in targets:
        odoo.call(target_model, "message_post", [t["id"]],
                  body=body, partner_ids=pids,
                  message_type="comment", subtype_xmlid="mail.mt_comment")
    print(f"✅ 已写入 {len(targets)} 个单据"
          + (f"，已通知 {', '.join(u['name'] for u in users)}" if users else ""))


def _resolve_activity(odoo: Odoo, ref: str) -> dict:
    """活动 id 或 单号 → mail.activity 记录（单号取其上最近一条待办活动）。"""
    fields = ["summary", "res_model", "res_id", "user_id", "date_deadline"]
    if ref.isdigit():
        acts = odoo.search_read("mail.activity", [["id", "=", int(ref)]], fields, limit=1)
        if acts:
            return acts[0]
    model, rec = resolve_record(odoo, ref)
    acts = odoo.search_read("mail.activity",
                            [["res_model", "=", model], ["res_id", "=", rec["id"]]],
                            fields, limit=1, order="date_deadline")
    if not acts:
        raise OdooError(f"{rec['name']} 上没有待办活动。")
    return acts[0]


def cmd_activity_done(args):
    odoo = Odoo()
    act = _resolve_activity(odoo, args.ref)
    print("✅ 将要执行：完成跟进活动")
    print(f"   活动: {act.get('summary') or '(无摘要)'} on {act['res_model']}#{act['res_id']}"
          f" | 负责 {m2o_name(act.get('user_id'))} | 截止 {act.get('date_deadline')}")
    _confirm_gate(args.yes)
    odoo.call("mail.activity", "action_feedback", [act["id"]],
              feedback=args.feedback or "已完成")
    print("✅ 活动已完成并归档。")


def cmd_activity_reschedule(args):
    odoo = Odoo()
    act = _resolve_activity(odoo, args.ref)
    print("🗓 将要执行：跟进活动改期")
    print(f"   活动: {act.get('summary') or '(无摘要)'} on {act['res_model']}#{act['res_id']}")
    print(f"   截止: {act.get('date_deadline')} → {args.date}")
    _confirm_gate(args.yes)
    odoo.write("mail.activity", act["id"], {"date_deadline": args.date})
    print("✅ 已改期。")


def build_parser():
    p = argparse.ArgumentParser(description="写操作（确认制：默认 dry-run，--yes 执行）")
    sub = p.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("note", help="单据留言@人")
    n.add_argument("ref"); n.add_argument("--text", required=True)
    n.add_argument("--at", action="append", help="可重复，@内部用户姓名")
    n.add_argument("--yes", action="store_true")

    r = sub.add_parser("remind", help="建跟进提醒")
    r.add_argument("ref"); r.add_argument("--to", required=True)
    r.add_argument("--date", required=True, help="YYYY-MM-DD")
    r.add_argument("--summary"); r.add_argument("--note")
    r.add_argument("--yes", action="store_true")

    s = sub.add_parser("reschedule", help="调制造单计划开始")
    s.add_argument("ref"); s.add_argument("--start", required=True, help="YYYY-MM-DD [HH:MM]")
    s.add_argument("--yes", action="store_true")

    d = sub.add_parser("delay", help="调销售单承诺交期")
    d.add_argument("ref"); d.add_argument("--date", required=True, help="YYYY-MM-DD")
    d.add_argument("--yes", action="store_true")

    u = sub.add_parser("undo-note", help="删除误发留言")
    u.add_argument("message_id")
    u.add_argument("--yes", action="store_true")

    w = sub.add_parser("worknote", help="订单要求→关联制造单留言@车间")
    w.add_argument("ref")
    w.add_argument("--text", required=True)
    w.add_argument("--at", action="append", help="可重复，@内部用户姓名")
    w.add_argument("--yes", action="store_true")

    ad = sub.add_parser("activity-done", help="完成跟进活动")
    ad.add_argument("ref", help="活动 id 或 单号")
    ad.add_argument("--feedback")
    ad.add_argument("--yes", action="store_true")

    ar = sub.add_parser("activity-reschedule", help="跟进活动改期")
    ar.add_argument("ref", help="活动 id 或 单号")
    ar.add_argument("--date", required=True, help="YYYY-MM-DD")
    ar.add_argument("--yes", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"note": cmd_note, "remind": cmd_remind, "reschedule": cmd_reschedule,
         "delay": cmd_delay, "undo-note": cmd_undo_note, "worknote": cmd_worknote,
         "activity-done": cmd_activity_done,
         "activity-reschedule": cmd_activity_reschedule}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
