#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目看板脚本 - 扫描项目管理库，生成状态总览

使用方法:
    python dashboard.py              # 终端输出
    python dashboard.py --output dashboard.md  # 输出到文件
"""

import io
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Windows 终端 UTF-8 兼容
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 项目管理库根目录
PROJECTS_ROOT = Path(r"D:\projects-data")

# 排除的目录
EXCLUDE_DIRS = {"templates", "tools"}

# 有效状态值
VALID_STATUSES = {"待分发", "进行中", "待评审", "返工", "已验收"}


def parse_brief_md(brief_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    解析项目的 brief.md 文件，提取项目名称和优先级。
    
    Returns:
        (项目名称, 优先级) 或 (None, None)
    """
    try:
        content = brief_path.read_text(encoding="utf-8")
        
        # 提取项目名称: - **项目名称：** xxx
        name_match = re.search(r"-\s*\*\*项目名称[：:]\*\*\s*(.+?)(?:\n|$)", content)
        project_name = name_match.group(1).strip() if name_match else None
        
        # 提取优先级: - **优先级：** 高 / 中 / 低
        priority_match = re.search(r"-\s*\*\*优先级[：:]\*\*\s*(高|中|低)", content)
        priority = priority_match.group(1) if priority_match else None
        
        return project_name, priority
        
    except Exception as e:
        print(f"警告: 解析 brief.md 失败 [{brief_path}]: {e}", file=sys.stderr)
        return None, None


