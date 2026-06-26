#!/usr/bin/env python3
"""
inventory-eye 库存监控与预警模块

提供库存水平监控、低库存预警、过期预警、库存概览等功能。
"""

import argparse
import json
import os
import sys
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    check_subscription, days_until_expiry, format_number, format_percentage,
    load_inventory, load_transactions, read_json_input,
    output_json, output_error, output_success,
)


# ============================================================
# 监控功能
# ============================================================

def action_check(args) -> None:
    """全面检查库存状态，返回综合报告。"""
    inventory = load_inventory()
    skus = inventory["skus"]
    sub = check_subscription()

    if not skus:
        output_success({
            "action": "check",
            "message": "库存为空，请先导入库存数据",
            "total_skus": 0,
        })
        return

    low_stock = []
    expiring = []
    out_of_stock = []
    healthy = []

    for s in skus:
        qty = s.get("quantity", 0)
        safety = s.get("safety_stock", 0)

        if qty == 0:
            out_of_stock.append(s)
        elif qty <= safety:
            low_stock.append(s)
        else:
            healthy.append(s)

        # 过期检查
        days_left = days_until_expiry(s.get("expiry_date"))
        if days_left is not None:
            if sub["tier"] == "paid":
                # 付费版：多级提醒（已过期、7天、30天、60天、90天）
                if days_left <= 0:
                    expiring.append({**s, "_expiry_status": "已过期", "_days_left": days_left})
                elif days_left <= 7:
                    expiring.append({**s, "_expiry_status": "即将过期（7天内）", "_days_left": days_left})
                elif days_left <= 30:
                    expiring.append({**s, "_expiry_status": "临近过期（30天内）", "_days_left": days_left})
                elif days_left <= 60:
                    expiring.append({**s, "_expiry_status": "注意（60天内）", "_days_left": days_left})
                elif days_left <= 90:
                    expiring.append({**s, "_expiry_status": "提醒（90天内）", "_days_left": days_left})
            else:
                # 免费版：基础提醒（已过期、30天内）
                if days_left <= 0:
                    expiring.append({**s, "_expiry_status": "已过期", "_days_left": days_left})
                elif days_left <= 30:
                    expiring.append({**s, "_expiry_status": "即将过期（30天内）", "_days_left": days_left})

    # 排序：过期最紧急的排前面
    expiring.sort(key=lambda x: x["_days_left"])

    total_value = sum(s.get("quantity", 0) * s.get("unit_cost", 0) for s in skus)
    total_retail = sum(s.get("quantity", 0) * s.get("selling_price", 0) for s in skus)

    output_success({
        "action": "check",
        "tier": sub["tier"],
        "summary": {
            "total_skus": len(skus),
            "total_quantity": sum(s.get("quantity", 0) for s in skus),
            "total_cost_value": round(total_value, 2),
            "total_retail_value": round(total_retail, 2),
            "out_of_stock_count": len(out_of_stock),
            "low_stock_count": len(low_stock),
            "expiring_count": len(expiring),
            "healthy_count": len(healthy),
        },
        "out_of_stock": [{"sku_id": s["sku_id"], "name": s["name"], "warehouse": s.get("warehouse", "")} for s in out_of_stock],
        "low_stock": [{
            "sku_id": s["sku_id"], "name": s["name"],
            "quantity": s["quantity"], "safety_stock": s.get("safety_stock", 0),
            "shortage": s.get("safety_stock", 0) - s["quantity"],
            "warehouse": s.get("warehouse", ""),
        } for s in low_stock],
        "expiring": [{
            "sku_id": s["sku_id"], "name": s["name"],
            "expiry_date": s.get("expiry_date", ""),
            "days_left": s["_days_left"],
            "status": s["_expiry_status"],
            "quantity": s.get("quantity", 0),
        } for s in expiring],
    })


