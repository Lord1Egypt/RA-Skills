#!/usr/bin/env python3
"""
项目初始化脚本 - 为招商助手创建新项目
使用方法: python3 init_project.py <项目ID> <项目名称>
"""

import os
import sys
import json
from pathlib import Path

WORKSPACE_DIR = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")


def create_project(project_id, project_name, park_info=None):
    """创建新项目"""
    # 创建项目目录
    project_dir = os.path.join(WORKSPACE_DIR, "projects", project_id)
    
    if os.path.exists(project_dir):
        print(f"❌ 项目已存在: {project_dir}")
        return False
    
    # 创建目录结构
    os.makedirs(os.path.join(project_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "output"), exist_ok=True)
    
    # 创建项目配置
    config = {
        "project_name": project_name,
        "project_id": project_id,
        "knowledge_source": "tencent_doc",
        "tencent_doc": {
            "房源销控表": "YOUR_DOC_ID",
            "房源销控表_sheet_id": "YOUR_SHEET_ID",
            "客户跟进记录": "YOUR_DOC_ID",
            "客户跟进记录_sheet_id": "YOUR_SHEET_ID",
            "租金报价表": "YOUR_DOC_ID",
            "租金报价表_sheet_id": "YOUR_SHEET_ID",
            "配套资源表": "YOUR_DOC_ID",
            "配套资源表_sheet_id": "YOUR_SHEET_ID"
        },
        "local_files": {
            "房源销控表": "data/房源销控表.json",
            "客户跟进记录": "data/客户跟进记录.json",
            "租金报价表": "data/租金报价表.json",
            "配套资源表": "data/配套资源表.json"
        },
        "park_info": park_info or {
            "name": project_name,
            "address": "",
            "total_area": "",
            "contact": ""
        },
        "created_at": __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
        "version": "1.0.0"
    }
    
    config_file = os.path.join(project_dir, "config.json")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 更新全局配置
    global_config_file = os.path.join(WORKSPACE_DIR, "config.json")
    if os.path.exists(global_config_file):
        with open(global_config_file, "r", encoding="utf-8") as f:
            global_config = json.load(f)
    else:
        global_config = {
            "default_project": project_id,
            "projects": [],
            "knowledge_sources": {
                "tencent_doc": {
                    "description": "腾讯文档智能表格",
                    "setup_guide": "配置file_id和sheet_id"
                },
                "local_file": {
                    "description": "本地JSON/CSV文件",
                    "setup_guide": "指定文件路径"
                }
            }
        }
    
    if project_id not in global_config["projects"]:
        global_config["projects"].append(project_id)
    
    with open(global_config_file, "w", encoding="utf-8") as f:
        json.dump(global_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 项目创建成功!")
    print(f"  项目ID: {project_id}")
    print(f"  项目名称: {project_name}")
    print(f"  项目目录: {project_dir}")
    print(f"\n📝 下一步:")
    print(f"  1. 编辑配置文件: {config_file}")
    print(f"  2. 配置腾讯文档ID或本地文件路径")
    print(f"  3. 运行脚本时添加 --project {project_id} 参数")
    
    return True


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python3 init_project.py <项目ID> <项目名称> [园区地址] [总面积] [联系人]")
        print("示例: python3 init_project.py demo-park-b '示例软件园' '示例市XX区' '80000㎡' '赵经理 1XX-XXXX-XXXX'")
        sys.exit(1)
    
    project_id = sys.argv[1]
    project_name = sys.argv[2]
    
    park_info = {}
    if len(sys.argv) > 3:
        park_info["name"] = project_name
        park_info["address"] = sys.argv[3] if len(sys.argv) > 3 else ""
        park_info["total_area"] = sys.argv[4] if len(sys.argv) > 4 else ""
        park_info["contact"] = sys.argv[5] if len(sys.argv) > 5 else ""
    
    create_project(project_id, project_name, park_info)


if __name__ == "__main__":
    main()
