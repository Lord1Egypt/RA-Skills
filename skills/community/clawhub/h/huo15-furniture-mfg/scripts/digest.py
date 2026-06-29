#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
digest.py — 晨报 / 风险预警（P2，配合 OpenClaw 原生 cron 定时推送）

命令
  morning                    晨报：昨日成绩单 + 今日应交 + 风险快照 + 延期TOP
  alerts [--quiet-if-clean]  风险预警：延期 / 采购逾期 / 缺料 / 待检积压
                             --quiet-if-clean 时无风险则不输出（cron 静默跳过）

输出为企微友好纯文本；中文 1 字 = 3 字节，企微 text 限 2048 字节，
本脚本输出已控制在安全长度内，可整段直接作为一条消息发送。

示例
  python3 digest.py morning
  python3 digest.py alerts --quiet-if-clean
"""

from __future__ import annotations

import argparse
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import day_range_utc, from_utc, m2o_name, money, now_utc, qty

WIP_STATES = ["confirmed", "progress", "to_close"]


def _risk_counts(odoo: Odoo) -> dict:
    now = now_utc()
    return {
        "wip": odoo.search_count("mrp.production", [["state", "in", WIP_STATES]]),
        "late": odoo.search_count(
            "mrp.production",
            [["state", "in", WIP_STATES], ["date_deadline", "<", now]]),
        "short": odoo.search_count(
            "mrp.production",
            [["state", "in", WIP_STATES],
             ["components_availability_state", "in", ["late", "unavailable"]]]),
        "po_overdue": odoo.search_count(
            "purchase.order",
            [["state", "=", "purchase"], ["receipt_status", "in", ["pending", "partial"]],
             ["date_planned", "<", now]]),
        "qc_todo": odoo.search_count("quality.check", [["quality_state", "=", "none"]]),
    }


def cmd_morning(args):
    odoo = Odoo()
    lines = [f"📊 制造晨报 · {from_utc(day_range_utc(0)[0], '%m月%d日')}"]

    # 昨日成绩单
    ys, ye = day_range_utc(-1)
    so = odoo.read_group("sale.order",
                         [["date_order", ">=", ys], ["date_order", "<=", ye],
                          ["state", "in", ["sale", "done"]]],
                         ["amount_total"], [], lazy=False)
    n_so = so[0].get("__count", 0) if so else 0
    amt = so[0].get("amount_total", 0) if (so and n_so) else 0
    n_done = odoo.search_count("mrp.production",
                               [["date_finished", ">=", ys], ["date_finished", "<=", ye],
                                ["state", "=", "done"]])
    n_ship = odoo.search_count("stock.picking",
                               [["date_done", ">=", ys], ["date_done", "<=", ye],
                                ["state", "=", "done"], ["picking_type_id.code", "=", "outgoing"]])
    qc = odoo.read_group("quality.check",
                         [["control_date", ">=", ys], ["control_date", "<=", ye],
                          ["quality_state", "in", ["pass", "fail"]]],
                         [], ["quality_state"], lazy=False)
    qmap = {g["quality_state"]: g.get("__count", 0) for g in qc}
    lines.append(f"昨日：接单 {n_so} 张/{money(amt)} · 完工 {n_done} 张 · 发货 {n_ship} 单"
                 f" · 质检 合格{qmap.get('pass', 0)}/不合格{qmap.get('fail', 0)}")

    # 今日应交未发
    ts, te = day_range_utc(0)
    due = odoo.search_read(
        "sale.order",
        [["commitment_date", ">=", ts], ["commitment_date", "<=", te],
         ["state", "=", "sale"],
         ["delivery_status", "in", ["pending", "started", "partial"]]],
        ["name", "partner_id", "x_follower_user_id"], limit=6)
    if due:
        lines.append(f"📅 今日应交未发 {len(due)} 张：")
        for o in due[:5]:
            follow = m2o_name(o.get("x_follower_user_id"))
            lines.append(f"  · {o['name']} {m2o_name(o['partner_id'])}"
                         + (f"（跟单 {follow}）" if follow else ""))
        if len(due) > 5:
            lines.append(f"  …等共 {len(due)} 张")
    else:
        lines.append("📅 今日无应交未发订单")

    # 风险快照 + 延期 TOP3
    r = _risk_counts(odoo)
    lines.append(f"⚠️ 风险：在制 {r['wip']} | 延期 {r['late']} | 缺料 {r['short']}"
                 f" | 采购逾期 {r['po_overdue']} | 待检 {r['qc_todo']}")
    if r["late"]:
        top = odoo.search_read(
            "mrp.production",
            [["state", "in", WIP_STATES], ["date_deadline", "<", now_utc()]],
            ["name", "product_id", "product_qty", "date_deadline"],
            limit=3, order="date_deadline asc")
        lines.append("延期最久：")
        for m in top:
            lines.append(f"  · {m['name']} {m2o_name(m['product_id'])}×{qty(m['product_qty'])}"
                         f"（截止 {from_utc(m['date_deadline'], '%m-%d')}）")
    print("\n".join(lines))


def cmd_alerts(args):
    odoo = Odoo()
    r = _risk_counts(odoo)
    issues = []
    if r["late"]:
        top = odoo.search_read(
            "mrp.production",
            [["state", "in", WIP_STATES], ["date_deadline", "<", now_utc()]],
            ["name", "date_deadline"], limit=1, order="date_deadline asc")[0]
        issues.append(f"· 延期制造单 {r['late']} 张（最久 {top['name']}，"
                      f"{from_utc(top['date_deadline'], '%m-%d')} 截止）")
    if r["po_overdue"]:
        top = odoo.search_read(
            "purchase.order",
            [["state", "=", "purchase"], ["receipt_status", "in", ["pending", "partial"]],
             ["date_planned", "<", now_utc()]],
            ["name", "partner_id", "date_planned"], limit=1, order="date_planned asc")[0]
        issues.append(f"· 采购逾期 {r['po_overdue']} 张（最久 {top['name']} "
                      f"{m2o_name(top['partner_id'])}，{from_utc(top['date_planned'], '%m-%d')} 应到）")
    if r["short"]:
        issues.append(f"· 缺料阻塞在制单 {r['short']} 张")
    if r["qc_todo"] >= args.qc_backlog:
        issues.append(f"· 待检积压 {r['qc_todo']} 张（阈值 {args.qc_backlog}）")

    if not issues:
        if not args.quiet_if_clean:
            print("✅ 当前无延期 / 逾期 / 缺料 / 待检积压风险。")
        return
    print("⚠️ 制造风险预警")
    print("\n".join(issues))
    print("回复「延期明细」「采购逾期」可看完整清单。")


def build_parser():
    p = argparse.ArgumentParser(description="晨报 / 风险预警")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("morning", help="晨报")
    a = sub.add_parser("alerts", help="风险预警")
    a.add_argument("--quiet-if-clean", action="store_true",
                   help="无风险时不输出（cron 用）")
    a.add_argument("--qc-backlog", type=int, default=50,
                   help="待检积压报警阈值（默认 50）")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"morning": cmd_morning, "alerts": cmd_alerts}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
