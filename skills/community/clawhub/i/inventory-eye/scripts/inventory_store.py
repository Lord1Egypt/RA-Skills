#!/usr/bin/env python3
"""
inventory-eye 库存数据管理模块

提供库存数据的导入、增删改查、导出功能，支持 CSV 导入和 JSON 存储。
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# 将 scripts 目录加入路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    check_subscription, check_sku_limit, check_warehouse_limit,
    format_sku, parse_date, parse_csv_columns, read_csv_file,
    load_inventory, save_inventory, add_transaction,
    read_json_input, output_json, output_error, output_success,
)


# ============================================================
# 库存操作
# ============================================================

def _validate_sku(sku: Dict[str, Any]) -> Dict[str, Any]:
    """验证并标准化 SKU 数据。

    Args:
        sku: 原始 SKU 数据字典。

    Returns:
        标准化后的 SKU 字典。

    Raises:
        ValueError: 当必填字段缺失时抛出。
    """
    if not sku.get("sku_id"):
        raise ValueError("SKU 编码（sku_id）为必填字段")
    if not sku.get("name"):
        raise ValueError("商品名称（name）为必填字段")

    now = datetime.now().isoformat()
    return {
        "sku_id": format_sku(sku["sku_id"]),
        "name": str(sku["name"]).strip(),
        "category": str(sku.get("category", "")).strip() or "未分类",
        "quantity": max(0, int(float(sku.get("quantity", 0)))),
        "unit_cost": round(float(sku.get("unit_cost", 0)), 2),
        "selling_price": round(float(sku.get("selling_price", 0)), 2),
        "safety_stock": max(0, int(float(sku.get("safety_stock", 10)))),
        "warehouse": str(sku.get("warehouse", "默认仓库")).strip() or "默认仓库",
        "expiry_date": parse_date(sku.get("expiry_date")) or "",
        "last_inbound_date": parse_date(sku.get("last_inbound_date")) or "",
        "last_outbound_date": parse_date(sku.get("last_outbound_date")) or "",
        "created_at": sku.get("created_at", now),
        "updated_at": now,
    }


def action_import(args) -> None:
    """从 CSV 文件导入库存数据。"""
    filepath = args.file
    if not filepath:
        output_error("请通过 --file 参数指定 CSV 文件路径", "MISSING_FILE")
        return

    if not os.path.exists(filepath):
        output_error(f"文件不存在: {filepath}", "FILE_NOT_FOUND")
        return

    sub = check_subscription()
    inventory = load_inventory()
    existing_skus = {s["sku_id"] for s in inventory["skus"]}

    try:
        rows = read_csv_file(filepath)
    except ValueError as e:
        output_error(str(e), "CSV_READ_ERROR")
        return

    if not rows:
        output_error("CSV 文件为空或无有效数据", "EMPTY_FILE")
        return

    # 自动映射列名
    header = list(rows[0].keys())
    mapping = parse_csv_columns(header)

    imported = 0
    updated = 0
    skipped = 0
    errors = []

    for i, row in enumerate(rows, 1):
        try:
            sku_data = {}
            for field, col in mapping.items():
                if col and col in row:
                    sku_data[field] = row[col]

            if not sku_data.get("sku_id") and not sku_data.get("name"):
                skipped += 1
                continue

            # 如果没有 sku_id，用行号生成
            if not sku_data.get("sku_id"):
                sku_data["sku_id"] = f"SKU-{i:05d}"

            validated = _validate_sku(sku_data)
            sku_id = validated["sku_id"]

            # 检查仓库限制
            current_warehouses = list({s["warehouse"] for s in inventory["skus"]})
            if validated["warehouse"] not in current_warehouses:
                if not check_warehouse_limit(current_warehouses + [validated["warehouse"]]):
                    errors.append(f"第{i}行: 仓库数量超出{sub['tier']}版限制（最多{sub['max_warehouses']}个）")
                    skipped += 1
                    continue

            if sku_id in existing_skus:
                # 更新已有 SKU
                for j, s in enumerate(inventory["skus"]):
                    if s["sku_id"] == sku_id:
                        validated["created_at"] = s["created_at"]
                        inventory["skus"][j] = validated
                        break
                updated += 1
            else:
                # 检查 SKU 数量限制
                if not check_sku_limit(len(inventory["skus"])):
                    errors.append(f"第{i}行: SKU 数量已达{sub['tier']}版上限（{sub['max_skus']}个）")
                    skipped += 1
                    continue
                inventory["skus"].append(validated)
                existing_skus.add(sku_id)
                imported += 1

        except (ValueError, TypeError) as e:
            errors.append(f"第{i}行: {e}")
            skipped += 1

    save_inventory(inventory)

    result = {
        "action": "import",
        "file": filepath,
        "column_mapping": {k: v for k, v in mapping.items() if v},
        "imported": imported,
        "updated": updated,
        "skipped": skipped,
        "total_skus": len(inventory["skus"]),
    }
    if errors:
        result["errors"] = errors[:20]  # 最多显示 20 条错误

    output_success(result)


def action_add(args) -> None:
    """添加单个 SKU。"""
    data = read_json_input(args)
    if not data:
        output_error("请通过 --data 或 --data-file 提供 SKU 数据", "MISSING_DATA")
        return

    sub = check_subscription()
    inventory = load_inventory()

    try:
        validated = _validate_sku(data)
    except ValueError as e:
        output_error(str(e), "VALIDATION_ERROR")
        return

    # 检查 SKU 是否已存在
    for s in inventory["skus"]:
        if s["sku_id"] == validated["sku_id"]:
            output_error(f"SKU {validated['sku_id']} 已存在，请使用 update 操作", "DUPLICATE_SKU")
            return

    # 检查 SKU 限制
    if not check_sku_limit(len(inventory["skus"])):
        output_error(
            f"SKU 数量已达{sub['tier']}版上限（{sub['max_skus']}个），请升级至付费版（¥89/月）",
            "SKU_LIMIT_EXCEEDED",
        )
        return

    # 检查仓库限制
    current_warehouses = list({s["warehouse"] for s in inventory["skus"]})
    if validated["warehouse"] not in current_warehouses:
        if not check_warehouse_limit(current_warehouses + [validated["warehouse"]]):
            output_error(
                f"仓库数量已达{sub['tier']}版上限（{sub['max_warehouses']}个），请升级至付费版（¥89/月）",
                "WAREHOUSE_LIMIT_EXCEEDED",
            )
            return

    inventory["skus"].append(validated)
    save_inventory(inventory)

    output_success({
        "action": "add",
        "sku": validated,
        "total_skus": len(inventory["skus"]),
    })


def action_update(args) -> None:
    """更新已有 SKU 信息。"""
    data = read_json_input(args)
    if not data:
        output_error("请通过 --data 或 --data-file 提供更新数据", "MISSING_DATA")
        return

    sku_id = format_sku(data.get("sku_id", ""))
    if not sku_id:
        output_error("更新操作需要提供 sku_id", "MISSING_SKU_ID")
        return

    inventory = load_inventory()

    found = False
    for i, s in enumerate(inventory["skus"]):
        if s["sku_id"] == sku_id:
            # 合并更新
            for key, val in data.items():
                if key in ("created_at",):
                    continue
                if key == "sku_id":
                    s[key] = format_sku(val)
                elif key == "quantity":
                    s[key] = max(0, int(float(val)))
                elif key in ("unit_cost", "selling_price"):
                    s[key] = round(float(val), 2)
                elif key == "safety_stock":
                    s[key] = max(0, int(float(val)))
                elif key in ("expiry_date", "last_inbound_date", "last_outbound_date"):
                    parsed = parse_date(val)
                    if parsed:
                        s[key] = parsed
                else:
                    s[key] = val
            s["updated_at"] = datetime.now().isoformat()
            inventory["skus"][i] = s
            found = True
            break

    if not found:
        output_error(f"未找到 SKU: {sku_id}", "SKU_NOT_FOUND")
        return

    save_inventory(inventory)
    output_success({
        "action": "update",
        "sku": inventory["skus"][i],
    })


def action_delete(args) -> None:
    """删除指定 SKU。"""
    data = read_json_input(args)
    if not data:
        output_error("请通过 --data 提供要删除的 sku_id", "MISSING_DATA")
        return

    sku_id = format_sku(data.get("sku_id", ""))
    if not sku_id:
        output_error("删除操作需要提供 sku_id", "MISSING_SKU_ID")
        return

    inventory = load_inventory()
    original_count = len(inventory["skus"])
    inventory["skus"] = [s for s in inventory["skus"] if s["sku_id"] != sku_id]

    if len(inventory["skus"]) == original_count:
        output_error(f"未找到 SKU: {sku_id}", "SKU_NOT_FOUND")
        return

    save_inventory(inventory)
    output_success({
        "action": "delete",
        "sku_id": sku_id,
        "remaining_skus": len(inventory["skus"]),
    })


def action_list(args) -> None:
    """列出所有库存 SKU。"""
    inventory = load_inventory()
    skus = inventory["skus"]

    # 支持按仓库、分类筛选
    data = read_json_input(args)
    if data:
        if data.get("warehouse"):
            skus = [s for s in skus if s.get("warehouse") == data["warehouse"]]
        if data.get("category"):
            skus = [s for s in skus if s.get("category") == data["category"]]

    sub = check_subscription()
    output_success({
        "action": "list",
        "tier": sub["tier"],
        "total": len(skus),
        "max_skus": sub["max_skus"],
        "skus": skus,
    })


def action_get(args) -> None:
    """获取单个 SKU 详情。"""
    data = read_json_input(args)
    if not data:
        output_error("请通过 --data 提供 sku_id", "MISSING_DATA")
        return

    sku_id = format_sku(data.get("sku_id", ""))
    if not sku_id:
        output_error("需要提供 sku_id", "MISSING_SKU_ID")
        return

    inventory = load_inventory()
    for s in inventory["skus"]:
        if s["sku_id"] == sku_id:
            output_success({"action": "get", "sku": s})
            return

    output_error(f"未找到 SKU: {sku_id}", "SKU_NOT_FOUND")


def action_export(args) -> None:
    """将库存数据导出为 CSV 文件。"""
    inventory = load_inventory()
    skus = inventory["skus"]

    if not skus:
        output_error("库存为空，无数据可导出", "EMPTY_INVENTORY")
        return

    data = read_json_input(args)
    output_path = None
    if data and data.get("output"):
        output_path = data["output"]
    elif args.file:
        output_path = args.file

    if not output_path:
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "output",
            f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    fieldnames = [
        "sku_id", "name", "category", "quantity", "unit_cost", "selling_price",
        "safety_stock", "warehouse", "expiry_date", "last_inbound_date",
        "last_outbound_date", "created_at", "updated_at",
    ]

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(skus)

    output_success({
        "action": "export",
        "file": os.path.abspath(output_path),
        "total_skus": len(skus),
    })


def action_inbound(args) -> None:
    """入库操作：增加指定 SKU 的库存数量。"""
    data = read_json_input(args)
    if not data:
        output_error("请提供入库数据（sku_id, quantity）", "MISSING_DATA")
        return

    sku_id = format_sku(data.get("sku_id", ""))
    quantity = int(float(data.get("quantity", 0)))
    note = data.get("note", "")

    if not sku_id:
        output_error("入库操作需要提供 sku_id", "MISSING_SKU_ID")
        return
    if quantity <= 0:
        output_error("入库数量必须大于 0", "INVALID_QUANTITY")
        return

    inventory = load_inventory()
    found = False
    for s in inventory["skus"]:
        if s["sku_id"] == sku_id:
            s["quantity"] += quantity
            s["last_inbound_date"] = datetime.now().strftime("%Y-%m-%d")
            s["updated_at"] = datetime.now().isoformat()
            found = True
            add_transaction("inbound", sku_id, quantity, note)
            save_inventory(inventory)
            output_success({
                "action": "inbound",
                "sku_id": sku_id,
                "added": quantity,
                "new_quantity": s["quantity"],
            })
            return

    if not found:
        output_error(f"未找到 SKU: {sku_id}", "SKU_NOT_FOUND")


def action_outbound(args) -> None:
    """出库操作：减少指定 SKU 的库存数量。"""
    data = read_json_input(args)
    if not data:
        output_error("请提供出库数据（sku_id, quantity）", "MISSING_DATA")
        return

    sku_id = format_sku(data.get("sku_id", ""))
    quantity = int(float(data.get("quantity", 0)))
    note = data.get("note", "")

    if not sku_id:
        output_error("出库操作需要提供 sku_id", "MISSING_SKU_ID")
        return
    if quantity <= 0:
        output_error("出库数量必须大于 0", "INVALID_QUANTITY")
        return

    inventory = load_inventory()
    for s in inventory["skus"]:
        if s["sku_id"] == sku_id:
            if s["quantity"] < quantity:
                output_error(
                    f"库存不足: {s['name']}（{sku_id}）当前库存 {s['quantity']}，请求出库 {quantity}",
                    "INSUFFICIENT_STOCK",
                )
                return
            s["quantity"] -= quantity
            s["last_outbound_date"] = datetime.now().strftime("%Y-%m-%d")
            s["updated_at"] = datetime.now().isoformat()
            add_transaction("outbound", sku_id, quantity, note)
            save_inventory(inventory)
            output_success({
                "action": "outbound",
                "sku_id": sku_id,
                "removed": quantity,
                "new_quantity": s["quantity"],
            })
            return

    output_error(f"未找到 SKU: {sku_id}", "SKU_NOT_FOUND")


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="库存慧眼 — 库存数据管理工具",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["import", "add", "update", "delete", "list", "get", "export",
                 "inbound", "outbound"],
        help="操作类型",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 格式的数据参数",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="JSON 数据文件路径",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="CSV 文件路径（用于导入/导出）",
    )

    args = parser.parse_args()

    actions = {
        "import": action_import,
        "add": action_add,
        "update": action_update,
        "delete": action_delete,
        "list": action_list,
        "get": action_get,
        "export": action_export,
        "inbound": action_inbound,
        "outbound": action_outbound,
    }

    try:
        actions[args.action](args)
    except Exception as e:
        output_error(f"操作失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
