#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
order.py — 销售订单跟踪（跟单员核心场景）

命令
  status <关键词>            订单全链路状态：SO → 制造单 → 出入库 → 质检 一次穿透
                             关键词可以是订单号（SO-260531-758，支持模糊）或客户名
  list [--days N] [--undelivered] [--customer 名称] [--limit N]
                             订单列表（默认最近 30 天）
  channels [--days 30]       渠道来源统计：电商平台单（带来源单号）vs 直营/经销
                             （test 库实测 64% 订单带平台来源单号）

示例
  python3 order.py status SO-260531-758
  python3 order.py status 梁泽光
  python3 order.py list --undelivered
  python3 order.py channels --days 30
"""

from __future__ import annotations

import argparse
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import (
    AVAIL_STATE, DELIVERY_STATUS, INVOICE_STATUS, MO_STATE, PICKING_STATE,
    QC_STATE, SO_STATE, days_ago_utc, from_utc, label, m2o_name, money, qty,
    render_table,
)

SO_FIELDS = [
    "name", "partner_id", "state", "date_order", "commitment_date", "expected_date",
    "delivery_status", "invoice_status", "amount_total", "user_id", "origin",
    "client_order_ref",
    # huo15_sale_contractt_exchanges 定制字段（test 库实测存在）
    "x_salesperson_user_id", "x_follower_user_id", "x_source_order_ref",
    "x_actual_shipment_time",
]


def _find_orders(odoo: Odoo, keyword: str, limit: int = 5) -> list[dict]:
    """先按单号模糊找，找不到再按客户名找其最近订单。"""
    orders = odoo.search_read(
        "sale.order", [["name", "ilike", keyword]],
        SO_FIELDS, limit=limit, order="date_order desc",
    )
    if orders:
        return orders
    partners = odoo.name_search("res.partner", keyword, limit=5)
    if not partners:
        return []
    pids = [p[0] for p in partners]
    return odoo.search_read(
        "sale.order", [["partner_id", "in", pids]],
        SO_FIELDS, limit=limit, order="date_order desc",
    )


def _print_status(odoo: Odoo, so: dict, full: bool = True):
    print(f"📋 {so['name']}  —  {m2o_name(so['partner_id'])}")
    print(f"   状态: {label(SO_STATE, so['state'])}"
          f" | 发货: {label(DELIVERY_STATUS, so.get('delivery_status'))}"
          f" | 开票: {label(INVOICE_STATUS, so.get('invoice_status'))}"
          f" | 金额: {money(so['amount_total'])}")
    line2 = [f"下单: {from_utc(so.get('date_order'))}"]
    if so.get("commitment_date"):
        line2.append(f"承诺交期: {from_utc(so['commitment_date'], '%Y-%m-%d')}")
    if so.get("expected_date"):
        line2.append(f"预计交付: {from_utc(so['expected_date'], '%Y-%m-%d')}")
    if so.get("x_actual_shipment_time"):
        line2.append(f"实际发货: {from_utc(so['x_actual_shipment_time'])}")
    print("   " + " | ".join(line2))
    people = []
    sales = m2o_name(so.get("x_salesperson_user_id")) or m2o_name(so.get("user_id"))
    if sales:
        people.append(f"销售: {sales}")
    if so.get("x_follower_user_id"):
        people.append(f"跟单: {m2o_name(so['x_follower_user_id'])}")
    ref = so.get("x_source_order_ref") or so.get("client_order_ref")
    if ref:
        people.append(f"来源单号: {ref}")
    if people:
        print("   " + " | ".join(people))
    if not full:
        return

    # 明细行
    lines = odoo.search_read(
        "sale.order.line",
        [["order_id", "=", so["id"]], ["display_type", "=", False]],
        ["product_id", "product_uom_qty", "qty_delivered", "price_subtotal"],
    )
    if lines:
        rows = [[m2o_name(l["product_id"]), qty(l["product_uom_qty"]),
                 qty(l["qty_delivered"]), money(l["price_subtotal"])] for l in lines]
        print("\n── 明细 ──")
        print(render_table(rows, ["产品", "订购", "已发", "小计"]))

    # 制造单（链路：mrp.production.origin = SO 单号，test 库覆盖率 92%）
    mos = odoo.search_read(
        "mrp.production", [["origin", "=", so["name"]]],
        ["name", "product_id", "product_qty", "state", "components_availability",
         "components_availability_state", "date_start", "date_finished"],
        order="id",
    )
    print("\n── 生产 ──")
    if mos:
        rows = []
        for m in mos:
            avail = m.get("components_availability") or label(AVAIL_STATE, m.get("components_availability_state"))
            done = from_utc(m["date_finished"], "%m-%d") if m.get("date_finished") else ""
            rows.append([m["name"], m2o_name(m["product_id"]), qty(m["product_qty"]),
                         label(MO_STATE, m["state"]), avail, done])
        print(render_table(rows, ["制造单", "产品", "数量", "状态", "备料", "完工"]))
    else:
        print("（无关联制造单 —— 可能是现货直发或外购）")

    # 出入库
    picks = odoo.search_read(
        "stock.picking", [["sale_id", "=", so["id"]]],
        ["name", "picking_type_id", "state", "scheduled_date", "date_done"],
        order="id",
    )
    if not picks:
        picks = odoo.search_read(
            "stock.picking", [["origin", "=", so["name"]]],
            ["name", "picking_type_id", "state", "scheduled_date", "date_done"],
            order="id",
        )
    print("\n── 发货 ──")
    if picks:
        rows = [[p["name"], m2o_name(p["picking_type_id"]),
                 label(PICKING_STATE, p["state"]),
                 from_utc(p["scheduled_date"], "%m-%d") if p.get("scheduled_date") else "",
                 from_utc(p["date_done"], "%m-%d %H:%M") if p.get("date_done") else ""]
                for p in picks]
        print(render_table(rows, ["单据", "作业类型", "状态", "计划", "完成"]))
    else:
        print("（无出入库单）")

    # 质检（挂在制造单或出入库单上；状态字段是 quality_state 不是 state）
    qc_domain = ["|",
                 ["production_id", "in", [m["id"] for m in mos] or [0]],
                 ["picking_id", "in", [p["id"] for p in picks] or [0]]]
    checks = odoo.search_read(
        "quality.check", qc_domain,
        ["name", "title", "product_id", "quality_state", "control_date", "user_id"],
        order="id",
    )
    if checks:
        rows = [[c["name"], c.get("title") or "", m2o_name(c["product_id"]),
                 label(QC_STATE, c["quality_state"]),
                 from_utc(c["control_date"], "%m-%d") if c.get("control_date") else "",
                 m2o_name(c.get("user_id"))]
                for c in checks]
        print("\n── 质检 ──")
        print(render_table(rows, ["质检单", "项目", "产品", "结果", "日期", "责任人"]))


def cmd_status(args):
    odoo = Odoo()
    orders = _find_orders(odoo, args.keyword)
    if not orders:
        print(f"未找到订单或客户：{args.keyword}")
        return
    if len(orders) == 1:
        _print_status(odoo, orders[0])
        return
    # 多张：第一张全量展开，其余给摘要
    _print_status(odoo, orders[0])
    print(f"\n（该关键词共匹配 {len(orders)} 张订单，其余：）")
    rows = [[o["name"], m2o_name(o["partner_id"]), label(SO_STATE, o["state"]),
             label(DELIVERY_STATUS, o.get("delivery_status")), money(o["amount_total"]),
             from_utc(o["date_order"], "%Y-%m-%d")]
            for o in orders[1:]]
    print(render_table(rows, ["订单", "客户", "状态", "发货", "金额", "下单日期"]))


def cmd_list(args):
    odoo = Odoo()
    domain = [["state", "in", ["sale", "done"]]]
    if args.days:
        domain.append(["date_order", ">=", days_ago_utc(args.days)])
    if args.undelivered:
        domain.append(["delivery_status", "in", ["pending", "started", "partial"]])
    if args.customer:
        partners = odoo.name_search("res.partner", args.customer, limit=10)
        if not partners:
            print(f"未找到客户：{args.customer}")
            return
        domain.append(["partner_id", "in", [p[0] for p in partners]])
    orders = odoo.search_read(
        "sale.order", domain,
        ["name", "partner_id", "date_order", "commitment_date", "delivery_status",
         "amount_total", "x_follower_user_id"],
        limit=args.limit, order="date_order desc",
    )
    rows = [[o["name"], m2o_name(o["partner_id"]),
             from_utc(o["date_order"], "%m-%d"),
             from_utc(o["commitment_date"], "%m-%d") if o.get("commitment_date") else "",
             label(DELIVERY_STATUS, o.get("delivery_status")),
             money(o["amount_total"]), m2o_name(o.get("x_follower_user_id"))]
            for o in orders]
    title = "未发完订单" if args.undelivered else f"最近 {args.days} 天订单"
    print(f"📦 {title}（{len(orders)} 张）\n")
    print(render_table(rows, ["订单", "客户", "下单", "交期", "发货状态", "金额", "跟单"]))


def cmd_channels(args):
    odoo = Odoo()
    base = [["state", "in", ["sale", "done"]],
            ["date_order", ">=", days_ago_utc(args.days)]]

    def agg(extra):
        g = odoo.read_group("sale.order", base + extra, ["amount_total"], [], lazy=False)
        n = g[0].get("__count", 0) if g else 0
        return n, (g[0].get("amount_total", 0) if (g and n) else 0)

    n_ecom, amt_ecom = agg([["x_source_order_ref", "!=", False]])
    n_direct, amt_direct = agg([["x_source_order_ref", "=", False]])
    total_n = n_ecom + n_direct
    print(f"🛒 最近 {args.days} 天渠道来源（确认订单 {total_n} 张）\n")
    rows = [
        ["电商平台（带来源单号）", n_ecom,
         f"{n_ecom / total_n * 100:.0f}%" if total_n else "-", money(amt_ecom)],
        ["直营/经销（无来源单号）", n_direct,
         f"{n_direct / total_n * 100:.0f}%" if total_n else "-", money(amt_direct)],
    ]
    print(render_table(rows, ["渠道", "单数", "占比", "金额"]))

    # 平台单号前缀分布（同前缀≈同平台，如 69 开头为抖音系单号）
    refs = odoo.search_read("sale.order", base + [["x_source_order_ref", "!=", False]],
                            ["x_source_order_ref"], limit=1000)
    if refs:
        from collections import Counter
        c = Counter((r["x_source_order_ref"] or "")[:2] for r in refs)
        dist = " · ".join(f"{k}xx:{v}单" for k, v in c.most_common(6))
        print(f"\n平台单号前缀分布：{dist}")
        print("（同前缀基本同平台；69 开头为抖音系格式。接小红书/抖音店铺连接器后可精确到平台。）")


def build_parser():
    p = argparse.ArgumentParser(description="销售订单跟踪")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="订单全链路状态穿透")
    s.add_argument("keyword", help="订单号或客户名")

    l = sub.add_parser("list", help="订单列表")
    l.add_argument("--days", type=int, default=30)
    l.add_argument("--undelivered", action="store_true", help="只看未发完的")
    l.add_argument("--customer", help="按客户筛选")
    l.add_argument("--limit", type=int, default=30)

    c = sub.add_parser("channels", help="渠道来源统计")
    c.add_argument("--days", type=int, default=30)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "status":
            cmd_status(args)
        elif args.cmd == "list":
            cmd_list(args)
        elif args.cmd == "channels":
            cmd_channels(args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
