#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stock.py — 辉火套件ERP「库存 Inventory」查询与出入库（stock.picking/quant/move）

字段坑（详见 references/odoo-sales-purchase-stock-api.md）：
  - 查产品库存最简走 product.product 的 free_qty/qty_available/virtual_available（compute，可 read/domain）；
    限仓库/库位走 context（{'warehouse_id':..} / {'location':..}），不是 domain。
  - 出入库单明细用 move_ids（v19 已删 move_ids_without_package）；完成量是 quantity（非 qty_done）。
  - button_validate 必传 context skip_backorder=True，否则返回向导 dict 而非 True。

命令
  qty        查产品库存   qty <产品> [--warehouse W]
  pickings   列待处理出入库单  --in 收货 / --out 发货 / --internal 调拨
  show       出入库单明细（move 行）
  validate   验证出入库单（预留→设完成量→过账；写操作，执行前向用户确认）
  locations  列内部库位
  warehouses 列仓库

示例
  python3 stock.py qty 办公椅
  python3 stock.py pickings --in
  python3 stock.py validate 55
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table

CODE = {"incoming": "收货", "outgoing": "发货", "internal": "调拨"}
PSTATE = {"draft": "草稿", "waiting": "等待上游", "confirmed": "待预留",
          "assigned": "就绪", "done": "完成", "cancel": "取消"}


def _num(v) -> str:
    try:
        return f"{float(v or 0):g}"
    except (TypeError, ValueError):
        return str(v)


def _resolve(odoo: Odoo, model: str, ref, label: str):
    if str(ref).isdigit():
        return int(ref)
    r = odoo.name_search(model, str(ref), limit=1)
    if not r:
        raise OdooError(f"找不到{label}「{ref}」。")
    return r[0][0]


def cmd_qty(odoo: Odoo, args):
    pid = _resolve(odoo, "product.product", args.product, "产品")
    ctx = {}
    if args.warehouse:
        ctx["warehouse_id"] = _resolve(odoo, "stock.warehouse", args.warehouse, "仓库")
    p = odoo.execute_kw("product.product", "read", [[pid]], {
        "fields": ["name", "qty_available", "free_qty", "virtual_available",
                   "incoming_qty", "outgoing_qty"], "context": ctx})
    if not p:
        raise OdooError(f"产品 #{pid} 不存在。")
    p = p[0]
    if args.json:
        print(json.dumps(p, ensure_ascii=False, default=str))
        return
    print(f"📦 {p['name']}" + (f"（仓库 {args.warehouse}）" if args.warehouse else "（全部内部库位）"))
    print(f"   在手 {_num(p.get('qty_available'))}  |  可用 {_num(p.get('free_qty'))}  |  "
          f"预测 {_num(p.get('virtual_available'))}")
    print(f"   待入库 {_num(p.get('incoming_qty'))}  |  待出库 {_num(p.get('outgoing_qty'))}")
    # 按库位拆（read_group quant）
    rows = odoo.read_group(
        "stock.quant", [["product_id", "=", pid], ["location_id.usage", "=", "internal"]],
        ["quantity:sum", "reserved_quantity:sum"], ["location_id"], lazy=False)
    if rows:
        print("\n   按库位：")
        tbl = [[m2o_name(r.get("location_id")), _num(r.get("quantity")),
                _num(r.get("quantity", 0) - r.get("reserved_quantity", 0))] for r in rows]
        for line in render_table(tbl, ["库位", "在手", "可用"]).splitlines():
            print("   " + line)


def cmd_pickings(odoo: Odoo, args):
    domain = [("state", "in", ["waiting", "confirmed", "assigned"])]
    if args.incoming:
        domain.append(("picking_type_code", "=", "incoming"))
    elif args.outgoing:
        domain.append(("picking_type_code", "=", "outgoing"))
    elif args.internal:
        domain.append(("picking_type_code", "=", "internal"))
    if args.done:
        domain = [("state", "=", "done")]
        if args.incoming:
            domain.append(("picking_type_code", "=", "incoming"))
        elif args.outgoing:
            domain.append(("picking_type_code", "=", "outgoing"))
    pks = odoo.search_read(
        "stock.picking", domain,
        ["name", "partner_id", "picking_type_code", "scheduled_date", "state", "origin"],
        order="scheduled_date asc", limit=args.limit)
    if args.json:
        print(json.dumps(pks, ensure_ascii=False, default=str))
        return
    rows = [[k["id"], k["name"], CODE.get(k.get("picking_type_code"), "-"),
             PSTATE.get(k["state"], k["state"]), m2o_name(k.get("partner_id")) or "-",
             from_utc(k.get("scheduled_date") or "", "%m-%d %H:%M") or "-",
             (k.get("origin") or "")[:14]] for k in pks]
    print(render_table(rows, ["ID", "单号", "类型", "状态", "联系人", "计划", "来源"]))
    print(f"\n共 {len(pks)} 单")


