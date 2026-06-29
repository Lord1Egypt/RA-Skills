#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sales.py — 辉火套件ERP「销售 Sales」订单管理（sale.order + sale.order.line）

字段坑（详见 references/odoo-sales-purchase-stock-api.md）：
  - v19 行字段：product_uom_id（非 product_uom）、tax_ids（非 tax_id）；行数量 product_uom_qty。
  - state 无 done：draft(报价单)/sent(已发送)/sale(销售订单)/cancel；锁定用 locked 布尔。
  - 确认 action_confirm 是写操作（装 sale_stock 会自动建交货单）——执行前向用户确认。

命令
  list     列订单   默认我的；--draft 报价单 / --confirmed 已确认 / --customer / --all
  show     订单详情 + 明细行
  add      建报价单 --customer X --line "产品:数量[:单价]"（--line 可重复）
  confirm  确认订单（draft→sale，建交货单）
  cancel   取消订单
  invoice  生成发票（_create_invoices）

示例
  python3 sales.py add --customer "某客户" --line "办公椅:10" --line "办公桌:5:800"
  python3 sales.py list --draft
  python3 sales.py confirm 42
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table

SO = "sale.order"
SOL = "sale.order.line"
STATE = {"draft": "报价单", "sent": "已发送", "sale": "销售订单", "cancel": "已取消"}
INV_STATUS = {"no": "无需开票", "to invoice": "待开票", "invoiced": "已开票", "upselling": "可追销"}


def _money(v) -> str:
    try:
        return f"{float(v or 0):,.2f}"
    except (TypeError, ValueError):
        return str(v)


def _resolve(odoo: Odoo, model: str, ref, label: str, args=None):
    if str(ref).isdigit():
        return int(ref)
    r = odoo.name_search(model, str(ref), args=args or [], limit=1)
    if not r:
        raise OdooError(f"找不到{label}「{ref}」。")
    return r[0][0]


def _parse_lines(odoo: Odoo, specs: list) -> list:
    cmds = []
    for spec in specs:
        parts = [p.strip() for p in spec.split(":")]
        vals = {"product_id": _resolve(odoo, "product.product", parts[0], "产品"),
                "product_uom_qty": float(parts[1]) if len(parts) > 1 and parts[1] else 1.0}
        if len(parts) > 2 and parts[2]:
            vals["price_unit"] = float(parts[2])
        cmds.append((0, 0, vals))
    return cmds


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = []
    if args.draft:
        domain.append(("state", "in", ["draft", "sent"]))
    elif args.confirmed:
        domain.append(("state", "=", "sale"))
    elif not args.all:
        domain.append(("user_id", "=", uid))
    if args.customer:
        domain.append(("partner_id", "=", _resolve(odoo, "res.partner", args.customer, "客户")))
    orders = odoo.search_read(
        SO, domain,
        ["name", "partner_id", "state", "amount_total", "date_order", "invoice_status"],
        order="date_order desc", limit=args.limit)
    if args.json:
        print(json.dumps(orders, ensure_ascii=False, default=str))
        return
    rows, total = [], 0.0
    for o in orders:
        total += o.get("amount_total") or 0
        rows.append([o["id"], o["name"], STATE.get(o["state"], o["state"]),
                     m2o_name(o.get("partner_id")) or "-", _money(o.get("amount_total")),
                     INV_STATUS.get(o.get("invoice_status"), o.get("invoice_status") or "-")])
    print(render_table(rows, ["ID", "单号", "状态", "客户", "金额", "开票"]))
    print(f"\n共 {len(orders)} 单，金额合计 {_money(total)}")


