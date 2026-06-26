#!/usr/bin/env python3
"""
project-nerve Sprint 分析器（付费功能）

提供冲刺速度计算、任务漏斗分析、燃尽图数据生成和综合冲刺报告。
所有功能均需付费订阅。
"""

import json
import math
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    format_task_table,
    generate_bar_chart,
    generate_line_chart,
    generate_pie_chart,
    get_data_file,
    load_input_data,
    normalize_status,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    parse_date,
    read_json_file,
    require_paid_feature,
    today_str,
)


# ============================================================
# 数据文件路径
# ============================================================

TASKS_CACHE_FILE = "tasks_cache.json"


def _get_cached_tasks() -> List[Dict[str, Any]]:
    """读取缓存的任务数据。"""
    data = read_json_file(get_data_file(TASKS_CACHE_FILE))
    if isinstance(data, list):
        return data
    return []


# ============================================================
# 时间范围辅助
# ============================================================

def _parse_date_range(data: Dict[str, Any]) -> tuple:
    """解析时间范围参数。

    支持 start_date/end_date 或 days（最近N天）。

    Args:
        data: 包含时间范围参数的字典。

    Returns:
        (start_dt, end_dt) 元组。
    """
    now = datetime.now()

    if data.get("start_date") and data.get("end_date"):
        start_dt = parse_date(data["start_date"]) or (now - timedelta(days=14))
        end_dt = parse_date(data["end_date"]) or now
    else:
        days = int(data.get("days", 14))
        start_dt = now - timedelta(days=days)
        end_dt = now

    return start_dt, end_dt


def _filter_by_date_range(
    tasks: List[Dict[str, Any]],
    start_dt: datetime,
    end_dt: datetime,
    date_field: str = "updated_at",
) -> List[Dict[str, Any]]:
    """根据时间范围过滤任务。

    Args:
        tasks: 任务列表。
        start_dt: 开始时间。
        end_dt: 结束时间。
        date_field: 用于比较的日期字段名。

    Returns:
        过滤后的任务列表。
    """
    result = []
    for task in tasks:
        dt = parse_date(task.get(date_field, ""))
        if dt and start_dt <= dt <= end_dt:
            result.append(task)
    return result


# ============================================================
# 操作实现
# ============================================================

def velocity(data: Dict[str, Any]) -> None:
    """计算冲刺速度。

    速度 = 指定时间范围内已完成的任务数量。
    同时计算每日平均完成量和趋势。

    Args:
        data: 包含时间范围参数的字典。
    """
    if not require_paid_feature("sprint_analytics", "冲刺分析"):
        return

    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 task_aggregator fetch-all 获取任务", code="NO_DATA")
        return

    start_dt, end_dt = _parse_date_range(data)
    total_days = max((end_dt - start_dt).days, 1)

    # 过滤时间范围内的已完成任务
    completed_tasks = [
        t for t in tasks
        if t.get("status") == "已完成"
    ]
    completed_in_range = _filter_by_date_range(completed_tasks, start_dt, end_dt)

    # 按天统计完成数量
    daily_counts = {}
    for task in completed_in_range:
        dt = parse_date(task.get("updated_at", ""))
        if dt:
            day_key = dt.strftime("%Y-%m-%d")
            daily_counts[day_key] = daily_counts.get(day_key, 0) + 1

    # 填充空日期
    current = start_dt
    daily_data = []
    while current <= end_dt:
        day_key = current.strftime("%Y-%m-%d")
        count = daily_counts.get(day_key, 0)
        daily_data.append({"label": day_key[-5:], "value": count})  # MM-DD 格式
        current += timedelta(days=1)

    total_completed = len(completed_in_range)
    daily_avg = round(total_completed / total_days, 1) if total_days > 0 else 0

    # 按平台统计
    source_stats = {}
    for task in completed_in_range:
        src = task.get("source", "未知")
        source_stats[src] = source_stats.get(src, 0) + 1

    # 生成速度趋势图
    chart = ""
    if daily_data:
        chart = generate_line_chart("每日完成任务数趋势", daily_data, x_label="日期", y_label="完成数")

    output_success({
        "sprint_period": f"{start_dt.strftime('%Y-%m-%d')} ~ {end_dt.strftime('%Y-%m-%d')}",
        "total_days": total_days,
        "total_completed": total_completed,
        "daily_average": daily_avg,
        "source_stats": source_stats,
        "daily_data": daily_data,
        "chart": chart,
    })


