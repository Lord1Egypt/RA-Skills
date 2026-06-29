#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
purchase.py — 采购到货跟踪

命令
  incoming [--limit N]       在途采购单（已确认但未收齐），按预计到货日排序，逾期标 ⚠️
  overdue [--limit N]        逾期未到货（预计到货日已过）

示例
  python3 purchase.py incoming
  python3 purchase.py overdue
"""

from __future__ import annotations

import argparse
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import (
    RECEIPT_STATUS, from_utc, label, m2o_name, money, now_utc, render_table,
)

PO_FIELDS = ["name", "partner_id", "date_planned", "receipt_status",
             "amount_total", "user_id", "origin"]
OPEN_DOMAIN = [["state", "=", "purchase"],
               ["receipt_status", "in", ["pending", "partial"]]]


def _po_rows(pos: list[dict]) -> list[list]:
    now = now_utc()
    rows = []
    for po in pos:
        planned = po.get("date_planned") or ""
        flag = "⚠️ " if planned and planned < now else ""
        rows.append([flag + po["name"], m2o_name(po["partner_id"]),
                     from_utc(planned, "%m-%d") if planned else "",
                     label(RECEIPT_STATUS, po.get("receipt_status")),
                     money(po["amount_total"]), m2o_name(po.get("user_id")),
                     po.get("origin") or ""])
    return rows


HEADERS = ["采购单", "供应商", "预计到货", "收货状态", "金额", "采购员", "来源"]


def cmd_incoming(args):
    odoo = Odoo()
    pos = odoo.search_read("purchase.order", OPEN_DOMAIN, PO_FIELDS,
                           limit=args.limit, order="date_planned asc")
    if not pos:
        print("✅ 没有在途采购单。")
        return
    print(f"🚚 在途采购单（{len(pos)} 张，⚠️ = 已超预计到货日）\n")
    print(render_table(_po_rows(pos), HEADERS))


def cmd_overdue(args):
    odoo = Odoo()
    domain = OPEN_DOMAIN + [["date_planned", "<", now_utc()]]
    pos = odoo.search_read("purchase.order", domain, PO_FIELDS,
                           limit=args.limit, order="date_planned asc")
    if not pos:
        print("✅ 没有逾期未到货的采购单。")
        return
    print(f"⚠️ 逾期未到货采购单（{len(pos)} 张）\n")
    print(render_table(_po_rows(pos), HEADERS))


def build_parser():
    p = argparse.ArgumentParser(description="采购到货跟踪")
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("incoming", help="在途采购")
    i.add_argument("--limit", type=int, default=30)
    o = sub.add_parser("overdue", help="逾期未到货")
    o.add_argument("--limit", type=int, default=30)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"incoming": cmd_incoming, "overdue": cmd_overdue}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
