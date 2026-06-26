#!/usr/bin/env python3
"""
列出所有项目
用法: python3 list_projects.py [--status STATUS]
"""

import json
import os
from pathlib import Path
from datetime import datetime

def list_projects(status_filter=None):
    """列出所有项目"""
    
    projects_dir = Path("projects")
    
    if not projects_dir.exists():
        print("📁 项目目录为空")
        return
    
    projects = []
    for file in projects_dir.glob("*.json"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                project = json.load(f)
                if status_filter is None or project.get("status") == status_filter:
                    projects.append(project)
        except Exception as e:
            print(f"⚠️  读取文件失败 {file}: {e}")
    
    if not projects:
        print("📁 没有找到项目")
        return
    
    # 按更新时间排序
    projects.sort(key=lambda x: x.get("updatedAt", ""), reverse=True)
    
    print(f"\n📋 项目列表 (共 {len(projects)} 个)\n")
    print(f"{'ID':<20} {'名称':<25} {'状态':<10} {'进度':<8} {'更新日期'}")
    print("-" * 80)
    
    for p in projects:
        # 计算整体进度
        tasks = p.get("tasks", [])
        if tasks:
            total_progress = sum(t.get("progress", 0) for t in tasks) / len(tasks)
            progress_str = f"{total_progress:.0f}%"
        else:
            progress_str = "N/A"
        
        updated = p.get("updatedAt", "")[:10] if p.get("updatedAt") else "N/A"
        
        print(f"{p['id']:<20} {p['name'][:24]:<25} {p.get('status', 'N/A'):<10} {progress_str:<8} {updated}")
    
    print()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="列出所有项目")
    parser.add_argument("--status", "-s", help="按状态筛选")
    args = parser.parse_args()
    
    list_projects(args.status)
