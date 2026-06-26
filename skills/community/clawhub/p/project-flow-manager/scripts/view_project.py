#!/usr/bin/env python3
"""
查看项目详情
用法: python3 view_project.py <project-id>
"""

import json
import sys
from pathlib import Path

def view_project(project_id):
    """查看项目详情"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    print(f"\n📊 项目详情: {project['name']}\n")
    print(f"ID: {project['id']}")
    print(f"描述: {project.get('description', 'N/A')}")
    print(f"状态: {project.get('status', 'N/A')}")
    print(f"起止时间: {project.get('startDate', '未设置')} ~ {project.get('endDate', '未设置')}")
    print(f"创建时间: {project.get('createdAt', 'N/A')[:10]}")
    print(f"更新时间: {project.get('updatedAt', 'N/A')[:10]}")
    
    # 部门信息
    print(f"\n🏢 参与部门 ({len(project.get('departments', []))}个):")
    for dept in project.get("departments", []):
        print(f"  • {dept['name']} | 负责人: {dept.get('owner', '未设置')} | 职责: {dept.get('responsibility', 'N/A')}")
    
    # 里程碑
    print(f"\n🎯 里程碑 ({len(project.get('milestones', []))}个):")
    for ms in project.get("milestones", []):
        status_icon = "✅" if ms.get("status") == "已完成" else "🔄" if ms.get("status") == "进行中" else "⏳"
        print(f"  {status_icon} {ms['name']} | 计划: {ms.get('date', '未设置')} | 状态: {ms.get('status', 'N/A')}")
    
    # 任务统计
    tasks = project.get("tasks", [])
    print(f"\n📋 任务统计 ({len(tasks)}个):")
    if tasks:
        status_counts = {}
        for t in tasks:
            status = t.get("status", "未设置")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            print(f"  • {status}: {count}个")
        
        # 整体进度
        total_progress = sum(t.get("progress", 0) for t in tasks) / len(tasks)
        print(f"\n  整体进度: {total_progress:.1f}%")
        
        # 最近更新的任务
        print(f"\n  最近任务:")
        recent_tasks = sorted(tasks, key=lambda x: x.get("updatedAt", ""), reverse=True)[:5]
        for t in recent_tasks:
            print(f"    • {t['name']} ({t.get('progress', 0)}%) - {t.get('status', 'N/A')}")
    
    # KPI
    kpis = project.get("kpis", [])
    print(f"\n📈 KPI指标 ({len(kpis)}个):")
    for kpi in kpis:
        print(f"  • {kpi['name']}: 目标 {kpi.get('target', 'N/A')} | 当前 {kpi.get('current', 'N/A')} | 状态: {kpi.get('status', 'N/A')}")
    
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 view_project.py <project-id>")
        sys.exit(1)
    
    view_project(sys.argv[1])
