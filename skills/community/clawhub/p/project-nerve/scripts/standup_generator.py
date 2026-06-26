#!/usr/bin/env python3
"""
project-nerve 站会报告生成器

扫描最近的任务活动，生成每日站会和每周总结报告。
支持跨平台汇总，输出格式化 Markdown。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    format_task_table,
    get_data_file,
    is_overdue,
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
# 时间过滤辅助
# ============================================================

def _tasks_updated_since(tasks: List[Dict[str, Any]], since: datetime) -> List[Dict[str, Any]]:
    """过滤出指定时间之后有更新的任务。

    Args:
        tasks: 任务列表。
        since: 起始时间。

    Returns:
        过滤后的任务列表。
    """
    result = []
    for task in tasks:
        dt = parse_date(task.get("updated_at", ""))
        if dt and dt >= since:
            result.append(task)
    return result


def _tasks_by_status(tasks: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """按状态过滤任务。"""
    return [t for t in tasks if t.get("status") == status]


def _task_summary_line(task: Dict[str, Any]) -> str:
    """生成单个任务的摘要行。

    Args:
        task: 任务字典。

    Returns:
        格式化的摘要行字符串。
    """
    title = task.get("title", "无标题")
    if len(title) > 50:
        title = title[:47] + "..."
    source = task.get("source", "")
    priority = task.get("priority", "")
    assignee = task.get("assignee", "")

    parts = [f"**{title}**"]
    if source:
        parts.append(f"[{source}]")
    if priority and priority in ("紧急", "高"):
        parts.append(f"({priority})")
    if assignee:
        parts.append(f"@{assignee}")

    return " ".join(parts)


# ============================================================
# 操作实现
# ============================================================

def daily_standup(data: Optional[Dict[str, Any]] = None) -> None:
    """生成每日站会报告。

    扫描过去 24 小时的任务活动，生成标准站会格式：
    - 昨日完成
    - 今日计划
    - 阻碍事项

    Args:
        data: 可选参数（assignee 过滤）。
    """
    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 task_aggregator fetch-all 获取任务", code="NO_DATA")
        return

    now = datetime.now()
    yesterday = now - timedelta(hours=24)
    today_date = today_str()

    # 可选：按负责人过滤
    assignee = ""
    if data:
        assignee = data.get("assignee", "").strip()
    if assignee:
        tasks = [t for t in tasks if assignee.lower() in (t.get("assignee") or "").lower()]

    # 最近 24 小时有更新的任务
    recent_tasks = _tasks_updated_since(tasks, yesterday)

    # 昨日完成：最近 24h 内状态变为已完成的任务
    completed = _tasks_by_status(recent_tasks, "已完成")

    # 今日计划：当前进行中 + 待办（按优先级排序，取前 10）
    in_progress = _tasks_by_status(tasks, "进行中")
    todo_tasks = _tasks_by_status(tasks, "待办")
    priority_order = {"紧急": 0, "高": 1, "中": 2, "低": 3}
    planned = sorted(
        in_progress + todo_tasks,
        key=lambda t: priority_order.get(t.get("priority", "中"), 2)
    )[:10]

    # 阻碍事项：逾期或紧急未完成
    blockers = []
    for task in tasks:
        if task.get("status") in ("已完成", "已关闭"):
            continue
        reasons = []
        if task.get("due_date") and is_overdue(task["due_date"]):
            reasons.append(f"逾期（截止: {task['due_date']}）")
        if task.get("priority") == "紧急" and task.get("status") == "进行中":
            reasons.append("紧急任务进行中")
        if reasons:
            blockers.append({"task": task, "reasons": reasons})

    # 构建 Markdown 报告
    report_parts = []
    title_suffix = f" — {assignee}" if assignee else ""
    report_parts.append(f"# 每日站会{title_suffix} — {today_date}\n")

    # 昨日完成
    report_parts.append("## 昨日完成\n")
    if completed:
        for task in completed:
            report_parts.append(f"- {_task_summary_line(task)}")
    else:
        report_parts.append("- （暂无完成任务）")
    report_parts.append("")

    # 今日计划
    report_parts.append("## 今日计划\n")
    if planned:
        for task in planned:
            status_tag = "进行中" if task.get("status") == "进行中" else "待启动"
            report_parts.append(f"- [{status_tag}] {_task_summary_line(task)}")
    else:
        report_parts.append("- （暂无计划任务）")
    report_parts.append("")

    # 阻碍事项
    report_parts.append("## 阻碍事项\n")
    if blockers:
        for item in blockers:
            task = item["task"]
            reasons = "、".join(item["reasons"])
            report_parts.append(f"- {_task_summary_line(task)} — {reasons}")
    else:
        report_parts.append("- （暂无阻碍）")
    report_parts.append("")

    # 统计摘要
    report_parts.append("---")
    report_parts.append(f"完成 {len(completed)} | 计划 {len(planned)} | 阻碍 {len(blockers)}")
    report_parts.append(f"\n*由 project-nerve 自动生成 — {now_iso()}*")

    report_md = "\n".join(report_parts)

    output_success({
        "report": report_md,
        "summary": {
            "date": today_date,
            "completed_count": len(completed),
            "planned_count": len(planned),
            "blocker_count": len(blockers),
        },
    })


def weekly_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成每周总结报告。

    扫描过去 7 天的任务活动，生成周报格式：
    - 本周完成
    - 进行中
    - 下周计划

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("standup_report", "周报生成"):
        return

    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 task_aggregator fetch-all 获取任务", code="NO_DATA")
        return

    now = datetime.now()
    week_ago = now - timedelta(days=7)
    today_date = today_str()
    week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")

    # 可选：按负责人过滤
    assignee = ""
    if data:
        assignee = data.get("assignee", "").strip()
    if assignee:
        tasks = [t for t in tasks if assignee.lower() in (t.get("assignee") or "").lower()]

    # 本周有更新的任务
    recent_tasks = _tasks_updated_since(tasks, week_ago)

    # 本周完成
    completed = _tasks_by_status(recent_tasks, "已完成")

    # 进行中
    in_progress = _tasks_by_status(tasks, "进行中")

    # 下周计划（待办按优先级排序取前 15）
    todo_tasks = _tasks_by_status(tasks, "待办")
    priority_order = {"紧急": 0, "高": 1, "中": 2, "低": 3}
    next_week_plan = sorted(
        todo_tasks,
        key=lambda t: priority_order.get(t.get("priority", "中"), 2)
    )[:15]

    # 按平台统计完成情况
    source_completed = {}
    for task in completed:
        src = task.get("source", "未知")
        source_completed[src] = source_completed.get(src, 0) + 1

    # 按优先级统计进行中任务
    priority_in_progress = {}
    for task in in_progress:
        prio = task.get("priority", "中")
        priority_in_progress[prio] = priority_in_progress.get(prio, 0) + 1

    # 逾期统计
    overdue_tasks = [
        t for t in tasks
        if t.get("status") not in ("已完成", "已关闭") and t.get("due_date") and is_overdue(t["due_date"])
    ]

    # 构建 Markdown 报告
    report_parts = []
    title_suffix = f" — {assignee}" if assignee else ""
    report_parts.append(f"# 周报{title_suffix} — {week_start} ~ {today_date}\n")

    # 概览
    report_parts.append("## 本周概览\n")
    report_parts.append("| 指标 | 数值 |")
    report_parts.append("|------|------|")
    report_parts.append(f"| 本周完成 | {len(completed)} |")
    report_parts.append(f"| 进行中 | {len(in_progress)} |")
    report_parts.append(f"| 待办 | {len(todo_tasks)} |")
    report_parts.append(f"| 逾期 | {len(overdue_tasks)} |")
    report_parts.append("")

    # 本周完成
    report_parts.append("## 本周完成\n")
    if completed:
        for task in completed:
            report_parts.append(f"- {_task_summary_line(task)}")
        report_parts.append("")
        # 平台分布
        if source_completed:
            report_parts.append("**按平台统计**:")
            for src, cnt in sorted(source_completed.items(), key=lambda x: x[1], reverse=True):
                report_parts.append(f"- {src}: {cnt} 个")
    else:
        report_parts.append("- （本周暂无完成任务）")
    report_parts.append("")

    # 进行中
    report_parts.append("## 进行中\n")
    if in_progress:
        for task in in_progress[:10]:
            report_parts.append(f"- {_task_summary_line(task)}")
        if len(in_progress) > 10:
            report_parts.append(f"- ...等共 {len(in_progress)} 个任务")
    else:
        report_parts.append("- （暂无进行中任务）")
    report_parts.append("")

    # 下周计划
    report_parts.append("## 下周计划\n")
    if next_week_plan:
        for task in next_week_plan:
            report_parts.append(f"- {_task_summary_line(task)}")
    else:
        report_parts.append("- （暂无计划任务）")
    report_parts.append("")

    # 风险提醒
    if overdue_tasks:
        report_parts.append("## 风险提醒\n")
        for task in overdue_tasks[:5]:
            report_parts.append(f"- {_task_summary_line(task)} — 逾期（截止: {task.get('due_date', '')}）")
        if len(overdue_tasks) > 5:
            report_parts.append(f"- ...等共 {len(overdue_tasks)} 个逾期任务")
        report_parts.append("")

    report_parts.append(f"---\n*由 project-nerve 自动生成 — {now_iso()}*")

    report_md = "\n".join(report_parts)

    output_success({
        "report": report_md,
        "summary": {
            "period": f"{week_start} ~ {today_date}",
            "completed_count": len(completed),
            "in_progress_count": len(in_progress),
            "todo_count": len(todo_tasks),
            "overdue_count": len(overdue_tasks),
        },
    })


def generate_standup(data: Optional[Dict[str, Any]] = None) -> None:
    """智能生成站会报告（自动选择日报或周报）。

    如果是周一，生成周报；否则生成日报。

    Args:
        data: 可选参数。
    """
    now = datetime.now()
    report_type = "daily"
    if data:
        report_type = data.get("type", "daily").strip().lower()

    # 周一自动切换为周报
    if report_type == "auto":
        if now.weekday() == 0:  # 周一
            report_type = "weekly"
        else:
            report_type = "daily"

    if report_type == "weekly":
        weekly_report(data)
    else:
        daily_standup(data)


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve 站会报告生成器")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "daily": lambda: daily_standup(data),
        "weekly": lambda: weekly_report(data),
        "generate": lambda: generate_standup(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
