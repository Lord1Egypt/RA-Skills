#!/usr/bin/env python3
"""
knowledge-mesh 搜索报告导出模块

支持将搜索结果导出为 Markdown 报告、CSV 文件，
生成趋势分析图表和使用统计。

用法:
    python3 report_exporter.py --action export-markdown --data '{"query":"...","results":[...]}'
    python3 report_exporter.py --action export-csv --data '{"results":[...]}'
    python3 report_exporter.py --action trending --data '{"results":[...]}'
    python3 report_exporter.py --action stats
"""

import csv
import io
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    SOURCE_DISPLAY_NAMES,
    check_subscription,
    format_source_badge,
    get_data_file,
    highlight_match,
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

# 搜索历史文件
SEARCH_HISTORY_FILE = "search_history.json"

# 导出统计文件
EXPORT_STATS_FILE = "export_stats.json"


# ============================================================
# 搜索历史管理
# ============================================================

def _get_search_history() -> List[Dict[str, Any]]:
    """读取搜索历史记录。"""
    data = read_json_file(get_data_file(SEARCH_HISTORY_FILE))
    if isinstance(data, list):
        return data
    return []


def _save_search_history(history: List[Dict[str, Any]]) -> None:
    """保存搜索历史记录。"""
    # 最多保留 500 条记录
    write_json_file(get_data_file(SEARCH_HISTORY_FILE), history[-500:])


def _record_export(export_type: str, count: int) -> None:
    """记录导出操作到统计数据。

    Args:
        export_type: 导出类型。
        count: 导出记录数。
    """
    stats_file = get_data_file(EXPORT_STATS_FILE)
    stats = read_json_file(stats_file)
    if not isinstance(stats, dict):
        stats = {"exports": [], "total_exports": 0}

    stats["exports"].append({
        "type": export_type,
        "count": count,
        "timestamp": now_iso(),
    })
    stats["total_exports"] = stats.get("total_exports", 0) + 1

    # 最多保留最近 200 条导出记录
    stats["exports"] = stats["exports"][-200:]

    write_json_file(stats_file, stats)


# ============================================================
# Markdown 报告生成
# ============================================================

def _generate_markdown_report(
    query: str,
    results: List[Dict[str, Any]],
    title: Optional[str] = None,
) -> str:
    """生成 Markdown 格式的搜索报告。

    Args:
        query: 搜索查询。
        results: 搜索结果列表。
        title: 可选的报告标题。

    Returns:
        Markdown 报告字符串。
    """
    report_title = title or f"知识搜索报告: {query}"
    today = today_str()

    parts = []
    parts.append(f"# {report_title}\n")
    parts.append(f"**查询关键词**: {query}")
    parts.append(f"**搜索时间**: {now_iso()}")
    parts.append(f"**结果总数**: {len(results)} 条\n")

    # 来源分布统计
    source_counts = Counter()
    for r in results:
        source_counts[r.get("source", "unknown")] += 1

    if source_counts:
        parts.append("## 来源分布\n")
        parts.append("| 来源 | 结果数 |")
        parts.append("|------|--------|")
        for source, count in source_counts.most_common():
            display = SOURCE_DISPLAY_NAMES.get(source, source)
            parts.append(f"| {display} | {count} |")
        parts.append("")

    # 搜索结果详情
    parts.append("## 搜索结果\n")

    for idx, r in enumerate(results, 1):
        source = r.get("source", "")
        badge = format_source_badge(source)
        result_title = r.get("title", "无标题")
        url = r.get("url", "")
        snippet = r.get("snippet", "")
        author = r.get("author", "")
        created = r.get("created_at", "")
        score = r.get("_combined_score", r.get("score", 0))
        tags = r.get("tags", [])

        # 高亮查询词
        highlighted_title = highlight_match(result_title, query)
        highlighted_snippet = highlight_match(truncate_text(snippet, 250), query)

        parts.append(f"### {idx}. {badge} {highlighted_title}\n")

        if url:
            parts.append(f"- **链接**: [{url}]({url})")
        if author:
            parts.append(f"- **作者**: {author}")
        if created:
            parts.append(f"- **发布日期**: {created}")
        if isinstance(score, (int, float)) and score > 0:
            parts.append(f"- **相关度**: {score:.2f}")
        if tags:
            tag_str = ", ".join(f"`{t}`" for t in tags[:5])
            parts.append(f"- **标签**: {tag_str}")

        parts.append(f"\n> {highlighted_snippet}\n")

    # 页脚
    parts.append("---\n")
    parts.append(f"*报告由 knowledge-mesh 于 {now_iso()} 生成*")

    return "\n".join(parts)


