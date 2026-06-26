#!/usr/bin/env python3
"""
添加里程碑
用法: python3 add_milestone.py <project-id> --name NAME --date YYYY-MM-DD
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def generate_id(prefix="ms"):
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"

def add_milestone(project_id, name, date_str="", status="待开始"):
    """添加里程碑到项目"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return False
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    ms_id = generate_id("ms")
    milestone = {
        "id": ms_id,
        "name": name,
        "date": date_str,
        "status": status
    }
    
    project["milestones"].append(milestone)
    project["updatedAt"] = datetime.now().isoformat()
    
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 里程碑添加成功!")
    print(f"   ID: {ms_id}")
    print(f"   名称: {name}")
    print(f"   计划日期: {date_str or '未设置'}")
    print(f"   状态: {status}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="添加里程碑")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("--name", "-n", required=True, help="里程碑名称")
    parser.add_argument("--date", "-d", default="", help="计划日期 (YYYY-MM-DD)")
    parser.add_argument("--status", "-s", default="待开始", 
                        choices=["待开始", "进行中", "已完成", "已延期"],
                        help="状态")
    
    args = parser.parse_args()
    
    add_milestone(args.project_id, args.name, args.date, args.status)