def funnel(data: Dict[str, Any]) -> None:
    """任务漏斗分析。

    统计各状态的任务数量和占比：待办 → 进行中 → 已完成。

    Args:
        data: 可选参数（可指定 platform 过滤）。
    """
    if not require_paid_feature("sprint_analytics", "冲刺分析"):
        return

    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 task_aggregator fetch-all 获取任务", code="NO_DATA")
        return

    # 可选平台过滤
    platform = data.get("platform", "").strip().lower() if data else ""
    if platform:
        tasks = [t for t in tasks if t.get("source") == platform]

    total = len(tasks)
    if total == 0:
        output_error("过滤后无任务数据", code="NO_DATA")
        return

    # 统计各状态
    status_counts = {"待办": 0, "进行中": 0, "已完成": 0, "已关闭": 0}
    for task in tasks:
        status = task.get("status", "待办")
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts["待办"] += 1

    # 计算百分比
    funnel_data = []
    for status in ["待办", "进行中", "已完成", "已关闭"]:
        count = status_counts[status]
        pct = round(count / total * 100, 1) if total > 0 else 0
        funnel_data.append({
            "status": status,
            "count": count,
            "percentage": pct,
        })

    # 生成饼图
    pie_data = [{"label": item["status"], "value": item["count"]} for item in funnel_data if item["count"] > 0]
    pie_chart = generate_pie_chart("任务状态分布", pie_data)

    # 生成柱状图
    bar_data = [{"label": item["status"], "value": item["count"]} for item in funnel_data]
    bar_chart = generate_bar_chart("任务漏斗", bar_data, x_label="状态", y_label="数量")

    # 计算转化率
    todo_count = status_counts["待办"]
    in_progress_count = status_counts["进行中"]
    done_count = status_counts["已完成"]

    start_to_progress = round(in_progress_count / (todo_count + in_progress_count + done_count) * 100, 1) if total > 0 else 0
    progress_to_done = round(done_count / max(in_progress_count + done_count, 1) * 100, 1)

    output_success({
        "total": total,
        "funnel": funnel_data,
        "conversion": {
            "启动率": f"{start_to_progress}%",
            "完成率": f"{progress_to_done}%",
        },
        "pie_chart": pie_chart,
        "bar_chart": bar_chart,
    })


