#!/usr/bin/env python3
"""
inventory-eye 共享工具模块

提供数据格式化、输入输出处理、订阅校验、库存专用辅助函数等通用功能。
"""

import csv
import json
import os
import re
import sys
from datetime import datetime, date
from typing import Any, Dict, List, Optional


# ============================================================
# 常量与配置
# ============================================================

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-bdi", "inventory-eye")
ENV_DATA_DIR = "IE_DATA_DIR"
ENV_SUBSCRIPTION_TIER = "IE_SUBSCRIPTION_TIER"

# SKU 字段定义
SKU_FIELDS = [
    "sku_id", "name", "category", "quantity", "unit_cost", "selling_price",
    "safety_stock", "warehouse", "expiry_date", "last_inbound_date",
    "last_outbound_date", "created_at", "updated_at",
]

# 订阅等级配置
_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_skus": 100,
        "max_warehouses": 1,
        "features": [
            "csv_import",
            "inventory_overview",
            "fixed_threshold_alert",
            "basic_expiry_alert",
        ],
    },
    "paid": {
        "tier": "paid",
        "max_skus": 2000,
        "max_warehouses": 5,
        "features": [
            "csv_import",
            "inventory_overview",
            "dynamic_safety_stock",
            "multi_level_expiry_alert",
            "slow_moving_analysis",
            "reorder_suggestion",
            "turnover_analysis",
        ],
    },
}


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录路径，不存在时自动创建。

    优先使用环境变量 IE_DATA_DIR，否则使用默认路径
    ~/.openclaw-bdi/inventory-eye/

    Returns:
        数据目录的绝对路径。
    """
    data_dir = os.environ.get(ENV_DATA_DIR, DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_inventory_file() -> str:
    """获取库存数据文件路径。

    Returns:
        库存 JSON 文件的绝对路径。
    """
    return os.path.join(get_data_dir(), "inventory.json")


def get_transactions_file() -> str:
    """获取出入库记录文件路径。

    Returns:
        交易记录 JSON 文件的绝对路径。
    """
    return os.path.join(get_data_dir(), "transactions.json")


# ============================================================
# 数字格式化
# ============================================================

def format_number(value: float, decimals: int = 2) -> str:
    """将数字格式化为带千分位分隔符的字符串。

    Args:
        value: 待格式化的数值。
        decimals: 小数位数，默认为 2。

    Returns:
        格式化后的字符串，例如 1234567 → "1,234,567.00"

    Raises:
        TypeError: 当 value 无法转换为数字时抛出。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")

    if decimals <= 0:
        return f"{int(round(num)):,}"
    return f"{num:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """将小数格式化为百分比字符串。

    Args:
        value: 待格式化的小数值（0.156 表示 15.6%）。
        decimals: 百分比小数位数，默认为 1。

    Returns:
        百分比字符串，例如 0.156 → "15.6%"

    Raises:
        TypeError: 当 value 无法转换为数字时抛出。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")

    pct = num * 100
    return f"{pct:.{decimals}f}%"


