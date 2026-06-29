#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
partner.py — 客户档案（查询 + 文本建档）

命令
  show <客户名>                客户档案：联系方式 + 应收 + 成交汇总 + 最近订单（只读）
  add --text "<一段文本>" [--yes]
                             文本一句话建客户档案：粘贴"张三 138xxxx 佛山顺德…"
                             → huo15_contact_autofill 自动解析姓名/电话/地址（确认制）
  remove <id> [--yes]         删除联系人（仅无关联订单的，误建补救）

示例
  python3 partner.py show 亿美诺
  python3 partner.py add --text "李梦 13800001234 广东省佛山市顺德区乐从镇家具城A区12号"
"""

from __future__ import annotations

import argparse
import re
import sys

from actions import _confirm_gate
from odoo_client import Odoo, OdooError
from odoo_utils import DELIVERY_STATUS, SO_STATE, from_utc, label, m2o_name, money, render_table


def cmd_show(args):
    odoo = Odoo()
    hits = odoo.name_search("res.partner", args.keyword, limit=5)
    if not hits:
        print(f"未找到客户：{args.keyword}")
        return
    pid, _ = hits[0]
    p = odoo.read("res.partner", [pid],
                  ["name", "phone", "email", "street", "city", "credit",
                   "user_id", "category_id", "comment"])[0]
    print(f"👤 {p['name']}")
    contact = [x for x in [p.get("phone"), p.get("email")] if x]
    if contact:
        print(f"   联系: {' | '.join(contact)}")
    addr = " ".join(x for x in [p.get("city") or "", p.get("street") or ""] if x)
    if addr:
        print(f"   地址: {addr}")
    extra = []
    if p.get("user_id"):
        extra.append(f"业务员: {m2o_name(p['user_id'])}")
    if p.get("credit"):
        extra.append(f"应收余额: {money(p['credit'])}")
    if extra:
        print("   " + " | ".join(extra))
    if len(hits) > 1:
        print(f"   （同名匹配还有: {', '.join(h[1] for h in hits[1:])}）")

    domain = [["partner_id", "=", pid], ["state", "in", ["sale", "done"]]]
    agg = odoo.read_group("sale.order", domain, ["amount_total"], [], lazy=False)
    if agg and agg[0].get("__count"):
        print(f"\n   成交: {agg[0]['__count']} 单 / {money(agg[0]['amount_total'])}")

    orders = odoo.search_read(
        "sale.order", [["partner_id", "=", pid]],
        ["name", "date_order", "state", "delivery_status", "amount_total"],
        limit=args.limit, order="date_order desc")
    if orders:
        rows = [[o["name"], from_utc(o["date_order"], "%Y-%m-%d"),
                 label(SO_STATE, o["state"]),
                 label(DELIVERY_STATUS, o.get("delivery_status")),
                 money(o["amount_total"])] for o in orders]
        print(f"\n── 最近订单（{len(orders)} 张）──")
        print(render_table(rows, ["订单", "日期", "状态", "发货", "金额"]))


def cmd_add(args):
    odoo = Odoo()
    text = (args.text or "").strip()
    if not text:
        raise OdooError("文本为空：用 --text \"姓名 电话 地址\" 提供。")
    print("👤 将要执行：新建客户档案（文本智能解析 · contact_autofill）")
    print(f"   原文：{text}")
    _confirm_gate(args.yes)
    # res.partner 必填 name（RPC create 不触发 onchange）；用文本首段占位，apply 后覆盖
    placeholder = re.split(r"[\s\d]", text, maxsplit=1)[0] or text[:8]
    pid = odoo.create("res.partner",
                      {"name": placeholder, "autofill_text": text, "customer_rank": 1})
    try:
        odoo.call("res.partner", "action_apply_autofill_text", [pid])
    except OdooError as e:
        print(f"   ⚠️ 自动解析未完全成功（{e}），已按首段建档，可在系统补全。")
    p = odoo.read("res.partner", [pid],
                  ["name", "phone", "email", "street", "city"])[0]
    # contact_autofill 常把整段塞进 name；若 name 仍含手机号数字，回退首段姓名保持整洁
    if p.get("name") and any(ch.isdigit() for ch in p["name"]):
        odoo.write("res.partner", pid, {"name": placeholder})
        p["name"] = placeholder
    print(f"✅ 已建档（id={pid}）：{p.get('name') or '(未解析出姓名)'}")
    contact = [x for x in [p.get("phone"), p.get("email")] if x]
    if contact:
        print("   联系:", " | ".join(contact))
    addr = " ".join(x for x in [p.get("city") or "", p.get("street") or ""] if x)
    if addr:
        print("   地址:", addr)
    print(f"   解析有误可删：python3 partner.py remove {pid} --yes")


def cmd_remove(args):
    odoo = Odoo()
    pid = int(args.partner_id)
    p = odoo.search_read("res.partner", [["id", "=", pid]], ["name"], limit=1)
    if not p:
        print(f"联系人 {pid} 不存在（可能已删除）。")
        return
    n_so = odoo.search_count("sale.order", [["partner_id", "=", pid]])
    if n_so:
        raise OdooError(f"{p[0]['name']} 有 {n_so} 张关联订单，拒绝删除（避免误删有业务的客户）。")
    print(f"🗑 将要执行：删除联系人 {p[0]['name']}（id={pid}，无关联订单）")
    _confirm_gate(args.yes)
    odoo.unlink("res.partner", pid)
    print("✅ 已删除。")


def build_parser():
    p = argparse.ArgumentParser(description="客户档案（查询 + 文本建档）")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show", help="客户档案")
    s.add_argument("keyword", help="客户名（模糊）")
    s.add_argument("--limit", type=int, default=10)
    a = sub.add_parser("add", help="文本一句话建客户档案")
    a.add_argument("--text", required=True)
    a.add_argument("--yes", action="store_true")
    r = sub.add_parser("remove", help="删除联系人（仅无订单）")
    r.add_argument("partner_id")
    r.add_argument("--yes", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"show": cmd_show, "add": cmd_add, "remove": cmd_remove}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
