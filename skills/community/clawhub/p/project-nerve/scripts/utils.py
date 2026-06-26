#!/usr/bin/env python3
"""
project-nerve 共享工具模块

提供数据存储、订阅校验、优先级/状态标准化、数据格式化等通用功能。
跨平台项目管理聚合器的基础工具集。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


# ============================================================
# 常量定义
# ============================================================

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-bdi", "project-nerve")

# 统一优先级定义
PRIORITIES = ["紧急", "高", "中", "低"]

# 统一状态定义
STATUSES = ["待办", "进行中", "已完成", "已关闭"]

# 支持的平台列表
SUPPORTED_PLATFORMS = ["trello", "github", "linear", "notion", "obsidian"]

# 优先级映射表：将各平台的优先级字符串映射到统一优先级
_PRIORITY_MAP: Dict[str, str] = {
    # 中文
    "紧急": "紧急",
    "urgent": "紧急",
    "critical": "紧急",
    "p0": "紧急",
    "highest": "紧急",
    "blocker": "紧急",
    "高": "高",
    "high": "高",
    "p1": "高",
    "important": "高",
    "中": "中",
    "medium": "中",
    "normal": "中",
    "p2": "中",
    "default": "中",
    "低": "低",
    "low": "低",
    "minor": "低",
    "p3": "低",
    "trivial": "低",
    "none": "低",
    "no priority": "低",
    "nopriority": "低",
}

# 状态映射表：将各平台的状态字符串映射到统一状态
_STATUS_MAP: Dict[str, str] = {
    # 中文
    "待办": "待办",
    "未开始": "待办",
    "进行中": "进行中",
    "处理中": "进行中",
    "已完成": "已完成",
    "完成": "已完成",
    "已关闭": "已关闭",
    "关闭": "已关闭",
    # 英文 — Trello / GitHub / Linear / Notion 常见状态
    "todo": "待办",
    "to do": "待办",
    "backlog": "待办",
    "open": "待办",
    "new": "待办",
    "not started": "待办",
    "triage": "待办",
    "in progress": "进行中",
    "in_progress": "进行中",
    "doing": "进行中",
    "started": "进行中",
    "active": "进行中",
    "in review": "进行中",
    "in_review": "进行中",
    "done": "已完成",
    "completed": "已完成",
    "resolved": "已完成",
    "merged": "已完成",
    "closed": "已关闭",
    "cancelled": "已关闭",
    "canceled": "已关闭",
    "archived": "已关闭",
    "won't fix": "已关闭",
    "wontfix": "已关闭",
    "duplicate": "已关闭",
}


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录路径。

    优先读取环境变量 PNC_DATA_DIR，若未设置则使用默认路径
    ~/.openclaw-bdi/project-nerve/。
    自动创建目录（若不存在）。

    Returns:
        数据目录的绝对路径。
    """
    data_dir = os.environ.get("PNC_DATA_DIR", DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_data_file(filename: str) -> str:
    """获取数据文件的完整路径。

    Args:
        filename: 文件名（如 "sources.json"）。

    Returns:
        数据文件的绝对路径。
    """
    return os.path.join(get_data_dir(), filename)


# ============================================================
# JSON 输入输出
# ============================================================

def read_json_file(filepath: str) -> Any:
    """读取 JSON 文件并返回解析后的数据。

    Args:
        filepath: JSON 文件路径。

    Returns:
        解析后的数据对象。若文件不存在，返回空列表。
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def write_json_file(filepath: str, data: Any) -> None:
    """将数据写入 JSON 文件。

    Args:
        filepath: 目标文件路径。
        data: 待写入的数据。
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def output_json(data: Any) -> None:
    """将数据以 JSON 格式输出到标准输出。

    Args:
        data: 待输出的数据。
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
# 命令行参数解析
# ============================================================

def parse_common_args(description: str = "project-nerve 项目管理工具") -> argparse.ArgumentParser:
    """创建通用命令行参数解析器。

    Args:
        description: 工具描述文本。

    Returns:
        配置好通用参数的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--action",
        required=True,
        help="操作类型",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 格式的数据字符串",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="JSON 数据文件路径",
    )
    return parser


