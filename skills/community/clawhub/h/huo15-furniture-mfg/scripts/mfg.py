#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mfg.py — 制造单（生产）查询

命令
  wip [--limit N]            在制清单（已确认/生产中/待关闭）
  late                       延期清单（超过截止日期还没完工）
  shortage [制造单号]         欠料检查：
                             无参 → 列出所有等料/缺料的在制单
                             带单号 → 展开该单组件明细，标出缺哪些料

示例
  python3 mfg.py wip
  python3 mfg.py late
  python3 mfg.py shortage
  python3 mfg.py shortage MO-260604-643
"""

from __future__ import annotations

import argparse
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import (
    AVAIL_STATE, MO_STATE, RESERVATION_STATE, from_utc, label, m2o_name,
    now_utc, qty, render_table,
)

WIP_STATES = ["confirmed", "progress", "to_close"]
MO_FIELDS = [
    "name", "product_id", "product_qty", "qty_producing", "state",
    "components_availability", "components_availability_state",
    "reservation_state", "date_start", "date_deadline", "origin",
]


def _mo_rows(mos: list[dict]) -> list[list]:
    rows = []
    for m in mos:
        avail = m.get("components_availability") or label(AVAIL_STATE, m.get("components_availability_state"))
        deadline = from_utc(m["date_deadline"], "%m-%d") if m.get("date_deadline") else ""
        rows.append([m["name"], m2o_name(m["product_id"]), qty(m["product_qty"]),
                     label(MO_STATE, m["state"]), avail, deadline, m.get("origin") or ""])
    return rows


def cmd_wip(args):
    odoo = Odoo()
    mos = odoo.search_read(
        "mrp.production", [["state", "in", WIP_STATES]],
        MO_FIELDS, limit=args.limit, order="date_deadline asc, id",
    )
    total = odoo.search_count("mrp.production", [["state", "in", WIP_STATES]])
    print(f"🏭 在制制造单（共 {total} 张，显示 {len(mos)} 张，按截止日期排序）\n")
    print(render_table(_mo_rows(mos), ["制造单", "产品", "数量", "状态", "备料", "截止", "来源"]))


def cmd_late(args):
    odoo = Odoo()
    domain = [["state", "in", WIP_STATES], ["date_deadline", "<", now_utc()]]
    mos = odoo.search_read("mrp.production", domain, MO_FIELDS,
                           limit=args.limit, order="date_deadline asc")
    if not mos:
        print("✅ 没有延期的在制单。")
        return
    print(f"⚠️ 延期制造单（{len(mos)} 张，截止日期已过仍未完工）\n")
    print(render_table(_mo_rows(mos), ["制造单", "产品", "数量", "状态", "备料", "截止", "来源"]))


def cmd_shortage(args):
    odoo = Odoo()
    if not args.mo:
        domain = [["state", "in", WIP_STATES],
                  ["components_availability_state", "in", ["expected", "late", "unavailable"]]]
        mos = odoo.search_read("mrp.production", domain, MO_FIELDS,
                               limit=args.limit, order="date_deadline asc")
        if not mos:
            print("✅ 在制单全部齐料。")
            return
        print(f"⚠️ 等料/缺料的在制单（{len(mos)} 张）\n")
        print(render_table(_mo_rows(mos), ["制造单", "产品", "数量", "状态", "备料", "截止", "来源"]))
        print("\n用 `mfg.py shortage <制造单号>` 看具体缺哪些料。")
        return

    mos = odoo.search_read("mrp.production", [["name", "ilike", args.mo]],
                           MO_FIELDS + ["move_raw_ids"], limit=1)
    if not mos:
        print(f"未找到制造单：{args.mo}")
        return
    mo = mos[0]
    avail = mo.get("components_availability") or label(AVAIL_STATE, mo.get("components_availability_state"))
    print(f"🏭 {mo['name']}  {m2o_name(mo['product_id'])} × {qty(mo['product_qty'])}")
    print(f"   状态: {label(MO_STATE, mo['state'])} | 备料: {avail}"
          f" | 就绪度: {label(RESERVATION_STATE, mo.get('reservation_state'))}"
          + (f" | 来源: {mo['origin']}" if mo.get("origin") else ""))
    if not mo.get("move_raw_ids"):
        # 和栖大部分制造单不挂 BOM（全库组件行仅个位数），无法逐项欠料分析
        print("（该制造单未挂 BOM / 无组件清单，无法逐项分析欠料；上方“备料”状态仍可参考）")
        return
    # 组件明细：Odoo 19 实收数量字段是 quantity（不是 17 以前的 quantity_done）
    moves = odoo.read(
        "stock.move", mo["move_raw_ids"],
        ["product_id", "product_uom_qty", "quantity", "forecast_availability",
         "forecast_expected_date", "state"],
    )
    rows, short = [], 0
    for mv in moves:
        if mv["state"] in ("done", "cancel"):
            continue
        demand = mv["product_uom_qty"]
        forecast = mv.get("forecast_availability") or 0
        lack = forecast < demand
        if lack:
            short += 1
        eta = from_utc(mv["forecast_expected_date"], "%m-%d") if mv.get("forecast_expected_date") else ""
        rows.append([("⚠️ " if lack else "") + m2o_name(mv["product_id"]),
                     qty(demand), qty(forecast), eta])
    print(f"\n── 组件（{short} 项缺口）──")
    print(render_table(rows, ["物料", "需求", "可预测供应", "预计到料"]))


def build_parser():
    p = argparse.ArgumentParser(description="制造单查询")
    sub = p.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("wip", help="在制清单")
    w.add_argument("--limit", type=int, default=30)
    l = sub.add_parser("late", help="延期清单")
    l.add_argument("--limit", type=int, default=50)
    s = sub.add_parser("shortage", help="欠料检查")
    s.add_argument("mo", nargs="?", help="制造单号（可选）")
    s.add_argument("--limit", type=int, default=30)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "wip":
            cmd_wip(args)
        elif args.cmd == "late":
            cmd_late(args)
        elif args.cmd == "shortage":
            cmd_shortage(args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
