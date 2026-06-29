#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
purchase.py — 辉火套件ERP「采购 Purchase」订单管理（purchase.order + purchase.order.line）

字段坑（详见 references/odoo-sales-purchase-stock-api.md）：
  - 行数量字段是 product_qty（不是 product_uom_qty！销售才用 product_uom_qty）。
  - v19 行字段：product_uom_id（非 product_uom）、tax_ids（非 taxes_id）；订单备注 note（非 notes）。
  - state 无 done：draft(询价单)/sent/to approve(待批准)/purchase(采购订单)/cancel；锁定用 locked。
  - button_confirm 是写操作（确认后自动建入库单 stock.picking）——执行前向用户确认。
  - qty_received 实物产品不可直接写（由入库单 done 自动算）。

命令
  list     列采购单 默认我的；--rfq 询价单 / --confirmed 已确认 / --vendor / --all
  show     采购单详情 + 明细行
  add      建询价单 --vendor X --line "产品:数量[:单价]"（--line 可重复）
  confirm  确认（draft→purchase 或 to approve）
  approve  批准（to approve→purchase）
  cancel   取消采购单
  bill     生成供应商账单（action_create_invoice）

示例
  python3 purchase.py add --vendor "某供应商" --line "原料A:100:5" --line "原料B:50"
  python3 purchase.py list --rfq
  python3 purchase.py confirm 18
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table

PO = "purchase.order"
POL = "purchase.order.line"
STATE = {"draft": "询价单", "sent": "已发送", "to approve": "待批准",
         "purchase": "采购订单", "cancel": "已取消"}
RECEIPT = {"pending": "未收货", "partial": "部分收货", "full": "已收货"}
INV_STATUS = {"no": "无需开票", "to invoice": "待开票", "invoiced": "已开票"}


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
                "product_qty": float(parts[1]) if len(parts) > 1 and parts[1] else 1.0}
        if len(parts) > 2 and parts[2]:
            vals["price_unit"] = float(parts[2])
        cmds.append((0, 0, vals))
    return cmds


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = []
    if args.rfq:
        domain.append(("state", "in", ["draft", "sent"]))
    elif args.confirmed:
        domain.append(("state", "=", "purchase"))
    elif not args.all:
        domain.append(("user_id", "=", uid))
    if args.vendor:
        domain.append(("partner_id", "=", _resolve(odoo, "res.partner", args.vendor, "供应商")))
    orders = odoo.search_read(
        PO, domain,
        ["name", "partner_id", "state", "amount_total", "date_order", "receipt_status", "invoice_status"],
        order="date_order desc", limit=args.limit)
    if args.json:
        print(json.dumps(orders, ensure_ascii=False, default=str))
        return
    rows, total = [], 0.0
    for o in orders:
        total += o.get("amount_total") or 0
        rows.append([o["id"], o["name"], STATE.get(o["state"], o["state"]),
                     m2o_name(o.get("partner_id")) or "-", _money(o.get("amount_total")),
                     RECEIPT.get(o.get("receipt_status"), "-"),
                     INV_STATUS.get(o.get("invoice_status"), o.get("invoice_status") or "-")])
    print(render_table(rows, ["ID", "单号", "状态", "供应商", "金额", "收货", "开票"]))
    print(f"\n共 {len(orders)} 单，金额合计 {_money(total)}")