def load_input_data(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    """从命令行参数加载输入数据。

    优先使用 --data 参数，其次尝试 --data-file 参数。

    Args:
        args: 解析后的命令行参数。

    Returns:
        解析后的字典数据，若无输入数据则返回 None。

    Raises:
        ValueError: 当 JSON 解析失败或文件读取失败时抛出。
    """
    if args.data:
        try:
            data = json.loads(args.data)
            if not isinstance(data, dict):
                raise ValueError(f"期望 JSON 对象，实际类型为 {type(data).__name__}")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")

    if args.data_file:
        if not os.path.exists(args.data_file):
            raise ValueError(f"数据文件不存在: {args.data_file}")
        try:
            with open(args.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(f"期望 JSON 对象，实际类型为 {type(data).__name__}")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"数据文件 JSON 解析失败: {e}")

    return None


# ============================================================
# 订阅校验
# ============================================================

_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_sources": 2,
        "max_tasks_display": 50,
        "features": [
            "basic_query",
            "task_list",
            "source_connect",
        ],
    },
    "paid": {
        "tier": "paid",
        "max_sources": 10,
        "max_tasks_display": 500,
        "features": [
            "basic_query",
            "task_list",
            "source_connect",
            "sprint_analytics",
            "standup_report",
            "blocker_analysis",
            "mermaid_chart",
            "bulk_sync",
        ],
    },
}


