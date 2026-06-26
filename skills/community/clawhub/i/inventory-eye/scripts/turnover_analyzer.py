#!/usr/bin/env python3
"""
inventory-eye 库存周转率与滞销分析模块（付费功能）

提供库存周转率计算、滞销品识别、库存分析报告生成等功能。
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    check_subscription, require_paid, format_number, format_percentage,
    format_chinese_unit, days_until_expiry,
    load_inventory, load_transactions, read_json_input,
    output_json, output_error, output_success,
)


# ============================================================
# 周转率计算
# ============================================================

def _calculate_turnover(skus: List[Dict], transactions: List[Dict], days: int) -> List[Dict[str, Any]]:
    """计算每个 SKU 的周转率。

    周转率 = 期间出库成本 / 平均库存成本
    周转天数 = 期间天数 / 周转率

    Args:
        skus: SKU 列表。
        transactions: 交易记录列表。
        days: 分析周期天数。

    Returns:
        每个 SKU 的周转率数据列表。
    """
    cutoff = (date.today() - timedelta(days=days)).isoformat()

    results = []
    for s in skus:
        sku_id = s["sku_id"]
        unit_cost = s.get("unit_cost", 0)
        current_qty = s.get("quantity", 0)

        # 统计期间出库量
        outbound_txs = [
            t for t in transactions
            if t.get("type") == "outbound"
            and t.get("sku_id") == sku_id
            and t.get("timestamp", "") >= cutoff
        ]
        total_outbound = sum(t.get("quantity", 0) for t in outbound_txs)

        # 统计期间入库量
        inbound_txs = [
            t for t in transactions
            if t.get("type") == "inbound"
            and t.get("sku_id") == sku_id
            and t.get("timestamp", "") >= cutoff
        ]
        total_inbound = sum(t.get("quantity", 0) for t in inbound_txs)

        # 估算期初库存 = 当前库存 + 期间出库 - 期间入库
        beginning_qty = current_qty + total_outbound - total_inbound
        beginning_qty = max(0, beginning_qty)

        # 平均库存
        avg_qty = (beginning_qty + current_qty) / 2.0
        avg_inventory_cost = avg_qty * unit_cost

        # COGS（期间出库成本）
        cogs = total_outbound * unit_cost

        # 周转率
        turnover_rate = 0.0
        turnover_days = float("inf")
        if avg_inventory_cost > 0:
            turnover_rate = cogs / avg_inventory_cost
            if turnover_rate > 0:
                turnover_days = days / turnover_rate

        # 日均销售
        daily_avg = total_outbound / days if days > 0 else 0

        results.append({
            "sku_id": sku_id,
            "name": s.get("name", ""),
            "category": s.get("category", ""),
            "warehouse": s.get("warehouse", ""),
            "current_quantity": current_qty,
            "unit_cost": unit_cost,
            "period_outbound": total_outbound,
            "period_inbound": total_inbound,
            "cogs": round(cogs, 2),
            "avg_inventory_cost": round(avg_inventory_cost, 2),
            "turnover_rate": round(turnover_rate, 2),
            "turnover_days": round(turnover_days, 1) if turnover_days != float("inf") else None,
            "daily_avg_sales": round(daily_avg, 2),
        })

    # 按周转率排序（低周转在前，更需关注）
    results.sort(key=lambda x: x["turnover_rate"])
    return results


def action_turnover(args) -> None:
    """计算库存周转率。"""
    require_paid("库存周转分析")

    inventory = load_inventory()
    skus = inventory["skus"]
    transactions = load_transactions()

    data = read_json_input(args)
    days = 30
    if data and data.get("days"):
        days = int(data["days"])

    if not skus:
        output_success({"action": "turnover", "message": "库存为空", "items": []})
        return

    results = _calculate_turnover(skus, transactions, days)

    # 汇总统计
    total_cogs = sum(r["cogs"] for r in results)
    total_avg_inv = sum(r["avg_inventory_cost"] for r in results)
    overall_turnover = total_cogs / total_avg_inv if total_avg_inv > 0 else 0
    overall_days = days / overall_turnover if overall_turnover > 0 else None

    output_success({
        "action": "turnover",
        "period_days": days,
        "total_skus": len(results),
        "overall": {
            "total_cogs": round(total_cogs, 2),
            "total_avg_inventory": round(total_avg_inv, 2),
            "turnover_rate": round(overall_turnover, 2),
            "turnover_days": round(overall_days, 1) if overall_days else None,
        },
        "items": results,
    })


# ============================================================
# 滞销品分析
# ============================================================

def action_slow_moving(args) -> None:
    """识别滞销商品。"""
    require_paid("滞销品识别")

    inventory = load_inventory()
    skus = inventory["skus"]
    transactions = load_transactions()

    data = read_json_input(args)
    threshold_days = 30  # 默认30天无出库即为滞销
    if data and data.get("days"):
        threshold_days = int(data["days"])

    today = date.today()
    slow_items = []

    for s in skus:
        sku_id = s["sku_id"]
        qty = s.get("quantity", 0)

        if qty == 0:
            continue  # 无库存的不算滞销

        # 查找最近一次出库时间
        outbound_txs = [
            t for t in transactions
            if t.get("type") == "outbound" and t.get("sku_id") == sku_id
        ]
        outbound_txs.sort(key=lambda t: t.get("timestamp", ""), reverse=True)

        if outbound_txs:
            last_outbound_str = outbound_txs[0].get("timestamp", "")[:10]
            try:
                last_outbound = datetime.strptime(last_outbound_str, "%Y-%m-%d").date()
                idle_days = (today - last_outbound).days
            except ValueError:
                idle_days = threshold_days + 1
        else:
            # 从未出库过，使用入库日期或创建日期
            last_date_str = s.get("last_inbound_date") or s.get("created_at", "")[:10]
            try:
                last_dt = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                idle_days = (today - last_dt).days
            except ValueError:
                idle_days = threshold_days + 1

        if idle_days >= threshold_days:
            stock_value = qty * s.get("unit_cost", 0)
            retail_value = qty * s.get("selling_price", 0)

            suggestion = "建议促销清仓"
            if idle_days >= 90:
                suggestion = "严重滞销，建议大幅折扣或退回供应商"
            elif idle_days >= 60:
                suggestion = "中度滞销，建议打折促销"
            elif idle_days >= 30:
                suggestion = "轻度滞销，建议搭配销售或促销"

            slow_items.append({
                "sku_id": sku_id,
                "name": s.get("name", ""),
                "category": s.get("category", ""),
                "warehouse": s.get("warehouse", ""),
                "quantity": qty,
                "unit_cost": s.get("unit_cost", 0),
                "stock_value": round(stock_value, 2),
                "retail_value": round(retail_value, 2),
                "idle_days": idle_days,
                "last_outbound": outbound_txs[0].get("timestamp", "")[:10] if outbound_txs else "无记录",
                "suggestion": suggestion,
            })

    # 按滞销天数排序（最严重的在前）
    slow_items.sort(key=lambda x: x["idle_days"], reverse=True)

    total_frozen_value = sum(i["stock_value"] for i in slow_items)

    output_success({
        "action": "slow_moving",
        "threshold_days": threshold_days,
        "total": len(slow_items),
        "total_frozen_value": round(total_frozen_value, 2),
        "items": slow_items,
    })


# ============================================================
# 综合报告
# ============================================================

def action_report(args) -> None:
    """生成库存周转分析报告（Markdown 格式）。"""
    require_paid("库存周转分析报告")

    inventory = load_inventory()
    skus = inventory["skus"]
    transactions = load_transactions()

    data = read_json_input(args)
    days = 30
    if data and data.get("days"):
        days = int(data["days"])

    if not skus:
        output_success({"action": "report", "message": "库存为空", "report": ""})
        return

    turnover_data = _calculate_turnover(skus, transactions, days)

    # 汇总
    total_cogs = sum(r["cogs"] for r in turnover_data)
    total_avg_inv = sum(r["avg_inventory_cost"] for r in turnover_data)
    overall_rate = total_cogs / total_avg_inv if total_avg_inv > 0 else 0
    overall_days_val = days / overall_rate if overall_rate > 0 else None

    # 按分类汇总周转率
    cat_data: Dict[str, Dict[str, float]] = {}
    for r in turnover_data:
        cat = r.get("category", "未分类")
        if cat not in cat_data:
            cat_data[cat] = {"cogs": 0, "avg_inv": 0, "count": 0}
        cat_data[cat]["cogs"] += r["cogs"]
        cat_data[cat]["avg_inv"] += r["avg_inventory_cost"]
        cat_data[cat]["count"] += 1

    # 构建 Markdown 报告
    report_lines = [
        f"# 库存周转分析报告",
        f"",
        f"**分析周期**: 近 {days} 天 | **报告日期**: {date.today().isoformat()}",
        f"",
        f"---",
        f"",
        f"## 整体概况",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| SKU 总数 | {len(skus)} |",
        f"| 期间总出库成本 | ¥{format_number(total_cogs)} |",
        f"| 平均库存成本 | ¥{format_number(total_avg_inv)} |",
        f"| 整体周转率 | {overall_rate:.2f} 次 |",
        f"| 整体周转天数 | {f'{overall_days_val:.1f} 天' if overall_days_val else 'N/A'} |",
        f"",
    ]

    # 分类周转率表格
    report_lines.extend([
        f"## 分类周转率",
        f"",
        f"| 分类 | SKU数 | 出库成本 | 平均库存 | 周转率 |",
        f"|------|-------|---------|---------|--------|",
    ])
    for cat, cd in sorted(cat_data.items(), key=lambda x: x[1]["cogs"], reverse=True):
        cat_rate = cd["cogs"] / cd["avg_inv"] if cd["avg_inv"] > 0 else 0
        report_lines.append(
            f"| {cat} | {cd['count']} | ¥{format_number(cd['cogs'])} | ¥{format_number(cd['avg_inv'])} | {cat_rate:.2f} |"
        )

    # Mermaid 分类周转率图表
    report_lines.extend([
        f"",
        f"## 分类周转率图表",
        f"",
        f"```mermaid",
        f"xychart-beta",
        f'  title "各分类周转率（近{days}天）"',
        f"  x-axis [{', '.join(json.dumps(c, ensure_ascii=False) for c in cat_data.keys())}]",
        f"  y-axis \"周转率（次）\"",
        "  bar [{}]".format(", ".join("{:.2f}".format(cd["cogs"] / cd["avg_inv"] if cd["avg_inv"] > 0 else 0) for cd in cat_data.values())),
        f"```",
        f"",
    ])

    # Top 10 高周转 SKU
    high_turnover = sorted(turnover_data, key=lambda x: x["turnover_rate"], reverse=True)[:10]
    report_lines.extend([
        f"## Top 10 高周转 SKU",
        f"",
        f"| 排名 | SKU | 名称 | 周转率 | 日均销量 |",
        f"|------|-----|------|--------|---------|",
    ])
    for i, r in enumerate(high_turnover, 1):
        report_lines.append(
            f"| {i} | {r['sku_id']} | {r['name']} | {r['turnover_rate']:.2f} | {r['daily_avg_sales']:.1f} |"
        )

    # Top 10 低周转 SKU
    low_turnover = [r for r in turnover_data if r["current_quantity"] > 0][:10]
    report_lines.extend([
        f"",
        f"## Top 10 低周转 SKU（需关注）",
        f"",
        f"| 排名 | SKU | 名称 | 周转率 | 库存量 | 库存金额 |",
        f"|------|-----|------|--------|--------|---------|",
    ])
    for i, r in enumerate(low_turnover, 1):
        stock_val = r["current_quantity"] * r["unit_cost"]
        report_lines.append(
            f"| {i} | {r['sku_id']} | {r['name']} | {r['turnover_rate']:.2f} | {r['current_quantity']} | ¥{format_number(stock_val)} |"
        )

    report_lines.extend([
        f"",
        f"---",
        f"",
        f"> 📊 由 库存慧眼（inventory-eye）自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ])

    report = "\n".join(report_lines)

    output_success({
        "action": "report",
        "period_days": days,
        "report": report,
    })


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="库存慧眼 — 周转率与滞销分析（付费功能）",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["turnover", "slow-moving", "report"],
        help="分析操作类型",
    )
    parser.add_argument("--data", default=None, help="JSON 格式的参数")
    parser.add_argument("--data-file", default=None, help="JSON 参数文件路径")
    parser.add_argument("--days", type=int, default=30, help="分析周期天数（默认30天）")

    args = parser.parse_args()

    # 将 --days 参数合并到 data 中
    if args.days != 30:
        if not args.data:
            args.data = json.dumps({"days": args.days})
        else:
            try:
                d = json.loads(args.data)
                d["days"] = args.days
                args.data = json.dumps(d)
            except json.JSONDecodeError:
                pass

    action_map = {
        "turnover": action_turnover,
        "slow-moving": action_slow_moving,
        "report": action_report,
    }

    try:
        action_map[args.action](args)
    except SystemExit:
        pass
    except Exception as e:
        output_error(f"分析操作失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
