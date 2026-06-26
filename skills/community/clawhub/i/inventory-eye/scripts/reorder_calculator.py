#!/usr/bin/env python3
"""
inventory-eye 补货量计算模块（付费功能）

根据历史销售数据计算最优补货量，提供智能补货建议。
补货公式: reorder_qty = (daily_avg_sales × lead_time × safety_factor) - current_stock
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
    check_subscription, require_paid, format_number,
    load_inventory, load_transactions, read_json_input,
    output_json, output_error, output_success,
)


# ============================================================
# 默认参数
# ============================================================

DEFAULT_LEAD_TIME = 7          # 默认供货周期（天）
DEFAULT_SAFETY_FACTOR = 1.5    # 默认安全系数
DEFAULT_ANALYSIS_DAYS = 30     # 默认分析天数
MIN_REORDER_QTY = 1            # 最小补货量


# ============================================================
# 补货计算
# ============================================================

def _calc_daily_avg_sales(sku_id: str, transactions: List[Dict], days: int) -> float:
    """计算指定 SKU 的日均销售量。

    Args:
        sku_id: SKU 编码。
        transactions: 交易记录列表。
        days: 分析天数。

    Returns:
        日均销售量。
    """
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    outbound = [
        t for t in transactions
        if t.get("type") == "outbound"
        and t.get("sku_id") == sku_id
        and t.get("timestamp", "") >= cutoff
    ]
    total = sum(t.get("quantity", 0) for t in outbound)
    return total / days if days > 0 else 0


def _calculate_reorder(
    sku: Dict[str, Any],
    transactions: List[Dict],
    lead_time: int = DEFAULT_LEAD_TIME,
    safety_factor: float = DEFAULT_SAFETY_FACTOR,
    analysis_days: int = DEFAULT_ANALYSIS_DAYS,
) -> Optional[Dict[str, Any]]:
    """计算单个 SKU 的补货建议。

    公式: reorder_qty = (daily_avg_sales × lead_time × safety_factor) - current_stock

    Args:
        sku: SKU 数据。
        transactions: 交易记录。
        lead_time: 供货周期天数。
        safety_factor: 安全系数。
        analysis_days: 历史分析天数。

    Returns:
        补货建议字典，若无需补货返回 None。
    """
    sku_id = sku["sku_id"]
    current_stock = sku.get("quantity", 0)
    safety_stock = sku.get("safety_stock", 0)
    unit_cost = sku.get("unit_cost", 0)

    daily_avg = _calc_daily_avg_sales(sku_id, transactions, analysis_days)

    # 需求量 = 日均 × 供货周期 × 安全系数
    demand = daily_avg * lead_time * safety_factor

    # 补货量 = 需求量 - 当前库存
    reorder_qty = math.ceil(demand - current_stock)

    # 如果也低于安全库存，取较大值
    safety_deficit = safety_stock - current_stock
    if safety_deficit > reorder_qty:
        reorder_qty = safety_deficit

    if reorder_qty < MIN_REORDER_QTY:
        return None  # 不需要补货

    # 预计可售天数
    days_remaining = current_stock / daily_avg if daily_avg > 0 else float("inf")

    # 紧急程度
    urgency = "normal"
    if current_stock == 0:
        urgency = "critical"
    elif days_remaining <= lead_time:
        urgency = "urgent"
    elif current_stock <= safety_stock:
        urgency = "warning"

    return {
        "sku_id": sku_id,
        "name": sku.get("name", ""),
        "category": sku.get("category", ""),
        "warehouse": sku.get("warehouse", ""),
        "current_stock": current_stock,
        "safety_stock": safety_stock,
        "daily_avg_sales": round(daily_avg, 2),
        "lead_time": lead_time,
        "safety_factor": safety_factor,
        "reorder_qty": reorder_qty,
        "reorder_cost": round(reorder_qty * unit_cost, 2),
        "unit_cost": unit_cost,
        "days_remaining": round(days_remaining, 1) if days_remaining != float("inf") else None,
        "urgency": urgency,
    }


def action_calculate(args) -> None:
    """计算所有需要补货的 SKU。"""
    require_paid("AI补货计算")

    inventory = load_inventory()
    skus = inventory["skus"]
    transactions = load_transactions()

    data = read_json_input(args)
    lead_time = DEFAULT_LEAD_TIME
    safety_factor = DEFAULT_SAFETY_FACTOR
    analysis_days = DEFAULT_ANALYSIS_DAYS

    if data:
        lead_time = int(data.get("lead_time", lead_time))
        safety_factor = float(data.get("safety_factor", safety_factor))
        analysis_days = int(data.get("days", analysis_days))

    if not skus:
        output_success({"action": "calculate", "message": "库存为空", "items": []})
        return

    reorder_items = []
    for sku in skus:
        result = _calculate_reorder(sku, transactions, lead_time, safety_factor, analysis_days)
        if result:
            reorder_items.append(result)

    # 按紧急程度排序
    urgency_order = {"critical": 0, "urgent": 1, "warning": 2, "normal": 3}
    reorder_items.sort(key=lambda x: (urgency_order.get(x["urgency"], 9), -x["reorder_qty"]))

    total_cost = sum(i["reorder_cost"] for i in reorder_items)

    output_success({
        "action": "calculate",
        "parameters": {
            "lead_time": lead_time,
            "safety_factor": safety_factor,
            "analysis_days": analysis_days,
        },
        "total_items": len(reorder_items),
        "total_reorder_cost": round(total_cost, 2),
        "critical": len([i for i in reorder_items if i["urgency"] == "critical"]),
        "urgent": len([i for i in reorder_items if i["urgency"] == "urgent"]),
        "warning": len([i for i in reorder_items if i["urgency"] == "warning"]),
        "items": reorder_items,
    })


def action_suggest(args) -> None:
    """为指定 SKU 生成详细补货建议。"""
    require_paid("AI补货建议")

    data = read_json_input(args)
    if not data or not data.get("sku_id"):
        output_error("请通过 --data 提供 sku_id", "MISSING_DATA")
        return

    from utils import format_sku
    sku_id = format_sku(data["sku_id"])

    inventory = load_inventory()
    transactions = load_transactions()

    target_sku = None
    for s in inventory["skus"]:
        if s["sku_id"] == sku_id:
            target_sku = s
            break

    if not target_sku:
        output_error(f"未找到 SKU: {sku_id}", "SKU_NOT_FOUND")
        return

    lead_time = int(data.get("lead_time", DEFAULT_LEAD_TIME))
    safety_factor = float(data.get("safety_factor", DEFAULT_SAFETY_FACTOR))

    # 多周期分析
    suggestions = []
    for period in [7, 14, 30, 60, 90]:
        daily_avg = _calc_daily_avg_sales(sku_id, transactions, period)
        demand = daily_avg * lead_time * safety_factor
        reorder = math.ceil(max(demand - target_sku.get("quantity", 0), 0))
        suggestions.append({
            "analysis_period": f"近{period}天",
            "daily_avg_sales": round(daily_avg, 2),
            "suggested_reorder": reorder,
            "reorder_cost": round(reorder * target_sku.get("unit_cost", 0), 2),
        })

    # 推荐值取30天的
    recommended = _calculate_reorder(target_sku, transactions, lead_time, safety_factor, 30)

    output_success({
        "action": "suggest",
        "sku": {
            "sku_id": target_sku["sku_id"],
            "name": target_sku.get("name", ""),
            "current_stock": target_sku.get("quantity", 0),
            "safety_stock": target_sku.get("safety_stock", 0),
            "unit_cost": target_sku.get("unit_cost", 0),
        },
        "parameters": {
            "lead_time": lead_time,
            "safety_factor": safety_factor,
        },
        "multi_period_analysis": suggestions,
        "recommended": recommended,
    })


def action_report(args) -> None:
    """生成补货建议报告（Markdown 格式）。"""
    require_paid("补货建议报告")

    inventory = load_inventory()
    skus = inventory["skus"]
    transactions = load_transactions()

    data = read_json_input(args)
    lead_time = DEFAULT_LEAD_TIME
    safety_factor = DEFAULT_SAFETY_FACTOR

    if data:
        lead_time = int(data.get("lead_time", lead_time))
        safety_factor = float(data.get("safety_factor", safety_factor))

    if not skus:
        output_success({"action": "report", "report": "库存为空，无数据可生成报告。"})
        return

    # 计算所有补货建议
    reorder_items = []
    for sku in skus:
        result = _calculate_reorder(sku, transactions, lead_time, safety_factor, DEFAULT_ANALYSIS_DAYS)
        if result:
            reorder_items.append(result)

    urgency_order = {"critical": 0, "urgent": 1, "warning": 2, "normal": 3}
    reorder_items.sort(key=lambda x: (urgency_order.get(x["urgency"], 9), -x["reorder_qty"]))

    total_cost = sum(i["reorder_cost"] for i in reorder_items)

    # 按紧急程度分组
    critical = [i for i in reorder_items if i["urgency"] == "critical"]
    urgent = [i for i in reorder_items if i["urgency"] == "urgent"]
    warning = [i for i in reorder_items if i["urgency"] == "warning"]
    normal = [i for i in reorder_items if i["urgency"] == "normal"]

    urgency_labels = {"critical": "🔴 缺货", "urgent": "🟠 紧急", "warning": "🟡 预警", "normal": "🟢 正常"}

    lines = [
        f"# 补货建议报告",
        f"",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} | **供货周期**: {lead_time}天 | **安全系数**: {safety_factor}",
        f"",
        f"---",
        f"",
        f"## 概况",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 需补货SKU数 | {len(reorder_items)} |",
        f"| 缺货（critical） | {len(critical)} |",
        f"| 紧急（urgent） | {len(urgent)} |",
        f"| 预警（warning） | {len(warning)} |",
        f"| 一般（normal） | {len(normal)} |",
        f"| 预计补货总成本 | ¥{format_number(total_cost)} |",
        f"",
    ]

    # Mermaid 紧急程度分布
    lines.extend([
        f"## 紧急程度分布",
        f"",
        f"```mermaid",
        f"pie title 补货紧急程度分布",
        f'  "缺货" : {len(critical)}',
        f'  "紧急" : {len(urgent)}',
        f'  "预警" : {len(warning)}',
        f'  "一般" : {len(normal)}',
        f"```",
        f"",
    ])

    # 补货清单
    lines.extend([
        f"## 补货清单",
        f"",
        f"| 紧急度 | SKU | 名称 | 当前库存 | 建议补货 | 补货成本 | 可售天数 |",
        f"|--------|-----|------|---------|---------|---------|---------|",
    ])

    for item in reorder_items:
        urgency_label = urgency_labels.get(item["urgency"], "")
        days_rem = f"{item['days_remaining']}天" if item["days_remaining"] is not None else "已断货"
        lines.append(
            f"| {urgency_label} | {item['sku_id']} | {item['name']} | "
            f"{item['current_stock']} | {item['reorder_qty']} | "
            f"¥{format_number(item['reorder_cost'])} | {days_rem} |"
        )

    lines.extend([
        f"",
        f"---",
        f"",
        f"### 计算说明",
        f"",
        f"- **补货公式**: 补货量 = (日均销量 × 供货周期 × 安全系数) - 当前库存",
        f"- **日均销量**: 基于近{DEFAULT_ANALYSIS_DAYS}天出库数据计算",
        f"- **供货周期**: {lead_time}天",
        f"- **安全系数**: {safety_factor}",
        f"",
        f"> 📦 由 库存慧眼（inventory-eye）自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ])

    report = "\n".join(lines)

    output_success({
        "action": "report",
        "total_items": len(reorder_items),
        "total_cost": round(total_cost, 2),
        "report": report,
    })


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="库存慧眼 — 补货量计算（付费功能）",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["calculate", "suggest", "report"],
        help="操作类型",
    )
    parser.add_argument("--data", default=None, help="JSON 格式的参数")
    parser.add_argument("--data-file", default=None, help="JSON 参数文件路径")

    args = parser.parse_args()

    try:
        action_map = {
            "calculate": action_calculate,
            "suggest": action_suggest,
            "report": action_report,
        }
        action_map[args.action](args)
    except SystemExit:
        pass
    except Exception as e:
        output_error(f"补货计算失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
