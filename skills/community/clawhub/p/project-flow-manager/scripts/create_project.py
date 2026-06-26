#!/usr/bin/env python3
"""
创建新项目
用法: python3 create_project.py [--template TEMPLATE] [--name NAME]
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

def generate_id(prefix="proj"):
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"

def create_project(name=None, description=None, template="custom"):
    """创建新项目"""
    
    project_id = generate_id("proj")
    
    if not name:
        name = input("项目名称: ").strip()
    if not description:
        description = input("项目描述 (可选): ").strip() or ""
    
    # 根据模板设置默认值
    templates = {
        "it-project": {
            "departments": [
                {"id": "dept-001", "name": "产品部", "owner": "", "responsibility": "需求分析、产品设计"},
                {"id": "dept-002", "name": "技术部", "owner": "", "responsibility": "系统开发、技术实现"},
                {"id": "dept-003", "name": "测试部", "owner": "", "responsibility": "质量保证、测试验收"},
                {"id": "dept-004", "name": "运维部", "owner": "", "responsibility": "部署上线、运维保障"}
            ],
            "milestones": [
                {"id": "ms-001", "name": "需求评审", "date": "", "status": "待开始"},
                {"id": "ms-002", "name": "设计完成", "date": "", "status": "待开始"},
                {"id": "ms-003", "name": "开发完成", "date": "", "status": "待开始"},
                {"id": "ms-004", "name": "测试通过", "date": "", "status": "待开始"},
                {"id": "ms-005", "name": "上线发布", "date": "", "status": "待开始"}
            ]
        },
        "marketing-campaign": {
            "departments": [
                {"id": "dept-001", "name": "市场部", "owner": "", "responsibility": "活动策划、执行"},
                {"id": "dept-002", "name": "设计部", "owner": "", "responsibility": "视觉设计、物料制作"},
                {"id": "dept-003", "name": "运营部", "owner": "", "responsibility": "渠道投放、数据分析"}
            ],
            "milestones": [
                {"id": "ms-001", "name": "方案确定", "date": "", "status": "待开始"},
                {"id": "ms-002", "name": "物料准备", "date": "", "status": "待开始"},
                {"id": "ms-003", "name": "活动上线", "date": "", "status": "待开始"},
                {"id": "ms-004", "name": "活动结束", "date": "", "status": "待开始"},
                {"id": "ms-005", "name": "效果复盘", "date": "", "status": "待开始"}
            ]
        },
        "product-launch": {
            "departments": [
                {"id": "dept-001", "name": "产品部", "owner": "", "responsibility": "产品规划、功能定义"},
                {"id": "dept-002", "name": "研发部", "owner": "", "responsibility": "产品开发"},
                {"id": "dept-003", "name": "市场部", "owner": "", "responsibility": "市场推广、PR"},
                {"id": "dept-004", "name": "销售部", "owner": "", "responsibility": "销售准备、培训"}
            ],
            "milestones": [
                {"id": "ms-001", "name": "产品定义", "date": "", "status": "待开始"},
                {"id": "ms-002", "name": "MVP完成", "date": "", "status": "待开始"},
                {"id": "ms-003", "name": "内测启动", "date": "", "status": "待开始"},
                {"id": "ms-004", "name": "公测发布", "date": "", "status": "待开始"},
                {"id": "ms-005", "name": "正式发布", "date": "", "status": "待开始"}
            ]
        },
        "custom": {
            "departments": [],
            "milestones": []
        }
    }
    
    template_data = templates.get(template, templates["custom"])
    
    project = {
        "id": project_id,
        "name": name,
        "description": description,
        "status": "规划中",
        "startDate": "",
        "endDate": "",
        "template": template,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "departments": template_data["departments"],
        "milestones": template_data["milestones"],
        "tasks": [],
        "kpis": [],
        "reports": [],
        "notes": []
    }
    
    # 确保目录存在
    projects_dir = Path("projects")
    projects_dir.mkdir(exist_ok=True)
    
    # 保存项目文件
    project_file = projects_dir / f"{project_id}.json"
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 项目创建成功!")
    print(f"   ID: {project_id}")
    print(f"   名称: {name}")
    print(f"   模板: {template}")
    print(f"   文件: {project_file}")
    
    return project_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建新项目")
    parser.add_argument("--name", "-n", help="项目名称")
    parser.add_argument("--description", "-d", help="项目描述")
    parser.add_argument("--template", "-t", default="custom", 
                        choices=["custom", "it-project", "marketing-campaign", "product-launch"],
                        help="项目模板")
    
    args = parser.parse_args()
    
    create_project(args.name, args.description, args.template)
