#!/usr/bin/env python3
"""
添加部门
用法: python3 add_department.py <project-id> --name NAME --owner OWNER
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def generate_id(prefix="dept"):
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"

def add_department(project_id, name, owner="", responsibility=""):
    """添加部门到项目"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return False
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    dept_id = generate_id("dept")
    department = {
        "id": dept_id,
        "name": name,
        "owner": owner,
        "responsibility": responsibility
    }
    
    project["departments"].append(department)
    project["updatedAt"] = datetime.now().isoformat()
    
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 部门添加成功!")
    print(f"   ID: {dept_id}")
    print(f"   名称: {name}")
    print(f"   负责人: {owner or '未设置'}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="添加部门")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("--name", "-n", required=True, help="部门名称")
    parser.add_argument("--owner", "-o", default="", help="负责人")
    parser.add_argument("--responsibility", "-r", default="", help="职责描述")
    
    args = parser.parse_args()
    
    add_department(args.project_id, args.name, args.owner, args.responsibility)
