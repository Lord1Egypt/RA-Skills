#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大恩专题策略三步法 - 方案生成器
"""

import json
from datetime import datetime
from pathlib import Path

STATE_DIR = Path(__file__).parent.parent / "state"
PROJECTS_DIR = STATE_DIR / "projects"

def ensure_dirs():
    """确保目录存在"""
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

def create_project(project_name):
    """创建新项目"""
    ensure_dirs()
    
    project = {
        "name": project_name,
        "created_at": datetime.now().isoformat(),
        "status": "draft",
        "steps": {
            "step1": {"title": "核心课题", "content": "", "completed": False},
            "step2": {"title": "解决方案", "content": "", "completed": False},
            "step3": {"title": "传播规划", "content": "", "completed": False}
        }
    }
    
    project_file = PROJECTS_DIR / f"{project_name}.json"
    project_file.write_text(json.dumps(project, ensure_ascii=False, indent=2))
    
    return project

def list_projects():
    """列出所有项目"""
    ensure_dirs()
    projects = []
    for f in PROJECTS_DIR.glob("*.json"):
        project = json.loads(f.read_text())
        completed_steps = sum(1 for s in project["steps"].values() if s["completed"])
        projects.append({
            "name": project["name"],
            "created_at": project["created_at"],
            "progress": f"{completed_steps}/3"
        })
    return projects

# 三步法模板
STEP_TEMPLATES = {
    1: """【课题界定】

课题一：[课题名称]
• 挑战描述：______
• 解决方向：______

课题二：[课题名称]
• 挑战描述：______
• 解决方向：______
""",
    2: """【策略方向】
总体策略：______
执行路径：______
传播调性：______、______、______

【市场定位】
地段定位：______
客群定位：______
差异化定位：______

【核心卖点】
核心卖点一：______
• 支撑点：______

核心卖点二：______
• 支撑点：______

【项目定位】
定位语：______
SLOGAN：______
""",
    3: """【传播节奏】

阶段一：[时间范围] - [阶段名称]
目标：______
动作1：______
动作2：______

阶段二：[时间范围] - [阶段名称]
目标：______
动作1：______
动作2：______

阶段三：[时间范围] - [阶段名称]
目标：______
动作1：______
动作2：______
"""
}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python three_steps.py <命令> [参数]")
        print("命令:")
        print("  new <项目名>           创建新项目")
        print("  list                   列出所有项目")
        print("  template <步骤号>      获取步骤模板 (1-3)")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "new":
        if len(sys.argv) < 3:
            print("请指定项目名")
        else:
            project = create_project(sys.argv[2])
            print(f"✅ 项目已创建: {sys.argv[2]}")
    
    elif cmd == "list":
        projects = list_projects()
        if projects:
            print("项目列表:")
            for p in projects:
                print(f"  • {p['name']} ({p['progress']})")
        else:
            print("暂无项目")
    
    elif cmd == "template":
        if len(sys.argv) < 3:
            print("请指定步骤号 (1-3)")
        else:
            step_num = int(sys.argv[2])
            if step_num in STEP_TEMPLATES:
                print(f"\n=== Step {step_num} 模板 ===\n")
                print(STEP_TEMPLATES[step_num])
    
    else:
        print(f"未知命令: {cmd}")