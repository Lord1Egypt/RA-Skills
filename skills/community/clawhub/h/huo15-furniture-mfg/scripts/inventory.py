#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inventory.py — 库存查询

命令
  find <关键词> [--limit N]   按 名称/内部编号/条码/型号 模糊查产品库存
                              （型号 = 客户 Studio 定制字段 x_studio_xinghao）

示例
  python3 inventory.py find 云栖
  python3 inventory.py find C3
"""

from __future__ import annotations

import argparse
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import m2o_name, qty, render_table


def cmd_find(args):
    odoo = Odoo()
    kw = args.keyword
    domain = ["|", "|", "|",
              ["name", "ilike", kw],
              ["default_code", "ilike", kw],
              ["barcode", "ilike", kw],
              ["x_studio_xinghao", "ilike", kw]]
    # qty_available 等数量字段是非存储计算字段，不能进 SQL order by，取回后本地排序
    prods = odoo.search_read(
        "product.product", domain,
        ["name", "default_code", "x_studio_xinghao", "qty_available", "free_qty",
         "virtual_available", "incoming_qty", "outgoing_qty", "uom_id"],
        limit=args.limit, order="name asc",
    )
    if not prods:
        print(f"未找到产品：{kw}")
        return
    prods.sort(key=lambda p: -p["qty_available"])
    rows = []
    for p in prods:
        flag = ""
        if p["qty_available"] < 0:
            flag = "❗"
        elif p["qty_available"] == 0:
            flag = "○"
        rows.append([flag + p["name"], p.get("default_code") or "",
                     p.get("x_studio_xinghao") or "",
                     qty(p["qty_available"]), qty(p["free_qty"]),
                     qty(p["incoming_qty"]), qty(p["outgoing_qty"]),
                     qty(p["virtual_available"]), m2o_name(p["uom_id"])])
    print(f"📦 库存查询「{kw}」（{len(prods)} 个产品；❗负库存 ○零库存）\n")
    print(render_table(
        rows, ["产品", "编号", "型号", "在手", "可用", "入向", "出向", "预测", "单位"]))


def build_parser():
    p = argparse.ArgumentParser(description="库存查询")
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find", help="模糊查库存")
    f.add_argument("keyword")
    f.add_argument("--limit", type=int, default=15)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "find":
            cmd_find(args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