# ============================================================
# CSV 导出
# ============================================================

def _generate_csv(results: List[Dict[str, Any]]) -> str:
    """将搜索结果导出为 CSV 格式。

    Args:
        results: 搜索结果列表。

    Returns:
        CSV 格式字符串。
    """
    fieldnames = [
        "source", "title", "url", "snippet", "author",
        "created_at", "score", "tags",
    ]

    output_buf = io.StringIO()
    writer = csv.DictWriter(output_buf, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        row = {
            "source": SOURCE_DISPLAY_NAMES.get(r.get("source", ""), r.get("source", "")),
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": truncate_text(r.get("snippet", ""), 200),
            "author": r.get("author", ""),
            "created_at": r.get("created_at", ""),
            "score": r.get("_combined_score", r.get("score", 0)),
            "tags": ", ".join(r.get("tags", [])),
        }
        writer.writerow(row)

    return output_buf.getvalue()


# ============================================================
# 趋势分析（付费功能）
# ============================================================

def _generate_trending_report(results: List[Dict[str, Any]]) -> str:
    """生成趋势分析报告，包含 Mermaid 图表。

    Args:
        results: 搜索结果列表。

    Returns:
        Markdown 格式的趋势报告。
    """
    parts = []
    parts.append("# 知识趋势分析报告\n")
    parts.append(f"**生成时间**: {now_iso()}")
    parts.append(f"**分析样本**: {len(results)} 条结果\n")

    # 来源分布饼图
    source_counts = Counter()
    for r in results:
        source_counts[r.get("source", "unknown")] += 1

    parts.append("## 来源分布\n")
    parts.append("```mermaid")
    parts.append("pie title 知识来源分布")
    for source, count in source_counts.most_common():
        display = SOURCE_DISPLAY_NAMES.get(source, source)
        parts.append(f'    "{display}" : {count}')
    parts.append("```\n")

    # 时间趋势（按周分组）
    week_counts = Counter()
    for r in results:
        created = r.get("created_at", "")
        if created:
            try:
                if "T" in created:
                    dt = datetime.strptime(created.split("T")[0], "%Y-%m-%d")
                else:
                    dt = datetime.strptime(created, "%Y-%m-%d")
                # 按周分组
                week_start = dt - timedelta(days=dt.weekday())
                week_key = week_start.strftime("%m/%d")
                week_counts[week_key] += 1
            except (ValueError, TypeError):
                continue

    if week_counts:
        # 按时间排序
        sorted_weeks = sorted(week_counts.items())
        recent_weeks = sorted_weeks[-8:]  # 最近 8 周

        parts.append("## 内容发布时间趋势\n")
        labels = [f'"{w[0]}"' for w in recent_weeks]
        values = [str(w[1]) for w in recent_weeks]

        parts.append("```mermaid")
        parts.append("xychart-beta")
        parts.append('    title "近期内容发布趋势"')
        parts.append(f'    x-axis [{", ".join(labels)}]')
        parts.append('    y-axis "内容数量"')
        parts.append(f'    bar [{", ".join(values)}]')
        parts.append("```\n")

    # 热门标签
    all_tags = []
    for r in results:
        all_tags.extend(r.get("tags", []))

    if all_tags:
        tag_counts = Counter(all_tags).most_common(15)

        parts.append("## 热门标签\n")
        parts.append("| 标签 | 出现次数 |")
        parts.append("|------|----------|")
        for tag, count in tag_counts:
            parts.append(f"| `{tag}` | {count} |")
        parts.append("")

        # Mermaid 柱状图展示 Top 10 标签
        top10_tags = tag_counts[:10]
        if top10_tags:
            tag_labels = [f'"{t[0]}"' for t in top10_tags]
            tag_values = [str(t[1]) for t in top10_tags]

            parts.append("```mermaid")
            parts.append("xychart-beta")
            parts.append('    title "Top 10 热门标签"')
            parts.append(f'    x-axis [{", ".join(tag_labels)}]')
            parts.append('    y-axis "出现次数"')
            parts.append(f'    bar [{", ".join(tag_values)}]')
            parts.append("```\n")

    # 高分结果
    scored = [r for r in results if r.get("score", 0) > 0 or r.get("_combined_score", 0) > 0]
    if scored:
        scored.sort(key=lambda r: r.get("_combined_score", r.get("score", 0)), reverse=True)
        top5 = scored[:5]

        parts.append("## 高相关度内容 Top 5\n")
        for idx, r in enumerate(top5, 1):
            badge = format_source_badge(r.get("source", ""))
            title = r.get("title", "无标题")
            url = r.get("url", "")
            score = r.get("_combined_score", r.get("score", 0))

            parts.append(f"{idx}. {badge} **{title}**")
            if url:
                parts.append(f"   - 链接: {url}")
            parts.append(f"   - 相关度: {score:.2f}")
        parts.append("")

    parts.append("---\n")
    parts.append("*由 knowledge-mesh 自动生成*")

    return "\n".join(parts)


# ============================================================
# 操作实现
# ============================================================

def action_export_markdown(data: Dict[str, Any]) -> None:
    """导出搜索结果为 Markdown 报告。

    Args:
        data: 包含 query、results 的字典，可选 title 和 file_path。
    """
    query = data.get("query", "")
    results = data.get("results", [])
    title = data.get("title")
    file_path = data.get("file_path")

    if not results:
        output_error("无搜索结果可导出", code="NO_DATA")
        return

    report = _generate_markdown_report(query, results, title)

    if file_path:
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report)
            _record_export("markdown", len(results))
            output_success({
                "message": f"报告已导出到 {file_path}",
                "file_path": file_path,
                "result_count": len(results),
            })
        except IOError as e:
            output_error(f"文件写入失败: {e}", code="IO_ERROR")
    else:
        _record_export("markdown", len(results))
        output_success({
            "report": report,
            "result_count": len(results),
        })