def cmd_show(odoo: Odoo, args):
    o = odoo.read(PO, [args.id], [
        "name", "partner_id", "state", "amount_untaxed", "amount_tax", "amount_total",
        "date_order", "user_id", "receipt_status", "invoice_status", "order_line", "partner_ref"])
    if not o:
        raise OdooError(f"采购单 #{args.id} 不存在。")
    o = o[0]
    print(f"🧾 采购单 {o['name']}（#{args.id}）  [{STATE.get(o['state'], o['state'])}]")
    print(f"   供应商：{m2o_name(o.get('partner_id')) or '-'}   采购员：{m2o_name(o.get('user_id')) or '-'}")
    print(f"   日期：{from_utc(o.get('date_order') or '', '%Y-%m-%d') or '-'}   供应商参考：{o.get('partner_ref') or '-'}")
    print(f"   收货：{RECEIPT.get(o.get('receipt_status'), '-')}   开票：{INV_STATUS.get(o.get('invoice_status'), '-')}")
    print(f"   未税 {_money(o.get('amount_untaxed'))} + 税 {_money(o.get('amount_tax'))} = 总额 {_money(o.get('amount_total'))}")
    lines = odoo.read(POL, o.get("order_line") or [], [
        "product_id", "name", "product_qty", "qty_received", "price_unit", "price_subtotal", "display_type"])
    rows = []
    for ln in lines:
        if ln.get("display_type"):
            rows.append(["—", (ln.get("name") or "")[:40], "", "", ""])
            continue
        rows.append([m2o_name(ln.get("product_id"))[:18], ln.get("product_qty"),
                     ln.get("qty_received"), _money(ln.get("price_unit")), _money(ln.get("price_subtotal"))])
    print("\n   明细：")
    for line in render_table(rows, ["产品", "数量", "已收", "单价", "小计"]).splitlines():
        print("   " + line)


def cmd_add(odoo: Odoo, args):
    vals = {"partner_id": _resolve(odoo, "res.partner", args.vendor, "供应商"),
            "order_line": _parse_lines(odoo, args.line)}
    if args.ref:
        vals["partner_ref"] = args.ref
    oid = odoo.create(PO, vals)
    o = odoo.read(PO, [oid], ["name", "amount_total"])[0]
    print(f"✅ 已建询价单 {o['name']}（#{oid}），金额 {_money(o.get('amount_total'))}")


def cmd_confirm(odoo: Odoo, args):
    odoo.execute_kw(PO, "button_confirm", [[args.id]])
    o = odoo.read(PO, [args.id], ["state"])[0]
    print(f"✅ 采购单 #{args.id} 已确认 → {STATE.get(o['state'], o['state'])}（采购订单会自动建入库单；待批准需 approve）")


def cmd_approve(odoo: Odoo, args):
    odoo.execute_kw(PO, "button_approve", [[args.id]])
    print(f"✅ 采购单 #{args.id} 已批准 → 采购订单")


def cmd_cancel(odoo: Odoo, args):
    odoo.execute_kw(PO, "button_cancel", [[args.id]])
    print(f"✅ 采购单 #{args.id} 已取消")


def cmd_bill(odoo: Odoo, args):
    odoo.execute_kw(PO, "action_create_invoice", [[args.id]])
    print(f"✅ 已为采购单 #{args.id} 生成供应商账单")


def build_parser():
    p = argparse.ArgumentParser(description="辉火套件ERP 采购订单")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="列采购单")
    li.add_argument("--rfq", action="store_true", help="询价单")
    li.add_argument("--confirmed", action="store_true")
    li.add_argument("--vendor")
    li.add_argument("--all", action="store_true")
    li.add_argument("--limit", type=int, default=80)

    sh = sub.add_parser("show", help="采购单详情")
    sh.add_argument("id", type=int)

    ad = sub.add_parser("add", help="建询价单")
    ad.add_argument("--vendor", required=True)
    ad.add_argument("--line", action="append", required=True, help='"产品:数量[:单价]"，可重复')
    ad.add_argument("--ref", help="供应商参考号")

    for name, hlp in [("confirm", "确认"), ("approve", "批准"), ("cancel", "取消"), ("bill", "生成账单")]:
        sp = sub.add_parser(name, help=hlp)
        sp.add_argument("id", type=int)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"list": cmd_list, "show": cmd_show, "add": cmd_add, "confirm": cmd_confirm,
                    "approve": cmd_approve, "cancel": cmd_cancel, "bill": cmd_bill}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
