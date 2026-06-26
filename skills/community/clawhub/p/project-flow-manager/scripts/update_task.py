#!/usr/bin/env python3
"""
更新任务
用法: python3 update_task.py <project-id> <task-id> [--progress N] [--status STATUS]
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def update_task(project_id, task_id, progress=None, status=None, notes=None, blockers=None):
    """更新任务信息"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return False
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    # 查找任务
    task = None
    for t in project.get("tasks", []):
        if t["id"] == task_id:
            task = t
            break
    
    if not task:
        print(f"❌ 任务不存在: {task_id}")
        print(f"   可用任务: {', '.join([t['id'] for t in project.get('tasks', [])])}")
        return False
    
    # 更新字段
    if progress is not None:
        task["progress"] = max(0, min(100, progress))
        # 自动更新状态
        if task["progress"] == 100:
            task["status"] = "已完成"
        elif task["progress"] > 0:
            task["status"] = "进行中"
    
    if status:
        task["status"] = status
        # 同步进度
        if status == "已完成":
            task["progress"] = 100
        elif status == "待开始":
            task["progress"] = 0
    
    if notes:
        task["notes"] = notes
    
    if blockers:
        if isinstance(blockers, str):
            blockers = [b.strip() for b in blockers.split(",") if b.strip()]
        task["blockers"] = blockers
    
    task["updatedAt"] = datetime.now().isoformat()
    project["updatedAt"] = datetime.now().isoformat()
    
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 任务更新成功!")
    print(f"   任务: {task['name']}")
    print(f"   进度: {task['progress']}%")
    print(f"   状态: {task['status']}")
    if task.get("blockers"):
        print(f"   阻塞: {', '.join(task['blockers'])}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新任务")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("task_id", help="任务ID")
    parser.add_argument("--progress", "-p", type=int, help="进度 (0-100)")
    parser.add_argument("--status", "-s", 
                        choices=["待开始", "进行中", "已完成", "已阻塞", "已取消"],
                        help="状态")
    parser.add_argument("--notes", "-n", help="备注")
    parser.add_argument("--blockers", "-b", help="阻塞项 (逗号分隔)")
    
    args = parser.parse_args()
    
    update_task(args.project_id, args.task_id, args.progress, args.status, args.notes, args.blockers)
