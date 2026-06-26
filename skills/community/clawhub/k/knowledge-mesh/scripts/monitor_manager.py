#!/usr/bin/env python3
"""
knowledge-mesh 知识主题监控管理器（付费功能）

支持设置关键词监控，定期检查各知识源的新内容，
生成日报/周报摘要。

用法:
    python3 monitor_manager.py --action add --data '{"keywords":["fastapi","async"],"sources":["github","stackoverflow"]}'
    python3 monitor_manager.py --action remove --data '{"id":"MON..."}'
    python3 monitor_manager.py --action list
    python3 monitor_manager.py --action check --data '{"id":"MON..."}'
    python3 monitor_manager.py --action digest --data '{"period":"daily"}'
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    SUPPORTED_SOURCES,
    SOURCE_DISPLAY_NAMES,
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    today_str,
    truncate_text,
    write_json_file,
)


# ============================================================
# 常量
# ============================================================

# 监控配置文件
MONITORS_FILE = "monitors.json"

# 监控结果缓存文件
MONITOR_RESULTS_FILE = "monitor_results.json"

# 最大监控数量
MAX_MONITORS = 20

# 检查结果最大保留天数
MAX_RESULT_DAYS = 30


# ============================================================
# 数据访问
# ============================================================

def _get_monitors() -> List[Dict[str, Any]]:
    """读取所有监控配置。"""
    data = read_json_file(get_data_file(MONITORS_FILE))
    if isinstance(data, list):
        return data
    return []


def _save_monitors(monitors: List[Dict[str, Any]]) -> None:
    """保存监控配置。"""
    write_json_file(get_data_file(MONITORS_FILE), monitors)


def _find_monitor(monitors: List[Dict], monitor_id: str) -> Optional[Dict]:
    """根据 ID 查找监控。"""
    for m in monitors:
        if m.get("id") == monitor_id:
            return m
    return None


def _get_results() -> Dict[str, List[Dict[str, Any]]]:
    """读取监控结果缓存。

    Returns:
        {monitor_id: [results]} 映射。
    """
    data = read_json_file(get_data_file(MONITOR_RESULTS_FILE))
    if isinstance(data, dict):
        return data
    return {}


def _save_results(results: Dict[str, List[Dict[str, Any]]]) -> None:
    """保存监控结果缓存。"""
    write_json_file(get_data_file(MONITOR_RESULTS_FILE), results)


def _cleanup_old_results(results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """清理超过保留期限的结果。

    Args:
        results: 监控结果映射。

    Returns:
        清理后的结果映射。
    """
    cutoff = (datetime.now() - timedelta(days=MAX_RESULT_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")
    cleaned = {}
    for mid, items in results.items():
        kept = [r for r in items if r.get("checked_at", "") >= cutoff]
        if kept:
            cleaned[mid] = kept
    return cleaned


# ============================================================
# 搜索辅助（简化版，避免循环导入）
# ============================================================

def _simple_search(keywords: List[str], sources: List[str], since: str) -> List[Dict[str, Any]]:
    """执行简化搜索，用于监控检查。

    通过 source_searcher 模块执行搜索，过滤 since 之后的结果。

    Args:
        keywords: 关键词列表。
        sources: 知识源列表。
        since: 起始时间（ISO 格式）。

    Returns:
        新内容列表。
    """
    # 动态导入避免模块级循环依赖
    try:
        # 尝试导入 source_searcher 中的适配器
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        from source_searcher import _SOURCE_ADAPTERS
    except ImportError:
        return []

    query = " ".join(keywords)
    all_results = []

    for source in sources:
        if source not in SUPPORTED_SOURCES:
            continue
        adapter = _SOURCE_ADAPTERS.get(source)
        if not adapter:
            continue

        try:
            results = adapter(query, max_results=20)
            # 过滤 since 之后的结果
            for r in results:
                created = r.get("created_at", "")
                if created and created >= since:
                    r["monitor_source"] = source
                    all_results.append(r)
        except Exception:
            # 监控检查时静默忽略搜索错误
            continue

    return all_results


# ============================================================
# 摘要生成
# ============================================================

def _generate_digest_markdown(
    monitors: List[Dict[str, Any]],
    results: Dict[str, List[Dict[str, Any]]],
    period: str,
) -> str:
    """生成监控摘要 Markdown 报告。

    Args:
        monitors: 监控配置列表。
        results: 监控结果映射。
        period: 摘要周期（daily/weekly）。

    Returns:
        Markdown 格式的摘要报告。
    """
    period_label = "日报" if period == "daily" else "周报"
    today = today_str()

    # 确定时间范围
    if period == "daily":
        since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")

    parts = []
    parts.append(f"# 知识监控{period_label} — {today}\n")
    parts.append(f"**生成时间**: {now_iso()}")
    parts.append(f"**监控数量**: {len(monitors)} 个")
    parts.append(f"**统计周期**: {'过去 24 小时' if period == 'daily' else '过去 7 天'}\n")

    total_new = 0

    for monitor in monitors:
        mid = monitor.get("id", "")
        keywords = monitor.get("keywords", [])
        monitor_sources = monitor.get("sources", [])
        keyword_str = "、".join(keywords)

        # 获取该监控的结果
        monitor_results = results.get(mid, [])
        # 过滤时间范围内的结果
        period_results = [
            r for r in monitor_results
            if r.get("checked_at", "") >= since
        ]

        total_new += len(period_results)

        parts.append(f"## 监控: {keyword_str}\n")
        parts.append(f"- **关键词**: {keyword_str}")
        source_names = [SOURCE_DISPLAY_NAMES.get(s, s) for s in monitor_sources]
        parts.append(f"- **监控源**: {', '.join(source_names)}")
        parts.append(f"- **新内容**: {len(period_results)} 条\n")

        if period_results:
            for idx, r in enumerate(period_results[:10], 1):
                title = r.get("title", "无标题")
                url = r.get("url", "")
                source = r.get("source", "")
                badge = f"[{SOURCE_DISPLAY_NAMES.get(source, source)}]"
                snippet = truncate_text(r.get("snippet", ""), 100)

                parts.append(f"### {idx}. {badge} {title}")
                if url:
                    parts.append(f"- 链接: {url}")
                parts.append(f"- 摘要: {snippet}")
                parts.append("")

            if len(period_results) > 10:
                parts.append(f"*... 以及其他 {len(period_results) - 10} 条结果*\n")
        else:
            parts.append("*暂无新内容*\n")

    # 汇总
    parts.append("---\n")
    parts.append(f"**总计**: {len(monitors)} 个监控主题，{total_new} 条新内容\n")
    parts.append("---")
    parts.append("*由 knowledge-mesh 自动生成*")

    return "\n".join(parts)


# ============================================================
# 操作实现
# ============================================================

def action_add(data: Dict[str, Any]) -> None:
    """添加新的主题监控。

    Args:
        data: 包含 keywords（关键词列表）和可选 sources（知识源列表）的字典。
    """
    if not require_paid_feature("topic_monitor", "主题监控"):
        return

    keywords = data.get("keywords", [])
    if not keywords:
        output_error("请提供监控关键词列表（keywords）", code="VALIDATION_ERROR")
        return

    if isinstance(keywords, str):
        keywords = [keywords]

    sources = data.get("sources", ["github", "stackoverflow"])
    if isinstance(sources, str):
        sources = [sources]

    # 校验知识源
    for s in sources:
        if s not in SUPPORTED_SOURCES:
            valid = "、".join(SUPPORTED_SOURCES)
            output_error(f"不支持的知识源: {s}，支持: {valid}", code="INVALID_SOURCE")
            return

    monitors = _get_monitors()

    if len(monitors) >= MAX_MONITORS:
        output_error(
            f"已达监控数量上限（{MAX_MONITORS} 个），请先删除不需要的监控。",
            code="LIMIT_EXCEEDED",
        )
        return

    now = now_iso()
    monitor = {
        "id": generate_id("MON"),
        "keywords": keywords,
        "sources": sources,
        "last_checked": now,
        "created_at": now,
        "active": True,
    }

    monitors.append(monitor)
    _save_monitors(monitors)

    output_success({
        "message": f"监控已创建，关键词: {', '.join(keywords)}",
        "monitor": monitor,
    })


def action_remove(data: Dict[str, Any]) -> None:
    """删除指定的主题监控。

    Args:
        data: 包含 id（监控 ID）的字典。
    """
    monitor_id = data.get("id", "").strip()
    if not monitor_id:
        output_error("请提供监控ID（id）", code="VALIDATION_ERROR")
        return

    monitors = _get_monitors()
    original_count = len(monitors)
    monitors = [m for m in monitors if m.get("id") != monitor_id]

    if len(monitors) == original_count:
        output_error(f"未找到监控: {monitor_id}", code="NOT_FOUND")
        return

    _save_monitors(monitors)

    # 同时删除相关结果
    results = _get_results()
    if monitor_id in results:
        del results[monitor_id]
        _save_results(results)

    output_success({"message": f"监控 {monitor_id} 已删除"})


def action_list(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有主题监控。"""
    monitors = _get_monitors()

    monitor_list = []
    for m in monitors:
        monitor_list.append({
            "id": m.get("id", ""),
            "keywords": m.get("keywords", []),
            "sources": m.get("sources", []),
            "last_checked": m.get("last_checked", ""),
            "created_at": m.get("created_at", ""),
            "active": m.get("active", True),
        })

    output_success({
        "total": len(monitor_list),
        "monitors": monitor_list,
    })