def burndown(data: Dict[str, Any]) -> None:
    """生成燃尽图数据。

    计算指定时间范围内，每天剩余待完成任务的数量变化。

    Args:
        data: 包含时间范围参数的字典。
    """
    if not require_paid_feature("mermaid_chart", "Mermaid 图表"):
        return

    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 task_aggregator fetch-all 获取任务", code="NO_DATA")
        return

    start_dt, end_dt = _parse_date_range(data)
    total_days = max((end_dt - start_dt).days, 1)

    # 计算总任务数（排除已关闭）
    active_tasks = [t for t in tasks if t.get("status") != "已关闭"]
    total_tasks = len(active_tasks)

    # 统计每天完成数量（累计）
    completed_by_day = {}
    for task in active_tasks:
        if task.get("status") == "已完成":
            dt = parse_date(task.get("updated_at", ""))
            if dt:
                day_key = dt.strftime("%Y-%m-%d")
                completed_by_day[day_key] = completed_by_day.get(day_key, 0) + 1

    # 生成燃尽数据
    burndown_data = []
    ideal_data = []
    cumulative_completed = 0
    current = start_dt

    day_index = 0
    while current <= end_dt:
        day_key = current.strftime("%Y-%m-%d")
        cumulative_completed += completed_by_day.get(day_key, 0)
        remaining = total_tasks - cumulative_completed

        burndown_data.append({
            "label": day_key[-5:],
            "value": max(remaining, 0),
        })

        # 理想燃尽线
        ideal_remaining = total_tasks - (total_tasks * day_index / total_days)
        ideal_data.append({
            "label": day_key[-5:],
            "value": round(max(ideal_remaining, 0), 1),
        })

        current += timedelta(days=1)
        day_index += 1

    # 生成 Mermaid xychart-beta（实际 + 理想）
    chart_lines = ["```mermaid", "xychart-beta", '    title "冲刺燃尽图"']

    labels = [f'"{d["label"]}"' for d in burndown_data]
    chart_lines.append(f'    x-axis [{", ".join(labels)}]')
    chart_lines.append('    y-axis "剩余任务数"')

    actual_values = [str(d["value"]) for d in burndown_data]
    chart_lines.append(f'    line [{", ".join(actual_values)}]')

    ideal_values = [str(d["value"]) for d in ideal_data]
    chart_lines.append(f'    line [{", ".join(ideal_values)}]')

    chart_lines.append("```")
    chart = "\n".join(chart_lines)

    output_success({
        "sprint_period": f"{start_dt.strftime('%Y-%m-%d')} ~ {end_dt.strftime('%Y-%m-%d')}",
        "total_tasks": total_tasks,
        "completed": cumulative_completed,
        "remaining": total_tasks - cumulative_completed,
        "burndown_data": burndown_data,
        "ideal_data": ideal_data,
        "chart": chart,
    })