def action_alerts(args) -> None:
    """获取所有预警信息汇总。"""
    inventory = load_inventory()
    skus = inventory["skus"]
    sub = check_subscription()

    alerts = []

    for s in skus:
        qty = s.get("quantity", 0)
        safety = s.get("safety_stock", 0)

        # 缺货预警
        if qty == 0:
            alerts.append({
                "level": "critical",
                "type": "out_of_stock",
                "message": f"【缺货】{s['name']}（{s['sku_id']}）库存为零",
                "sku_id": s["sku_id"],
                "name": s["name"],
            })
        elif qty <= safety:
            deficit = safety - qty
            alerts.append({
                "level": "warning",
                "type": "low_stock",
                "message": f"【低库存】{s['name']}（{s['sku_id']}）当前 {qty}，低于安全库存 {safety}，缺口 {deficit}",
                "sku_id": s["sku_id"],
                "name": s["name"],
                "quantity": qty,
                "safety_stock": safety,
            })

        # 过期预警
        days_left = days_until_expiry(s.get("expiry_date"))
        if days_left is not None:
            if days_left <= 0:
                alerts.append({
                    "level": "critical",
                    "type": "expired",
                    "message": f"【已过期】{s['name']}（{s['sku_id']}）已过期 {abs(days_left)} 天，库存 {qty}",
                    "sku_id": s["sku_id"],
                    "name": s["name"],
                    "days_left": days_left,
                })
            elif days_left <= 7:
                alerts.append({
                    "level": "critical",
                    "type": "expiring_soon",
                    "message": f"【即将过期】{s['name']}（{s['sku_id']}）{days_left}天后过期，库存 {qty}",
                    "sku_id": s["sku_id"],
                    "name": s["name"],
                    "days_left": days_left,
                })
            elif days_left <= 30:
                alerts.append({
                    "level": "warning",
                    "type": "expiring",
                    "message": f"【过期预警】{s['name']}（{s['sku_id']}）{days_left}天后过期，库存 {qty}",
                    "sku_id": s["sku_id"],
                    "name": s["name"],
                    "days_left": days_left,
                })
            elif sub["tier"] == "paid" and days_left <= 90:
                alerts.append({
                    "level": "info",
                    "type": "expiry_notice",
                    "message": f"【过期提醒】{s['name']}（{s['sku_id']}）{days_left}天后过期",
                    "sku_id": s["sku_id"],
                    "name": s["name"],
                    "days_left": days_left,
                })

    # 按严重程度排序
    level_order = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda a: level_order.get(a["level"], 9))

    output_success({
        "action": "alerts",
        "tier": sub["tier"],
        "total_alerts": len(alerts),
        "critical": len([a for a in alerts if a["level"] == "critical"]),
        "warning": len([a for a in alerts if a["level"] == "warning"]),
        "info": len([a for a in alerts if a["level"] == "info"]),
        "alerts": alerts,
    })


def action_low_stock(args) -> None:
    """获取低库存商品列表。"""
    inventory = load_inventory()
    skus = inventory["skus"]
    sub = check_subscription()

    low_stock_items = []
    for s in skus:
        qty = s.get("quantity", 0)
        safety = s.get("safety_stock", 0)

        if sub["tier"] == "paid":
            # 付费版：动态安全库存（根据近30天出库量计算）
            transactions = load_transactions()
            thirty_days_ago = (date.today() - timedelta(days=30)).isoformat()
            recent_outbound = [
                t for t in transactions
                if t.get("type") == "outbound"
                and t.get("sku_id") == s["sku_id"]
                and t.get("timestamp", "") >= thirty_days_ago
            ]
            total_outbound = sum(t.get("quantity", 0) for t in recent_outbound)
            daily_avg = total_outbound / 30.0 if total_outbound > 0 else 0
            dynamic_safety = max(safety, int(daily_avg * 7))  # 至少7天的用量

            if qty <= dynamic_safety:
                low_stock_items.append({
                    "sku_id": s["sku_id"],
                    "name": s["name"],
                    "category": s.get("category", ""),
                    "quantity": qty,
                    "safety_stock": safety,
                    "dynamic_safety_stock": dynamic_safety,
                    "daily_avg_sales": round(daily_avg, 1),
                    "shortage": dynamic_safety - qty,
                    "days_remaining": round(qty / daily_avg, 1) if daily_avg > 0 else float("inf"),
                    "warehouse": s.get("warehouse", ""),
                })
        else:
            # 免费版：固定阈值
            if qty <= safety:
                low_stock_items.append({
                    "sku_id": s["sku_id"],
                    "name": s["name"],
                    "category": s.get("category", ""),
                    "quantity": qty,
                    "safety_stock": safety,
                    "shortage": safety - qty,
                    "warehouse": s.get("warehouse", ""),
                })

    # 按缺口排序（缺口大的在前）
    low_stock_items.sort(key=lambda x: x.get("shortage", 0), reverse=True)

    output_success({
        "action": "low_stock",
        "tier": sub["tier"],
        "total": len(low_stock_items),
        "items": low_stock_items,
    })