def cmd_show(odoo: Odoo, args):
    k = odoo.read("stock.picking", [args.id], [
        "name", "partner_id", "picking_type_code", "state", "location_id",
        "location_dest_id", "scheduled_date", "origin", "move_ids"])
    if not k:
        raise OdooError(f"出入库单 #{args.id} 不存在。")
    k = k[0]
    print(f"📋 {k['name']}（#{args.id}）  [{CODE.get(k.get('picking_type_code'), '-')} · {PSTATE.get(k['state'], k['state'])}]")
    print(f"   {m2o_name(k.get('location_id'))} → {m2o_name(k.get('location_dest_id'))}")
    print(f"   联系人：{m2o_name(k.get('partner_id')) or '-'}   来源：{k.get('origin') or '-'}")
    moves = odoo.read("stock.move", k.get("move_ids") or [], [
        "product_id", "product_uom_qty", "quantity", "state"])
    rows = [[m2o_name(m.get("product_id"))[:24], _num(m.get("product_uom_qty")),
             _num(m.get("quantity")), m.get("state")] for m in moves]
    print("\n   明细（需求/完成）：")
    for line in render_table(rows, ["产品", "需求", "完成", "状态"]).splitlines():
        print("   " + line)


def cmd_validate(odoo: Odoo, args):
    odoo.execute_kw("stock.picking", "action_assign", [[args.id]])
    moves = odoo.search_read(
        "stock.move", [["picking_id", "=", args.id], ["state", "not in", ["done", "cancel"]]],
        ["product_uom_qty"])
    for m in moves:
        odoo.write("stock.move", [m["id"]], {"quantity": m["product_uom_qty"], "picked": True})
    res = odoo.execute_kw("stock.picking", "button_validate", [[args.id]], {
        "context": {"skip_backorder": True, "picking_ids_not_to_backorder": [args.id]}})
    if res is True:
        print(f"✅ 出入库单 #{args.id} 已验证完成（state→done）")
    else:
        print(f"⚠️ 出入库单 #{args.id} 验证返回向导（可能有部分缺货/欠单），请在 odoo 界面处理")


def cmd_locations(odoo: Odoo, args):
    locs = odoo.search_read(
        "stock.location", [["usage", "=", "internal"]],
        ["complete_name", "warehouse_id"], order="complete_name", limit=args.limit)
    rows = [[x["id"], x.get("complete_name"), m2o_name(x.get("warehouse_id")) or "-"] for x in locs]
    print(render_table(rows, ["ID", "库位", "仓库"]))


def cmd_warehouses(odoo: Odoo, args):
    whs = odoo.search_read("stock.warehouse", [], ["name", "code"], order="name")
    rows = [[w["id"], w["name"], w.get("code") or "-"] for w in whs]
    print(render_table(rows, ["ID", "仓库", "代码"]))


def build_parser():
    p = argparse.ArgumentParser(description="辉火套件ERP 库存查询与出入库")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("qty", help="查产品库存")
    q.add_argument("product")
    q.add_argument("--warehouse", help="限定仓库")

    pk = sub.add_parser("pickings", help="列出入库单")
    pk.add_argument("--in", dest="incoming", action="store_true", help="收货")
    pk.add_argument("--out", dest="outgoing", action="store_true", help="发货")
    pk.add_argument("--internal", action="store_true", help="内部调拨")
    pk.add_argument("--done", action="store_true", help="看已完成")
    pk.add_argument("--limit", type=int, default=80)

    sh = sub.add_parser("show", help="出入库单明细")
    sh.add_argument("id", type=int)

    va = sub.add_parser("validate", help="验证出入库单")
    va.add_argument("id", type=int)

    sub.add_parser("locations", help="列内部库位").add_argument("--limit", type=int, default=100)
    sub.add_parser("warehouses", help="列仓库")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"qty": cmd_qty, "pickings": cmd_pickings, "show": cmd_show,
                    "validate": cmd_validate, "locations": cmd_locations, "warehouses": cmd_warehouses}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
