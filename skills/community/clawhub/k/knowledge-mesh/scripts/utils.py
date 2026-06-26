#!/usr/bin/env python3
"""
knowledge-mesh 共享工具模块

提供数据目录管理、订阅校验、参数解析、数据格式化等通用功能。
统一搜索 GitHub、Stack Overflow、Discord、Confluence、Notion、Slack 等知识源。
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


# ============================================================
# 常量定义
# ============================================================

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-bdi", "knowledge-mesh")

# 支持的知识源列表
SUPPORTED_SOURCES = [
    "github",
    "stackoverflow",
    "discord",
    "confluence",
    "notion",
    "slack",
    "baidu",
    "obsidian",
]

# 各知识源显示名称
SOURCE_DISPLAY_NAMES = {
    "github": "GitHub",
    "stackoverflow": "Stack Overflow",
    "discord": "Discord",
    "confluence": "Confluence",
    "notion": "Notion",
    "slack": "Slack",
    "baidu": "百度搜索",
    "obsidian": "Obsidian",
}

# 各知识源对应的环境变量
SOURCE_ENV_KEYS = {
    "github": "KM_GITHUB_TOKEN",
    "stackoverflow": "KM_STACKOVERFLOW_KEY",
    "discord": "KM_DISCORD_BOT_TOKEN",
    "confluence": "KM_CONFLUENCE_TOKEN",
    "notion": "KM_NOTION_TOKEN",
    "slack": "KM_SLACK_TOKEN",
    "baidu": "KM_BAIDU_API_KEY",
    "obsidian": "KM_OBSIDIAN_VAULT_PATH",
}


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录路径。

    优先读取环境变量 KM_DATA_DIR，若未设置则使用默认路径
    ~/.openclaw-bdi/knowledge-mesh/。
    自动创建目录（若不存在）。

    Returns:
        数据目录的绝对路径。
    """
    data_dir = os.environ.get("KM_DATA_DIR", DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_data_file(filename: str) -> str:
    """获取数据文件的完整路径。

    Args:
        filename: 文件名（如 "index_data.json"）。

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

def parse_common_args(description: str = "knowledge-mesh 知识搜索工具") -> argparse.ArgumentParser:
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
        "max_sources": 3,
        "daily_searches": 10,
        "max_results": 20,
        "features": [
            "basic_search",
            "github_search",
            "stackoverflow_search",
        ],
    },
    "paid": {
        "tier": "paid",
        "max_sources": 10,
        "daily_searches": -1,
        "max_results": 100,
        "features": [
            "basic_search",
            "github_search",
            "stackoverflow_search",
            "discord_search",
            "confluence_search",
            "notion_search",
            "slack_search",
            "local_index",
            "topic_monitor",
            "synthesis",
            "mermaid_chart",
            "export",
        ],
    },
}


def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 KM_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get("KM_SUBSCRIPTION_TIER", "free")

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
            f"「{display_name}」为付费版功能。当前为免费版，请升级至付费版（¥129/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return False
    return True


# ============================================================
# 搜索配额管理
# ============================================================

def _get_usage_file() -> str:
    """获取搜索使用量记录文件路径。"""
    return get_data_file("usage.json")


def check_search_quota() -> bool:
    """检查今日搜索配额是否充足。

    Returns:
        True 表示配额充足，False 表示已达上限（已输出错误信息）。
    """
    sub = check_subscription()
    daily_limit = sub["daily_searches"]

    # 付费版不限搜索次数
    if daily_limit < 0:
        return True

    usage = read_json_file(_get_usage_file())
    if not isinstance(usage, dict):
        usage = {}

    today = today_str()
    today_count = usage.get(today, 0)

    if today_count >= daily_limit:
        output_error(
            f"今日搜索次数已达上限（{daily_limit} 次）。请升级至付费版（¥129/月）以获取无限搜索。",
            code="QUOTA_EXCEEDED",
        )
        return False

    return True


def increment_search_count() -> None:
    """递增今日搜索计数。"""
    filepath = _get_usage_file()
    usage = read_json_file(filepath)
    if not isinstance(usage, dict):
        usage = {}

    today = today_str()
    usage[today] = usage.get(today, 0) + 1

    # 清理 7 天前的记录
    cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    usage = {k: v for k, v in usage.items() if k >= cutoff}

    write_json_file(filepath, usage)


# ============================================================
# 通用工具函数
# ============================================================

def generate_id(prefix: str = "KM") -> str:
    """生成唯一 ID。

    基于时间戳生成，格式为 前缀+时间戳。

    Args:
        prefix: ID 前缀，默认为 "KM"（知识网格）。

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


def truncate_text(text: str, max_len: int = 200) -> str:
    """截断文本到指定最大长度。

    若超过最大长度，截断并追加省略号。

    Args:
        text: 原始文本。
        max_len: 最大长度，默认 200。

    Returns:
        截断后的文本。
    """
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def highlight_match(text: str, query: str) -> str:
    """在文本中高亮匹配的查询词。

    使用 **加粗** 标记匹配部分（Markdown 格式）。

    Args:
        text: 原始文本。
        query: 查询关键词。

    Returns:
        高亮后的文本。
    """
    if not text or not query:
        return text or ""

    # 将查询拆分为多个关键词
    keywords = [kw.strip() for kw in query.split() if kw.strip()]
    result = text
    for kw in keywords:
        # 不区分大小写替换
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        result = pattern.sub(lambda m: f"**{m.group(0)}**", result)

    return result


def format_source_badge(source_name: str) -> str:
    """格式化知识源标签显示。

    生成 Markdown 格式的知识源标签。

    Args:
        source_name: 知识源名称（如 "github"）。

    Returns:
        格式化后的标签字符串，如 "[GitHub]"。
    """
    display = SOURCE_DISPLAY_NAMES.get(source_name, source_name)
    return f"[{display}]"


def hash_text(text: str) -> str:
    """计算文本的 MD5 哈希值。

    Args:
        text: 待哈希的文本。

    Returns:
        MD5 哈希字符串。
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def clean_html(html_text: str) -> str:
    """简单清理 HTML 标签，返回纯文本。

    Args:
        html_text: 包含 HTML 标签的文本。

    Returns:
        清理后的纯文本。
    """
    if not html_text:
        return ""
    # 移除 HTML 标签
    text = re.sub(r"<[^>]+>", "", html_text)
    # 处理常见的 HTML 实体
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&nbsp;", " ")
    # 压缩连续空白
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_iso_datetime(dt_str: str) -> Optional[datetime]:
    """解析 ISO 格式的日期时间字符串。

    Args:
        dt_str: ISO 日期时间字符串。

    Returns:
        datetime 对象，解析失败返回 None。
    """
    if not dt_str:
        return None
    try:
        # 处理多种常见格式
        if "T" in dt_str:
            # 移除时区后缀
            clean = re.sub(r"[Zz]$", "", dt_str)
            clean = re.sub(r"[+\-]\d{2}:\d{2}$", "", clean)
            # 截断微秒
            if "." in clean:
                clean = clean.split(".")[0]
            return datetime.strptime(clean, "%Y-%m-%dT%H:%M:%S")
        else:
            return datetime.strptime(dt_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def days_ago(dt_str: str) -> int:
    """计算指定日期距今的天数。

    Args:
        dt_str: 日期时间字符串。

    Returns:
        距今天数（正数表示过去），解析失败返回 0。
    """
    dt = parse_iso_datetime(dt_str)
    if dt is None:
        return 0
    delta = datetime.now() - dt
    return max(0, delta.days)
