#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
overview.py — 产销存一页总览（老板/厂长视图，也是晨报数据源）

命令
  today                      今日总览（接单/应交/完工/发货/质检 + 风险快照）
  yesterday                  昨日总览

示例
  python3 overview.py today
"""

from __future__ import annotations

import argparse
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import (
    DELIVERY_STATUS, day_range_utc, from_utc, label, m2o_name, money, now_utc,
    qty, render_table,
)


def _overview(offset: int):
    odoo = Odoo()
    day_label = "今日" if offset == 0 else "昨日"
    start, end = day_range_utc(offset)
    date_str = from_utc(start, "%Y-%m-%d")
    print(f"📊 {day_label}总览  {date_str}\n")

    # 接单
    so_domain = [["date_order", ">=", start], ["date_order", "<=", end],
                 ["state", "in", ["sale", "done"]]]
    agg = odoo.read_group("sale.order", so_domain, ["amount_total"], [], lazy=False)
    n_so = agg[0].get("__count", 0) if agg else 0
    amt = agg[0].get("amount_total", 0) if (agg and n_so) else 0
    print(f"🧾 接单: {n_so} 张 / {money(amt)}")

    # 应交（承诺交期落在当天、还没发完的销售单）
    due = odoo.search_read(
        "sale.order",
        [["commitment_date", ">=", start], ["commitment_date", "<=", end],
         ["state", "=", "sale"],
         ["delivery_status", "in", ["pending", "started", "partial"]]],
        ["name", "partner_id", "delivery_status", "x_follower_user_id"], limit=20,
    )
    print(f"📅 {day_label}应交未发: {len(due)} 张")
    if due:
        rows = [[o["name"], m2o_name(o["partner_id"]),
                 label(DELIVERY_STATUS, o.get("delivery_status")),
                 m2o_name(o.get("x_follower_user_id"))] for o in due]
        print(render_table(rows, ["订单", "客户", "发货状态", "跟单"]))

    # 完工
    mo_done = odoo.search_read(
        "mrp.production",
        [["date_finished", ">=", start], ["date_finished", "<=", end], ["state", "=", "done"]],
        ["name", "product_id", "product_qty"], limit=50,
    )
    total_qty = sum(m["product_qty"] for m in mo_done)
    print(f"\n🏭 完工: {len(mo_done)} 张制造单 / {qty(total_qty)} 件")

    # 发货（出库完成）
    out_done = odoo.search_read(
        "stock.picking",
        [["date_done", ">=", start], ["date_done", "<=", end], ["state", "=", "done"],
         ["picking_type_id.code", "=", "outgoing"]],
        ["name", "partner_id", "sale_id"], limit=50,
    )
    print(f"🚚 发货: {len(out_done)} 单")
    if out_done:
        rows = [[pk["name"], m2o_name(pk["partner_id"]), m2o_name(pk.get("sale_id"))]
                for pk in out_done[:10]]
        print(render_table(rows, ["出库单", "客户", "销售单"]))

    # 质检
    qc = odoo.read_group(
        "quality.check",
        [["control_date", ">=", start], ["control_date", "<=", end],
         ["quality_state", "in", ["pass", "fail"]]],
        [], ["quality_state"], lazy=False,
    )
    qmap = {g["quality_state"]: g.get("__count", 0) for g in qc}
    print(f"\n🔍 质检: 合格 {qmap.get('pass', 0)} / 不合格 {qmap.get('fail', 0)}")

    # 风险快照（与日期无关的当前态）
    wip_states = ["confirmed", "progress", "to_close"]
    n_wip = odoo.search_count("mrp.production", [["state", "in", wip_states]])
    n_late = odoo.search_count(
        "mrp.production", [["state", "in", wip_states], ["date_deadline", "<", now_utc()]])
    n_short = odoo.search_count(
        "mrp.production",
        [["state", "in", wip_states],
         ["components_availability_state", "in", ["late", "unavailable"]]])
    n_po_overdue = odoo.search_count(
        "purchase.order",
        [["state", "=", "purchase"], ["receipt_status", "in", ["pending", "partial"]],
         ["date_planned", "<", now_utc()]])
    n_qc_todo = odoo.search_count("quality.check", [["quality_state", "=", "none"]])
    print(f"\n⚠️ 风险快照: 在制 {n_wip} 张"
          f" | 延期 {n_late} 张"
          f" | 缺料 {n_short} 张"
          f" | 采购逾期 {n_po_overdue} 张"
          f" | 待检 {n_qc_todo} 张")
    if n_late:
        print("   → 延期明细: python3 mfg.py late")
    if n_short:
        print("   → 缺料明细: python3 mfg.py shortage")


def build_parser():
    p = argparse.ArgumentParser(description="产销存总览")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("today", help="今日总览")
    sub.add_parser("yesterday", help="昨日总览")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        _overview(0 if args.cmd == "today" else -1)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