def cmd_show(odoo: Odoo, args):
    o = odoo.read(SO, [args.id], [
        "name", "partner_id", "state", "amount_untaxed", "amount_tax", "amount_total",
        "date_order", "user_id", "invoice_status", "order_line", "client_order_ref"])
    if not o:
        raise OdooError(f"销售单 #{args.id} 不存在。")
    o = o[0]
    print(f"🧾 销售单 {o['name']}（#{args.id}）  [{STATE.get(o['state'], o['state'])}]")
    print(f"   客户：{m2o_name(o.get('partner_id')) or '-'}   销售员：{m2o_name(o.get('user_id')) or '-'}")
    print(f"   日期：{from_utc(o.get('date_order') or '', '%Y-%m-%d') or '-'}   客户参考：{o.get('client_order_ref') or '-'}")
    print(f"   未税 {_money(o.get('amount_untaxed'))} + 税 {_money(o.get('amount_tax'))} = 总额 {_money(o.get('amount_total'))}")
    lines = odoo.read(SOL, o.get("order_line") or [], [
        "product_id", "name", "product_uom_qty", "qty_delivered", "price_unit",
        "discount", "price_subtotal", "display_type"])
    rows = []
    for ln in lines:
        if ln.get("display_type"):
            rows.append(["—", (ln.get("name") or "")[:40], "", "", "", ""])
            continue
        rows.append([m2o_name(ln.get("product_id"))[:18], ln.get("product_uom_qty"),
                     ln.get("qty_delivered"), _money(ln.get("price_unit")),
                     f"{int(ln.get('discount') or 0)}%", _money(ln.get("price_subtotal"))])
    print("\n   明细：")
    for line in render_table(rows, ["产品", "数量", "已交", "单价", "折扣", "小计"]).splitlines():
        print("   " + line)


def cmd_add(odoo: Odoo, args):
    vals = {"partner_id": _resolve(odoo, "res.partner", args.customer, "客户"),
            "order_line": _parse_lines(odoo, args.line)}
    if args.ref:
        vals["client_order_ref"] = args.ref
    oid = odoo.create(SO, vals)
    o = odoo.read(SO, [oid], ["name", "amount_total"])[0]
    print(f"✅ 已建报价单 {o['name']}（#{oid}），金额 {_money(o.get('amount_total'))}")


def cmd_confirm(odoo: Odoo, args):
    odoo.execute_kw(SO, "action_confirm", [[args.id]])
    print(f"✅ 销售单 #{args.id} 已确认（draft→销售订单；装 sale_stock 已自动建交货单）")


def cmd_cancel(odoo: Odoo, args):
    odoo.execute_kw(SO, "action_cancel", [[args.id]])
    print(f"✅ 销售单 #{args.id} 已取消")


def cmd_invoice(odoo: Odoo, args):
    inv = odoo.execute_kw(SO, "_create_invoices", [[args.id]])
    ids = inv if isinstance(inv, list) else []
    if ids:
        moves = odoo.read("account.move", ids, ["name", "amount_total"])
        print("✅ 已生成发票：" + ", ".join(f"{m['name']}({_money(m['amount_total'])})" for m in moves))
    else:
        print(f"✅ 已为销售单 #{args.id} 生成发票")


def build_parser():
    p = argparse.ArgumentParser(description="辉火套件ERP 销售订单")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="列订单")
    li.add_argument("--draft", action="store_true")
    li.add_argument("--confirmed", action="store_true")
    li.add_argument("--customer")
    li.add_argument("--all", action="store_true")
    li.add_argument("--limit", type=int, default=80)

    sh = sub.add_parser("show", help="订单详情")
    sh.add_argument("id", type=int)

    ad = sub.add_parser("add", help="建报价单")
    ad.add_argument("--customer", required=True)
    ad.add_argument("--line", action="append", required=True, help='"产品:数量[:单价]"，可重复')
    ad.add_argument("--ref", help="客户参考号")

    for name, hlp in [("confirm", "确认订单"), ("cancel", "取消订单"), ("invoice", "生成发票")]:
        sp = sub.add_parser(name, help=hlp)
        sp.add_argument("id", type=int)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"list": cmd_list, "show": cmd_show, "add": cmd_add,
                    "confirm": cmd_confirm, "cancel": cmd_cancel, "invoice": cmd_invoice}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