def sprint_report(data: Dict[str, Any]) -> None:
    """生成综合冲刺报告。

    包含速度、漏斗、燃尽等多维度分析的 Markdown 报告。

    Args:
        data: 包含时间范围参数的字典。
    """
    if not require_paid_feature("sprint_analytics", "冲刺分析"):
        return

    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 task_aggregator fetch-all 获取任务", code="NO_DATA")
        return

    start_dt, end_dt = _parse_date_range(data)
    total_days = max((end_dt - start_dt).days, 1)
    period_str = f"{start_dt.strftime('%Y-%m-%d')} ~ {end_dt.strftime('%Y-%m-%d')}"

    # 排除已关闭
    active_tasks = [t for t in tasks if t.get("status") != "已关闭"]
    total_tasks = len(active_tasks)

    # 状态统计
    status_counts = {"待办": 0, "进行中": 0, "已完成": 0}
    for task in active_tasks:
        status = task.get("status", "待办")
        if status in status_counts:
            status_counts[status] += 1

    # 范围内完成的任务
    completed_in_range = _filter_by_date_range(
        [t for t in active_tasks if t.get("status") == "已完成"],
        start_dt, end_dt
    )
    velocity_value = len(completed_in_range)
    daily_avg = round(velocity_value / total_days, 1)

    # 优先级分布
    priority_counts = {"紧急": 0, "高": 0, "中": 0, "低": 0}
    for task in active_tasks:
        prio = task.get("priority", "中")
        if prio in priority_counts:
            priority_counts[prio] += 1

    # 平台分布
    source_counts = {}
    for task in active_tasks:
        src = task.get("source", "未知")
        source_counts[src] = source_counts.get(src, 0) + 1

    # 逾期任务
    from utils import is_overdue as _is_overdue
    overdue_tasks = [
        t for t in active_tasks
        if t.get("status") not in ("已完成",) and t.get("due_date") and _is_overdue(t["due_date"])
    ]

    # 构建 Markdown 报告
    report_parts = []
    report_parts.append(f"# 冲刺报告 — {period_str}\n")
    report_parts.append(f"统计周期: {period_str} | 总计 {total_days} 天\n")

    # 核心指标
    report_parts.append("## 核心指标\n")
    report_parts.append("| 指标 | 数值 |")
    report_parts.append("|------|------|")
    report_parts.append(f"| 总任务数 | {total_tasks} |")
    report_parts.append(f"| 本期完成 | {velocity_value} |")
    report_parts.append(f"| 日均完成 | {daily_avg} |")
    report_parts.append(f"| 待办任务 | {status_counts['待办']} |")
    report_parts.append(f"| 进行中 | {status_counts['进行中']} |")
    report_parts.append(f"| 逾期任务 | {len(overdue_tasks)} |")
    report_parts.append("")

    # 完成率
    completion_rate = round(status_counts["已完成"] / total_tasks * 100, 1) if total_tasks > 0 else 0
    report_parts.append(f"**整体完成率**: {completion_rate}%\n")

    # 状态分布饼图
    status_pie_data = [
        {"label": k, "value": v} for k, v in status_counts.items() if v > 0
    ]
    if status_pie_data:
        report_parts.append("## 状态分布\n")
        report_parts.append(generate_pie_chart("任务状态分布", status_pie_data))
        report_parts.append("")

    # 优先级分布柱状图
    priority_bar_data = [
        {"label": k, "value": v} for k, v in priority_counts.items() if v > 0
    ]
    if priority_bar_data:
        report_parts.append("## 优先级分布\n")
        report_parts.append(generate_bar_chart("任务优先级分布", priority_bar_data, x_label="优先级", y_label="数量"))
        report_parts.append("")

    # 平台分布
    if source_counts:
        report_parts.append("## 平台分布\n")
        report_parts.append("| 平台 | 任务数 | 占比 |")
        report_parts.append("|------|--------|------|")
        for src, cnt in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            pct = round(cnt / total_tasks * 100, 1) if total_tasks > 0 else 0
            report_parts.append(f"| {src} | {cnt} | {pct}% |")
        report_parts.append("")

    # 逾期任务列表
    if overdue_tasks:
        report_parts.append("## 逾期任务\n")
        report_parts.append(format_task_table(overdue_tasks[:10]))
        if len(overdue_tasks) > 10:
            report_parts.append(f"\n> 仅显示前 10 个，共 {len(overdue_tasks)} 个逾期任务。")
        report_parts.append("")

    # 建议
    report_parts.append("## 改进建议\n")
    suggestion_idx = 1
    if len(overdue_tasks) > 0:
        report_parts.append(f"{suggestion_idx}. 当前有 {len(overdue_tasks)} 个逾期任务，建议优先处理或重新评估截止日期。")
        suggestion_idx += 1
    if priority_counts.get("紧急", 0) > 3:
        report_parts.append(f"{suggestion_idx}. 紧急任务数量较多（{priority_counts['紧急']} 个），建议评估是否存在优先级膨胀问题。")
        suggestion_idx += 1
    if completion_rate < 50:
        report_parts.append(f"{suggestion_idx}. 整体完成率仅 {completion_rate}%，建议分析瓶颈环节并调整冲刺范围。")
        suggestion_idx += 1
    if daily_avg < 1:
        report_parts.append(f"{suggestion_idx}. 日均完成量较低（{daily_avg}），建议检查任务拆分粒度或团队产能。")
        suggestion_idx += 1
    if suggestion_idx == 1:
        report_parts.append("各项指标表现良好，建议继续保持当前节奏。")
    report_parts.append("")

    report_parts.append(f"---\n*报告由 project-nerve 自动生成 — {now_iso()}*")

    report_md = "\n".join(report_parts)

    output_success({
        "report": report_md,
        "summary": {
            "period": period_str,
            "total_tasks": total_tasks,
            "velocity": velocity_value,
            "daily_average": daily_avg,
            "completion_rate": completion_rate,
            "overdue_count": len(overdue_tasks),
        },
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve Sprint 分析器")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "velocity": lambda: velocity(data or {}),
        "funnel": lambda: funnel(data or {}),
        "burndown": lambda: burndown(data or {}),
        "report": lambda: sprint_report(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