def action_check(data: Dict[str, Any]) -> None:
    """检查指定监控的新内容。

    Args:
        data: 包含 id（监控 ID）的字典。如果 id 为 "all" 则检查所有监控。
    """
    if not require_paid_feature("topic_monitor", "主题监控"):
        return

    monitor_id = data.get("id", "").strip()
    if not monitor_id:
        output_error("请提供监控ID（id）或 'all'", code="VALIDATION_ERROR")
        return

    monitors = _get_monitors()
    results = _get_results()

    check_list = []
    if monitor_id == "all":
        check_list = monitors
    else:
        monitor = _find_monitor(monitors, monitor_id)
        if not monitor:
            output_error(f"未找到监控: {monitor_id}", code="NOT_FOUND")
            return
        check_list = [monitor]

    check_results = {}
    now = now_iso()

    for monitor in check_list:
        mid = monitor.get("id", "")
        keywords = monitor.get("keywords", [])
        sources = monitor.get("sources", [])
        last_checked = monitor.get("last_checked", "")

        # 搜索新内容
        new_items = _simple_search(keywords, sources, last_checked)

        # 为每个结果添加检查时间
        for item in new_items:
            item["checked_at"] = now

        # 追加到结果缓存
        if mid not in results:
            results[mid] = []
        results[mid].extend(new_items)

        # 更新最后检查时间
        monitor["last_checked"] = now

        check_results[mid] = {
            "keywords": keywords,
            "new_count": len(new_items),
            "items": new_items[:10],
        }

    # 清理旧结果
    results = _cleanup_old_results(results)

    # 保存
    _save_monitors(monitors)
    _save_results(results)

    total_new = sum(cr["new_count"] for cr in check_results.values())

    output_success({
        "checked_monitors": len(check_list),
        "total_new_items": total_new,
        "details": check_results,
    })


def action_digest(data: Dict[str, Any]) -> None:
    """生成监控摘要报告。

    Args:
        data: 包含 period（daily/weekly）的字典。
    """
    if not require_paid_feature("topic_monitor", "主题监控"):
        return

    period = data.get("period", "daily").strip().lower()
    if period not in ("daily", "weekly"):
        output_error("period 参数必须为 daily 或 weekly", code="VALIDATION_ERROR")
        return

    monitors = _get_monitors()
    results = _get_results()

    if not monitors:
        output_error("暂无监控主题，请先添加监控", code="NO_MONITORS")
        return

    report = _generate_digest_markdown(monitors, results, period)

    output_success({
        "period": period,
        "monitor_count": len(monitors),
        "report": report,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh 主题监控管理")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "add": lambda: action_add(data or {}),
        "remove": lambda: action_remove(data or {}),
        "list": lambda: action_list(data),
        "check": lambda: action_check(data or {}),
        "digest": lambda: action_digest(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
