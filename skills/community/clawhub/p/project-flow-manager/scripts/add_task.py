#!/usr/bin/env python3
"""
添加任务
用法: python3 add_task.py <project-id> --name NAME --dept DEPT_ID --start DATE --end DATE
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def generate_id(prefix="task"):
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"

def add_task(project_id, name, department_id, milestone_id="", 
             start_date="", end_date="", priority="中", assignee=""):
    """添加任务到项目"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return False
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    # 验证部门ID
    dept_ids = [d["id"] for d in project.get("departments", [])]
    if department_id not in dept_ids:
        print(f"⚠️  警告: 部门ID {department_id} 不存在于项目中")
        print(f"   可用部门: {', '.join(dept_ids) if dept_ids else '无'}")
    
    task_id = generate_id("task")
    task = {
        "id": task_id,
        "name": name,
        "departmentId": department_id,
        "milestoneId": milestone_id,
        "startDate": start_date,
        "endDate": end_date,
        "status": "待开始",
        "progress": 0,
        "priority": priority,
        "assignee": assignee,
        "blockers": [],
        "notes": "",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    project["tasks"].append(task)
    project["updatedAt"] = datetime.now().isoformat()
    
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 任务添加成功!")
    print(f"   ID: {task_id}")
    print(f"   名称: {name}")
    print(f"   部门: {department_id}")
    print(f"   优先级: {priority}")
    print(f"   负责人: {assignee or '未分配'}")
    print(f"   时间: {start_date or '?'} ~ {end_date or '?'}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="添加任务")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("--name", "-n", required=True, help="任务名称")
    parser.add_argument("--dept", "-d", required=True, help="部门ID")
    parser.add_argument("--milestone", "-m", default="", help="里程碑ID")
    parser.add_argument("--start", "-s", default="", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", "-e", default="", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--priority", "-p", default="中", 
                        choices=["高", "中", "低"],
                        help="优先级")
    parser.add_argument("--assignee", "-a", default="", help="负责人")
    
    args = parser.parse_args()
    
    add_task(args.project_id, args.name, args.dept, args.milestone,
             args.start, args.end, args.priority, args.assignee)