def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 PNC_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get("PNC_SUBSCRIPTION_TIER", "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    return dict(_SUBSCRIPTION_TIERS[tier])


def require_paid_feature(feature_name: str, display_name: str) -> bool:
    """检查当前订阅是否支持指定功能。

    若不支持，输出升级提示并返回 False。

    Args:
        feature_name: 功能内部名称。
        display_name: 功能显示名称（用于提示信息）。

    Returns:
        True 表示功能可用，False 表示不可用（已输出错误信息）。
    """
    sub = check_subscription()
    if feature_name not in sub["features"]:
        output_error(
            f"「{display_name}」为付费版功能。当前为免费版，请升级至付费版（¥99/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return False
    return True


# ============================================================
# 标准化工具函数
# ============================================================

def normalize_priority(p: str) -> str:
    """将各平台的优先级字符串映射到统一优先级。

    支持中文（紧急/高/中/低）和英文（urgent/high/medium/low 等）。
    无法识别的优先级默认返回 "中"。

    Args:
        p: 原始优先级字符串。

    Returns:
        统一优先级：紧急 / 高 / 中 / 低。
    """
    if not p:
        return "中"
    key = p.strip().lower()
    return _PRIORITY_MAP.get(key, "中")


def normalize_status(s: str) -> str:
    """将各平台的状态字符串映射到统一状态。

    支持中文（待办/进行中/已完成/已关闭）和英文常见状态。
    无法识别的状态默认返回 "待办"。

    Args:
        s: 原始状态字符串。

    Returns:
        统一状态：待办 / 进行中 / 已完成 / 已关闭。
    """
    if not s:
        return "待办"
    key = s.strip().lower()
    return _STATUS_MAP.get(key, "待办")


def format_task_table(tasks: List[Dict[str, Any]]) -> str:
    """将任务列表格式化为 Markdown 表格。

    表格列：序号 | 标题 | 平台 | 状态 | 优先级 | 负责人 | 截止日期

    Args:
        tasks: 统一格式的任务字典列表。

    Returns:
        Markdown 表格字符串。
    """
    if not tasks:
        return "暂无任务数据。"

    lines = [
        "| # | 标题 | 平台 | 状态 | 优先级 | 负责人 | 截止日期 |",
        "|---|------|------|------|--------|--------|----------|",
    ]
    for idx, task in enumerate(tasks, start=1):
        title = task.get("title", "无标题")
        # 截断过长标题
        if len(title) > 40:
            title = title[:37] + "..."
        source = task.get("source", "-")
        status = task.get("status", "-")
        priority = task.get("priority", "-")
        assignee = task.get("assignee", "-") or "-"
        due_date = task.get("due_date", "-") or "-"
        lines.append(f"| {idx} | {title} | {source} | {status} | {priority} | {assignee} | {due_date} |")

    return "\n".join(lines)


# ============================================================
# ID 与时间工具
# ============================================================

def generate_id(prefix: str = "T") -> str:
    """生成唯一 ID。

    基于时间戳生成，格式为 前缀+时间戳。

    Args:
        prefix: ID 前缀，默认为 "T"（任务）。

    Returns:
        唯一 ID 字符串。
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}{timestamp}"


def now_iso() -> str:
    """返回当前时间的 ISO 格式字符串。

    Returns:
        ISO 格式时间字符串，如 "2026-03-19T10:30:00"。
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def today_str() -> str:
    """返回今天的日期字符串。

    Returns:
        日期字符串，格式为 "YYYY-MM-DD"。
    """
    return datetime.now().strftime("%Y-%m-%d")


# ============================================================
# Mermaid 图表生成
# ============================================================

def generate_pie_chart(title: str, data: List[Dict[str, Any]]) -> str:
    """生成 Mermaid 饼图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。

    Returns:
        Mermaid 饼图代码块字符串。
    """
    lines = ["```mermaid", f"pie title {title}"]
    for item in data:
        label = item.get("label", "未知")
        value = item.get("value", 0)
        lines.append(f'    "{label}" : {value}')
    lines.append("```")
    return "\n".join(lines)


def generate_bar_chart(
    title: str,
    data: List[Dict[str, Any]],
    x_label: str = "类别",
    y_label: str = "数值",
) -> str:
    """生成 Mermaid xychart-beta 柱状图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。
        x_label: X 轴标签。
        y_label: Y 轴标签。

    Returns:
        Mermaid 柱状图代码块字符串。
    """
    labels = [f'"{item.get("label", "")}"' for item in data]
    values = [str(item.get("value", 0)) for item in data]

    lines = [
        "```mermaid",
        "xychart-beta",
        f'    title "{title}"',
        f'    x-axis [{", ".join(labels)}]',
        f'    y-axis "{y_label}"',
        f'    bar [{", ".join(values)}]',
        "```",
    ]
    return "\n".join(lines)


def generate_line_chart(
    title: str,
    data: List[Dict[str, Any]],
    x_label: str = "时间",
    y_label: str = "数值",
) -> str:
    """生成 Mermaid xychart-beta 折线图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。
        x_label: X 轴标签。
        y_label: Y 轴标签。

    Returns:
        Mermaid 折线图代码块字符串。
    """
    labels = [f'"{item.get("label", "")}"' for item in data]
    values = [str(item.get("value", 0)) for item in data]

    lines = [
        "```mermaid",
        "xychart-beta",
        f'    title "{title}"',
        f'    x-axis [{", ".join(labels)}]',
        f'    y-axis "{y_label}"',
        f'    line [{", ".join(values)}]',
        "```",
    ]
    return "\n".join(lines)


# ============================================================
# 日期辅助函数
# ============================================================

def calculate_days_since(date_str: str) -> int:
    """计算从指定日期到今天的天数。

    Args:
        date_str: 日期字符串，格式为 YYYY-MM-DD 或 ISO 格式。

    Returns:
        距今天数（正数表示过去，负数表示未来）。
    """
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            dt = dt.replace(tzinfo=None)
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - dt
        return delta.days
    except (ValueError, TypeError):
        return 0


def is_overdue(due_date: str) -> bool:
    """判断任务是否已逾期。

    Args:
        due_date: 截止日期字符串（YYYY-MM-DD 或 ISO 格式）。

    Returns:
        True 表示已逾期，False 表示未逾期或无截止日期。
    """
    if not due_date:
        return False
    days = calculate_days_since(due_date)
    return days > 0


def parse_date(date_str: str) -> Optional[datetime]:
    """解析日期字符串为 datetime 对象。

    支持 YYYY-MM-DD 和 ISO 格式。

    Args:
        date_str: 日期字符串。

    Returns:
        datetime 对象，解析失败返回 None。
    """
    if not date_str:
        return None
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.replace(tzinfo=None)
        else:
            return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None