def action_expiring(args) -> None:
    """获取即将过期商品列表。"""
    inventory = load_inventory()
    skus = inventory["skus"]
    sub = check_subscription()

    data = read_json_input(args)
    check_days = 30
    if data and data.get("days"):
        check_days = int(data["days"])

    expiring_items = []
    for s in skus:
        days_left = days_until_expiry(s.get("expiry_date"))
        if days_left is None:
            continue

        if days_left <= check_days:
            status = "正常"
            level = "info"
            if days_left <= 0:
                status = "已过期"
                level = "critical"
            elif days_left <= 7:
                status = "即将过期"
                level = "critical"
            elif days_left <= 30:
                status = "临近过期"
                level = "warning"
            elif days_left <= 60:
                status = "注意"
                level = "info"
            elif days_left <= 90:
                status = "提醒"
                level = "info"

            item = {
                "sku_id": s["sku_id"],
                "name": s["name"],
                "category": s.get("category", ""),
                "quantity": s.get("quantity", 0),
                "expiry_date": s.get("expiry_date", ""),
                "days_left": days_left,
                "status": status,
                "level": level,
                "warehouse": s.get("warehouse", ""),
                "stock_value": round(s.get("quantity", 0) * s.get("unit_cost", 0), 2),
            }
            expiring_items.append(item)

    expiring_items.sort(key=lambda x: x["days_left"])

    total_risk_value = sum(i["stock_value"] for i in expiring_items)

    output_success({
        "action": "expiring",
        "tier": sub["tier"],
        "check_days": check_days,
        "total": len(expiring_items),
        "total_risk_value": round(total_risk_value, 2),
        "items": expiring_items,
    })


def action_overview(args) -> None:
    """生成库存概览报告。"""
    inventory = load_inventory()
    skus = inventory["skus"]
    sub = check_subscription()

    if not skus:
        output_success({
            "action": "overview",
            "message": "库存为空",
            "total_skus": 0,
        })
        return

    total_qty = sum(s.get("quantity", 0) for s in skus)
    total_cost = sum(s.get("quantity", 0) * s.get("unit_cost", 0) for s in skus)
    total_retail = sum(s.get("quantity", 0) * s.get("selling_price", 0) for s in skus)

    # 按分类统计
    categories: Dict[str, Dict[str, Any]] = {}
    for s in skus:
        cat = s.get("category", "未分类")
        if cat not in categories:
            categories[cat] = {"count": 0, "quantity": 0, "cost_value": 0, "retail_value": 0}
        categories[cat]["count"] += 1
        categories[cat]["quantity"] += s.get("quantity", 0)
        categories[cat]["cost_value"] += s.get("quantity", 0) * s.get("unit_cost", 0)
        categories[cat]["retail_value"] += s.get("quantity", 0) * s.get("selling_price", 0)

    # 按仓库统计
    warehouses: Dict[str, Dict[str, Any]] = {}
    for s in skus:
        wh = s.get("warehouse", "默认仓库")
        if wh not in warehouses:
            warehouses[wh] = {"count": 0, "quantity": 0, "cost_value": 0}
        warehouses[wh]["count"] += 1
        warehouses[wh]["quantity"] += s.get("quantity", 0)
        warehouses[wh]["cost_value"] += s.get("quantity", 0) * s.get("unit_cost", 0)

    # 低库存数
    low_stock_count = sum(1 for s in skus if s.get("quantity", 0) <= s.get("safety_stock", 0))
    out_of_stock_count = sum(1 for s in skus if s.get("quantity", 0) == 0)

    # 过期统计
    expiring_30 = 0
    expired = 0
    for s in skus:
        dl = days_until_expiry(s.get("expiry_date"))
        if dl is not None:
            if dl <= 0:
                expired += 1
            elif dl <= 30:
                expiring_30 += 1

    # 四舍五入分类/仓库统计值
    for cat_data in categories.values():
        cat_data["cost_value"] = round(cat_data["cost_value"], 2)
        cat_data["retail_value"] = round(cat_data["retail_value"], 2)
    for wh_data in warehouses.values():
        wh_data["cost_value"] = round(wh_data["cost_value"], 2)

    overview = {
        "action": "overview",
        "tier": sub["tier"],
        "date": date.today().isoformat(),
        "summary": {
            "total_skus": len(skus),
            "total_quantity": total_qty,
            "total_cost_value": round(total_cost, 2),
            "total_retail_value": round(total_retail, 2),
            "potential_profit": round(total_retail - total_cost, 2),
            "out_of_stock": out_of_stock_count,
            "low_stock": low_stock_count,
            "expired": expired,
            "expiring_30_days": expiring_30,
        },
        "by_category": categories,
        "by_warehouse": warehouses,
        "sku_limit": f"{len(skus)}/{sub['max_skus']}",
        "warehouse_limit": f"{len(warehouses)}/{sub['max_warehouses']}",
    }

    output_success(overview)


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="库存慧眼 — 库存监控与预警",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["check", "alerts", "low-stock", "expiring", "overview"],
        help="监控操作类型",
    )
    parser.add_argument("--data", default=None, help="JSON 格式的参数")
    parser.add_argument("--data-file", default=None, help="JSON 参数文件路径")

    args = parser.parse_args()

    action_map = {
        "check": action_check,
        "alerts": action_alerts,
        "low-stock": action_low_stock,
        "expiring": action_expiring,
        "overview": action_overview,
    }

    try:
        action_map[args.action](args)
    except Exception as e:
        output_error(f"监控操作失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