def parse_task_md(task_path: Path) -> Optional[Dict]:
    """
    解析任务规格书文件，提取任务信息。
    
    Returns:
        包含任务信息的字典，解析失败返回 None
    """
    try:
        content = task_path.read_text(encoding="utf-8")
        
        # 提取任务标题 (第一行 # xxx)
        title_match = re.search(r"^#\s+(.+?)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "未知任务"
        
        # 提取任务编号
        task_id_match = re.search(r"-\s*\*\*任务编号[：:]\*\*\s*(TASK-\d+)", content)
        task_id = task_id_match.group(1) if task_id_match else None
        
        # 提取指派人
        assignee_match = re.search(r"-\s*\*\*指派给[：:]\*\*\s*(.+?)(?:\n|$)", content)
        assignee = assignee_match.group(1).strip() if assignee_match else "未指派"
        # 清理 markdown 格式（如 _(agent 名称)_）
        assignee = re.sub(r"[_\[\]]", "", assignee).strip()
        
        # 提取优先级
        priority_match = re.search(r"-\s*\*\*优先级[：:]\*\*\s*(高|中|低)", content)
        priority = priority_match.group(1) if priority_match else "未知"
        
        # 提取状态
        status_match = re.search(r"-\s*\*\*状态[：:]\*\*\s*(.+?)(?:\n|$)", content)
        if status_match:
            status = status_match.group(1).strip()
            # 只取有效状态部分（如 "待分发 / 进行中" 只取第一个）
            status = status.split("/")[0].strip()
            # 验证状态是否有效
            if status not in VALID_STATUSES:
                print(f"警告: 任务 {task_path.name} 状态无效: {status}", file=sys.stderr)
                status = "未知"
        else:
            status = "未知"
        
        return {
            "task_id": task_id or task_path.stem.split("-")[0],
            "assignee": assignee,
            "priority": priority,
            "status": status,
            "title": title,
        }
        
    except Exception as e:
        print(f"警告: 解析任务文件失败 [{task_path}]: {e}", file=sys.stderr)
        return None


def scan_projects() -> List[Dict]:
    """
    扫描项目目录，收集所有项目和任务信息。
    
    Returns:
        项目列表，每个项目包含名称、优先级和任务列表
    """
    projects = []
    
    if not PROJECTS_ROOT.exists():
        print(f"警告: 项目目录不存在 [{PROJECTS_ROOT}]", file=sys.stderr)
        return projects
    
    for item in PROJECTS_ROOT.iterdir():
        # 跳过非目录和排除目录
        if not item.is_dir() or item.name in EXCLUDE_DIRS:
            continue
        
        # 解析 brief.md
        brief_path = item / "brief.md"
        if not brief_path.exists():
            print(f"警告: 项目缺少 brief.md [{item.name}]", file=sys.stderr)
            continue
        
        project_name, priority = parse_brief_md(brief_path)
        
        # 收集任务
        tasks = []
        tasks_dir = item / "tasks"
        if tasks_dir.exists() and tasks_dir.is_dir():
            for task_file in tasks_dir.iterdir():
                if task_file.name.startswith("TASK-") and task_file.suffix == ".md":
                    task_info = parse_task_md(task_file)
                    if task_info:
                        tasks.append(task_info)
        
        projects.append({
            "dir_name": item.name,
            "name": project_name or item.name,
            "priority": priority or "未知",
            "tasks": tasks,
        })
    
    return projects


def parse_task_registry(registry_path: Path) -> List[Dict]:
    """
    解析项目签到表，提取任务认领记录。
    
    Returns:
        签到表条目列表
    """
    entries = []
    try:
        content = registry_path.read_text(encoding="utf-8")
        # 匹配表格行：| TASK-XXX | 描述 | 认领人 | 状态 | 开始时间 | 过期时间 | 产出位置 |
        for line in content.split("\n"):
            line = line.strip()
            if not line.startswith("|") or line.startswith("| 任务") or line.startswith("|--") or "_(暂无)_" in line:
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 4:
                entries.append({
                    "task_id": cells[0],
                    "desc": cells[1] if len(cells) > 1 else "",
                    "assignee": cells[2] if len(cells) > 2 else "",
                    "status": cells[3] if len(cells) > 3 else "",
                    "start_time": cells[4] if len(cells) > 4 else "",
                    "expire_time": cells[5] if len(cells) > 5 else "",
                })
    except Exception as e:
        print(f"警告: 解析签到表失败 [{registry_path}]: {e}", file=sys.stderr)
    return entries


def check_consistency(projects: List[Dict]) -> List[str]:
    """
    检查各项目的签到表与 task-spec 状态一致性。
    
    Returns:
        问题列表
    """
    issues = []
    
    for project in projects:
        project_dir = PROJECTS_ROOT / project["dir_name"]
        registry_path = project_dir / "task-registry.md"
        
        # 收集 task-spec 的状态
        task_statuses = {t["task_id"]: t["status"] for t in project["tasks"]}
        
        # 检查签到表
        if registry_path.exists():
            registry_entries = parse_task_registry(registry_path)
            registry_ids = {e["task_id"] for e in registry_entries}
            
            for entry in registry_entries:
                tid = entry["task_id"]
                reg_status = entry["status"]
                
                # 签到表有但 task-spec 没有
                if tid not in task_statuses:
                    issues.append(f"[{project['name']}] 签到表有 {tid} 但找不到对应的 task-spec")
                
                # 状态矛盾检查
                elif tid in task_statuses:
                    spec_status = task_statuses[tid]
                    # task-spec 已验收但签到表还在进行中
                    if spec_status == "已验收" and reg_status in ("认领中", "进行中"):
                        issues.append(f"[{project['name']}] {tid} task-spec 已验收，但签到表状态仍为「{reg_status}」")
                    # task-spec 待分发但签到表已认领
                    if spec_status == "待分发" and reg_status in ("认领中", "进行中"):
                        issues.append(f"[{project['name']}] {tid} task-spec 待分发，但签到表状态为「{reg_status}」")
            
            # task-spec 进行中但签到表没登记
            for tid, status in task_statuses.items():
                if status == "进行中" and tid not in registry_ids:
                    issues.append(f"[{project['name']}] {tid} 正在进行但未在签到表登记")
        else:
            # 有进行中的任务但没有签到表
            active_tasks = [t for t in project["tasks"] if t["status"] in ("进行中", "待评审")]
            if active_tasks:
                issues.append(f"[{project['name']}] 有 {len(active_tasks)} 个活跃任务但项目目录下没有 task-registry.md")
    
    return issues


def generate_dashboard(projects: List[Dict]) -> str:
    """
    生成看板输出内容。
    
    Args:
        projects: 项目列表
        
    Returns:
        格式化的看板字符串
    """
    lines = []
    
    # 标题和时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines.append("=== 项目看板 ===")
    lines.append(f"生成时间：{now}")
    lines.append("")
    
    # 无项目提示
    if not projects:
        lines.append("暂无活跃项目")
        return "\n".join(lines) + "\n"
    
    # 统计计数
    status_counts = {status: 0 for status in VALID_STATUSES}
    status_counts["未知"] = 0
    
    # 项目和任务
    for project in projects:
        # 项目标题行
        lines.append(f"📁 {project['name']} [优先级: {project['priority']}]")
        
        # 任务列表
        for task in project["tasks"]:
            task_line = f"  {task['task_id']} | {task['assignee']} | {task['priority']} | {task['status']} | {task['title']}"
            lines.append(task_line)
            
            # 统计
            if task["status"] in status_counts:
                status_counts[task["status"]] += 1
            else:
                status_counts["未知"] += 1
        
        lines.append("")
    
    # 统计汇总
    lines.append("📊 统计")
    stats_parts = []
    for status in ["待分发", "进行中", "待评审", "返工", "已验收"]:
        if status_counts[status] > 0:
            stats_parts.append(f"{status}: {status_counts[status]}")
    if status_counts["未知"] > 0:
        stats_parts.append(f"未知: {status_counts['未知']}")
    
    lines.append(f"  {' | '.join(stats_parts) if stats_parts else '暂无任务'}")
    
    # 一致性检查
    issues = check_consistency(projects)
    if issues:
        lines.append("")
        lines.append("⚠️  一致性问题")
        for issue in issues:
            lines.append(f"  - {issue}")
    else:
        lines.append("")
        lines.append("✅ 签到表与任务状态一致")
    
    return "\n".join(lines) + "\n"


def main():
    """主函数"""
    # 解析命令行参数
    output_file = None
    args = sys.argv[1:]
    
    if "--output" in args:
        try:
            output_idx = args.index("--output")
            output_file = args[output_idx + 1]
        except (ValueError, IndexError):
            print("错误: --output 参数需要指定文件名", file=sys.stderr)
            sys.exit(1)
    
    # 扫描项目
    projects = scan_projects()
    
    # 生成看板
    dashboard = generate_dashboard(projects)
    
    # 输出
    if output_file:
        output_path = Path(output_file)
        # 确保父目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(dashboard, encoding="utf-8")
        print(f"看板已输出到: {output_path}")
    else:
        print(dashboard)


if __name__ == "__main__":
    main()