def format_chinese_unit(value: float) -> str:
    """将大数字转换为中文单位表示（万、亿）。

    Args:
        value: 待转换的数值。

    Returns:
        带中文单位的字符串，例如:
        - 12345 → "1.23万"
        - 123456789 → "1.23亿"
        - 999 → "999"

    Raises:
        TypeError: 当 value 无法转换为数字时抛出。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")

    abs_num = abs(num)
    sign = "-" if num < 0 else ""

    if abs_num >= 1e8:
        result = abs_num / 1e8
        return f"{sign}{result:.2f}亿"
    elif abs_num >= 1e4:
        result = abs_num / 1e4
        return f"{sign}{result:.2f}万"
    else:
        if abs_num == int(abs_num):
            return f"{sign}{int(abs_num)}"
        return f"{sign}{abs_num:.2f}"


# ============================================================
# 库存专用格式化
# ============================================================

def format_sku(sku_id: str) -> str:
    """格式化 SKU 编码，确保统一大写并去除首尾空白。

    Args:
        sku_id: 原始 SKU 编码。

    Returns:
        标准化后的 SKU 编码。
    """
    if not sku_id or not isinstance(sku_id, str):
        return str(sku_id or "").strip()
    return sku_id.strip().upper()


def days_until_expiry(expiry_date: Optional[str]) -> Optional[int]:
    """计算距离过期日期的天数。

    Args:
        expiry_date: 过期日期字符串，支持 YYYY-MM-DD 格式。

    Returns:
        距离过期的天数（负数表示已过期），若无过期日期则返回 None。
    """
    if not expiry_date:
        return None
    try:
        exp = datetime.strptime(str(expiry_date).strip(), "%Y-%m-%d").date()
        delta = exp - date.today()
        return delta.days
    except (ValueError, TypeError):
        return None


def parse_date(date_str: Optional[str]) -> Optional[str]:
    """解析并标准化日期字符串为 YYYY-MM-DD 格式。

    支持格式: YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY

    Args:
        date_str: 待解析的日期字符串。

    Returns:
        标准化的日期字符串（YYYY-MM-DD），解析失败返回 None。
    """
    if not date_str:
        return None
    date_str = str(date_str).strip()
    if not date_str:
        return None

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def parse_csv_columns(header: List[str]) -> Dict[str, Optional[str]]:
    """自动识别 CSV 列名与 SKU 字段的映射关系。

    通过关键词匹配，自动将 CSV 表头映射到标准 SKU 字段。

    Args:
        header: CSV 文件的表头列名列表。

    Returns:
        映射字典 {SKU字段名: CSV列名}，未匹配的字段值为 None。
    """
    mapping: Dict[str, Optional[str]] = {f: None for f in SKU_FIELDS}

    # 关键词映射规则
    rules = {
        "sku_id": ["sku", "编码", "编号", "货号", "商品编码", "sku_id", "skuid", "商品id"],
        "name": ["名称", "商品名", "品名", "产品名", "name", "商品名称", "产品名称"],
        "category": ["分类", "类别", "品类", "category", "类目"],
        "quantity": ["数量", "库存", "库存量", "qty", "quantity", "stock", "现有库存"],
        "unit_cost": ["成本", "进价", "采购价", "cost", "unit_cost", "进货价"],
        "selling_price": ["售价", "销售价", "selling_price", "price", "零售价", "标价"],
        "safety_stock": ["安全库存", "最低库存", "safety_stock", "safety", "预警值"],
        "warehouse": ["仓库", "库房", "warehouse", "仓"],
        "expiry_date": ["过期", "保质期", "到期", "expiry", "有效期", "过期日期"],
        "last_inbound_date": ["入库日期", "入库时间", "进货日期", "inbound"],
        "last_outbound_date": ["出库日期", "出库时间", "销售日期", "outbound"],
    }

    header_lower = [h.strip().lower() for h in header]

    for field, keywords in rules.items():
        for kw in keywords:
            kw_lower = kw.lower()
            for i, col in enumerate(header_lower):
                if kw_lower == col or kw_lower in col:
                    mapping[field] = header[i].strip()
                    break
            if mapping[field]:
                break

    return mapping


# ============================================================
# JSON 输入输出
# ============================================================

def read_json_input(args) -> Any:
    """从命令行参数或标准输入读取 JSON 数据。

    优先使用 --data 参数，其次 --data-file 参数，最后从 stdin 读取。

    Args:
        args: argparse 解析后的命名空间，应包含 data 和 data_file 属性。

    Returns:
        解析后的 JSON 数据。

    Raises:
        ValueError: 当所有来源均无可用数据时抛出。
    """
    if hasattr(args, "data") and args.data:
        try:
            return json.loads(args.data)
        except json.JSONDecodeError as e:
            raise ValueError(f"--data 参数 JSON 解析失败: {e}")

    if hasattr(args, "data_file") and args.data_file:
        if not os.path.exists(args.data_file):
            raise ValueError(f"数据文件不存在: {args.data_file}")
        with open(args.data_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"数据文件 JSON 解析失败: {e}")

    if not sys.stdin.isatty():
        raw = sys.stdin.read()
        if raw.strip():
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError(f"标准输入 JSON 解析失败: {e}")

    return None


def output_json(data: Any) -> None:
    """将数据以 JSON 格式输出到标准输出。

    使用 ensure_ascii=False 以保留中文等非 ASCII 字符。

    Args:
        data: 待输出的数据（可被 JSON 序列化的任意对象）。
    """
    print(json.dumps(data, ensure_ascii=False, default=str))


def output_error(message: str, code: str = "ERROR") -> None:
    """输出标准错误响应到标准输出。

    Args:
        message: 错误描述信息。
        code: 错误代码，默认为 "ERROR"。
    """
    result = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    output_json(result)


def output_success(data: Any) -> None:
    """输出标准成功响应到标准输出。

    Args:
        data: 成功时返回的数据负载。
    """
    result = {
        "success": True,
        "data": data,
    }
    output_json(result)


# ============================================================
# 订阅校验
# ============================================================

def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 IE_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get(ENV_SUBSCRIPTION_TIER, "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    return dict(_SUBSCRIPTION_TIERS[tier])


def require_paid(feature_name: str) -> None:
    """检查当前是否为付费版，若非付费版则输出错误并退出。

    Args:
        feature_name: 功能名称，用于错误提示。
    """
    sub = check_subscription()
    if sub["tier"] != "paid":
        output_error(
            f"「{feature_name}」为付费版功能。当前为免费版，请升级至付费版（¥89/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        sys.exit(0)


def check_sku_limit(current_count: int) -> bool:
    """检查 SKU 数量是否超出当前订阅限制。

    Args:
        current_count: 当前 SKU 数量。

    Returns:
        True 表示未超限，False 表示已超限。
    """
    sub = check_subscription()
    return current_count < sub["max_skus"]


def check_warehouse_limit(warehouses: List[str]) -> bool:
    """检查仓库数量是否超出当前订阅限制。

    Args:
        warehouses: 当前已有仓库名称列表。

    Returns:
        True 表示未超限，False 表示已超限。
    """
    sub = check_subscription()
    return len(set(warehouses)) <= sub["max_warehouses"]


# ============================================================
# 数据持久化
# ============================================================

def load_inventory() -> Dict[str, Any]:
    """从文件加载库存数据。

    Returns:
        库存数据字典，包含 skus（SKU列表）和 metadata（元数据）。
    """
    filepath = get_inventory_file()
    if not os.path.exists(filepath):
        return {"skus": [], "metadata": {"created_at": datetime.now().isoformat(), "version": "1.0"}}

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"skus": [], "metadata": {"created_at": datetime.now().isoformat(), "version": "1.0"}}


def save_inventory(data: Dict[str, Any]) -> None:
    """将库存数据保存到文件。

    Args:
        data: 库存数据字典。
    """
    data["metadata"] = data.get("metadata", {})
    data["metadata"]["updated_at"] = datetime.now().isoformat()
    filepath = get_inventory_file()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def load_transactions() -> List[Dict[str, Any]]:
    """从文件加载出入库记录。

    Returns:
        交易记录列表。
    """
    filepath = get_transactions_file()
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_transactions(transactions: List[Dict[str, Any]]) -> None:
    """将出入库记录保存到文件。

    Args:
        transactions: 交易记录列表。
    """
    filepath = get_transactions_file()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2, default=str)


def add_transaction(tx_type: str, sku_id: str, quantity: int, note: str = "") -> None:
    """添加一条出入库记录。

    Args:
        tx_type: 交易类型，"inbound"（入库）或 "outbound"（出库）。
        sku_id: SKU 编码。
        quantity: 数量。
        note: 备注说明。
    """
    transactions = load_transactions()
    transactions.append({
        "type": tx_type,
        "sku_id": format_sku(sku_id),
        "quantity": quantity,
        "note": note,
        "timestamp": datetime.now().isoformat(),
    })
    save_transactions(transactions)


# ============================================================
# CSV 解析
# ============================================================

def read_csv_file(filepath: str) -> List[Dict[str, str]]:
    """读取 CSV 文件并返回字典列表。

    Args:
        filepath: CSV 文件路径。

    Returns:
        每行数据对应一个字典的列表。

    Raises:
        ValueError: 当文件不存在或格式错误时抛出。
    """
    if not os.path.exists(filepath):
        raise ValueError(f"CSV 文件不存在: {filepath}")

    rows = []
    encodings = ["utf-8", "utf-8-sig", "gbk", "gb2312"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f)
                rows = [row for row in reader]
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            raise ValueError(f"读取 CSV 文件失败: {e}")
    else:
        raise ValueError(f"无法以支持的编码读取 CSV 文件: {filepath}")

    return rows