def action_export_csv(data: Dict[str, Any]) -> None:
    """导出搜索结果为 CSV 格式。

    Args:
        data: 包含 results 的字典，可选 file_path。
    """
    results = data.get("results", [])
    file_path = data.get("file_path")

    if not results:
        output_error("无搜索结果可导出", code="NO_DATA")
        return

    csv_content = _generate_csv(results)

    if file_path:
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                f.write(csv_content)
            _record_export("csv", len(results))
            output_success({
                "message": f"CSV 已导出到 {file_path}",
                "file_path": file_path,
                "result_count": len(results),
            })
        except IOError as e:
            output_error(f"文件写入失败: {e}", code="IO_ERROR")
    else:
        _record_export("csv", len(results))
        output_success({
            "csv": csv_content,
            "result_count": len(results),
        })


def action_trending(data: Dict[str, Any]) -> None:
    """生成趋势分析报告（付费功能）。

    Args:
        data: 包含 results 的字典。
    """
    if not require_paid_feature("mermaid_chart", "趋势图表分析"):
        return

    results = data.get("results", [])
    if not results:
        output_error("无搜索结果可分析", code="NO_DATA")
        return

    report = _generate_trending_report(results)

    output_success({
        "report": report,
        "result_count": len(results),
    })


def action_stats(data: Optional[Dict[str, Any]] = None) -> None:
    """显示搜索使用统计。"""
    # 读取使用量数据
    usage_file = get_data_file("usage.json")
    usage = read_json_file(usage_file)
    if not isinstance(usage, dict):
        usage = {}

    # 读取导出统计
    stats_file = get_data_file(EXPORT_STATS_FILE)
    export_stats = read_json_file(stats_file)
    if not isinstance(export_stats, dict):
        export_stats = {"exports": [], "total_exports": 0}

    # 搜索统计
    today = today_str()
    today_searches = usage.get(today, 0)
    total_searches = sum(usage.values())

    # 过去 7 天统计
    daily_stats = {}
    for i in range(7):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_stats[day] = usage.get(day, 0)

    # 检查订阅信息
    sub = check_subscription()
    daily_limit = sub.get("daily_searches", 10)
    remaining = max(0, daily_limit - today_searches) if daily_limit >= 0 else -1

    # 导出统计
    export_type_counts = Counter()
    for exp in export_stats.get("exports", []):
        export_type_counts[exp.get("type", "unknown")] += 1

    output_success({
        "subscription_tier": sub["tier"],
        "today_searches": today_searches,
        "daily_limit": daily_limit,
        "remaining_today": remaining,
        "total_searches_7d": total_searches,
        "daily_breakdown": daily_stats,
        "total_exports": export_stats.get("total_exports", 0),
        "export_by_type": dict(export_type_counts),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh 搜索报告导出")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "export-markdown": lambda: action_export_markdown(data or {}),
        "export-csv": lambda: action_export_csv(data or {}),
        "trending": lambda: action_trending(data or {}),
        "stats": lambda: action_stats(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
